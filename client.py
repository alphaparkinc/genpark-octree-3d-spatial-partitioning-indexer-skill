class OctreeNode:
    def __init__(self, center: tuple[float, float, float], half_width: float, max_depth: int = 4):
        self.center = center
        self.half_width = half_width
        self.max_depth = max_depth
        self.points = []
        self.children = None

    def _get_octant(self, pt: tuple[float, float, float]) -> int:
        idx = 0
        if pt[0] >= self.center[0]: idx |= 4
        if pt[1] >= self.center[1]: idx |= 2
        if pt[2] >= self.center[2]: idx |= 1
        return idx

    def insert(self, pt: tuple[float, float, float], data: str = None) -> bool:
        if self.children is None:
            if len(self.points) < 4 or self.max_depth == 0:
                self.points.append((pt, data))
                return True
            self._subdivide()

        octant = self._get_octant(pt)
        return self.children[octant].insert(pt, data)

    def _subdivide(self):
        self.children = []
        hw = self.half_width / 2.0
        for dx in [-hw, hw]:
            for dy in [-hw, hw]:
                for dz in [-hw, hw]:
                    c = (self.center[0] + dx, self.center[1] + dy, self.center[2] + dz)
                    self.children.append(OctreeNode(c, hw, self.max_depth - 1))
        for pt, data in self.points:
            octant = self._get_octant(pt)
            self.children[octant].insert(pt, data)
        self.points = []

    def query_range(self, min_bound: tuple[float, float, float], max_bound: tuple[float, float, float]) -> list:
        # Check bounding box overlap
        for d in range(3):
            if (self.center[d] + self.half_width < min_bound[d] or
                self.center[d] - self.half_width > max_bound[d]):
                return []

        results = []
        if self.children is None:
            for pt, data in self.points:
                if all(min_bound[i] <= pt[i] <= max_bound[i] for i in range(3)):
                    results.append({"point": pt, "data": data})
            return results

        for child in self.children:
            results.extend(child.query_range(min_bound, max_bound))
        return results
