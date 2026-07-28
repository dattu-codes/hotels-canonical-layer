# Hotels Canonical Layer – Technical Write-up

## Approach

The objective of this project was to merge duplicate hotel records from two independent suppliers into a single canonical hotel layer while preserving source provenance and assigning a confidence score to every match.

A brute-force comparison between every Supplier A hotel and every Supplier B hotel would require approximately 13 million comparisons, making it computationally expensive and difficult to scale. To reduce the search space, I first generated candidate matches using geographic proximity and lightweight filtering before applying fuzzy matching.

For each candidate pair, I compared multiple signals including:

- Hotel name similarity
- Address similarity
- Geographic distance (latitude/longitude)
- Star rating similarity

These signals were combined into a confidence score. The highest-confidence candidate above the matching threshold was selected as the canonical hotel while preserving references to both supplier records.

Hotels that could not be confidently matched were retained as single-source canonical hotels instead of being discarded, ensuring that every supplier hotel remained available in the canonical dataset.

---

# Room Matching

Room matching was performed only for hotels that had already been matched.

RapidFuzz token sort similarity was used to compare room names such as:

- Deluxe Twin Room
- Twin Deluxe Room

The room parser also normalizes attributes such as:

- Bed type
- Occupancy
- Meal plan
- View

Each room pair receives a confidence score.

Lower-confidence room pairs are returned as near-miss candidates instead of forcing incorrect matches.

---

# API Design

The project exposes the canonical layer through a FastAPI REST API.

Endpoints:

- `GET /hotels`
- `GET /hotels/{canonical_id}`

The hotel details endpoint returns:

- Canonical hotel
- Supplier A record
- Supplier B record
- Matched rooms
- Near-miss room candidates
- Hotel confidence score

Swagger/OpenAPI documentation is automatically available through FastAPI.

---

# Validation

To validate the matching pipeline, I manually inspected representative hotel matches and verified that hotel names, addresses, coordinates, and confidence scores were consistent.

I also verified the API using Swagger UI by testing:

- Hotel search
- Canonical hotel retrieval
- Matched hotels
- Supplier A-only hotels
- Supplier B-only hotels
- Room matching output

Finally, I confirmed that every hotel from both supplier datasets was represented in the final canonical output without duplicate supplier mappings.

---

# Approaches Considered but Discarded

I considered comparing every Supplier A hotel against every Supplier B hotel directly. However, this would require approximately 13 million comparisons and would not scale efficiently.

I also considered using LLMs to compare every hotel pair. Although this could improve some ambiguous matches, it would introduce significant API cost and latency. Instead, I used candidate generation followed by deterministic fuzzy matching, resulting in a fully reproducible solution with zero external API cost.

---

# Cost

Total external API spend:

**$0**

The entire pipeline relies on local processing using Python, Pandas, and RapidFuzz without requiring paid APIs or external LLM services.

---

# Scaling to 200,000 Hotels

The current implementation is designed for the assignment dataset and performs well at this scale. For significantly larger datasets involving hundreds of thousands of hotels and multiple suppliers, I would improve the architecture by:

- Using stronger blocking/indexing strategies for candidate generation.
- Building approximate nearest-neighbor indexes for embedding-based matching.
- Storing canonical data in a database instead of JSON files.
- Processing matching in parallel batches.
- Caching intermediate matching results.
- Supporting incremental updates for new supplier feeds instead of rebuilding the entire canonical layer.

These improvements would reduce computation time while maintaining matching quality.

---

# Trade-offs

Within the assignment time constraints, I prioritized:

- Accurate hotel matching
- Explainable confidence scores
- Reliable room matching
- A clean REST API
- Dockerized deployment
- Reproducibility

I intentionally avoided expensive LLM-based comparisons for every hotel pair because they would increase both API cost and latency without being necessary for this dataset. The chosen approach provides a scalable, deterministic, and cost-effective solution while remaining easy to understand and reproduce.