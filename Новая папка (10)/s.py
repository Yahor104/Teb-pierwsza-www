import pygame
import random
import copy
import sys
import matplotlib.pyplot as plt

# перед главным циклом
live_counts = []

pygame.init()
WIDTH, HEIGHT = 200, 100
SCALE = 6

screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("мир")

surface = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Количество существ
a = 1000

occupied = set()
poison = set()
food = set()
lives = []

weather = 1.3
pora_goda = "leto"
energy_from_food = 8
energy_from_sun = 3
energy_from_ground = 3
energy_from_all_life = 1
max_dejstwie = 6
hod = 0
hod500 = 0
max_nr_of_gens = 30
max_all = 0

def gene_if():
    global max_all
    max_all += 1
    if max_all >= 5:
        if if_gen == 0:
            if (x + 1, y) in occupied:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 1:
            if (x - 1, y) in occupied:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 2:
            if (x, y + 1) in occupied:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 3:
            if (x, y - 1) in occupied:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 4:
            if (x + 1, y) in poison:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 5:
            if (x - 1, y) in poison:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 6:
            if (x, y + 1) in poison:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 7:
            if (x, y - 1) in poison:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 8:
            if (x + 1, y) in food:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 9:
            if (x - 1, y) in food:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 10:
            if (x, y + 1) in food:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 11:
            if (x, y - 1) in food:
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 12:
            if pora_goda == "leto":
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 12:
            if pora_goda == "osen":
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 12:
            if pora_goda == "zima":
                life["genom_nr"] = if_gen_next
                gene_if()
        elif if_gen == 12:
            if pora_goda == "wesna":
                life["genom_nr"] = if_gen_next
                gene_if()


# Создание жизней
for _ in range(a):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)

    if (x, y) in occupied:
        continue

    life = {
        "x": x,
        "y": y,
        "energy": 50,
        "genom": [],
        "genom_nr": 0,
        "age" : 0,
        "max_age" : 100,
        "bron" : random.randint(0, 1)
    }

    occupied.add((x, y))
    lives.append(life)

# Геном
for life in lives:
    for _ in range(max_nr_of_gens):
        gen = {
            "->" : random.randint(0, 3),
            "next_gen" : random.randint(0, max_nr_of_gens - 1),
            "dejstwie" : random.randint(0, 5),
            "if_gen" : random.randint(0, max_dejstwie),
            "if_gen_next" : random.randint(0, max_nr_of_gens - 1)
        }
        life["genom"].append(gen)

