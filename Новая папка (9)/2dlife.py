import pygame
import random
import copy
import sys

pygame.init()
WIDTH, HEIGHT = 400, 100   # внутренняя логика
SCALE = 4  # во сколько раз увеличиваем экран

screen = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
pygame.display.set_caption("Цикличный мир с деревьями")

surface = pygame.Surface((WIDTH, HEIGHT))  # рисуем всё на маленьком surface

pygame.display.set_caption("Цикличный мир с деревьями")
clock = pygame.time.Clock()

# Количество семян
a = 1000

# с како высоты energy
c = 0

generation = 0
alive_trees = []
trees = []
seeds = []
new_seeds = []
occupied = set()
paused = False  # состояние паузы
seg_en = 0
max_gen_if = 479
energy_sun = 1.0

# Нижние блоки
for x in range(WIDTH):
    occupied.add((x, HEIGHT-1))

# Создание начальных семян
for i in range(a):
    seed = {
        "x": random.randint(0, WIDTH - 1),
        "y": random.randint(0, HEIGHT - 2),  # не на нижнем блоке
        "energy": 3000,
        "max_age" : random.randint(10, 100),
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
            "RIGHT": random.randint(0, 29),
            "gen_if": random.randint(0, max_gen_if)
        }
        seed["genom"].append(gen)

def restart_simulation():
    global trees, seeds, alive_trees, new_seeds, occupied, generation, paused

    generation = 0
    alive_trees = []
    trees = []
    seeds = []
    new_seeds = []
    occupied = set()
    paused = False  # состояние паузы


    # Нижние блоки
    for x in range(WIDTH):
        occupied.add((x, HEIGHT-1))

    # Создание начальных семян
    for i in range(a):
        seed = {
            "x": random.randint(0, WIDTH - 1),
            "y": random.randint(0, HEIGHT - 2),  # не на нижнем блоке
            "energy": 3000,
            "max_age" : random.randint(10, 100),
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
                "RIGHT": random.randint(0, 29),
                "gen_if": random.randint(0, 239)
            }
            seed["genom"].append(gen)



