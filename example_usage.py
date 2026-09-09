from client import OctreeNode

def main():
    print("=== Octree 3D Spatial Partitioning Indexer ===")
    root = OctreeNode(center=(0.0, 0.0, 0.0), half_width=50.0, max_depth=4)

    # Insert 3D spatial points
    root.insert((10.0, 10.0, 10.0), "drone_1")
    root.insert((-5.0, -2.0, 15.0), "drone_2")
    root.insert((40.0, 40.0, 40.0), "drone_3")
    root.insert((0.0, 5.0, 0.0), "base_station")

    # Range query: [0, 20] x [0, 20] x [0, 20]
    hits = root.query_range((0.0, 0.0, 0.0), (20.0, 20.0, 20.0))
    print("Range query hits:", hits)
    hit_ids = [h["data"] for h in hits]
    assert "drone_1" in hit_ids
    assert "base_station" in hit_ids
    assert "drone_3" not in hit_ids

    print("Octree 3D Indexer verified successfully!")

if __name__ == "__main__":
    main()
