# models/network.py
class Block:
    def __init__(self, block_id, start_station, end_station):
        self.block_id = block_id
        self.start_station = start_station
        self.end_station = end_station
        self.occupied_by = None

    def is_free(self):
        return self.occupied_by is None


class Station:
    def __init__(self, name, platforms):
        self.name = name
        self.platforms = {p: None for p in platforms}  # platform_id -> train

    def assign_platform(self, train, platform_id):
        if self.platforms[platform_id] is None:
            self.platforms[platform_id] = train
            return True
        return False

    def release_platform(self, platform_id):
        self.platforms[platform_id] = None


class Network:
    def __init__(self):
        # Stations: A,B,C,D
        self.stations = {
            "A": Station("A", ["P1", "P2", "P3"]),
            "B": Station("B", ["P1", "P2", "Siding"]),
            "C": Station("C", ["P1", "P2"]),
            "D": Station("D", ["P1", "P2", "P3"]),
        }

        # Blocks between stations (3 segments each)
        self.blocks = []
        self._build_blocks()

    def _build_blocks(self):
        pairs = [("A", "B"), ("B", "C"), ("C", "D")]
        for (s1, s2) in pairs:
            for i in range(1, 4):
                self.blocks.append(Block(f"{s1}-{s2}-b{i}", s1, s2))