# Главный цикл
# главный цикл
while True:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt  # чтобы выйти и построить график

        surface.fill((0, 0, 0))
        for x, y in food:
            pygame.draw.rect(surface, (0, 255, 0), (x, y, 1, 1))
        # Создаём словарь позиций
        pos_to_life = {(l["x"], l["y"]): l for l in lives}

        if pora_goda == "leto":
            weather = 1.3
        elif pora_goda == "osen":
            weather = 0.9
        elif pora_goda == "zima":
            weather = 0.7
        else:
            weather = 1
        dead = []
        new_lives = []

        for life in lives:
            if life["bron"] == 1:
                life["energy"] -= 1
            life["energy"] -= 1
            life["age"] += 1
            if life["energy"] <= 0 or life["age"] >= life["max_age"]:
                occupied.discard((life["x"], life["y"]))
                poison.add((life["x"], life["y"]))
                dead.append(life)
                continue
            elif life["energy"] >= 150:
                life["energy"] >= 140


            gen = life["genom"][life["genom_nr"]]
            life["genom_nr"] = gen["next_gen"]

            x, y = life["x"], life["y"]
            if_gen = gen["if_gen"]
            if_gen_next = gen["if_gen_next"]

            max_all = 0
            gene_if()

            # ==== ДВИЖЕНИЕ ====
            if gen["dejstwie"] == 0:
                dx, dy = 0, 0
                if gen["->"] == 0:   # вверх
                    dy = -1
                elif gen["->"] == 1: # влево
                    dx = -1
                elif gen["->"] == 2: # вниз
                    dy = 1
                elif gen["->"] == 3: # вправо
                    dx = 1

                nx = (x + dx) % WIDTH   # горизонтально зациклено
                ny = y + dy             # вертикаль пока без зацикливания


                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in occupied and (nx, ny) not in poison:
                    occupied.discard((x, y))
                    life["x"], life["y"] = nx, ny
                    occupied.add((nx, ny))

                    if (nx, ny) in food:
                        food.discard((nx, ny))
                        life["energy"] += energy_from_food

                pygame.draw.rect(surface, (0, 164, 212), (life["x"], life["y"], 1, 1))

            # ==== ПРЕВРАЩЕНИЕ ЯДА В ЕДУ ====
            elif gen["dejstwie"] == 1:
                dx, dy = 0, 0
                if gen["->"] == 0:
                    dy = -1
                elif gen["->"] == 1:
                    dx = -1
                elif gen["->"] == 2:
                    dy = 1
                elif gen["->"] == 3:
                    dx = 1

                tx = (x + dx) % WIDTH   # горизонтально зациклено
                ty = y + dy             # вертикаль пока без зацикливания
                if 0 <= tx < WIDTH and 0 <= ty < HEIGHT and (tx, ty) in poison:
                    poison.discard((tx, ty))
                    occupied.discard((tx, ty))
                    food.add((tx, ty))

                pygame.draw.rect(surface, (255, 160, 165), (x, y, 1, 1))

            # ==== ФОТОСИНТЕЗ ====
            elif gen["dejstwie"] == 2:
                if y < 13:
                    life["energy"] += energy_from_sun * 1.2 * weather * energy_from_all_life
                elif y < 25:
                    life["energy"] += energy_from_sun * 1 * weather * energy_from_all_life
                elif y < 38:
                    life["energy"] += energy_from_sun * 0.8 * weather * energy_from_all_life
                elif y < 50:
                    life["energy"] += energy_from_sun * 0.6 * weather * energy_from_all_life
                elif y < 63:
                    life["energy"] += energy_from_sun * 0.4 * weather * energy_from_all_life

                pygame.draw.rect(surface, (97, 189, 92), (x, y, 1, 1))

            # Действие убийства
            elif gen["dejstwie"] == 3:
                dx, dy = 0, 0
                if gen["->"] == 0:   # вверх
                    dy = -1
                elif gen["->"] == 1: # влево
                    dx = -1
                elif gen["->"] == 2: # вниз
                    dy = 1
                elif gen["->"] == 3: # вправо
                    dx = 1

                nx = (x + dx) % WIDTH   # горизонтально зациклено
                ny = y + dy             # вертикаль пока без зацикливания


                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in poison:
                    # Найти цель на клетке
                    target = pos_to_life.get((nx, ny))
                    if target and target not in dead and target["bron"] == 0:
                        dead.append(target)
                        occupied.discard((nx, ny))
                        life["energy"] += target["energy"] / 2
                    if (nx, ny) in food:
                        food.discard((nx, ny))
                        life["energy"] += energy_from_food

                    # перемещаем убийцу
                    occupied.discard((x, y))
                    life["x"], life["y"] = nx, ny
                    occupied.add((nx, ny))

                pygame.draw.rect(surface, (255, 248, 0), (life["x"], life["y"], 1, 1))
            elif gen["dejstwie"] == 4:
                if y > 87:
                    life["energy"] += energy_from_ground * 1.2 * energy_from_all_life
                elif y > 75:
                    life["energy"] += energy_from_ground * 1 * energy_from_all_life
                elif y > 63:
                    life["energy"] += energy_from_ground * 0.8 * energy_from_all_life
                elif y > 50:
                    life["energy"] += energy_from_ground * 0.6 * energy_from_all_life
                elif y > 38:
                    life["energy"] += energy_from_ground * 0.4 * energy_from_all_life

                pygame.draw.rect(surface, (79, 232, 179), (x, y, 1, 1))
            elif gen["dejstwie"] == 5:
                dx, dy = 0, 0
                if gen["->"] == 0:   # вверх
                    dy = -1
                elif gen["->"] == 1: # влево
                    dx = -1
                elif gen["->"] == 2: # вниз
                    dy = 1
                elif gen["->"] == 3: # вправо
                    dx = 1
                
                nx = (x + dx) % WIDTH   # горизонтально зациклено
                ny = y + dy             # вертикаль пока без зацикливания


                if (nx, ny) in occupied:
                    target = pos_to_life.get((nx, ny))
                    if target and target not in dead:
                        all_energy = life["energy"] + target["energy"]
                        life["energy"] = all_energy / 2
                        target["energy"] = all_energy / 2
                pygame.draw.rect(surface, (255, 147, 0), (x, y, 1, 1))
            else:
                pygame.draw.rect(surface, (186, 186, 186), (x, y, 1, 1))
            if life["energy"] > 99:
                new_life = {
                    "x": life["x"],
                    "y": life["y"],
                    "energy": life["energy"] / 2,
                    "genom": copy.deepcopy(life["genom"]),
                    "genom_nr": 0,
                    "age" : 0,
                    "max_age" : life["max_age"],
                    "bron" : life["bron"]
                }
                life["energy"] /= 2

                # найти свободную соседнюю клетку
                dirs = [(0,-1), (-1,0), (0,1), (1,0)]
                random.shuffle(dirs)
                for dx, dy in dirs:
                    nx = (life["x"] + dx) % WIDTH  # горизонтальное зацикливание
                    ny = life["y"] + dy
                    if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in occupied and (nx, ny) not in poison:
                        new_life["x"] = nx
                        new_life["y"] = ny
                        occupied.add((nx, ny))
                        break
                else:
                    continue  # нет места — ребёнка не создаём

                # небольшая мутация
                if random.randint(0, 1) == 0:
                    gen_mut = new_life["genom"][random.randint(0, 14)]
                    mut_type = random.randint(0, 5)
                    if mut_type == 0:
                        gen_mut["->"] = random.randint(0, 3)
                    elif mut_type == 1:
                        gen_mut["next_gen"] = random.randint(0, max_nr_of_gens - 1)
                    elif mut_type == 2:
                        gen_mut["dejstwie"] = random.randint(0, max_dejstwie)
                    elif mut_type == 3:
                        gen_mut["if_gen"] = random.randint(0, 24)
                    elif mut_type == 4:
                        gen_mut["if_gen_next"] = random.randint(0, max_nr_of_gens - 1)
                    elif mut_type == 5:
                        new_life["bron"] = random.randint(0, 1)

                new_lives.append(new_life)

        # удалить мёртвых
        for life in dead:
            if life in lives:  # проверка перед удалением
                lives.remove(life)


        # добавить новых
        lives.extend(new_lives)

        for x, y in poison:
            pygame.draw.rect(surface, (120, 0, 120), (x, y, 1, 1))

        screen.blit(
            pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE)),
            (0, 0)
        )
         # В конце каждого шага сохраняем количество живых
        live_counts.append(len(lives))

        # обновление экрана
        pygame.display.flip()
        clock.tick(60)
        if len(lives) < 1000:
            energy_from_all_life = 1
        elif len(lives) > 1000 and len(lives) < 2000:
            energy_from_all_life = 0.95
        elif len(lives) > 2000 and len(lives) < 3000:
            energy_from_all_life = 0.9
        elif len(lives) > 3000 and len(lives) < 4000:
            energy_from_all_life = 0.85
        elif len(lives) > 4000 and len(lives) < 5000:
            energy_from_all_life = 0.8
        elif len(lives) > 5000 and len(lives) < 6000:
            energy_from_all_life = 0.75
        elif len(lives) > 6000 and len(lives) < 7000:
            energy_from_all_life = 0.7
        elif len(lives) > 7000 and len(lives) < 8000:
            energy_from_all_life = 0.65
        elif len(lives) > 8000 and len(lives) < 9000:
            energy_from_all_life = 0.6
        elif len(lives) > 9000 and len(lives) < 10000:
            energy_from_all_life = 0.55
        elif len(lives) > 10000 and len(lives) < 11000:
            energy_from_all_life = 0.5
        elif len(lives) > 11000 and len(lives) < 12000:
            energy_from_all_life = 0.45
        elif len(lives) > 12000 and len(lives) < 13000:
            energy_from_all_life = 0.4
        elif len(lives) > 13000 and len(lives) < 14000:
            energy_from_all_life = 0.35
        elif len(lives) > 14000 and len(lives) < 15000:
            energy_from_all_life = 0.3
        elif len(lives) > 15000 and len(lives) < 16000:
            energy_from_all_life = 0.25
        elif len(lives) > 16000 and len(lives) < 17000:
            energy_from_all_life = 0.2
        elif len(lives) > 17000 and len(lives) < 18000:
            energy_from_all_life = 0.15
        elif len(lives) > 18000 and len(lives) < 19000:
            energy_from_all_life = 0.1
        elif len(lives) > 19000 and len(lives) < 20000:
            energy_from_all_life = 0.05
        elif len(lives) > 20000:
            energy_from_all_life = 0

        hod += 1
        hod500 += 1
        if hod500 >= 500:
            if pora_goda == "leto":
                pora_goda = "osen"
            elif pora_goda == "osen":
                pora_goda = "zima"
            elif pora_goda == "zima":
                pora_goda = "wesna"
            else:
                pora_goda = "leto"
            hod500 = 0
        print("Hod:", hod, "Live:", len(lives), "Pora goda", pora_goda, "weather:", weather, "FPS:", int(clock.get_fps()), "Life *:", energy_from_all_life)
        # Внутри главного цикла, после всех действий с живыми существами:

    except KeyboardInterrupt:
        print("Симуляция завершена пользователем.")
        break

    except Exception as e:
        print("Ошибка:", e)
        print("Симуляция остановлена.")
        break

# после выхода из цикла строим график
plt.plot(live_counts)
plt.title("Количество живых существ по времени")
plt.xlabel("Ходы")
plt.ylabel("Живые существа")
plt.show()