import pygame
import random
import copy
import sys

pygame.init()
WIDTH, HEIGHT = 200, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Цикличный мир с деревьями")
clock = pygame.time.Clock()

# Количество семян
a = 10

alive_trees = []
trees = []
seeds = []
new_seeds = []
occupied = set()

# Нижние блоки
for x in range(WIDTH):
    occupied.add((x, HEIGHT - 1))

# Создание начальных семян
for i in range(a):
    seed = {
        "x": random.randint(0, WIDTH - 1),
        "y": random.randint(0, HEIGHT - 2),  # не на нижнем блоке
        "energy": 60,
        "genom": []
    }
    seeds.append(seed)

# Геном семян
for seed in seeds:
    for i in range(15):
        gen = {
            "UP": random.randint(0, 29),
            "DOWN": random.randint(0, 29),
            "LEFT": random.randint(0, 29),
            "RIGHT": random.randint(0, 29)
        }
        seed["genom"].append(gen)

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # Рост деревьев
    alive_trees = []
    for tree in trees:
        new_segments = []
        for segment in tree["segments"]:
            tree["energy"] -= 10
            if segment["wood"]:
                base = HEIGHT - segment["y"]   # 1,2,3,4,5...
                multiplier = 3

                has_block = False
                has_free = False

                for yy in range(segment["y"] - 1, -1, -1):
                    if (segment["x"], yy) in occupied:
                        has_block = True
                    else:
                        has_free = True

                if has_block:
                    multiplier -= 1
                if has_free:
                    multiplier += 1

                if multiplier > 3:
                    multiplier = 3

                tree["energy"] += base * multiplier
                continue



            segment["wood"] = True
            nr_gen = segment["genom_nr"]
            gen = tree["genom"][nr_gen]

            # Вверх
            if segment["y"] > 0 and gen["UP"] < 15 and (segment["x"], segment["y"] - 1) not in occupied:
                new_segments.append({
                    "x": segment["x"],
                    "y": segment["y"] - 1,
                    "genom_nr": gen["UP"],
                    "wood": False
                })
                occupied.add((segment["x"], segment["y"] - 1))

            # Вниз
            if segment["y"] < HEIGHT - 1 and gen["DOWN"] < 15 and (segment["x"], segment["y"] + 1) not in occupied:
                new_segments.append({
                    "x": segment["x"],
                    "y": segment["y"] + 1,
                    "genom_nr": gen["DOWN"],
                    "wood": False
                })
                occupied.add((segment["x"], segment["y"] + 1))

            # Влево (циклично)
            new_x = (segment["x"] - 1) % WIDTH
            if gen["LEFT"] < 15 and (new_x, segment["y"]) not in occupied:
                new_segments.append({
                    "x": new_x,
                    "y": segment["y"],
                    "genom_nr": gen["LEFT"],
                    "wood": False
                })
                occupied.add((new_x, segment["y"]))

            # Вправо (циклично)
            new_x = (segment["x"] + 1) % WIDTH
            if gen["RIGHT"] < 15 and (new_x, segment["y"]) not in occupied:
                new_segments.append({
                    "x": new_x,
                    "y": segment["y"],
                    "genom_nr": gen["RIGHT"],
                    "wood": False
                })
                occupied.add((new_x, segment["y"]))

        tree["segments"].extend(new_segments)
        tree["age"] += 1
        if tree["age"] < tree["max_age"] and tree["energy"] > 0:
            alive_trees.append(tree)
        else:
            dead_seeds = []
            for seg in tree["segments"]:
                occupied.discard((seg["x"], seg["y"]))
                if not seg["wood"]:
                    dead_seeds.append(seg)

            if dead_seeds:
                available_energy = max(tree["energy"], 0)
                en_per_seed = available_energy / len(dead_seeds)
                tree["energy"] = 0

                for ds in dead_seeds:
                    new_seed = {
                        "x": ds["x"],
                        "y": ds["y"],
                        "energy": en_per_seed,
                        "genom": copy.deepcopy(tree["genom"])
                    }
                    if random.randint(0, 3) == 3:
                        gene = new_seed["genom"][random.randint(0, 14)]
                        direction = random.choice(["UP","DOWN","LEFT","RIGHT"])
                        gene[direction] = random.randint(0,29)

                    seeds.append(new_seed)  # ✅ только одно семя!
                    occupied.add((ds["x"], ds["y"]))

    trees = alive_trees

    # Падение семян и превращение в деревья
    new_seeds = []
    for seed in seeds:
        seed["x"] = seed["x"] % WIDTH  # цикличность по X
        if (seed["x"], seed["y"] + 1) not in occupied and seed["y"] != HEIGHT-2:
            seed["y"] += 1
            new_seeds.append(seed)
        elif seed["y"] != HEIGHT-2:
            continue
        else:
            # Превращаемся в дерево
            new_tree = {
                "color": [random.randint(0, 255) for _ in range(3)],
                "energy": seed["energy"],
                "genom": copy.deepcopy(seed["genom"]),
                "max_age": 80,
                "age": 0,
                "segments": [{
                    "x": seed["x"],
                    "y": seed["y"],
                    "genom_nr": 0,
                    "wood": False
                }]
            }
            trees.append(new_tree)
            occupied.add((seed["x"], seed["y"]))
    seeds = new_seeds

    # Рисуем деревья
    for tree in trees:
        for segment in tree["segments"]:
            color = tree["color"] if segment["wood"] else (255, 255, 255)
            pygame.draw.rect(screen, color, (segment["x"], segment["y"], 1, 1))

    # Рисуем семена
    for seed in seeds:
        pygame.draw.rect(screen, (255, 255, 255), (seed["x"], seed["y"], 1, 1))

    pygame.display.flip()
    clock.tick(1)
    print("Trees:", len(trees))
