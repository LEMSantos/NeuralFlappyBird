import pygame
from random import randint
from GeneticSearch import GeneticSearch


WIDTH = 288
HEIGHT = 512
FPS = 30
POPULATION_SIZE = 100
MAX_UP_SPEED = -8
MAX_DOWN_SPEED = 15
PIPE_SPEED = -5

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
birds = []
pipes = []
fitness = []
solutions = GeneticSearch(POPULATION_SIZE,0.8,0.15,[2,6,6,1])

for i in range(POPULATION_SIZE):
    birds.append({'x': 75, 'y': HEIGHT//3, 'alive': True, 'color':(randint(0,255),randint(0,255),randint(0,255)), 'speed_y': 0})

for i in range(3):
    rand_size = randint(50,242)
    if i == 0:
        pipes.append(({'x': WIDTH, 'y': 0, 'width': 50, 'height': rand_size},{'x': WIDTH, 'y': rand_size+100, 'width': 50, 'height': HEIGHT-(rand_size+100)}))
    else:
        pipes.append(({'x': pipes[i-1][0]['x'] + 200, 'y': 0, 'width': 50, 'height': rand_size},{'x': pipes[i-1][0]['x'] + 200, 'y': rand_size+100, 'width': 50, 'height': HEIGHT-(rand_size+100)}))

for i in range(POPULATION_SIZE):
    fitness.append(1)

def restart():
    global birds
    for i in range(len(birds)):
        birds[i]['y'] = HEIGHT//3
        birds[i]['alive'] = True
        birds[i]['speed_y'] = 0
    for i in range(POPULATION_SIZE):
        fitness[i] = 1
    pipes.clear()
    for i in range(3):
        rand_size = randint(50,242)
        if i == 0:
            pipes.append(({'x': WIDTH, 'y': 0, 'width': 50, 'height': rand_size},{'x': WIDTH, 'y': rand_size+100, 'width': 50, 'height': HEIGHT-(rand_size+100)}))
        else:
            pipes.append(({'x': pipes[i-1][0]['x'] + 200, 'y': 0, 'width': 50, 'height': rand_size},{'x': pipes[i-1][0]['x'] + 200, 'y': rand_size+100, 'width': 50, 'height': HEIGHT-(rand_size+100)}))


def birds_alive():
    global birds

    for bird in birds:
        if bird['alive']:
            return True
    return False

def colision_bird():
    global birds, pipes

    for i in range(len(birds)):
        if birds[i]['y'] < -20 or birds[i]['y'] >= 372:
            birds[i]['alive'] = False
            continue
        for pipe in pipes:
            if pipe[0]['hitbox'].colliderect(birds[i]['hitbox']) or pipe[1]['hitbox'].colliderect(birds[i]['hitbox']):
                birds[i]['alive'] = False                                                                                            

def colision_pixel(bird,pipe):
    if (pipe['x'] < bird['x']-40 < (pipe['x'] + pipe['width'])) and (pipe['y'] < bird['y']-40 < (pipe['y'] + pipe['height'])):
        return True
    return False
    


running = True
while running:
    #inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    #update
            
    population = solutions.getPopulation()
    for i in range(len(population)):
        inputs = []
        if birds[i]['x'] > pipes[0][0]['x'] + pipes[0][0]['width']:
            inputs.append(((pipes[1][0]['y'] + pipes[1][0]['height'] + 50) - birds[i]['y'])/HEIGHT)
            inputs.append((pipes[1][0]['x'] - birds[i]['x'])/WIDTH)
        else:
            inputs.append(((pipes[0][0]['y'] + pipes[0][0]['height'] + 50) - birds[i]['y'])/HEIGHT)
            inputs.append((pipes[0][0]['x'] - birds[i]['x'])/HEIGHT)
        if birds[i]['alive']:
            if population[i].feedForward(inputs)[0] >= 0.5:
                birds[i]['speed_y'] = MAX_UP_SPEED
            if birds[i]['speed_y'] < MAX_DOWN_SPEED:
                birds[i]['speed_y']+=1
            birds[i]['y']+=birds[i]['speed_y']
            fitness[i]+=1       
    for i in range(len(pipes)):
        pipes[i][0]['x'] += PIPE_SPEED
        pipes[i][1]['x'] += PIPE_SPEED
    if pipes[0][0]['x'] <= -100:
        rand_size = randint(50,242)
        pipes.pop(0)
        pipes.append(({'x': pipes[1][0]['x'] + 200, 'y': 0, 'width': 50, 'height': rand_size},{'x': pipes[1][0]['x'] + 200, 'y': rand_size+100, 'width': 50, 'height': HEIGHT-(rand_size+100)}))

    #draw
    screen.fill((255,255,255))
    for i in range(len(birds)):
        if birds[i]['alive']:
            birds[i]['hitbox'] = pygame.draw.rect(screen,birds[i]['color'],[birds[i]['x']-10,birds[i]['y']-10,20,20])
    for i in range(len(pipes)):
        for j in range(len(pipes[i])):
            pipes[i][j]['hitbox'] = pygame.draw.rect(screen,(0,255,0),[pipes[i][j]['x'],pipes[i][j]['y'],pipes[i][j]['width'],pipes[i][j]['height']])
    pygame.draw.rect(screen,(0,200,0),[0,HEIGHT-120,WIDTH,HEIGHT-(HEIGHT-120)])

    colision_bird()
    if not birds_alive():
        restart()
        solutions.evolution(fitness)
        continue
    
    pygame.display.update()
    clock.tick(FPS)

    
pygame.quit()
