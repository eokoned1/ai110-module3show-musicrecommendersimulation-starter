# 🎵 Music Recommender Simulation

Prepared in a Teaching Fellow (TF) role for Week 6 recommendation-system support and evaluation.

## Project Summary

As a TF, I implemented a rule-based music recommender that ranks songs from a small catalog using user taste preferences. Each song has structured features (genre, mood, energy, tempo, valence, danceability, acousticness), and each user profile specifies target preferences (favorite genre, favorite mood, target energy, and whether the user likes acoustic songs).

The recommender computes a score for every song, sorts by score, and returns the top k results with short natural-language explanations. I focused on making the logic transparent for TF grading and student debugging.

---

## How The System Works

### Song Features

Each song includes:
- id, title, artist
- genre and mood (categorical)
- energy, tempo_bpm, valence, danceability, acousticness (numeric)

The current scoring rule actively uses genre, mood, energy, and acousticness.

### User Profile

The profile contains:
- favorite genre
- favorite mood
- target energy (0 to 1)
- likes_acoustic (True or False)

### Scoring Rule

Each song gets points from four components:
- Genre match: +2.0 if song genre matches the user's favorite genre
- Mood match: +1.5 if song mood matches the user's favorite mood
- Energy closeness: +2.0 x (1 - |song_energy - target_energy|)
- Acoustic preference:
  - If likes_acoustic is True, add acousticness
  - If likes_acoustic is False, add (1 - acousticness)

This means exact genre/mood matches have strong influence, while energy and acousticness fine-tune ranking between similar songs.

### Recommendation Step

1. Load songs from data/songs.csv.
2. Score every song with the rule above.
3. Sort by score in descending order.
4. Return top k songs with explanations (for example: genre match, mood match, close energy, acoustic fit).

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

As a TF, I tested multiple user profiles to verify that recommendations changed in intuitive ways.

### Baseline Profile (Pop + Happy)

Profile:
- genre: pop
- mood: happy
- energy: 0.8
- likes_acoustic: False (default)

Top result: Sunrise City.

Why it ranked first:
- Genre match (+2.0)
- Mood match (+1.5)
- Very close energy (0.82 vs 0.80, about +1.96)
- Low acousticness fits non-acoustic preference (+0.82)

Approximate total: 6.28.

### Phase 4 Profile 2 (Chill Lofi)

Profile:
- genre: lofi
- mood: chill
- energy: 0.4
- likes_acoustic: True

Top recommendations:
1. Library Rain (6.26)
2. Midnight Coding (6.17)
3. Focus Flow (4.78)

Observation:
- The recommender strongly favored songs that matched lofi + chill and had high acousticness.
- Library Rain and Midnight Coding both fit all major criteria (genre, mood, energy closeness, acoustic preference), which explains their very high scores.

### Phase 4 Profile 3 (Intense Rock)

Profile:
- genre: rock
- mood: intense
- energy: 0.9
- likes_acoustic: False

Top recommendations:
1. Storm Runner (6.38)
2. Gym Hero (4.39)
3. Sunrise City (2.66)

Observation:
- Storm Runner clearly ranked first because it matched genre and mood exactly, had near-target energy, and low acousticness.
- Gym Hero did not match genre but still scored well from mood, high energy, and low acousticness.

### What This Shows

- The model responds predictably to profile changes.
- Exact genre and mood matches create the largest score jump.
- Energy closeness and acoustic preference help separate songs that are otherwise similar.
- Because the catalog is small, some profiles quickly run out of strong matches after the top 1 to 2 songs.

---

## Limitations and Risks

This recommender is transparent and easy to inspect, but it has several limitations.

- Small catalog effect: with only a small number of songs, many profiles have only one or two strong matches.
- Feature limitations: it ignores lyrics, language, culture, release era, and listening context (workout, study, commute).
- Static preferences: each run uses a single profile snapshot and does not learn from user feedback over time.
- Weight sensitivity: genre and mood weights are strong, so near matches in other features can be pushed down quickly.
- Potential bias: if the dataset underrepresents certain genres or moods, those users receive weaker recommendations.

---

## Reflection

From a TF perspective, this project showed me how quickly a recommender can feel "smart" even with a simple weighted formula. By turning user preferences and song features into numbers, the system consistently produced rankings that matched intuition for different profiles. I also learned that explanation text matters because it helps verify that the model ranked songs for the reasons I expected.

I also saw how bias can appear even in a small classroom simulation. If a catalog has uneven representation, users with less represented tastes get lower quality results, not because the algorithm is malicious but because the available data does not cover them well. Building and testing this as a TF reinforced that recommenders are socio-technical systems where design choices, weights, and dataset composition all shape user outcomes.


---

See the completed model card in [model_card.md](model_card.md).

