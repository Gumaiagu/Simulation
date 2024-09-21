import pygame
from random import randint, choice

WINDOW_SIZE = (1300, 800)
BACK_GROND_COLOR = (100, 100, 100)
FPS = 60    # frames per second

PREDATOR_NUMBER = 50    # Number of predators in the init of the simulation
PREDATOR_FOOD_TIME = 10     # Time in seconds that the predator can stay without food
PREDATOR_IMAGE = pygame.image.load('predator.png')  # Get the predator's image
PREDATOR_SIZE = (PREDATOR_IMAGE.get_width(), PREDATOR_IMAGE.get_height())    # Predator's image size
PREDATOR_SPEED = 1
PREDATOR_VISION_DISTANCE = 100
PREDATOR_MULTIPLY_FOODS = 2
PREDATOR_POSSIBLE_TIME = 30

FOOD_NUMBER = 50    # Number of foods in the init of the simulation
FOOD_SIZE = (32, 32)
FOOD_COLOR = (19, 117, 1)
FOOD_MULTIPLICATION_NUMBER = 0.5  # For each food that exist, more food is created

pygame.init()
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Evolution simulator')


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 32, 32)


def summon_food(foods):
    x = randint(100, WINDOW_SIZE[0] - 100)
    y = randint(100, WINDOW_SIZE[1] - 100)
    for food in foods:
        while True:
            if ((food.x - x) ** 2 + (food.y - y) ** 2) ** (1/2) <= FOOD_SIZE[0]:
                x = randint(100, WINDOW_SIZE[0] - 100)
                y = randint(100, WINDOW_SIZE[1] - 100)
                continue
            else:
                break
    foods.append(Food(x, y))


def grow(foods, ticks):
    if foods.__len__() < FOOD_NUMBER and ticks != 0 and ticks % (10 * 60) == 0:
        for i in range(0, round(foods.__len__() * FOOD_MULTIPLICATION_NUMBER)):
            x = randint(100, WINDOW_SIZE[0] - 100)
            y = randint(100, WINDOW_SIZE[1] - 100)
            foods.append(Food(x, y))


class Predator:
    def __init__(self, x, y, speed=PREDATOR_SPEED, vision_distance=PREDATOR_VISION_DISTANCE):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, PREDATOR_SIZE[0], PREDATOR_SIZE[1])
        self.time_to_die = PREDATOR_FOOD_TIME * FPS
        self.time_alive = PREDATOR_POSSIBLE_TIME * FPS

        # Variables that will be used to make the evolution
        self.vision_distance = vision_distance
        self.speed = speed
        self.eat_foods = 0

        # Variables that are used when walk random is functing
        self.ticks = 0
        self.directions = []

    def walk_random(self):
        if self.ticks % FPS * 2 == 0:
            self.directions = [choice(('a', 'd', 'stop')), choice(('w', 's', 'stop'))]

        for direction in self.directions:
            if direction == 'a' and self.x > 0:
                self.x -= self.speed
            elif direction == 'd' and self.x < WINDOW_SIZE[0] - PREDATOR_SIZE[0]:
                self.x += self.speed
            elif direction == 'w' and self.y > 0:
                self.y -= self.speed
            elif direction == 's' and self.y < WINDOW_SIZE[1] - PREDATOR_SIZE[1]:
                self.y += self.speed

    def walk(self, foods):
        distance_right = False
        closer = None
        if foods.__len__() != 0:
            closer = foods[0]
            for food in foods:
                distance = ((self.x - food.x) ** 2 + (self.y - food.y) ** 2) ** (1 / 2)
                if distance <= self.vision_distance:
                    distance_right = True
                    if distance <= ((self.x - closer.x) ** 2 + (self.y - closer.y) ** 2) ** (1 / 2):
                        closer = food

        if distance_right:
            if closer.x - self.x > 0:
                self.x += self.speed
            elif closer.x - self.x < 0:
                self.x -= self.speed
            if closer.y - self.y > 0:
                self.y += self.speed
            elif closer.y - self.y < 0:
                self.y -= self.speed
        else:
            self.walk_random()

        self.rect = pygame.Rect(self.x, self.y, PREDATOR_SIZE[0], PREDATOR_SIZE[1])

    def die(self):
        self.time_to_die -= 1
        self.time_alive -= 1


