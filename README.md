# Hotels Canonical Layer API

## Overview

This project merges duplicate hotel records from two suppliers into a single canonical hotel layer. It exposes the merged data through a FastAPI service with confidence scores, source provenance, and matched room information.

## Features

- Hotel matching using candidate generation and fuzzy matching
- Canonical hotel records with supplier references
- Room matching with confidence scores
- Near-miss room candidates
- REST API built with FastAPI
- Docker and Docker Compose support

---

## Tech Stack

- Python 3.13
- FastAPI
- Pandas
- RapidFuzz
- Docker

---

## Project Structure

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

## Run with Docker

Build and start the application:

```bash
docker compose up --build
```

The API will be available at:

```
http://localhost:8000
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## Run without Docker

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

---

## API Endpoints

### List Hotels

```
GET /hotels
```

Example:

```
GET /hotels?search=fortune
```

Supported query parameters:

- search
- limit
- offset

---

### Hotel Details

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
- Match confidence score

---

## Matching Approach

### Hotel Matching

Hotels are matched using:

- Candidate generation
- Fuzzy name matching
- Address similarity
- Geographic proximity
- Confidence scoring

### Room Matching

Rooms are matched using RapidFuzz token sort similarity. Each room match includes a confidence score, and uncertain matches are returned as near-miss candidates instead of being forced.

---

## Output

The generated canonical hotel dataset is stored in:

```
output/canonical_hotels.json
```

---

## API Spend

```
$0
```