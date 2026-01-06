import pygame
import sys
import random
import copy

pygame.init()
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мир с несколькими клетками")
clock = pygame.time.Clock()
new_cell_R = 100
hod = 0
waiting_seeds = []

# -------------------
# Опции
# -------------------
sun_cycle_enabled = True  # Включить/выключить смену дня и ночи
walls_enabled = True      # Включить/выключить стены

# -------------------
# Определяем стены
# -------------------
walls = set()
def create_walls():
    w = set()
    for y in range(0, HEIGHT):
        w.add((200, y))  # вертикальная слева
    for y in range(0, HEIGHT):
        w.add((800, y))  # вертикальная справа
    for x in range(0, WIDTH):
        w.add((x, 150))  # горизонтальная сверху
    return w

if walls_enabled:
    walls = create_walls()

# Энергия от list (регулируемая)
list_energy = 5

# -------------------
# День/ночь
# -------------------
sun_on = True          # текущее состояние солнца (True = день)
sun_counter = 0        # счётчик ходов для смены дня/ночи
sun_duration = 10      # длительность дня или ночи в ходах

# -------------------
# Функция для создания новой симуляции
# -------------------
def restart_simulation(num_cells=new_cell_R):
    new_cells = []
    for _ in range(num_cells):
        cell = {
            "genom": [],
            "ip": 0,
            "energy": 50,
            "segments": [{"x": random.randint(0, WIDTH-1),
                          "y": random.randint(0, HEIGHT-1),
                          "type": "head"}]
        }

        for _ in range(10):
            instruction = {
                "genom_if": random.randint(0, 100),
                "genome_instruction": [],
                "next_genom": random.randint(0, 9)
            }
            for i in range(4):
                instruction["genome_instruction"].append({
                    "genome_storona": i + 1,
                    "genome_type": random.randint(0, 255)
                })
            cell["genom"].append(instruction)
        new_cells.append(cell)
    return new_cells

# стартовая симуляция
cells = restart_simulation(num_cells=new_cell_R)
paused = False