def summon_predator(predators, speed=PREDATOR_SPEED, vision_distance=PREDATOR_VISION_DISTANCE):
    side = choice(('x', 'y'))
    if side == 'x':
        x = choice((0, WINDOW_SIZE[0] - PREDATOR_SIZE[0]))
        y = randint(0, WINDOW_SIZE[1] - PREDATOR_SIZE[1])
    else:
        x = randint(0, WINDOW_SIZE[0] - PREDATOR_SIZE[0])
        y = choice((0, WINDOW_SIZE[1] - PREDATOR_SIZE[1]))
    for predator in predators:
        while True:
            if ((predator.x - x) ** 2 + (predator.y - y) ** 2) ** (1/2) <= PREDATOR_SIZE[0]:
                if side == 'x':
                    x = choice((0, WINDOW_SIZE[0] - PREDATOR_SIZE[0]))
                    y = randint(0, WINDOW_SIZE[1] - PREDATOR_SIZE[1])
                else:
                    x = randint(0, WINDOW_SIZE[0] - PREDATOR_SIZE[0])
                    y = choice((0, WINDOW_SIZE[1] - PREDATOR_SIZE[1]))
                continue
            else:
                break
    predators.append(Predator(x, y, speed, vision_distance))


def append_ability(predators, predator):
    if (predators.__len__() < PREDATOR_NUMBER and predator.eat_foods != 0
            and predator.eat_foods % PREDATOR_MULTIPLY_FOODS == 0):
        ability = choice(('speed', 'visible_distance'))
        if ability == 'speed':
            if predator.speed > PREDATOR_SPEED:
                new_evolution = randint(-1, 1)
            else:
                new_evolution = randint(0, 1)
            summon_predator(predators, speed=predator.speed+new_evolution)
        elif ability == 'visible_distance':
            if predator.vision_distance > PREDATOR_VISION_DISTANCE:
                new_evolution = randint(-10, 10)
            else:
                new_evolution = randint(0, 10)
            summon_predator(predators, vision_distance=predator.vision_distance+new_evolution)
        predator.eat_foods -= PREDATOR_MULTIPLY_FOODS


def draw(foods, predators):
    window.fill(BACK_GROND_COLOR)
    for food in foods:
        pygame.draw.rect(window, FOOD_COLOR, food.rect)

    for predator in predators:
        window.blit(PREDATOR_IMAGE, (predator.x, predator.y))
    pygame.display.update()


def update(foods, predators, ticks):
    for predator in predators:
        predator.ticks += 1
        predator.die()
        predator.walk(foods)
        if predator.time_to_die == 0 or predator.time_alive == 0:
            predators.remove(predator)
        for food in foods:
            if predator.rect.colliderect(food.rect):
                foods.remove(food)
                predator.time_to_die = PREDATOR_FOOD_TIME * FPS
                predator.eat_foods += 1
        append_ability(predators, predator)

    if foods.__len__() == 0:
        for _ in range(0, FOOD_NUMBER):
            summon_food(foods)
    grow(foods, ticks)


def main():
    foods = []
    predators = []

    for _ in range(0, FOOD_NUMBER):
        summon_food(foods)

    for _ in range(0, PREDATOR_NUMBER):
        summon_predator(predators)

    clock = pygame.time.Clock()
    ticks = 0
    running = True
    while running:
        clock.tick(FPS)
        ticks += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        if predators.__len__() == 0:
            break
        draw(foods, predators)
        update(foods, predators, ticks)


if __name__ == '__main__':
    while True:
        main()
