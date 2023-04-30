import pygame
from time import sleep
pygame.init()

pieces = [ # all pieces
    [ # direction to take to have the piece
        [1, 0], # direction n°1
        [0, 1],
        [-1, 0]
    ],
    [
        [1, 0],
        [0, 1],
        [0, -1],
        [1, 0],
        [1, 0]
    ],
]

# Main class
class Game:
    def __init__(self):
        # variables
        self.brickSize = 25
        self.matriceLen = [20, 20]

        # Create the self.screen
        self.screen = pygame.display.set_mode((self.brickSize*self.matriceLen[0], self.brickSize*self.matriceLen[1]))

        # Title and Icon
        pygame.display.set_caption("Blockus")

        # Images
        self.brickImg = pygame.transform.scale(pygame.image.load("images/brick.png"), (self.brickSize, self.brickSize))

        # set properties
        self.matrice = [ [0 for i in range(self.matriceLen[1])] for j in range(self.matriceLen[0]) ]
        self.colors = [self.brickImg for i in range(3)]
        colors = [(255, 0, 0), 
                       (0, 255, 0), 
                       (0, 0, 255)]
        for color in range(len(colors)):
            self.fillColor(self.colors[color], colors[color])
        
        self.checkImg = pygame.Surface((self.brickSize, self.brickSize))
        self.fillColor(self.checkImg, (255, 255, 255))

        self.matrice[0][0] = 1

        self.render()
    
    def check(self, x, y, check: str ="all"):
        checkSameColor = True
        checkCorners = False

        try:
            for i in range(-1, 2):
                if (self.matrice[y][x+i] != 0 or self.matrice[y+i][x] != 0):
                    checkSameColor = False
                
            for j in [[-1, -1], [1, 1], [-1, 1], [1, -1]]:
                if self.matrice[y+j[0]][x+j[1]] != 0:
                    checkCorners = True
        except IndexError:
            pass
        
        if check == "all":
            return checkSameColor and checkCorners
        elif check == "color":
            return checkSameColor
        elif check == "corners":
            return checkCorners

    def render(self):
        self.screen.fill((0, 0, 0))
        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[y])):
                if self.matrice[y][x] != 0:
                    self.screen.blit(self.colors[self.matrice[y][x]], (x * self.brickSize, y * self.brickSize, self.brickSize, self.brickSize))
                    continue
                elif self.check(x, y):
                    self.screen.blit(self.checkImg, (x * self.brickSize, y * self.brickSize, self.brickSize, self.brickSize))
                    continue
        
        pygame.display.update()
    
    def place(self, x, y, pieceNum: int, color):
        # check if possible at first
        cornerFound = False
        colorFound = False

        for i in range(4):
            tempX = x
            tempY = y
            for move in self.rotate([[0, 0]] + pieces[pieceNum], i):
                tempX += move[0]
                tempY += move[1]
                if self.matrice[tempY][tempX] != 0 or not self.check(tempX, tempY, "color"):
                    colorFound = True

                if self.check(tempX, tempY, "corners"):
                    cornerFound = i
                    print("Corner found : "+str(cornerFound))
                
                # self.screen.blit(self.checkImg, (tempX * self.brickSize, tempY * self.brickSize, self.brickSize, self.brickSize))
                # pygame.display.update()
                # sleep(0.3)
            # self.render()
            
            if cornerFound != False and not colorFound:
                print(i)
                break
        
        if cornerFound == False or colorFound:
            print("Dododmage")
            return

        self.matrice[y][x] = color
        for move in self.rotate(pieces[pieceNum], cornerFound):
            x += move[0]
            y += move[1]
            self.matrice[y][x] = color
    
    def rotate(self, moves: list[list[int]], direction: int):
        for move in moves:
            if direction in [1, 3]:
                move[0], move[1] = move[1], move[0]
            
            if direction == 2:
                move[0] *= -1
                move[1] *= -1
            elif direction == 3:
                move[1] *= -1
        
        return moves
    
    def fillColor(self, surface, color):
        w, h = surface.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                surface.set_at((x, y), pygame.Color(r, g, b))


game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        x = x // game.brickSize
        y = y // game.brickSize
        if x < len(game.matrice[0]) and y < len(game.matrice) and game.matrice[y][x] == 0:
            game.place(x, y, 0, 2)
            game.render()