running = True
while running:
    # -------------------
    # Обработка событий
    # -------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                hod = 0
                cells = restart_simulation(num_cells=new_cell_R)
                waiting_seeds = []
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                list_energy += 1
            elif event.key == pygame.K_DOWN:
                list_energy = max(0, list_energy - 1)
            elif event.key == pygame.K_d:
                sun_cycle_enabled = not sun_cycle_enabled
                print("Смена дня и ночи:", "Включена" if sun_cycle_enabled else "Выключена")
            elif event.key == pygame.K_w:
                walls_enabled = not walls_enabled
                walls = create_walls() if walls_enabled else set()
                print("Стены:", "Включены" if walls_enabled else "Выключены")

    if paused:
        pygame.display.flip()
        clock.tick(10)
        continue

    # -------------------
    # Обновляем день/ночь
    # -------------------
    if sun_cycle_enabled:
        sun_counter += 1
        if sun_counter >= sun_duration:
            sun_on = not sun_on
            sun_counter = 0
    else:
        sun_on = True  # если режим выключен, всегда день

    screen.fill((0, 0, 0))
    new_cells = []
    alive_cells = []

    # множество занятых координат
    occupied = {(seg["x"], seg["y"]) for cell in cells for seg in cell["segments"]}
    if walls_enabled:
        occupied |= walls  # добавляем стены

    # -------------------
    # Обрабатываем клетки
    # -------------------
    for cell in cells:
        segments = cell["segments"]
        energy_cost = 0

        for segment in segments:
            if segment["type"] == "body":
                energy_cost += 0.5
            elif segment["type"] == "list":
                energy_cost += 0.1
            elif segment["type"] == "head":
                energy_cost += 3

        cell["energy"] -= energy_cost


        for segment in segments:
            if segment["type"] == "list" and sun_on:
                cell["energy"] += list_energy
            elif segment["type"] == "seed":
                segment["type"] = "head"
                cell["ip"] = 0
                cell.pop("parent", None)

        if cell["energy"] <= 0:
            continue
        alive_cells.append(cell)

        head = next((seg for seg in segments if seg["type"] == "head"), None)
        if head is None:
            continue

        instr = cell["genom"][cell["ip"]]
        head["type"] = "body"
        if instr["genom_if"] < 10:
            x, y = head["x"], head["y"]
            if (x - 1, y) in occupied:
                cell["ip"] = instr["genom_if"]
                continue
        elif instr["genom_if"] < 20:
            x, y = head["x"], head["y"]
            if (x - 1, y) in occupied:
                cell["ip"] = instr["genom_if"] - 10
                continue
        elif instr["genom_if"] < 30:
            x, y = head["x"], head["y"]
            if (x - 1, y) in occupied:
                cell["ip"] = instr["genom_if"] - 20
                continue
        elif instr["genom_if"] < 40:
            x, y = head["x"], head["y"]
            if (x - 1, y) in occupied:
                cell["ip"] = instr["genom_if"] - 30
                continue

        for i in range(4):
            cmd = instr["genome_instruction"][i]
            nx, ny = head["x"], head["y"]
            if cmd["genome_storona"] == 1: nx -= 1
            elif cmd["genome_storona"] == 2: ny += 1
            elif cmd["genome_storona"] == 3: nx += 1
            else: ny -= 1

            nx %= WIDTH
            ny %= HEIGHT

            if (nx, ny) in occupied:
                continue

            if cmd["genome_type"] < 50:
                typ = "head"
                cell["energy"] -= 5
            elif cmd["genome_type"] < 75:
                typ = "seed"
            elif cmd["genome_type"] < 150:
                typ = "list"
                cell["energy"] -= 5
            else:
                typ = "none"
                cell["energy"]

            if typ == "seed":
                if len(cells) + len(waiting_seeds) < 200:
                    b = copy.deepcopy(cell["genom"])
                    energy_for_new = cell["energy"] / 3
                    cell["energy"] -= energy_for_new
                    new_cell = {
                        "genom": b,
                        "ip": 0,
                        "energy": energy_for_new,
                        "segments": [{"x": nx, "y": ny, "type": "seed"}],
                        "parent": cell
                    }

                    if random.randint(0, 3) == 3:
                        new_gen = new_cell["genom"][random.randint(0, 9)]
                        r = random.randint(0, 2)
                        if r == 2:
                            new_gen["next_genom"] = random.randint(0, 9)
                        elif r == 1:
                            new_gen["genom_if"] = random.randint(0, 100)
                        else:
                            cmd_to_mutate = new_gen["genome_instruction"][random.randint(0, 3)]
                            cmd_to_mutate["genome_type"] = random.randint(0, 255)

                    waiting_seeds.append(new_cell)
                    occupied.add((nx, ny))
            else:
                segments.append({"x": nx, "y": ny, "type": typ})
                occupied.add((nx, ny))
                if len(segments) > 1000:
                    segments = segments[:1000]
                cell["segments"] = segments

        cell["ip"] = instr["next_genom"]

    # -------------------
    # Фильтруем клетки без головы
    # -------------------
    filtered_cells = [cell for cell in alive_cells if any(seg["type"] == "head" for seg in cell["segments"])]

    # -------------------
    # Активируем семена из очереди ожидания
    # -------------------
    slots_available = max(0, 200 - len(filtered_cells))
    to_activate = waiting_seeds[:slots_available]
    for seed_cell in to_activate:
        seed_cell["segments"][0]["type"] = "head"
        seed_cell["ip"] = 0
        seed_cell.pop("parent", None)
    waiting_seeds = waiting_seeds[slots_available:]
    cells = filtered_cells + to_activate

    # -------------------
    # Рисуем клетки
    # -------------------
    for cell in cells:
        for seg in cell["segments"]:
            if seg["type"] == "head":
                color = (0, 118, 189)
            elif seg["type"] == "list":
                color = (97, 189, 92)
            elif seg["type"] == "seed":
                color = (175, 219, 245)
            else:
                color = (246, 143, 70)
            pygame.draw.rect(screen, color, (int(seg["x"]), int(seg["y"]), 1, 1))

    # Рисуем стены
    if walls_enabled:
        for (wx, wy) in walls:
            pygame.draw.rect(screen, (255, 255, 255), (wx, wy, 1, 1))

    # -------------------
    # Панель Energy from LIST + Sun + Walls
    # -------------------
    panel_width, panel_height =0, 0
    panel_surface = pygame.Surface((panel_width, panel_height))
    panel_surface.fill((50, 50, 50))
    font = pygame.font.SysFont(None, 24)
    text_energy = font.render(f"Energy from LIST: {list_energy}", True, (255, 255, 255))
    text_ctrl = font.render("UP/DOWN - change 1 per press", True, (200, 200, 200))
    sun_text = font.render(f"Sun cycle: {'ON' if sun_cycle_enabled else 'OFF'}", True, (255, 255, 0))
    walls_text = font.render(f"Walls: {'ON' if walls_enabled else 'OFF'}", True, (255, 255, 255))
    panel_surface.blit(text_energy, (10, 10))
    panel_surface.blit(text_ctrl, (10, 40))
    panel_surface.blit(sun_text, (10, 70))
    panel_surface.blit(walls_text, (10, 100))
    screen.blit(panel_surface, (WIDTH - panel_width, 0))

    pygame.display.flip()
    clock.tick(60)
    hod += 1

    if hod % 10 == 0:
        print("Клетки:", len(cells), "Ходы:", hod, "Energy:", {list_energy})
