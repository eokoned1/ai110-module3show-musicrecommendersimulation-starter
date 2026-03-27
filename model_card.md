# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

VibeFinder 1.0

---

## 2. Intended Use

This model recommends the top 3 to 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic preference.

It is designed for classroom exploration of recommendation logic, not for production use with real users. The model assumes the user can be represented by one profile at a time and that these few features are enough to estimate taste.

---

## 3. How the Model Works

Each song has features such as genre, mood, energy, and acousticness. The user profile stores favorite genre, favorite mood, target energy, and whether the user likes acoustic songs.

The model gives points for:
- genre match (+2.0)
- mood match (+1.5)
- energy closeness (+2.0 x (1 - absolute difference from target energy))
- acoustic fit (add acousticness if the user likes acoustic songs, otherwise add 1 - acousticness)

Songs are sorted by total score from highest to lowest, and the top k songs are returned with a plain-language explanation.

---

## 4. Data

The dataset is a small CSV catalog in data/songs.csv with 10 songs.

Genres represented include pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Moods include happy, chill, intense, relaxed, focused, and moody.

I did not add or remove songs from the provided dataset. Important parts of music taste are missing, including lyrics, language, artist familiarity, release era, and cultural context.

---

## 5. Strengths

The recommender works well when the user profile clearly aligns with available songs in the catalog.

- For a pop/happy/high-energy user, Sunrise City ranked first as expected.
- For a chill/lofi/acoustic user, Library Rain and Midnight Coding ranked at the top and made intuitive sense.
- For an intense/rock/high-energy/non-acoustic user, Storm Runner ranked first and Gym Hero followed as a reasonable second choice.

Another strength is transparency: because the model is weighted and deterministic, it is easy to explain and debug.

---

## 6. Limitations and Bias

The model has several limitations.

- It only covers a tiny catalog, so some users will get weak matches by default.
- It ignores important factors such as lyrics, language, context, novelty, and popularity.
- It assumes all users can be represented by one fixed profile rather than changing preferences over time.
- Genre and mood weights are strong, which can overpower subtler taste signals.

Potential bias comes from dataset composition. If some genres, moods, or listening cultures are underrepresented, users from those groups receive lower quality recommendations.

---

## 7. Evaluation

I evaluated the recommender in three ways.

- Manual score check: I computed Sunrise City's score for the baseline profile and verified the result (about 6.28).
- Multi-profile runs: I tested baseline pop/happy, chill lofi, and intense rock profiles and checked whether top songs matched expectation.
- Unit tests: starter tests pass for recommendation ordering and explanation output.

One notable result was that after the top one or two songs, score quality drops quickly due to the small catalog size.

---

## 8. Future Work

If I extended this project, I would:

- add more songs and improve balance across genres and moods
- include extra features such as tempo range preference and lyrical themes
- add diversity constraints so top results are not too similar
- support feedback loops so recommendations adapt over time
- improve explanations by showing per-feature score contributions numerically

---

## 9. Personal Reflection

This project helped me understand that recommendation systems do not need to be complex to produce convincing outputs. A simple weighted design can already feel personalized when the chosen features line up with user expectations.

What surprised me was how strongly dataset size and feature coverage affect results. Even with a sensible scoring formula, missing representation in the catalog can make recommendations look biased or shallow. Building this changed how I think about real music apps: model quality is not only about algorithms, but also about data diversity, feature choices, and careful evaluation.
