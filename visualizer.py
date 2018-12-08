import sys, pygame, simulator, requests, simulator, time
from flask import json
pygame.init()

# Define some colors
BACKGROUND_COLOR = (0, 0, 0)
EMPTY_COLOR = (255, 255, 255)
PLAYER_COLOR = (128, 128, 128)
HOME_BASE_COLOR = (0, 255, 0)
ENEMY_BASE_COLOR = (128, 128, 0)
RED = (255, 0, 0)
ENEMY_COLOR = RED
COLLECTIBLE_COLOR = (0, 0, 255)
MARGIN = 1

size = width, height = 700, 500

pygame.display.set_caption("PUZZLER 2018")

screen = pygame.display.set_mode(size)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

sim = None

def getNewSim():
    url = 'http://127.0.0.1:5000/simulator/state'
    reason = 'unknown'
    try:
        r = requests.get(url)
        if(r.status_code==200):
            sim = simulator.Simulator(fromDict=r.json())
            return sim
    except:
        pass
    return None

def processInput(events): 
   for event in events: 
      if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  or (event.type == pygame.QUIT): 
         sys.exit(0)

entityToColor = dict({
    simulator.BoardPiece.Bot:PLAYER_COLOR,
    simulator.BoardPiece.Enemy:ENEMY_COLOR,
    simulator.BoardPiece.Diamond:COLLECTIBLE_COLOR,
    simulator.BoardPiece.HomeBase:HOME_BASE_COLOR,
    simulator.BoardPiece.EnemyBase:ENEMY_BASE_COLOR
})

def draw(sim):
    global width
    global height
    screen.fill(BACKGROUND_COLOR)
    if sim == None:
        textsurface = myfont.render('connecting...', True, RED)
        screen.blit(textsurface,(0,0))
    else:
        pieceWidth = width/sim.board.width - 2*MARGIN
        pieceHeight = height/sim.board.height - 2*MARGIN
        for x in range(sim.board.width):
            for y in range(sim.board.height):
                pygame.draw.rect(screen,
                                EMPTY_COLOR,
                                [(pieceWidth + 2*MARGIN) * x + MARGIN,
                                (pieceHeight + 2*MARGIN) * y + MARGIN,
                                pieceWidth,
                                pieceHeight])
        for entity in sim.board.entities:
            pygame.draw.rect(screen,
                entityToColor[entity.boardPiece],
                [(pieceWidth + 2*MARGIN) * entity.position.x + MARGIN,
                (pieceHeight + 2*MARGIN) * entity.position.y + MARGIN,
                pieceWidth,
                pieceHeight])
    pygame.display.flip()

while 1:
    processInput(pygame.event.get())
    newSim = getNewSim()
    simChanged = False
    if((newSim is None) != (sim is None)):
        simChanged = True
    elif((newSim is not None) and (sim is not None)):
        simChanged = newSim.frame != sim.frame
    sim = newSim
    if(simChanged):
        draw(sim)