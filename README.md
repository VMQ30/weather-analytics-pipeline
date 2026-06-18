# Weather Analytics Pipeline

This project is a small ETL pipeline that pulls live weather data for active cities, transforms it into analysis-friendly fields, and loads the results into a PostgreSQL database.

---

## Overview

The pipeline performs the following steps:

1. Reads the list of active cities from the database.
2. Fetches current weather information from the OpenWeatherMap API.
3. Transforms the raw data into useful analysis columns.
4. Appends the transformed records into the target database table.

---

## 🏗️ Project Architecture & Layout

The project follows a modular design pattern to ensure clean separation of concerns and robust testability.

```text
weather-analytics-pipeline/
│
├── .env                  # Local secrets and config variables (git ignored)
├── .gitignore            # Excludes temporary cache, files, and secrets
├── README.md             # Project documentation
├── requirements.txt      # Third-party runtime dependencies
│
├── src/
│   ├── __init__.py       # Package exposure layer
│   ├── extract.py        # E - DB target pull & API orchestration
│   ├── transform.py      # T - Data transformation and enrichment
│   └── load.py           # L - Bulk relational-safe upsert
│
└── main.py               # Main runtime orchestrator
```

---

## Prerequisites

Before running the pipeline, make sure you have:

- Python 3.10+
- A running PostgreSQL database
- An OpenWeatherMap API key
- The dependencies listed in `requirements.txt`

---

## Installation

Install project dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
DB_URL=postgresql://username:password@host:port/database_name
```

---

## Database Requirements

The pipeline expects:

### Source Table

`cities`

Required columns:

- `name`
- `is_active`

Example:

| name   | is_active |
| ------ | --------- |
| Manila | true      |
| Cebu   | true      |

### Destination Table

Create the destination table before running the pipeline.

Example target:

```text
cities_weather_info
```

---

## How to Run

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd weather-analytics-pipeline
```

### 2. Create and Activate a Virtual Environment (Recommended)

Create the environment:

```bash
python -m venv venv
```

Activate it:

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add:

```env
OPENWEATHER_API_KEY=your_openweather_api_key
DB_URL=postgresql://username:password@host:port/database_name
```

---

### 5. Run the Pipeline

```bash
python main.py
```

The script will:

- Validate required environment variables
- Connect to PostgreSQL
- Fetch weather records for active cities
- Transform the results
- Load transformed records into the target table

---

## Output Data

Each loaded weather record may include:

- City name
- Temperature (°C)
- Feels-like temperature
- Humidity
- Wind speed
- Weather condition
- Timestamp information
- Extreme heat/cold indicators
- Wind scale categories

---

## Logging

The application logs:

- Pipeline progress
- Warnings
- Environment validation failures
- Database and API errors

Logs are displayed directly in the console.

---

## Example Workflow

```text
cities
   ↓
extract.py
   ↓
transform.py
   ↓
load.py
   ↓
cities_weather_info
```

---

## Tech Stack

- Python
- PostgreSQL
- OpenWeatherMap API
- ETL Architecture
- Environment-based configuration (`.env`)
