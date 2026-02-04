import pygame
import random
import copy
import sys

pygame.init()
WIDTH, HEIGHT = 200, 100
SCALE = 6

screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("мир")

surface = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()

a = 100
max_nr_of_gens = 15
max_nr_of_gen_do = 5
cells = []
occupied = set()
coord_map = {}
hod = 0

def wrap(x, y):
    return x % WIDTH, y % HEIGHT

for i in range(a):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    cell = {
        "energy" : 200,
        "genom" : [],
        "max_segments" : 100,
        "max_age" : 300,
        "age" : 0,
        "segments" : [{
            "id" : 0,
            "gen" : 0,
            "do_gen" : False,
            "parent_id" : None,
            "what_gen_do" : 5,
            "x" : x,
            "y" : y
        }]
    }
    coord_map[(x, y)] = (cell, cell["segments"][0])
    occupied.add((x, y))
    for j in range(max_nr_of_gens):
        gen = {
            "UP_gen" : random.randint(0, max_nr_of_gens * 2 - 1),
            "DOWN_gen" : random.randint(0, max_nr_of_gens * 2 - 1),
            "LEFT_gen" : random.randint(0, max_nr_of_gens * 2 - 1),
            "RIGHT_gen" : random.randint(0, max_nr_of_gens * 2 - 1),
            "UP_do" : random.randint(0, max_nr_of_gen_do - 1),
            "DOWN_do" : random.randint(0, max_nr_of_gen_do - 1),
            "LEFT_do" : random.randint(0, max_nr_of_gen_do - 1),
            "RIGHT_do" : random.randint(0, max_nr_of_gen_do - 1)
        }
        cell["genom"].append(gen)
    cells.append(cell)

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    surface.fill((0,0,0))
    dead = []
    new_cells = []
    for cell in cells:
        cell["age"] += 1
        if cell["energy"] <= 0 or cell["age"] >= cell["max_age"]:
            dead.append(cell)
        cell["energy"] -= len(cell["segments"])
        new_segments = []
        for segment in cell["segments"]:
            if segment["do_gen"] == False and cell["energy"] > 30 and cell["max_segments"] > len(cell["segments"]):
                cell["energy"] -= 20
                cell_gen = cell["genom"][segment["gen"]]
                if cell_gen["UP_gen"] < 15:
                    nx, ny = wrap(segment["x"], segment["y"] - 1)
                    if (nx, ny) not in occupied:
                        used_ids = {seg["id"] for seg in cell["segments"]}
                        new_id = 0
                        while new_id in used_ids:
                            new_id += 1
                        new_segment = {
                            "id" : new_id,
                            "gen" : cell_gen["UP_gen"],
                            "do_gen" : False,
                            "parent_id" : segment["id"],
                            "what_gen_do" : cell_gen["UP_do"],
                            "x" : nx,
                            "y" : ny
                        }
                        coord_map[(nx, ny)] = (cell, new_segment)
                        occupied.add((nx, ny))
                        new_segments.append(new_segment)
                if cell_gen["DOWN_gen"] < 15:
                    nx, ny = wrap(segment["x"], segment["y"] + 1)
                    if (nx, ny) not in occupied:
                        used_ids = {seg["id"] for seg in cell["segments"]}
                        new_id = 0
                        while new_id in used_ids:
                            new_id += 1
                        new_segment = {
                            "id" : new_id,
                            "gen" : cell_gen["DOWN_gen"],
                            "do_gen" : False,
                            "parent_id" : segment["id"],
                            "what_gen_do" : cell_gen["DOWN_do"],
                            "x" : nx,
                            "y" : ny
                        }
                        coord_map[(nx, ny)] = (cell, new_segment)
                        occupied.add((nx, ny))
                        new_segments.append(new_segment)
                if cell_gen["LEFT_gen"] < 15:
                    nx, ny = wrap(segment["x"] - 1, segment["y"])
                    if (nx, ny) not in occupied:
                        used_ids = {seg["id"] for seg in cell["segments"]}
                        new_id = 0
                        while new_id in used_ids:
                            new_id += 1
                        new_segment = {
                            "id" : new_id,
                            "gen" : cell_gen["LEFT_gen"],
                            "do_gen" : False,
                            "parent_id" : segment["id"],
                            "what_gen_do" : cell_gen["LEFT_do"],
                            "x" : nx,
                            "y" : ny
                        }
                        coord_map[(nx, ny)] = (cell, new_segment)
                        occupied.add((nx, ny))
                        new_segments.append(new_segment)
                if cell_gen["RIGHT_gen"] < 15:
                    nx, ny = wrap(segment["x"] + 1, segment["y"])
                    if (nx, ny) not in occupied:
                        used_ids = {seg["id"] for seg in cell["segments"]}
                        new_id = 0
                        while new_id in used_ids:
                            new_id += 1
                        new_segment = {
                            "id" : new_id,
                            "gen" : cell_gen["RIGHT_gen"],
                            "do_gen" : False,
                            "parent_id" : segment["id"],
                            "what_gen_do" : cell_gen["RIGHT_do"],
                            "x" : nx,
                            "y" : ny
                        }
                        coord_map[(nx, ny)] = (cell, new_segment)
                        occupied.add((nx, ny))
                        new_segments.append(new_segment)
                segment["do_gen"] = True
            elif cell["max_segments"] < len(cell["segments"]):
                segment["do_gen"] = True
            if segment["what_gen_do"] == 0:
                cell["energy"] += 3
                pygame.draw.rect(surface, (97, 189, 92), (segment["x"], segment["y"], 1, 1))
            elif segment["what_gen_do"] == 1:
                if cell["energy"] > 99:
                    can = False
                    if (segment["x"], segment["y"] - 1) not in occupied and (segment["x"], segment["y"] - 5) not in occupied:
                        cell["energy"] -= 100
                        can = True
                        nx, ny = wrap(segment["x"], segment["y"] - 5)
                    elif (segment["x"], segment["y"] + 1) not in occupied and (segment["x"], segment["y"] + 5) not in occupied:
                        cell["energy"] -= 100
                        can = True
                        nx, ny = wrap(segment["x"], segment["y"] + 5)
                    elif (segment["x"] - 1, segment["y"]) not in occupied and (segment["x"] - 5, segment["y"]) not in occupied:
                        cell["energy"] -= 100
                        can = True
                        nx, ny = wrap(segment["x"] - 5, segment["y"])
                    elif (segment["x"] + 1, segment["y"]) not in occupied and (segment["x"] + 5, segment["y"]) not in occupied:
                        cell["energy"] -= 100
                        nx, ny = wrap(segment["x"] + 5, segment["y"])
                        can = True
                    if can == True:
                        new_cell = {
                            "energy" : 100,
                            "genom" : copy.deepcopy(cell["genom"]),
                            "max_segments" : 100,
                            "max_age" : 300,
                            "age" : 0,
                            "segments" : [{
                                "id" : 0,
                                "gen" : 0,
                                "do_gen" : False,
                                "parent_id" : None,
                                "what_gen_do" : 5,
                                "x" : nx,
                                "y" : ny
                            }]
                        }
                        occupied.add((nx, ny))
                        if random.randint(0, 1) == 0:
                            mutate_gen = random.randint(0, max_nr_of_gens - 1)
                            mutate = random.randint(0, 7)
                            gen = cell["genom"][mutate_gen]
                            if mutate < 4:
                                gen[mutate] = random.randint(0, max_nr_of_gens * 2 - 1)
                            else:
                                gen[mutate] = random.randint(0, max_nr_of_gen_do - 1)
                        new_cells.append(new_cell)

                pygame.draw.rect(surface, (204, 109, 0), (segment["x"], segment["y"], 1, 1))
            
            elif segment["what_gen_do"] == 2:
                # хищник
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = wrap(segment["x"] + dx, segment["y"] + dy)

                    target = coord_map.get((nx, ny))
                    if target:
                        cell2, seg2 = target
                        if cell2 is not cell:
                            # сбрасываем do_gen у родителя сегмента
                            for seg3 in cell2["segments"]:
                                if seg3["id"] == seg2["parent_id"]:
                                    seg3["do_gen"] = False
                                    break
                            # удаляем сегмент
                            cell2["segments"].remove(seg2)
                            coord_map.pop((nx, ny))
                            occupied.discard((nx, ny))
                            cell["energy"] += 25



                pygame.draw.rect(surface, (232, 226, 0), (segment["x"], segment["y"], 1, 1))
            elif segment["what_gen_do"] == 3:
                pygame.draw.rect(surface, (0, 164, 212), (segment["x"], segment["y"], 1, 1))
            elif segment["what_gen_do"] == 4:
                pygame.draw.rect(surface, (0, 164, 212), (segment["x"], segment["y"], 1, 1))
            else:
                pygame.draw.rect(surface, (0, 164, 212), (segment["x"], segment["y"], 1, 1))
        cell["segments"].extend(new_segments)
    for cell in dead:
        for seg in cell["segments"]:
            coord_map.pop((seg["x"], seg["y"]), None)
            occupied.discard((seg["x"], seg["y"]))
        cells.remove(cell)
    cells.extend(new_cells)
    screen.blit(pygame.transform.scale(surface, (WIDTH*SCALE, HEIGHT*SCALE)), (0, 0))
    pygame.display.flip()
    clock.tick(60)
    hod += 1
    print("Hod:", hod, "FPS:", int(clock.get_fps()), "Cells:", len(cells))