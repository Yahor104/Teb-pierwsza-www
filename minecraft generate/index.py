import random
import math
import os
import traceback

CHUNK_SIZE = 16
HEIGHT = 256
SEA_LEVEL = 63

block_symbols = {
    "bedrock": "BR",
    "stone": "ST",
    "dirt": "DI",
    "grass": "GR",
    "coal_ore": "CO",
    "iron_ore": "IR",
    "gold_ore": "GO",
    "redstone_ore": "RE",
    "diamond_ore": "DIAM",
    "lapis_ore": "LA",
    "water": "WA",
    "air": "  "
}

class ChunkGenerator:
    def __init__(self, seed, chunk_x, chunk_z):
        self.seed = seed
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.chunk = {}
        self.rand = random.Random(self._chunk_seed())

    def _chunk_seed(self):
        return (self.seed +
                self.chunk_x * 341873128712 +
                self.chunk_z * 132897987541)

    def height_noise(self, x, z):
        world_x = x + self.chunk_x * 16
        world_z = z + self.chunk_z * 16
        height = 64
        height += int(10 * math.sin(world_x * 0.05))
        height += int(10 * math.cos(world_z * 0.05))
        return max(1, min(255, height))

    def generate(self):
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                surface_height = self.height_noise(x, z)
                for y in range(HEIGHT):
                    if y <= 4 and y <= self.rand.randint(0, 4):
                        self.chunk[(x, y, z)] = "bedrock"
                    elif y < surface_height - 4:
                        self.chunk[(x, y, z)] = "stone"
                    elif y < surface_height:
                        self.chunk[(x, y, z)] = "dirt"
                    elif y == surface_height:
                        self.chunk[(x, y, z)] = "grass"
                    elif y <= SEA_LEVEL:
                        self.chunk[(x, y, z)] = "water"
                    else:
                        self.chunk[(x, y, z)] = "air"

        self.carve_caves()
        self.generate_ores()
        return self.chunk

    def carve_caves(self):
        for _ in range(self.rand.randint(0, 3)):
            cx = self.rand.randint(0, 15)
            cy = self.rand.randint(10, 70)
            cz = self.rand.randint(0, 15)
            radius = self.rand.randint(2, 4)
            for x in range(CHUNK_SIZE):
                for y in range(HEIGHT):
                    for z in range(CHUNK_SIZE):
                        dist = math.sqrt((x - cx)**2 + (y - cy)**2 + (z - cz)**2)
                        if dist < radius:
                            self.chunk[(x, y, z)] = "air"

    def generate_ore(self, block, veins, min_y, max_y, vein_size):
        for _ in range(veins):
            x = self.rand.randint(0, 15)
            y = self.rand.randint(min_y, max_y)
            z = self.rand.randint(0, 15)
            for _ in range(vein_size):
                dx = x + self.rand.randint(-1, 1)
                dy = y + self.rand.randint(-1, 1)
                dz = z + self.rand.randint(-1, 1)
                if (0 <= dx < CHUNK_SIZE and
                    0 <= dy < HEIGHT and
                    0 <= dz < CHUNK_SIZE and
                    self.chunk.get((dx, dy, dz)) == "stone"):
                    self.chunk[(dx, dy, dz)] = block

    def generate_ores(self):
        self.generate_ore("coal_ore", 20, 0, 127, 17)
        self.generate_ore("iron_ore", 20, 0, 63, 9)
        self.generate_ore("gold_ore", 2, 0, 31, 9)
        self.generate_ore("redstone_ore", 8, 0, 15, 8)
        self.generate_ore("diamond_ore", 1, 0, 15, 8)
        y = self.rand.randint(0, 16) + self.rand.randint(0, 16)
        self.generate_ore("lapis_ore", 1, y, y, 7)


# ============================
# START PROGRAMU
# ============================

try:
    print("=== GENERATOR CHUNKU (LAS + JASKINIE) ===\n")
    seed = int(input("Podaj seed świata: "))
    chunk_x = int(input("Podaj chunk X: "))
    chunk_z = int(input("Podaj chunk Z: "))

    gen = ChunkGenerator(seed, chunk_x, chunk_z)
    chunk = gen.generate()

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop, "chunk_output.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for y in range(HEIGHT):
            f.write(f"===== Y = {y} =====\n")
            for z in range(CHUNK_SIZE):
                line = ""
                for x in range(CHUNK_SIZE):
                    block = chunk[(x, y, z)]
                    symbol = block_symbols.get(block, "??")
                    line += f"{symbol} "
                f.write(line + "\n")
            f.write("\n")

    print("\n✔ Chunk wygenerowany i zapisany!")
    print("✔ Plik na pulpicie:", file_path)

except Exception:
    print("\nWystąpił błąd:\n")
    traceback.print_exc()

finally:
    input("\nNaciśnij ENTER aby zakończyć...")