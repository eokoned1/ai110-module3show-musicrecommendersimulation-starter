from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _score_song(song: Song, user: UserProfile) -> float:
        score = 0.0

        if song.genre.strip().lower() == user.favorite_genre.strip().lower():
            score += 2.0

        if song.mood.strip().lower() == user.favorite_mood.strip().lower():
            score += 1.5

        # Closer energy to the user's target gives a higher contribution.
        energy_closeness = 1.0 - abs(song.energy - user.target_energy)
        score += max(0.0, energy_closeness) * 2.0

        acoustic_fit = song.acousticness if user.likes_acoustic else (1.0 - song.acousticness)
        score += acoustic_fit

        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(
            self.songs,
            key=lambda song: self._score_song(song, user),
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons: List[str] = []

        if song.genre.strip().lower() == user.favorite_genre.strip().lower():
            reasons.append(f"genre matches your preference ({user.favorite_genre})")

        if song.mood.strip().lower() == user.favorite_mood.strip().lower():
            reasons.append(f"mood matches your preference ({user.favorite_mood})")

        energy_gap = abs(song.energy - user.target_energy)
        if energy_gap <= 0.15:
            reasons.append(f"energy is very close to your target ({user.target_energy:.2f})")
        elif energy_gap <= 0.30:
            reasons.append(f"energy is reasonably close to your target ({user.target_energy:.2f})")

        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append("it has a strong acoustic feel")
        if not user.likes_acoustic and song.acousticness <= 0.4:
            reasons.append("it has a more produced, less acoustic sound")

        if not reasons:
            return "This song is recommended because it is a balanced overall match for your profile."

        return "This song is recommended because " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    target_genre = str(user_prefs.get("genre", "")).strip().lower()
    target_mood = str(user_prefs.get("mood", "")).strip().lower()
    target_energy = float(user_prefs.get("energy", 0.5))
    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))

    def score(song: Dict) -> float:
        total = 0.0

        if str(song.get("genre", "")).strip().lower() == target_genre:
            total += 2.0

        if str(song.get("mood", "")).strip().lower() == target_mood:
            total += 1.5

        energy_closeness = 1.0 - abs(float(song.get("energy", 0.0)) - target_energy)
        total += max(0.0, energy_closeness) * 2.0

        acousticness = float(song.get("acousticness", 0.0))
        total += acousticness if likes_acoustic else (1.0 - acousticness)

        return total

    def explanation(song: Dict) -> str:
        reasons: List[str] = []

        if str(song.get("genre", "")).strip().lower() == target_genre and target_genre:
            reasons.append(f"genre matches ({song['genre']})")

        if str(song.get("mood", "")).strip().lower() == target_mood and target_mood:
            reasons.append(f"mood matches ({song['mood']})")

        energy_gap = abs(float(song.get("energy", 0.0)) - target_energy)
        if energy_gap <= 0.15:
            reasons.append("energy is very close to your target")

        acousticness = float(song.get("acousticness", 0.0))
        if likes_acoustic and acousticness >= 0.6:
            reasons.append("acoustic profile is a good fit")
        if not likes_acoustic and acousticness <= 0.4:
            reasons.append("lower acousticness fits your preference")

        if not reasons:
            return "Good overall match across multiple attributes"

        return "; ".join(reasons)

    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        song_score = score(song)
        scored.append((song, song_score, explanation(song)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
