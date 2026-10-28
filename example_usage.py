# -*- coding: utf-8 -*-
"""
Example usage of GenParkAgenticCommerceUCPCatalogResolver
Demonstrates multi-merchant UCP catalog resolution across Price, SLA, and Merchant Trust.
"""

from client import GenParkAgenticCommerceUCPCatalogResolver

def main():
    resolver = GenParkAgenticCommerceUCPCatalogResolver(weight_price=0.45, weight_sla=0.35, weight_trust=0.20)

    query = {"item_name": "Sony WH-1000XM5 Wireless Noise-Canceling Headphones"}

    res = resolver.resolve_catalog_offer(query)

    print("================================================================")
    print("GenPark Agentic Commerce UCP Catalog Resolver - Live Resolution")
    print("================================================================\n")
    print(f"Target Product         : {res['queried_item']}")
    print(f"Pareto Winner Merchant : {res['best_matched_offer']['merchant_name']} (${res['best_matched_offer']['list_price_usd']})")
    print(f"Delivery SLA Window    : {res['best_matched_offer']['delivery_sla_hours']} hours")
    print(f"Arbitrage Savings      : ${res['arbitrage_savings_vs_max_usd']} vs most expensive listing\n")
    print("UCP Merchant Leaderboard:")
    for m in res["pareto_ranking_leaderboard"]:
        print(f"  * {m['merchant_name']:<30} | ${m['list_price_usd']:>6.2f} | {m['delivery_sla_hours']:>4.1f}h SLA | Trust: {m['merchant_trust_score']} | Score: {m['composite_utility_score']}")

if __name__ == "__main__":
    main()