while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused  # переключаем паузу
            elif event.key == pygame.K_r:
                restart_simulation()  # перезапуск
            elif event.key == pygame.K_UP:
                energy_sun += 0.01
            elif event.key == pygame.K_DOWN:
                energy_sun -= 0.01

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            mx //= SCALE  # приведение к логическим координатам
            my //= SCALE
            for tree in trees:
                for seg in tree["segments"]:
                    if seg["x"] == mx and seg["y"] == my:
                        print("\nTREE GENOM")
                        for i, gene in enumerate(tree["genom"]):
                            print(
                                f"{i:02d}: "
                                f"UP={gene['UP']:2d} "
                                f"DOWN={gene['DOWN']:2d} "
                                f"LEFT={gene['LEFT']:2d} "
                                f"RIGHT={gene['RIGHT']:2d}"
                                f"gen_if={gene['gen_if']:2d} "
                            )
                        print("-" * 40)
                        print("Energy:", tree["energy"])
                        print("max_age:", tree["max_age"])
                        break

    if paused:
        pygame.display.flip()
        clock.tick(60)
        continue  # пропускаем рост деревьев и семян

    surface.fill((0, 0, 0))  # очистка

    # Рост деревьев
    alive_trees = []
    for tree in trees:
        for segment in tree["segments"]:
            tree["energy"] -= 10
            if segment["wood"]:
                seg_en += 1
        new_segments = []
        for segment in tree["segments"]:
            tree["energy"] -= 10
            if segment["wood"]:
                base = HEIGHT - segment["y"] - c

                # проверяем только сегменты сверху
                multiplier = 3
                for yy in range(segment["y"]):
                    if (segment["x"], yy) in occupied:
                        multiplier -= 1
                    elif (segment["x"], yy) not in occupied:
                        multiplier += 1
                    if multiplier > 3:
                        multiplier = 3

                tree["energy"] += base * multiplier * energy_sun
                continue


            segment["wood"] = True
            nr_gen = segment["genom_nr"]
            gen = tree["genom"][nr_gen]
            if gen["gen_if"] < 15:
                if (segment["x"], segment["y"] - 1) in occupied:
                    segment["genom_nr"] = gen["gen_if"]
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 30:
                if (segment["x"], segment["y"] + 1) in occupied:
                    segment["genom_nr"] = gen["gen_if"] - 15
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 45:
                if (segment["x"] - 1, segment["y"]) in occupied:
                    segment["genom_nr"] = gen["gen_if"] - 30
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 60:
                if (segment["x"] + 1, segment["y"]) in occupied:
                    segment["genom_nr"] = gen["gen_if"] - 45
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 75:
                e = (gen["gen_if"] - 60) * 300
                if tree["energy"] < e:
                    segment["genom_nr"] = gen["gen_if"] - 60
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 90:
                e = (gen["gen_if"] - 75) * 30
                if tree["energy"] < e:
                    segment["genom_nr"] = gen["gen_if"] - 75
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 105:
                e = (gen["gen_if"] - 90) * 300
                if tree["energy"] > e:
                    segment["genom_nr"] = gen["gen_if"] - 90
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 120:
                e = (gen["gen_if"] - 105) * 30
                if tree["energy"] > e:
                    segment["genom_nr"] = gen["gen_if"] - 105
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 135:
                if len(tree["segments"]) < gen["gen_if"] + tree["max_age"] * 1:
                    segment["genom_nr"] = gen["gen_if"] - 120
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 150:
                if len(tree["segments"]) > gen["gen_if"] + tree["max_age"] * 1:
                    segment["genom_nr"] = gen["gen_if"] - 135
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 165:
                if len(tree["segments"]) < gen["gen_if"] + tree["max_age"] * 2:
                    segment["genom_nr"] = gen["gen_if"] - 150
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 180:
                if len(tree["segments"]) > gen["gen_if"] + tree["max_age"] * 2:
                    segment["genom_nr"] = gen["gen_if"] - 165
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 195:
                if seg_en < gen["gen_if"] * 20:
                    segment["genom_nr"] = gen["gen_if"] - 180
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 210:
                if seg_en > gen["gen_if"] * 20:
                    segment["genom_nr"] = gen["gen_if"] - 195
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 225:
                if seg_en < gen["gen_if"] * 60:
                    segment["genom_nr"] = gen["gen_if"] - 210
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue
            elif gen["gen_if"] < 240:
                if seg_en > gen["gen_if"] * 60:
                    segment["genom_nr"] = gen["gen_if"] - 180
                    if segment["genom_nr"] < 0:
                        segment["genom_nr"] = 0
                    continue


            # Вверх
            if segment["y"] > 0 and gen["UP"] < 15 and (segment["x"], segment["y"] - 1) not in occupied:
                new_segments.append({
                    "x": segment["x"],
                    "y": segment["y"] - 1,
                    "genom_nr": gen["UP"],
                    "wood": False,
                    "seed" : False
                })
                occupied.add((segment["x"], segment["y"] - 1))

            # Вниз
            if segment["y"] < HEIGHT - 1 and gen["DOWN"] < 15 and (segment["x"], segment["y"] + 1) not in occupied:
                new_segments.append({
                    "x": segment["x"],
                    "y": segment["y"] + 1,
                    "genom_nr": gen["DOWN"],
                    "wood": False,
                    "seed" : False
                })
                occupied.add((segment["x"], segment["y"] + 1))

            # Влево (циклично)
            new_x = (segment["x"] - 1) % WIDTH
            if gen["LEFT"] < 15 and (new_x, segment["y"]) not in occupied:
                new_segments.append({
                    "x": new_x,
                    "y": segment["y"],
                    "genom_nr": gen["LEFT"],
                    "wood": False,
                    "seed" : False
                })
                occupied.add((new_x, segment["y"]))

            # Вправо (циклично)
            new_x = (segment["x"] + 1) % WIDTH
            if gen["RIGHT"] < 15 and (new_x, segment["y"]) not in occupied:
                new_segments.append({
                    "x": new_x,
                    "y": segment["y"],
                    "genom_nr": gen["RIGHT"],
                    "wood": False,
                    "seed" : False
                })
                occupied.add((new_x, segment["y"]))
            if gen["RIGHT"] > 15 and gen["LEFT"] > 15 and gen["UP"] > 15 and gen["DOWN"] > 15:
                segment["seed"] = True
            if segment["seed"] == True:
                segment["wood"] = False
        seg_en = 0
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
                        "max_age" : tree["max_age"],
                        "genom": copy.deepcopy(tree["genom"])
                    }
                    b = random.randint(0, 3)
                    if b == 3:
                        gene = new_seed["genom"][random.randint(0, 14)]
                        direction = random.choice(["UP","DOWN","LEFT","RIGHT"])
                        gene[direction] = random.randint(0,29)
                    elif b == 2:
                        new_seed["max_age"] += random.randint(-3, 3)
                    elif b == 1:
                        gene = new_seed["genom"][random.randint(0, 14)]
                        gene["gen_if"] = random.randint(0, max_gen_if)
                    

                    seeds.append(new_seed)
                    # occupied.add((ds["x"], ds["y"]))  # ❌ не нужно

    trees = alive_trees

    # Падение семян и превращение в деревья
    new_seeds = []
    for seed in seeds:
        seed["x"] = seed["x"] % WIDTH
        if (seed["x"], seed["y"] + 1) not in occupied and seed["y"] != HEIGHT-2 and seed["energy"] > 0:
            seed["y"] += 1
            new_seeds.append(seed)
        elif seed["y"] != HEIGHT-2:
            continue
        elif seed["energy"] > 0:
            new_tree = {
                "color": [random.randint(0, 255) for _ in range(3)],
                "energy": seed["energy"],
                "genom": copy.deepcopy(seed["genom"]),
                "max_age": seed["max_age"],
                "age": 0,
                "segments": [{
                    "x": seed["x"],
                    "y": seed["y"],
                    "genom_nr": 0,
                    "wood": False,
                    "seed" : False
                }]
            }
            trees.append(new_tree)
            occupied.add((seed["x"], seed["y"]))
    seeds = new_seeds

    # Рисуем деревья
    for tree in trees:
        for segment in tree["segments"]:
            color = tree["color"] if segment["wood"] else (255, 255, 255)
            pygame.draw.rect(surface, color, (segment["x"], segment["y"], 1, 1))

    # Рисуем семена
    for seed in seeds:
        pygame.draw.rect(surface, (255, 255, 255), (seed["x"], seed["y"], 1, 1))

    # Нижний блок
    for x in range(WIDTH):
        pygame.draw.rect(surface, (200, 200, 0), (x, HEIGHT-1, 1, 1))

    screen.blit(pygame.transform.scale(surface, (WIDTH*SCALE, HEIGHT*SCALE)), (0, 0))
    pygame.display.flip()
    clock.tick(60)
    world_energy = 0
    for tree in trees:
        world_energy += tree["energy"]
    for seed in seeds:
        world_energy += seed["energy"]
    generation += 1
    print("Trees:", len(trees), "World energy:", int(world_energy), "FPS:", int(clock.get_fps()), "Generation:", generation, "Sun energy:", energy_sun)

