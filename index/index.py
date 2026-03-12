import pygame
import sys
import random
import copy

# Inicjalizacja Pygame
pygame.init()


# Ustawienia okna
WIDTH, HEIGHT = 400, 200
SCALE = 4
screen = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))

surface = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")
clock = pygame.time.Clock()

cells = []
ocupited = set()

for i in range(100):
    cell = {
        "energy" : 100,
        "now_gen" : 0,
        "x" : random.randint(0, WIDTH - 1),
        "y" : random.randint(0, HEIGHT - 1),
        "genom" : []
    }
    for j in range(15):
        gen = {
            "do" : random.randint(0, 4),
            "do_2": random.randint(0, 3),
            "next" : random.randint(0, 14)
        }
        cell["genom"].append(gen)
    ocupited.add((cell["x"], cell["y"]))
    cells.append(cell)

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kolor tła (RGB)
    surface.fill((0, 0, 0))

    alive = []

    for cell in cells:
        cell["energy"] -= 1
        gen = cell["genom"][cell["now_gen"]]
        if gen["do"] == 0:
            cell["energy"] += 2
            pygame.draw.rect(surface, (0, 255, 0), (cell["x"], cell["y"], 1, 1))
        elif gen["do"] == 1:
            ate = False
            for other in cells:
                if other is cell:
                    continue

                # 4 sąsiedzi
                if other["x"] == cell["x"] and other["y"] == cell["y"] - 1:
                    ate = True
                elif other["x"] == cell["x"] and other["y"] == cell["y"] + 1:
                    ate = True
                elif other["x"] == cell["x"] - 1 and other["y"] == cell["y"]:
                    ate = True
                elif other["x"] == cell["x"] + 1 and other["y"] == cell["y"]:
                    ate = True

                if ate:
                    cell["energy"] += other["energy"]
                    other["energy"] = -1000
                    break

            pygame.draw.rect(surface, (255, 255, 0), (cell["x"], cell["y"], 1, 1))
        elif gen["do"] == 2:
            ocupited.discard((cell["x"], cell["y"]))

            # UP
            if gen["do_2"] == 0 and (cell["x"], cell["y"] - 1) not in ocupited:
                cell["y"] -= 1
            # DOWN
            elif gen["do_2"] == 1 and (cell["x"], cell["y"] + 1) not in ocupited:
                cell["y"] += 1
            #LEFT
            elif gen["do_2"] == 2 and (cell["x"] - 1, cell["y"]) not in ocupited:
                cell["x"] -= 1
            #RIGHT
            elif gen["do_2"] == 3 and (cell["x"] + 1, cell["y"]) not in ocupited:
                cell["x"] += 1

            # zawijanie świata
            cell["x"] %= WIDTH
            cell["y"] %= HEIGHT
            ocupited.add((cell["x"], cell["y"]))

            pygame.draw.rect(surface, (0, 0, 255), (cell["x"], cell["y"], 1, 1))
        elif gen["do"] == 3:
            pygame.draw.rect(surface, (255, 255, 255), (cell["x"], cell["y"], 1, 1))
        elif gen["do"] == 4:
            pygame.draw.rect(surface, (255, 255, 255), (cell["x"], cell["y"], 1, 1))
        if cell["energy"] <= 0:
            ocupited.discard((cell["x"], cell["y"]))
            continue
        elif cell["energy"] >= 200:
            new_cell = {
                "energy" : cell["energy"] / 2,
                "now_gen" : 0,
                "x" : cell["x"],
                "y" : cell["y"],
                "genom" : copy.deepcopy(cell["genom"])
            }
            # UP
            if (new_cell["x"], (new_cell["y"] + 1) % HEIGHT) not in ocupited:
                new_cell["y"] = (new_cell["y"] + 1) % HEIGHT
            # DOWN
            elif (new_cell["x"], (new_cell["y"] - 1) % HEIGHT) not in ocupited:
                new_cell["y"] = (new_cell["y"] - 1) % HEIGHT
            # RIGHT
            elif ((new_cell["x"] + 1) % WIDTH, new_cell["y"]) not in ocupited:
                new_cell["x"] = (new_cell["x"] + 1) % WIDTH
            # LEFT
            elif ((new_cell["x"] - 1) % WIDTH, new_cell["y"]) not in ocupited:
                new_cell["x"] = (new_cell["x"] - 1) % WIDTH
            else:
                continue


            cell["energy"] /= 2
            if random.randint(0, 3) == 0:
                gen = new_cell["genom"][random.randint(0, 14)]
                a = random.randint(0, 2)
                if a == 0:
                    gen["do"] = random.randint(0, 4)
                elif a == 1:
                    gen["do_2"] = random.randint(0, 3)
                else:
                    gen["next"] = random.randint(0, 14)

            alive.append(new_cell)
            ocupited.add((new_cell["x"], new_cell["y"]))
        cell["now_gen"] = gen["next"]
        alive.append(cell)
    cells = alive
    # Aktualizacja ekranu
    screen.blit(pygame.transform.scale(surface, (WIDTH*SCALE, HEIGHT*SCALE)), (0, 0))
    pygame.display.flip()
    clock.tick(600000000000)   # ograniczenie do 60 FPS

# Zakończenie programu
pygame.quit()
sys.exit()
