# Recipe Enhancement Platform

TBD

## Installation

This project uses [`uv`](https://docs.astral.sh/uv/) for fast, reliable Python package management.

### Prerequisites

- Python 3.13+
- `uv` package manager

## Quick Start

```bash
# Install dependencies
uv venv
source .venv/bin/activate
uv pip sync pyproject.toml

# Run the scraper
uv run python src/scraper_v2.py

# Scrape a single recipe (runs main() function)
uv run python src/scraper_v2.py
```

### Output Structure

Scraped data is saved as JSON files in the `data/` directory:

```json
{
  "recipe_id": "10813",
  "title": "Best Chocolate Chip Cookies",
  "url": "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/",
  "scraped_at": "2024-09-25T00:16:00.000000",
  "rating": {
    "value": "4.6",
    "count": "19353"
  },
  "ingredients": [...],
  "instructions": [...],
  "featured_tweaks": [
    {
      "text": "I used a half cup of sugar and one-and-a-half cups of brown sugar...",
      "rating": 5,
      "has_modification": true,
      "is_featured": true,
      "username": "Chef John"
    }
  ],
  "reviews": [...]
}
```

## Development

### Package Management

Add new dependencies:

```bash
uv add <package_name>
```

Remove dependencies:

```bash
uv remove <package_name>
```

Add development dependencies:

```bash
uv add --dev <package_name>
```
