import sys
import json
from client import OctreeNode

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    if method == "range_query":
        tree = OctreeNode((0, 0, 0), 100.0)
        for p in params.get("points", []):
            tree.insert(tuple(p["pos"]), p.get("data"))
        return {"hits": tree.query_range(tuple(params["min"]), tuple(params["max"]))}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
