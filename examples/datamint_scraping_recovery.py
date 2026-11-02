"""
Datamint - High-Throughput Crawling Resilience & Partial Schema Recovery
Module: datamint_scraping_recovery.py
Target: founders@datamint.xyz
"""

from __future__ import annotations
import json
import logging
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Datamint.CrawlRecovery")

class ScrapedProductProfile(BaseModel):
    title: str = Field(default="Untitled Product")
    price: float = Field(default=0.0)
    in_stock: bool = Field(default=True)
    sku: Optional[str] = None
    extraction_quality: str = "complete"

class DatamintResilientExtractor:
    """Extracts valid structured models from malformed or truncated HTML scrape payloads."""
    
    @staticmethod
    def extract_with_recovery(raw_json_str: str) -> ScrapedProductProfile:
        try:
            data = json.loads(raw_json_str)
            return ScrapedProductProfile(**data)
        except json.JSONDecodeError:
            logger.warning("Malformed JSON encountered during scrape. Engaging partial string heuristics...")
            # Partial heuristic recovery
            title = "Extracted Product"
            price = 0.0
            if '"title":' in raw_json_str:
                part = raw_json_str.split('"title":')[1].split('"')[1]
                title = part if part else title
            if '"price":' in raw_json_str:
                try:
                    price_str = raw_json_str.split('"price":')[1].split(",")[0].replace("}", "").strip()
                    price = float(price_str)
                except ValueError:
                    price = 0.0
            return ScrapedProductProfile(
                title=title,
                price=price,
                extraction_quality="recovered_from_partial_json"
            )

def run_tests():
    print("=== RUNNING DATAMINT SCRAPING RECOVERY HARNESS ===")
    extractor = DatamintResilientExtractor()

    # 1. Clean JSON
    clean_json = '{"title": "Industrial Thermal Sensor", "price": 249.99, "in_stock": true, "sku": "TS-991"}'
    res1 = extractor.extract_with_recovery(clean_json)
    assert res1.price == 249.99
    assert res1.extraction_quality == "complete"
    print("[PASS] Clean scrape payload parsed successfully.")

    # 2. Truncated / malformed JSON from interrupted network stream
    truncated_json = '{"title": "Industrial Thermal Sensor", "price": 249.99, "in_stock": tr'
    res2 = extractor.extract_with_recovery(truncated_json)
    assert res2.price == 249.99
    assert res2.extraction_quality == "recovered_from_partial_json"
    print("[PASS] Interrupted crawl stream recovered cleanly without throwing fatal exception.")
    print("=== DATAMINT VERIFICATION 100% COMPLETE ===")

if __name__ == "__main__":
    run_tests()
