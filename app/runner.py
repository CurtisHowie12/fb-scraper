"""Thin wrapper so the scraper can be run as `python -m app.runner <target>`."""
from app.scraper.runner import main

if __name__ == "__main__":
    main()
