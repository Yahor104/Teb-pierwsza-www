import pygame
import random
import math
import matplotlib.pyplot as plt

# --- Настройки ---
WIDTH, HEIGHT = 1000, 1000
NUM_AGENTS = 100
MUTATION_RATE = 0.000001
GENERATION_LENGTH = 300
TARGET_POS = (WIDTH // 2, 50)

# --- Оптимизация отрисовки ---
DRAW_EVERY_N_STEPS = 100  # отрисовывать агентов каждые N шагов

# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Искусственная Эволюция")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# --- Класс агента ---
class Agent:
    def __init__(self, dna=None):
        self.pos = [WIDTH // 2, HEIGHT - 50]
        self.vel = [0, 0]
        if dna:
            self.dna = dna
        else:
            self.dna = [[random.uniform(-1,1), random.uniform(-1,1)] for _ in range(GENERATION_LENGTH)]
        self.step = 0
        self.reached = False
        self.fitness = 0

    def update(self):
        if self.step < GENERATION_LENGTH and not self.reached:
            move = self.dna[self.step]
            self.vel[0] += move[0]
            self.vel[1] += move[1]
            # Ограничиваем максимальную скорость
            max_speed = 5
            self.vel[0] = max(-max_speed, min(max_speed, self.vel[0]))
            self.vel[1] = max(-max_speed, min(max_speed, self.vel[1]))
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.step += 1
            # Ограничение движения в пределах экрана
            self.pos[0] = max(0, min(WIDTH, self.pos[0]))
            self.pos[1] = max(0, min(HEIGHT, self.pos[1]))
            # Проверка на достижение цели
            if math.hypot(self.pos[0]-TARGET_POS[0], self.pos[1]-TARGET_POS[1]) < 10:
                self.reached = True

    def calculate_fitness(self):
        distance = math.hypot(self.pos[0]-TARGET_POS[0], self.pos[1]-TARGET_POS[1])
        self.fitness = 1 / (distance + 1)
        if self.reached:
            self.fitness *= 2

    def draw(self, screen):
        color = (0,255,0) if self.reached else (255,0,0)
        pygame.draw.circle(screen, color, (int(self.pos[0]), int(self.pos[1])), 5)

# --- Функции эволюции ---
def select_parent(agents):
    agents = sorted(agents, key=lambda a: a.fitness, reverse=True)
    return random.choice(agents[:10])

def crossover(dna1, dna2):
    point = random.randint(0, GENERATION_LENGTH-1)
    return dna1[:point] + dna2[point:]

def mutate(dna):
    for i in range(len(dna)):
        if random.random() < MUTATION_RATE:
            dna[i] = [random.uniform(-1,1), random.uniform(-1,1)]
    return dna

def next_generation(old_agents):
    for agent in old_agents:
        agent.calculate_fitness()
    new_agents = []
    for _ in range(NUM_AGENTS):
        parent1 = select_parent(old_agents)
        parent2 = select_parent(old_agents)
        child_dna = crossover(parent1.dna, parent2.dna)
        child_dna = mutate(child_dna)
        new_agents.append(Agent(child_dna))
    return new_agents

def calculate_statistics(agents):
    for agent in agents:
        agent.calculate_fitness()
    fitness_values = [a.fitness for a in agents]
    avg_fitness = sum(fitness_values)/len(fitness_values)
    best_fitness = max(fitness_values)
    reached_percent = sum(a.reached for a in agents)/len(agents)*100
    return avg_fitness, best_fitness, reached_percent

# --- Основной цикл ---
agents = [Agent() for _ in range(NUM_AGENTS)]
generation = 1
step = 0
step_counter = 0

# Для графика эволюции
avg_history = []
best_history = []
reached_history = []

running = True
while running:
    clock.tick(9999999999)
    step_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Обновление агентов ---
    for agent in agents:
        agent.update()

    # --- Отрисовка агентов каждые DRAW_EVERY_N_STEPS шагов ---
    if step_counter % DRAW_EVERY_N_STEPS == 0:
        screen.fill((30,30,30))
        pygame.draw.circle(screen, (0,0,255), TARGET_POS, 10)  # цель
        for agent in agents:
            agent.draw(screen)

        # Отображение статистики
        avg, best, reached = calculate_statistics(agents)
        stats_text = [
            f"Поколение: {generation}",
            f"Средний фитнес: {avg:.3f}",
            f"Лучший фитнес: {best:.3f}",
            f"% достигших цели: {reached:.1f}%"
        ]
        for i, text in enumerate(stats_text):
            img = font.render(text, True, (255,255,255))
            screen.blit(img, (10, 10 + i*20))

        pygame.display.flip()

    step += 1
    if step >= GENERATION_LENGTH:
        avg, best, reached = calculate_statistics(agents)
        avg_history.append(avg)
        best_history.append(best)
        reached_history.append(reached)
        print(f"Поколение {generation} | Avg Fitness: {avg:.3f} | Best Fitness: {best:.3f} | Reached: {reached:.1f}%")
        agents = next_generation(agents)
        step = 0
        generation += 1

# --- Построение графика после завершения ---
plt.figure(figsize=(10,5))
plt.plot(avg_history, label="Средний фитнес", color="orange", linewidth=2)
plt.plot(best_history, label="Лучший фитнес", color="green", linewidth=2)
plt.plot(reached_history, label="% достигших цели", color="blue", linewidth=2)
plt.xlabel("Поколение")
plt.ylabel("Значение")
plt.title("Эволюция агентов")
plt.grid(True)
plt.legend()
plt.show()

pygame.quit()
