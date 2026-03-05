import pygame
import sys
import random
from copy import deepcopy

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")

plants = []

for i in range(300):
    x = random.randint(0, 800)
    y = random.randint(0, 600)
    plant = {
        'max_age' : 200,
        'age' : 0,
        'energy' : 1000,
        'sections' : [{
            'x' : x,
            'y' : y,
            'active_gen' : 0,
            'active_work' : 1,
            'work_end' : False
        }],
        'genom' : []
    }
    for j in range(15):
            plant['genom'].append({
            'UP' : random.randint(0, 30),
            'UP_WORK' : random.randint(0, 2),
            'DOWN' : random.randint(0, 30),
            'DOWN_WORK' : random.randint(0, 2),
            'LEFT' : random.randint(0, 30),
            'LEFT_WORK' : random.randint(0, 2),
            'RIGHT' :random.randint(0, 30),
            'RIGHT_WORK' : random.randint(0, 2),
            'IF1' : 0,
            'IF2' : 0,
            'IF3' : 0
        })
    plants.append(plant)

ocupited = set((250, 250))
ocupited.add((250, 249))

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Kolor tła (RGB)
    screen.fill((0, 0, 0))
    alive = []

    for plant in plants:
        seeds = []
        plant['age'] += 1
        new_sections = []
        plant['energy'] -= len(plant['sections']) * 1.01
        for section in plant['sections']:
            if section['work_end'] == False:
                gen = plant['genom'][section['active_gen']]
                if gen['UP'] < 15 and (section['x'] % WIDTH, (section['y'] - 1) % HEIGHT) not in ocupited:
                    seg = {
                        'x' : section['x'],
                        'y' : section['y'] - 1,
                        'active_gen' : gen['UP'],
                        'active_work' : gen['UP_WORK'],
                        'work_end' : False
                    }
                    if gen['UP_WORK'] == 0 or gen['UP_WORK'] == 2: 
                        seg['work_end'] = True
                    section['x'] = (section['x']) % WIDTH
                    section['y'] = (section['y']) % HEIGHT
                    new_sections.append(seg)
                    ocupited.add((seg['x'], seg['y']))
                if gen['DOWN'] < 15 and (section['x'] % WIDTH, (section['y'] + 1) % HEIGHT) not in ocupited:
                    seg = {
                        'x' : section['x'],
                        'y' : section['y'] + 1,
                        'active_gen' : gen['DOWN'],
                        'active_work' : gen['DOWN_WORK'],
                        'work_end' : False
                    }
                    if gen['DOWN_WORK'] == 0 or gen['DOWN_WORK'] == 2: 
                        seg['work_end'] = True
                    section['x'] = (section['x']) % WIDTH
                    section['y'] = (section['y']) % HEIGHT
                    new_sections.append(seg)
                    ocupited.add((seg['x'], seg['y']))
                if gen['LEFT'] < 15 and ((section['x'] - 1) % WIDTH, section['y'] % HEIGHT) not in ocupited:
                    seg = {
                        'x' : section['x'] - 1,
                        'y' : section['y'],
                        'active_gen' : gen['LEFT'],
                        'active_work' : gen['LEFT_WORK'],
                        'work_end' : False
                    }
                    if gen['LEFT_WORK'] == 0 or gen['LEFT_WORK'] == 2: 
                        seg['work_end'] = True
                    section['x'] = (section['x']) % WIDTH
                    section['y'] = (section['y']) % HEIGHT
                    new_sections.append(seg)
                    ocupited.add((seg['x'], seg['y']))
                if gen['RIGHT'] < 15 and ((section['x'] + 1) % WIDTH, section['y'] % HEIGHT) not in ocupited:
                    seg = {
                        'x' : section['x'] + 1,
                        'y' : section['y'],
                        'active_gen' : gen['RIGHT'],
                        'active_work' : gen['RIGHT_WORK'],
                        'work_end' : False
                    }
                    if gen['RIGHT_WORK'] == 0 or gen['RIGHT_WORK'] == 2: 
                        seg['work_end'] = True
                    section['x'] = (section['x']) % WIDTH
                    section['y'] = (section['y']) % HEIGHT
                    new_sections.append(seg)
                    ocupited.add((seg['x'], seg['y']))
                section['work_end'] = True


            if section['active_work'] == 0:
                plant['energy'] += 2.5
                color = (0, 255, 0)
            elif section['active_work'] == 1:
                color = (224, 99, 0)
            elif section['active_work'] == 2:
                color = (0, 0, 255)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, (section['x'], section['y'], 1, 1))
        if plant['energy'] <= 0:
            for section in plant['sections']:
                ocupited.discard((section['x'], section['y']))
            continue
        plant['sections'].extend(new_sections)
        if plant['age'] >= plant['max_age']:
            for section in plant['sections']:
                ocupited.discard((section['x'], section['y']))
                if section['active_work'] != 2:
                    continue
                seeds.append(section)
            for pl in seeds:
                new_plant = {
                    'max_age' : 200,
                    'age' : 0,
                    'energy' : plant['energy'] / len(seeds),
                    'sections' : [{
                        'x' : pl['x'],
                        'y' : pl['y'],
                        'active_gen' : 0,
                        'active_work' : 1,
                        'work_end' : False
                    }],
                    'genom' : deepcopy(plant['genom'])
                }
                if random.randint(1, 4) == 1:  # 25% szansy na mutację
                    g = random.randint(0, 14)  # który gen mutujemy
                    key = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT',
                                        'UP_WORK', 'DOWN_WORK', 'LEFT_WORK', 'RIGHT_WORK'])

                    if key.endswith('WORK'):
                        # mutacja typu pracy
                        new_plant['genom'][g][key] = random.randint(0, 2)
                    else:
                        # mutacja kierunku
                        new_plant['genom'][g][key] = random.randint(0, 14)


                plants.append(new_plant)
            continue


        
        alive.append(plant)
    plants = alive

    # Aktualizacja ekranu
    pygame.display.flip()

# Zakończenie programu
pygame.quit()
sys.exit()

