# -*- coding: utf-8 -*-
"""
GenPark Agentic Commerce UCP Catalog Resolver MCP Server
Exposes Universal Commerce Protocol catalog resolution tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GenParkAgenticCommerceUCPCatalogResolver

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-ucp-catalog-resolver", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "resolve_catalog_offer",
                        "description": "Resolves multi-merchant Universal Commerce Protocol catalogs with Pareto optimal pricing and SLA routing.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "product_query": {
                                    "type": "object",
                                    "properties": {
                                        "item_name": {"type": "string"},
                                        "category": {"type": "string"}
                                    },
                                    "required": ["item_name"]
                                }
                            },
                            "required": ["product_query"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "resolve_catalog_offer":
            resolver = GenParkAgenticCommerceUCPCatalogResolver()
            res = resolver.resolve_catalog_offer(
                product_query=args.get("product_query", {"item_name": "Sony WH-1000XM5"}),
                merchant_offers=args.get("merchant_offers")
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        r = GenParkAgenticCommerceUCPCatalogResolver()
        test_res = r.resolve_catalog_offer({"item_name": "Test Wireless Headset"})
        print(f"Test Best Merchant: {test_res['best_matched_offer']['merchant_name']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
