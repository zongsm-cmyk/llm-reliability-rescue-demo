"""
Opaxa - Multi-System Data Ingestion & Pydantic Schema Reconciliation
Module: opaxa_multischema_reconciler.py
Target: colton@opaxa.com
"""

from __future__ import annotations
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Opaxa.SchemaReconciler")

class UnifiedLocationProfile(BaseModel):
    location_id: str = Field(min_length=1)
    business_name: str = Field(min_length=1)
    address: str
    phone: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    source_vendor: str

class MultiSchemaReconciler:
    """Reconciles inconsistent payloads from Google Places, Yelp, and internal POS systems."""
    
    @staticmethod
    def normalize_vendor_payload(raw_data: Dict[str, Any], vendor: str) -> UnifiedLocationProfile:
        try:
            if vendor == "google_places":
                return UnifiedLocationProfile(
                    location_id=str(raw_data.get("place_id", "")),
                    business_name=raw_data.get("name", "Unknown"),
                    address=raw_data.get("formatted_address", ""),
                    phone=raw_data.get("international_phone_number"),
                    rating=raw_data.get("rating"),
                    source_vendor="google_places"
                )
            elif vendor == "yelp_fusion":
                loc = raw_data.get("location", {})
                addr = ", ".join(loc.get("display_address", []))
                return UnifiedLocationProfile(
                    location_id=str(raw_data.get("id", "")),
                    business_name=raw_data.get("name", "Unknown"),
                    address=addr,
                    phone=raw_data.get("phone"),
                    rating=raw_data.get("rating"),
                    source_vendor="yelp_fusion"
                )
            elif vendor == "pos_internal":
                return UnifiedLocationProfile(
                    location_id=str(raw_data.get("store_code", "")),
                    business_name=raw_data.get("store_label", "Unknown"),
                    address=raw_data.get("street_line", "") + " " + raw_data.get("city_zip", ""),
                    phone=raw_data.get("contact_tel"),
                    rating=None,
                    source_vendor="pos_internal"
                )
            else:
                raise ValueError(f"Unsupported vendor schema: {vendor}")
        except ValidationError as err:
            logger.error("Schema validation failed on %s payload: %s", vendor, err)
            raise

def run_tests():
    print("=== RUNNING OPAXA MULTI-SCHEMA RECONCILIATION HARNESS ===")
    reconciler = MultiSchemaReconciler()

    # Vendor 1: Google Places
    g_payload = {
        "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
        "name": "Opaxa Store SF",
        "formatted_address": "100 Market St, San Francisco, CA",
        "rating": 4.8,
        "international_phone_number": "+1 415-555-0199"
    }
    res_g = reconciler.normalize_vendor_payload(g_payload, "google_places")
    assert res_g.location_id == "ChIJN1t_tDeuEmsRUsoyG83frY4"
    assert res_g.rating == 4.8
    print("[PASS] Google Places normalization verified.")

    # Vendor 2: Yelp Fusion
    y_payload = {
        "id": "yelp-sf-branch-99",
        "name": "Opaxa Store SF",
        "location": {"display_address": ["100 Market St", "San Francisco, CA 94105"]},
        "phone": "+14155550199",
        "rating": 4.5
    }
    res_y = reconciler.normalize_vendor_payload(y_payload, "yelp_fusion")
    assert res_y.location_id == "yelp-sf-branch-99"
    assert "San Francisco" in res_y.address
    print("[PASS] Yelp Fusion normalization verified.")

    # Vendor 3: Internal POS
    pos_payload = {
        "store_code": "POS-901",
        "store_label": "Downtown Branch",
        "street_line": "100 Market St",
        "city_zip": "SF 94105",
        "contact_tel": "415-555-0199"
    }
    res_pos = reconciler.normalize_vendor_payload(pos_payload, "pos_internal")
    assert res_pos.location_id == "POS-901"
    assert res_pos.source_vendor == "pos_internal"
    print("[PASS] Internal POS normalization verified.")
    print("=== OPAXA VERIFICATION 100% COMPLETE ===")

if __name__ == "__main__":
    run_tests()
