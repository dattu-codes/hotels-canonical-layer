# Hotels Canonical Layer – Technical Write-up

## Approach

The objective was to merge duplicate hotel records from two suppliers into a single canonical hotel layer while preserving source provenance and assigning confidence scores.

Instead of comparing every hotel from Supplier A with every hotel from Supplier B (approximately 13 million comparisons), I first generated candidate matches using lightweight filtering based on hotel names and location. This significantly reduced the search space before applying fuzzy matching.

For each candidate pair, I generated candidate matches using lightweight filtering and then applied fuzzy matching using RapidFuzz. Hotel names, addresses, geographic coordinates (latitude/longitude), and star ratings were used to compute an overall confidence score. The highest-confidence pair was selected as the canonical hotel while preserving links to both supplier records.

These signals were combined into a confidence score. The highest-confidence candidate became the canonical match while preserving both supplier IDs.

---

## Room Matching

Room matching was performed only for hotels that had already been matched.

RapidFuzz token sort similarity was used to compare room names such as:

- Deluxe Twin Room
- Twin Deluxe Room

Each room pair received a confidence score.

Matched rooms include:
- Supplier A room
- Supplier B room
- Confidence score

Lower-confidence matches are exposed as near-miss candidates instead of forcing incorrect mappings.

---

## API Design

The API was implemented using FastAPI.

Endpoints:

- `GET /hotels`
- `GET /hotels/{canonical_id}`

The hotel details endpoint returns:

- Canonical hotel
- Original Supplier A record
- Original Supplier B record
- Matched rooms
- Near-miss room candidates
- Hotel confidence score

Swagger documentation is automatically available through FastAPI.

---

## Cost

Total external API spend:

**$0**

The project relies entirely on local processing using Python and RapidFuzz.

---

## Scaling to 200,000 Hotels

The current implementation works well for the assignment dataset but would require improvements at larger scale.

To support hundreds of thousands of hotels and multiple suppliers, I would:

- Use blocking/indexing to reduce candidate generation.
- Build approximate nearest-neighbor indexes for embeddings.
- Store canonical data in a database instead of JSON.
- Execute matching in parallel batches.
- Cache intermediate matching results.
- Introduce incremental matching for new supplier feeds instead of rebuilding everything.

These optimizations would reduce both computation time and memory usage while maintaining matching quality.

---

## Trade-offs

To remain within the assignment time limit, I prioritized:

- Correct hotel matching
- Explainable confidence scores
- Clean API design
- Dockerized deployment
- Reproducibility

I intentionally avoided expensive LLM-based comparisons for every hotel pair because they would not scale efficiently and would unnecessarily increase API costs.