# -*- coding: utf-8 -*-
"""
GenPark Agentic Commerce UCP Catalog Resolver Client
Resolves multi-merchant Universal Commerce Protocol catalogs with Pareto optimal pricing and SLA routing.
Zero external dependencies -- Python 3.9+ standard library only.
"""

import math
from typing import Dict, Any, List

class GenParkAgenticCommerceUCPCatalogResolver:
    """
    Universal Commerce Protocol (UCP) Machine-to-Machine Resolver:
    Evaluates real-time merchant product availability, shipping SLAs, and multi-objective Pareto utilities.
    """

    def __init__(self, weight_price: float = 0.50, weight_sla: float = 0.30, weight_trust: float = 0.20):
        self.w_price = weight_price
        self.w_sla = weight_sla
        self.w_trust = weight_trust

    def calculate_sla_score(self, delivery_hours: float) -> float:
        """Exponential decay on delivery latency (24h = 0.85, 48h = 0.72, 120h = 0.45)."""
        return math.exp(-0.0065 * max(0.0, delivery_hours))

    def resolve_catalog_offer(
        self,
        product_query: Dict[str, Any],
        merchant_offers: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Computes Pareto-optimal merchant offer from UCP machine-readable endpoints.
        """
        if merchant_offers is None:
            merchant_offers = [
                {
                    "merchant_id": "MKT-WALMART-01",
                    "merchant_name": "Walmart Fulfillment",
                    "sku_id": "SKU-SONY-WH1000XM5",
                    "list_price_usd": 348.00,
                    "in_stock_quantity": 42,
                    "delivery_sla_hours": 24.0,
                    "merchant_trust_score": 0.96,
                    "protocol_endpoint": "https://api.walmart.com/ucp/v1/sku/XM5"
                },
                {
                    "merchant_id": "MKT-TARGET-02",
                    "merchant_name": "Target Restock",
                    "sku_id": "SKU-SONY-WH1000XM5",
                    "list_price_usd": 349.99,
                    "in_stock_quantity": 18,
                    "delivery_sla_hours": 20.0,
                    "merchant_trust_score": 0.95,
                    "protocol_endpoint": "https://api.target.com/ucp/v1/sku/XM5"
                },
                {
                    "merchant_id": "MKT-SHOPIFY-03",
                    "merchant_name": "Audiophile Direct (Shopify)",
                    "sku_id": "SKU-SONY-WH1000XM5",
                    "list_price_usd": 329.00,
                    "in_stock_quantity": 6,
                    "delivery_sla_hours": 72.0,
                    "merchant_trust_score": 0.88,
                    "protocol_endpoint": "https://audiophiledirect.com/ucp/v1/sku/XM5"
                },
                {
                    "merchant_id": "MKT-BESTBUY-04",
                    "merchant_name": "Best Buy Express",
                    "sku_id": "SKU-SONY-WH1000XM5",
                    "list_price_usd": 379.00,
                    "in_stock_quantity": 65,
                    "delivery_sla_hours": 4.0,
                    "merchant_trust_score": 0.98,
                    "protocol_endpoint": "https://api.bestbuy.com/ucp/v1/sku/XM5"
                }
            ]

        # Calculate price normalization bounds
        prices = [m["list_price_usd"] for m in merchant_offers]
        min_p = min(prices)
        max_p = max(prices)
        price_spread = max(0.01, max_p - min_p)

        scored_candidates = []
        for m in merchant_offers:
            # Normalized Price Utility: lower price = higher utility
            norm_price_util = 1.0 - ((m["list_price_usd"] - min_p) / price_spread)
            sla_util = self.calculate_sla_score(m["delivery_sla_hours"])
            trust_util = m["merchant_trust_score"]

            composite_util = (
                self.w_price * norm_price_util +
                self.w_sla * sla_util +
                self.w_trust * trust_util
            )

            scored_candidates.append({
                "merchant_id": m["merchant_id"],
                "merchant_name": m["merchant_name"],
                "sku_id": m["sku_id"],
                "list_price_usd": m["list_price_usd"],
                "delivery_sla_hours": m["delivery_sla_hours"],
                "merchant_trust_score": m["merchant_trust_score"],
                "composite_utility_score": round(composite_util, 4),
                "in_stock": m["in_stock_quantity"] > 0,
                "protocol_endpoint": m["protocol_endpoint"]
            })

        # Rank by composite utility
        scored_candidates.sort(key=lambda x: x["composite_utility_score"], reverse=True)
        winner = scored_candidates[0]
        arbitrage_savings = round(max_p - winner["list_price_usd"], 2)

        return {
            "queried_item": product_query.get("item_name", "Sony WH-1000XM5 Noise-Canceling Headphones"),
            "best_matched_offer": winner,
            "arbitrage_savings_vs_max_usd": arbitrage_savings,
            "pareto_ranking_leaderboard": scored_candidates
        }
