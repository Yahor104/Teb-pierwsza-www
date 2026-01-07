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
        "max_age" : 70,
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

def restart_simulation():
    global trees, seeds, alive_trees, new_seeds, occupied, generation, paused

    # Сброс состояния
    trees = []
    seeds = []
    alive_trees = []
    new_seeds = []
    occupied = set()
    paused = False
    generation = 0

    # Нижний блок земли
    for x in range(WIDTH):
        occupied.add((x, HEIGHT - 1))

    # Создание новых семян чуть выше земли
    for _ in range(a):
        seed = {
            "x": random.randint(0, WIDTH - 1),
            "y": random.randint(0, HEIGHT - 2),  # чуть выше нижнего блока
            "energy": 1000,
            "max_age": 70,
            "genom": []
        }

        # Геном семян
        for _ in range(15):
            gene = {
                "UP": random.randint(0, 29),
                "DOWN": random.randint(0, 29),
                "LEFT": random.randint(0, 29),
                "RIGHT": random.randint(0, 29)
            }
            seed["genom"].append(gene)

        seeds.append(seed)

    # Очистка экрана
    surface.fill((0, 0, 0))

    print("Симуляция перезапущена! 🌱")



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
        new_segments = []
        for segment in tree["segments"]:
            tree["energy"] -= 10
            if segment["wood"]:
                base = HEIGHT - segment["y"]
                base = base/2

                # проверяем только сегменты сверху
                multiplier = 3
                for yy in range(segment["y"]):
                    if (segment["x"], yy) in occupied:
                        multiplier -= 1
                    elif (segment["x"], yy) not in occupied:
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
                        "max_age" : tree["max_age"],
                        "genom": copy.deepcopy(tree["genom"])
                    }
                    a = random.randint(0, 3)
                    if a == 3:
                        gene = new_seed["genom"][random.randint(0, 14)]
                        direction = random.choice(["UP","DOWN","LEFT","RIGHT"])
                        gene[direction] = random.randint(0,29)
                    elif a == 2:
                        new_seed["max_age"] += random.randint(-3, 3)
                    

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
    print("Trees:", len(trees), "World energy:", int(world_energy), "FPS:", int(clock.get_fps()), "Generation:", generation)
