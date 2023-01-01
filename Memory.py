# implementation of card game - Memory
import sys
import pygame
from pygame.locals import *
import random

pygame.init()

WIDTH = 800 * 1.5
HEIGHT = 100

# Load images
CARD_BACK = pygame.image.load("Assets/CardBack.jpg")
CARD_BACK = pygame.transform.scale(CARD_BACK, (75, 100))
# CARD_BACK_WIDTH = 236
# CARD_BACK_HEIGHT = 355

ACE = pygame.image.load('Assets/AceDiamond.png')
ACE = pygame.transform.scale(ACE, (75, 100))
TWO = pygame.image.load('Assets/2Spade.png')
TWO = pygame.transform.scale(TWO, (75, 100))
THREE = pygame.image.load('Assets/3Heart.png')
THREE = pygame.transform.scale(THREE, (75, 100))
FOUR = pygame.image.load('Assets/4Club.png')
FOUR = pygame.transform.scale(FOUR, (75, 100))
FIVE = pygame.image.load('Assets/5Diamond.png')
FIVE = pygame.transform.scale(FIVE, (75, 100))
SIX = pygame.image.load('Assets/6Spade.png')
SIX = pygame.transform.scale(SIX, (75, 100))
SEVEN = pygame.image.load('Assets/7Heart.png')
SEVEN = pygame.transform.scale(SEVEN, (75, 100))
EIGHT = pygame.image.load('Assets/8Club.png')
EIGHT = pygame.transform.scale(EIGHT, (75, 100))
# CARD_WIDTH = 200
# CARD_HEIGHT = 250

CARDS = [ACE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT] * 2


# helper function to initialize globals
def new_game():
    """ Initial condition of new game"""
    global state, exposed, index_list, turns, color
    
    state = 0
    turns = 0
    color = "Green"
    # label.set_text("Turns = " + str(turns))
    random.shuffle(CARDS)
    exposed = [False] * 16
    """ list of index of flipped up cards """
    index_list = []

# define button
def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 25)
    text_render = font.render(text, True, (255,255,255))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x+w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y-2), (x, y+h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y+h), (x+w, y+h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x+w, y+h), (x+w, y), 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, index_list, turns, color
    
    """ if game is not complete, run code """
    if len(index_list) < 16:
        
        """ flip cards when clicked """
        """ only do an action/ event when card is flipped down """
        if (exposed[pos[0] // 75] == False):
            
            """ state 0 -> initial state """
            if state == 0:
                state = 1
                exposed[pos[0] // 75] = True
                index_list.extend([pos[0] // 75])
            
                """ count number of turns """
                turns += 1
                # label.set_text("Turns = " + str(turns))
            
                """ state 1 -> 1 card face up """
            elif state == 1:
                state = 2
                exposed[pos[0] // 75] = True
                index_list.extend([pos[0] // 75])
            
                """ state 2 -> 2 cards face up """
            elif state == 2:
                state = 1
                exposed[pos[0] // 75] = True
                index_list.extend([pos[0] // 75])
            
                """ count number of turns """
                turns += 1
                # label.set_text("Turns = " + str(turns))
            
                """ determine if cards are not pairs """
                if CARDS[index_list[-3]] != CARDS[index_list[-2]]:
                    """ if cards are not pairs, flip the cards back down """
                    exposed[index_list[-3]] = False
                    exposed[index_list[-2]] = False
                    """ if cards are not pairs, delete from pair list """
                    index_list.pop(-2)
                    index_list.pop(-2)
        
        """" Congratulatory Message """
        if len(index_list) == 16:
            exposed = [False] * 16
            color = "Black"
            
# cards are logically 50x100 pixels in size    
def draw(canvas):

    canvas.fill((0,0,0))

    # create button
    restartButton = button(window, (5, HEIGHT / 3), "Restart")

    # draw cards
    for card_index in range(len(CARDS)):
        card_pos = (75 * card_index) + 75
        """" Draw card layout flipped up """
#        canvas.draw_polygon([(card_pos, 0), (card_pos, HEIGHT),
#                ((card_pos + 75), HEIGHT), ((card_pos + 75), 0)],
#                1, "Black")
#         canvas.draw_image(CARDS[card_index], ((CARD_WIDTH / 2), (CARD_HEIGHT / 2)),
#                 ((CARD_WIDTH), (CARD_HEIGHT)), ((card_pos + (75 / 2)), (HEIGHT / 2)),
#                 ((75), (100)))
        canvas.blit(CARDS[card_index], (card_pos, 0))
    
        """" Draw card layout flipped down """
        if exposed[card_index] == False:
            # canvas.draw_image(CARD_BACK, ((CARD_BACK_WIDTH / 2), (CARD_BACK_HEIGHT / 2)),
            #     ((CARD_BACK_WIDTH), (CARD_BACK_HEIGHT)), ((card_pos + (75 / 2)), (HEIGHT / 2)),
            #     (75, 100))
            canvas.blit(CARD_BACK, (card_pos, 0))
            
    if len(index_list) == 16:
        canvas.draw_text("CONGRATULATIONS!", (230, 60), 75, "White")
        canvas.draw_text("Press restart to play another game.", (400, 90), 30, "Yellow")

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePosition = pygame.mouse.get_pos()
            if CARD_BACK.get_rect().collidepoint(mousePosition):
                mouseclick(mousePosition)
            elif restartButton.collidepoint(mousePosition):
                new_game()

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

# create frame and add a button and labels
# frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
# frame.add_button("Restart", new_game)
# label = frame.add_label("Turns = " + str(turns))
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Memory")

# # register event handlers
# frame.set_mouseclick_handler(mouseclick)
# frame.set_draw_handler(draw)
#
# # get things rolling
# new_game()
# frame.start()

new_game()
while True:

    draw(window)

    pygame.display.update()


# Always remember to review the grading rubric