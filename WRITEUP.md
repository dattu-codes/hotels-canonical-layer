# Hotels Canonical Layer – Technical Write-up

## Approach

The objective of this project was to merge duplicate hotel records from two independent suppliers into a single canonical hotel layer while preserving provenance and assigning confidence scores at both the hotel and room level.

A naïve approach would compare every hotel from Supplier A against every hotel from Supplier B (approximately 13 million comparisons). This is computationally expensive and unnecessary. Instead, the pipeline first performs candidate generation using geographic blocking within a configurable search radius to significantly reduce the number of hotel pairs that require detailed comparison.

Each candidate pair is then evaluated using multiple matching signals:

- Hotel name similarity
- Geographic distance (latitude/longitude)
- Star rating similarity

These signals are combined into a confidence score. The highest-confidence candidate above the acceptance threshold is merged into a canonical hotel record while preserving references to the original supplier records.

Hotels that cannot be confidently matched are retained as single-source canonical hotels instead of being discarded, ensuring complete coverage of both supplier datasets.

---

# Room Canonicalization

Room matching is performed only for hotels that have already been matched.

RapidFuzz token sort similarity is used to compare room names while handling variations such as:

- Deluxe Twin Room
- Twin Deluxe Room

To improve room consistency, room information is normalized into structured attributes including:

- Bed Type
- Occupancy
- Meal Plan
- View

For every matched hotel pair, the pipeline generates a persisted room-level canonical artifact (`canonical_rooms.json`).

Each canonical room record contains:

- Canonical Room ID
- Canonical Hotel ID
- Supplier A Room ID
- Supplier B Room ID
- Normalized room attributes
- Room-level confidence score
- Match status

Room match status is classified as:

- matched
- near_miss
- unmatched_a
- unmatched_b

Low-confidence room pairs are preserved as near-miss candidates instead of forcing incorrect matches, while rooms existing in only one supplier remain unmatched.

---

# Canonical Artifacts

The pipeline produces two persisted canonical outputs.

## Hotel Artifact

`output/canonical_hotels.json`

Contains:

- Canonical hotel information
- Supplier provenance
- Hotel confidence score

## Room Artifact

`output/canonical_rooms.json`

Contains:

- Canonical room information
- Canonical hotel reference
- Supplier room provenance
- Normalized room attributes
- Room confidence score
- Match status

Persisting these artifacts separates the matching pipeline from the serving layer and avoids recomputing room matches during every API request.

---

# API Design

The canonical layer is exposed through a FastAPI REST API.

Endpoints:

- `GET /hotels`
- `GET /hotels/{canonical_id}`

The hotel details endpoint returns:

- Canonical hotel
- Supplier A record
- Supplier B record
- Matched rooms
- Near-miss room candidates
- Unmatched Supplier A rooms
- Unmatched Supplier B rooms
- Hotel confidence score

The API reads the persisted canonical artifacts (`canonical_hotels.json` and `canonical_rooms.json`) rather than performing room alignment during every request, resulting in a cleaner separation between data generation and data serving.

Swagger/OpenAPI documentation is automatically available through FastAPI.

---

# Validation

The matching pipeline was validated by manually inspecting representative hotel matches and verifying that hotel names, geographic proximity, star ratings, and confidence scores were consistent with the expected canonical mappings.

The API was validated using Swagger UI by testing:

- Hotel search
- Canonical hotel retrieval
- Matched hotels
- Supplier A-only hotels
- Supplier B-only hotels
- Persisted room canonicalization
- Room matching output
- Near-miss and unmatched room responses

Finally, I verified that every supplier hotel appears exactly once in the final canonical hotel output and that room-level canonical records are generated only for matched hotel pairs while preserving supplier provenance.

---

# Approaches Considered but Discarded

I considered comparing every Supplier A hotel against every Supplier B hotel directly. However, this would require approximately 13 million comparisons and would not scale efficiently.

I also considered using LLMs to compare every hotel pair. Although this could improve some ambiguous matches, it would significantly increase both API cost and processing latency.

Instead, I used deterministic candidate generation followed by fuzzy matching. This approach is reproducible, explainable, inexpensive, and well suited to the assignment dataset.

---

# Cost

Total external API spend:

**$0**

The complete pipeline relies on local processing using Python, Pandas, and RapidFuzz without requiring paid APIs or external LLM services.

---

# Scaling to 200,000 Hotels

The current implementation is designed for the assignment dataset and performs well at this scale.

For significantly larger datasets involving hundreds of thousands of hotels and multiple suppliers, I would improve the architecture by:

- Stronger blocking and indexing strategies
- Approximate nearest-neighbor search for candidate generation
- Database-backed canonical storage instead of JSON artifacts
- Parallel matching pipelines
- Incremental processing of supplier updates
- Caching intermediate matching results

These improvements would reduce computation time while maintaining matching quality.

---

# Trade-offs

Within the assignment time constraints, I prioritized:

- Accurate hotel matching
- Explainable confidence scores
- Reliable room canonicalization
- Persisted canonical artifacts
- Clean REST API
- Dockerized deployment
- Reproducibility

I intentionally avoided expensive LLM-based comparisons across the full dataset because they would increase both cost and latency without being necessary for this assignment.

The resulting solution is deterministic, reproducible, cost-effective, and separates the matching pipeline from the API layer through persisted canonical hotel and room artifacts.