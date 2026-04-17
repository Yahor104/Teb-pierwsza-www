import pygame
import sys
import random
import copy

WIDTH, HEIGHT = 1920, 1080
FPS = 600
TITLE = "Pygame"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

bots = []
hod = 0
ocupited = set()

for i in range(500):
    ocupited.add((i+700, 700))
    ocupited.add((690, i+690))
    ocupited.add((1210, i+690))
for i in range(100):
    ocupited.add((i+690, 690))
    ocupited.add((i+1110, 690))

for i in range(300):
    bot = {
        'x': WIDTH/2,
        'y': HEIGHT-200,
        'score': 0,
        'now': 0,
        'genom': []
    }
    for j in range(10000):
        gen = {
            'next': random.randint(0, 9999),
            'x': random.randint(-1, 1),
            'y': random.randint(-1, 1),
            'if' : random.randint(0, 4),
            'if2' : random.randint(0, 9999)
        }
        bot['genom'].append(gen)
    bots.append(bot)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    hod += 1

    if hod >= 1000:
        bots = sorted(bots, key=lambda b: b['score'], reverse=True)

        # kopiujemy najlepszą 10 — TO JEST KLUCZOWE
        best10 = [copy.deepcopy(b) for b in bots[:10]]

        print("Najlepsze wyniki:")
        for i, b in enumerate(best10):
            print(i+1, "score:", b['score'])

        hod = 0

        # reset pozycji
        for bot in best10:
            bot['x'] = WIDTH/2
            bot['y'] = HEIGHT-200

        # nowa populacja zaczyna się od najlepszej 10
        bots = best10

        # tworzymy 290 mutacji
        for i in range(290):
            bot = copy.deepcopy(best10[random.randint(0, 9)])
            for j in range(10000):
                gen = bot['genom'][random.randint(0, 9999)]
                a = random.randint(1, 5)
                if a == 1:
                    gen['next'] = random.randint(0, 9999)
                elif a == 2:
                    gen['x'] = random.randint(-1, 1)
                elif a == 3:
                    gen['y'] = random.randint(-1, 1)
                elif a == 4:
                    gen['if'] = random.randint(0, 4)
                elif a == 5:
                    gen['if2'] = random.randint(0, 9999)
            bots.append(bot)

        continue

    for bot in bots:
        gen = bot['genom'][bot['now']]
        bot['now'] = gen['next']

        if gen['if'] == 0:
            if ((bot['x'], bot['y'] + 1)) in ocupited:
                gen = bot['genom'][gen['if2']]
                bot['now'] = gen['next']
        elif gen['if'] == 1:
            if ((bot['x'], bot['y'] - 1)) in ocupited:
                gen = bot['genom'][gen['if2']]
                bot['now'] = gen['next']
        elif gen['if'] == 2:
            if ((bot['x'] + 1, bot['y'])) in ocupited:
                gen = bot['genom'][gen['if2']]
                bot['now'] = gen['next']
        elif gen['if'] == 3:
            if ((bot['x'] - 1, bot['y'])) in ocupited:
                gen = bot['genom'][gen['if2']]
                bot['now'] = gen['next']

        if ((bot['x'] + gen['x']) % WIDTH, bot['y']) not in ocupited:
            bot['x'] = (bot['x'] + gen['x']) % WIDTH
        if ((bot['x'], bot['y'] + gen['y'])) not in ocupited:
            bot['y'] += gen['y']

        if bot['y']*-1 + HEIGHT > bot['score']:
            bot['score'] = bot['y']*-1 + HEIGHT-200

        pygame.draw.rect(screen, (255, 0, 0), (bot['x'], bot['y'], 1, 1))
    
    for (x, y) in ocupited:
        pygame.draw.rect(screen, (255, 255, 0), (x, y, 1, 1))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
