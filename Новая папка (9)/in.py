import pygame
import sys
import random
import copy
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 300, 300
FPS = 6000
TITLE = "Pygame"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

population_history = []
cells = []
ocupited = set()
poison = set()
hod = 0
hod_m = 0
now_m = 1
now = -0.1

for i in range(500):
    cell = {
        'energy' : 100,
        'x' : random.randint(0, WIDTH-1),
        'y' : random.randint(0, HEIGHT-1),
        'now' : 0,
        'age' : 0,
        'max_age' : 100,
        'genom' : []
    }
    for j in range(15):
        gen = {
            'next' : random.randint(0, 14),
            'do1' : random.randint(0, 3),
            'do2' : random.randint(0, 3),
            'if1' : random.randint(0, 10),
            'if2' : random.randint(0, 10),
            'if3' : random.randint(0, 100),
            'if4' : random.randint(0, 14)
        }
        cell['genom'].append(gen)
    ocupited.add((cell['x'], cell['y']))
    cells.append(cell)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    hod += 1
    hod_m += 1

    alive = []
    needEn = round(1 + len(cells)/20000 + now + len(poison)/200000, 1)

    for cell in cells:
        cell['energy'] -= needEn
        cell['age'] += 1

        if cell['energy'] <= 0 or cell['age'] >= cell['max_age']: # or cell['energy'] > 100:
            ocupited.discard((cell['x'], cell['y']))
            poison.add((cell['x'], cell['y']))
            continue

        gen = cell['genom'][cell['now']]

        if gen['if1'] == 0:
            if (gen['if2']/10)*2 > needEn:
                cell['now'] = gen['if4']
        elif gen['if1'] == 1:
            if (gen['if2']/10)*2 < needEn:
                cell['now'] = gen['if4']

        if gen['do1'] == 0:
            if gen['do2'] == 0 and ((cell['x']+1) % WIDTH, (cell['y']) % HEIGHT) not in ocupited and ((cell['x']+1) % WIDTH, (cell['y']) % HEIGHT) not in poison:
                ocupited.discard((cell['x'], cell['y']))
                cell['x'] += 1
                cell['x'] = cell['x'] % WIDTH
                cell['y'] = cell['y'] % HEIGHT
                ocupited.add((cell['x'], cell['y']))
            elif gen['do2'] == 1 and ((cell['x']-1) % WIDTH, (cell['y']) % HEIGHT) not in ocupited and ((cell['x']-1) % WIDTH, (cell['y']) % HEIGHT) not in poison:
                ocupited.discard((cell['x'], cell['y']))
                cell['x'] -= 1
                cell['x'] = cell['x'] % WIDTH
                cell['y'] = cell['y'] % HEIGHT
                ocupited.add((cell['x'], cell['y']))
            elif gen['do2'] == 2 and ((cell['x']) % WIDTH, (cell['y']+1) % HEIGHT) not in ocupited and ((cell['x']) % WIDTH, (cell['y']+1) % HEIGHT) not in poison:
                ocupited.discard((cell['x'], cell['y']))
                cell['y'] += 1
                cell['x'] = cell['x'] % WIDTH
                cell['y'] = cell['y'] % HEIGHT
                ocupited.add((cell['x'], cell['y']))
            elif gen['do2'] == 3 and ((cell['x']) % WIDTH, (cell['y']-1) % HEIGHT) not in ocupited and ((cell['x']) % WIDTH, (cell['y']-1) % HEIGHT) not in poison:
                ocupited.discard((cell['x'], cell['y']))
                cell['y'] -= 1
                cell['x'] = cell['x'] % WIDTH
                cell['y'] = cell['y'] % HEIGHT
                ocupited.add((cell['x'], cell['y']))
            cell['now'] = gen['next']
        elif gen['do1'] == 1:
            cell['energy'] += 2
        elif gen['do1'] == 2:
            # pola obok komórki
            neighbors = [
                ((cell['x'] + 1) % WIDTH, cell['y']),
                ((cell['x'] - 1) % WIDTH, cell['y']),
                (cell['x'], (cell['y'] + 1) % HEIGHT),
                (cell['x'], (cell['y'] - 1) % HEIGHT)
            ]

            for nx, ny in neighbors:
                if (nx, ny) in poison:
                    poison.remove((nx, ny))
                    cell['energy'] += 2 + len(poison) / 8000   # możesz zmienić wartość energii
                    break  # tylko jedna trucizna na turę

            cell['now'] = gen['next']
        elif gen['do1'] == 3:
            new = {
                'energy' : cell['energy'] / 2,
                'x' : cell['x'],
                'y' : cell['y'],
                'now' : 0,
                'age' : 0,
                'max_age' : cell['max_age'],
                'genom' : copy.deepcopy(cell['genom'])
            }
            if ((new['x']+1) % WIDTH, (new['y']) % HEIGHT) not in ocupited and ((new['x']+1) % WIDTH, (new['y']) % HEIGHT) not in poison:
                new['x'] = (new['x']+1) % WIDTH
                alive.append(new)
                ocupited.add((new['x'], new['y']))
                cell['energy'] = cell['energy'] / 2
            elif ((new['x']-1) % WIDTH, (new['y']) % HEIGHT) not in ocupited and ((new['x']-1) % WIDTH, (new['y']) % HEIGHT) not in poison:
                new['x'] = (new['x']-1) % WIDTH
                alive.append(new)
                ocupited.add((new['x'], new['y']))
                cell['energy'] = cell['energy'] / 2
            elif ((new['x']) % WIDTH, (new['y']+1) % HEIGHT) not in ocupited and ((new['x']) % WIDTH, (new['y']+1) % HEIGHT) not in poison:
                new['y'] = (new['y']+1) % HEIGHT
                alive.append(new)
                ocupited.add((new['x'], new['y']))
                cell['energy'] = cell['energy'] / 2
            elif ((new['x']) % WIDTH, (new['y']-1) % HEIGHT) not in ocupited and ((new['x']) % WIDTH, (new['y']-1) % HEIGHT) not in poison:
                new['y'] = (new['y']-1) % HEIGHT
                alive.append(new)
                ocupited.add((new['x'], new['y']))
                cell['energy'] = cell['energy'] / 2
            
            a = random.randint(0, 7)
            if random.randint(0, 3) == 0:
                g = new['genom'][random.randint(0, 14)]
                if a == 0:
                    g['next'] = random.randint(0, 14)
                elif a == 1:
                    g['do1'] = random.randint(0, 3)
                elif a == 2:
                    g['do2'] = random.randint(0, 3)
                elif a == 3:
                    new['max_age'] += random.randint(-2, 2)
                elif a == 4:
                    g['if1'] = random.randint(0, 10)
                elif a == 5:
                    g['if2'] = random.randint(0, 10)
                elif a == 6:
                    g['if3'] = random.randint(0, 100)
                elif a == 7:
                    g['if4'] = random.randint(0, 14)

        alive.append(cell)
        pygame.draw.rect(screen, (255, 255, 255), (cell['x'], cell['y'], 1, 1))

    cells = alive

    for px, py in poison:
        pygame.draw.rect(screen, (102, 0, 204), (px, py, 1, 1))

    if hod_m >= 1000:
        hod_m -= 1000
        if now_m == 1:
            now_m = 2
            now = -0.3
        elif now_m == 2:
            now_m = 3
            now = 0
        elif now_m == 3:
            now_m = 4
            now = 0.4
        elif now_m == 4:
            now_m = 1
            now = -0.1

    population_history.append(len(cells))
    print("Hod: ", hod,"  Cells: ", len(cells), "  FPS: ", int(clock.get_fps()), 'Energy need: ', needEn)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

plt.figure(figsize=(8, 4))
plt.plot(population_history, color='green')
plt.title("Population of Cells Over Time")
plt.xlabel("Frames")
plt.ylabel("Number of Living Cells")
plt.grid(True)
plt.show()

sys.exit()
