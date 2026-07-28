# Hotels Canonical Layer API

## Overview

This project implements a canonical hotel layer by resolving duplicate hotel records from two independent suppliers into a single unified dataset.

The system performs:

- Hotel entity resolution
- Canonical hotel generation
- Room matching and normalization
- REST API for querying canonical hotels

The API is implemented using FastAPI and can be started using Docker with a single command.

---

# Project Structure

```
app/
data/
docs/
output/
scripts/
tests/

Dockerfile
docker-compose.yml
requirements.txt
README.md
WRITEUP.md
```

---

# Requirements

- Docker Desktop

OR

- Python 3.13+

---

# Running the Project

## Option 1 (Recommended)

Build and start the API:

```bash
docker compose up --build
```

API:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

---

## Option 2 (Without Docker)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

---

# Canonical Output

The generated canonical dataset is located at:

```
output/canonical_hotels.json
```

The dataset contains:

- canonical_id
- merged hotel information
- supplier references
- confidence score

---

# API Endpoints

## 1. Search Hotels

```
GET /hotels
```

Example:

```
GET /hotels?search=fortune
```

Optional query parameters:

| Parameter | Description |
|-----------|-------------|
| search | Hotel name search |
| min_confidence | Minimum confidence score |
| limit | Pagination limit |
| offset | Pagination offset |

---

## 2. Hotel Details

```
GET /hotels/{canonical_id}
```

Example:

```
GET /hotels/CAN-A-35201-B-70235
```

Returns:

- Canonical hotel
- Supplier A record
- Supplier B record
- Matched rooms
- Near-miss room candidates
- Hotel confidence score

---

# Matching Strategy

## Hotel Matching

Candidate generation reduces unnecessary comparisons using geographic blocking.

Each candidate pair is scored using multiple signals:

- Hotel name similarity
- Geographic distance
- Address similarity
- Star rating comparison

Only matches with confidence ≥ 55 are accepted.

Hotels without a valid match are retained as single-source canonical hotels.

---

## Room Matching

Rooms are matched using RapidFuzz token similarity.

Normalized attributes include:

- Bed type
- Occupancy
- Meal plan
- View

Low-confidence room matches are returned as near-miss candidates instead of being forced.

---

# API Spend

```
$0
```

No paid APIs or LLM services were used.

---

# Notes

The repository includes:

- Source code
- Docker configuration
- Canonical output
- Technical write-up

The project is fully reproducible from the provided source code and dataset.