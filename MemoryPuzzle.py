#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Memory Puzzle
# Invent With Python

# PEP 8:
# CONSTANT_NAMES
# variable_names
# function_names
# method_names
# ClassNames
# ExceptionNames
# 4 spaces indentation
# 72 characters long (max 79)

import sys, pygame, random
from pygame.locals import *

FPS = 30 			# frames per second, maximum speed of the program
WINDOW_WIDTH = 400 	# in pixels
WINDOW_HEIGHT = 380
REVEAL_SPEED = 8 	# speed boxes' sliding reveals/cover
BOX_SIZE = 40 		# height and width
GAP_SIZE = 10 		# gap between boxes
BOARD_WIDTH = 2		# number of columns of icons
BOARD_HEIGHT = 4	# number of rows of icons

assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even\
                                          number of boxes for pairs of match.'

X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2 )
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2 )

# colors		R    G    B
GRAY		= (100, 100, 100)
NAVY_BLUE	= ( 60,  60, 100)
WHITE		= (255, 255, 255)
RED			= (255,   0,   0)
GREEN		= (  0, 255,   0)
BLUE		= (  0,   0, 255)
YELLOW		= (255, 255,   0)
ORANGE		= (255, 128,   0)
PURPLE		= (255,   0, 255)
CYAN		= (  0, 255, 255)

BG_COLOR = NAVY_BLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE
HIGHLIGHT_COLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT, \
'Board is too big for the number of shapes/colors defined.'

def main():
	global FPS_CLOCK, DISPLAY_SURF
	pygame.init()
	FPS_CLOCK = pygame.time.Clock()
	DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	
	mouse_x = 0 # used to store x coordinate of mouse event
	mouse_y = 0 # used to store y coordinate of mouse event
	
	pygame.display.set_caption('Memory Game')
	
	main_board = get_randomized_board()
	revealed_boxes = generate_revealed_boxes_data(False)
	
	first_selection = None # stores the (x, y) of the first box clicked.
	
	DISPLAY_SURF.fill(BG_COLOR)
	start_game_animation(main_board)
	
	tries = 0
	score = 0
	match = 1
	best = 0
	
	s = 'ó'
	s = s.decode('utf-8')
	
	colors = [RED, GREEN, ORANGE, PURPLE, YELLOW, CYAN ]
	random.shuffle(colors)
	font_obj = pygame.font.Font('freesansbold.ttf', 35)
	text_surface_obj = font_obj.render('Jogo da mem'+ s +'ria', True, colors[2])	
	text_rect_obj = text_surface_obj.get_rect()
	text_rect_obj.midtop = ((WINDOW_WIDTH / 2), 20)
	
	
	
	while True: # main game loop
		mouse_clicked = False
		DISPLAY_SURF.fill(BG_COLOR) # drawing the window
		draw_board(main_board, revealed_boxes)
		display_tries(tries, score, match, best)
		DISPLAY_SURF.blit(text_surface_obj, text_rect_obj)
		
		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mouse_x, mouse_y = event.pos
			elif event.type == MOUSEBUTTONUP:
				mouse_x, mouse_y = event.pos
				mouse_clicked = True
				
		box_x, box_y = get_box_at_pixel(mouse_x, mouse_y)
		if box_x != None and box_y != None:
			# The mouse is currently over a box.
			if not revealed_boxes[box_x][box_y]:
				draw_highlight_box(box_x, box_y)
			if not revealed_boxes[box_x][box_y] and mouse_clicked:
				reveal_boxes_animation(main_board, [(box_x, box_y)])
				revealed_boxes[box_x][box_y] = True # set box as revealed
				
				# print first_selection	
				
				if first_selection == None: # this was the first box clicked
					first_selection = (box_x, box_y)
				
					# print first_selection
					
					
					
				else: # this was the second one
				# Check if there is a match between the teo icons.
					tries += 1
					icon1_shape, icon1_color = get_shape_and_color(main_board, first_selection[0], first_selection[1])
					icon2_shape, icon2_color = get_shape_and_color(main_board, box_x, box_y)
					if icon1_shape != icon2_shape or icon1_color != icon2_color:
					# Icons don't match. Re-cover up both selections.
						pygame.time.wait(1000) #in milliseconds, 1 second
						cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (box_x, box_y)])
						revealed_boxes[first_selection[0]][first_selection[1]] = False
						revealed_boxes[box_x][box_y] = False
					elif has_won(revealed_boxes): #check if all pairs found
						game_won_animation(main_board)
						pygame.time.wait(2000)
					
						# Reset the board.
						main_board = get_randomized_board()
						revealed_boxes = generate_revealed_boxes_data(False)
					
						# Show the fully unrevealed board for a second.
						draw_board(main_board, revealed_boxes)
						pygame.display.update()
						pygame.time.wait(1000)
						
						if score < best or best == 0:
							best = score
						tries = 0
						score = 0
						match += 1
						
						# Replay the start game animation.
						start_game_animation(main_board)
						
					else:
						score += 1
					first_selection = None # reset this variable
				
		# Redraw the screen and wait a clock tick.
		pygame.display.update()
		FPS_CLOCK.tick(FPS)


		
def display_tries(tries, score, match, best):
	A = BOARD_WIDTH * BOARD_HEIGHT / 2
	font_obj = pygame.font.Font('freesansbold.ttf', 15)
	text_surface_obj1 = font_obj.render('Tentativas: %r' % tries, True, WHITE)	
	text_rect_obj1 = text_surface_obj1.get_rect()
	
	text_surface_obj2 = font_obj.render('Pontos: %r/%r' % (score, A), True, WHITE)	
	text_rect_obj2 = text_surface_obj2.get_rect()
	
	text_surface_obj3 = font_obj.render('Partida: %r' % match, True, WHITE)	
	text_rect_obj3 = text_surface_obj3.get_rect()
	
	text_surface_obj4 = font_obj.render('Melhor:' + ' %r tentativas' % best, True, WHITE)	
	text_rect_obj4 = text_surface_obj4.get_rect()
	
	text_rect_obj1.topleft = (15, 300)
	text_rect_obj2.topleft = (15, 340)
	text_rect_obj3.topleft = ((WINDOW_WIDTH / 2), 300)
	text_rect_obj4.topleft = ((WINDOW_WIDTH / 2), 340)
	
	DISPLAY_SURF.blit(text_surface_obj1, text_rect_obj1)
	DISPLAY_SURF.blit(text_surface_obj2, text_rect_obj2)
	DISPLAY_SURF.blit(text_surface_obj3, text_rect_obj3)
	# DISPLAY_SURF.blit(text_surface_obj4, text_rect_obj4)

		
def generate_revealed_boxes_data(val):
	revealed_boxes = []
	for i in range (BOARD_WIDTH):
		revealed_boxes.append([val] * BOARD_HEIGHT)
	return revealed_boxes
	
def get_randomized_board():
	"""Get a list of every possible shape in every possible colours, create
	the board with randomly placed icons.
	"""
	icons = []
	for color in ALL_COLORS:
		for shape in ALL_SHAPES:
			icons.append((shape, color))
	random.shuffle(icons) # randomize the order of the icons list
	num_icons_used = int(BOARD_WIDTH * BOARD_HEIGHT / 2) #calculate how many icons needed
	icons = icons[:num_icons_used] * 2 # create two of each
	random.shuffle(icons)
	# Create the board data structure, whit randomly placed icons.
	board = []
	for x in range(BOARD_WIDTH):
		column = []
		for y in range(BOARD_HEIGHT):
			column.append(icons[0])
			del icons [0] # remove icons already assigned
		board.append(column)
	return board

	
def split_into_groups_of(group_size, the_list):
	""" Splits a list into a list of lists, where the inner lists have
	at most group_size number of items.
	"""
	result = []
	for i in range(0, len(the_list), group_size):
		result.append(the_list[i:i + group_size])
	return result
	
def left_top_coords_of_box(box_x, box_y):
	""" Convert board coordinates to pixel coordinates"""
	left = box_x * (BOX_SIZE + GAP_SIZE) + X_MARGIN
	top = box_y * (BOX_SIZE + GAP_SIZE) + Y_MARGIN
	return (left, top)
	
def get_box_at_pixel(x, y):
	for box_x in range(BOARD_WIDTH):
		for box_y in range(BOARD_HEIGHT):
			left, top = left_top_coords_of_box(box_x, box_y)
			box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
			if box_rect.collidepoint(x, y):
				return (box_x, box_y)
	return (None, None)
	
def draw_icon(shape, color, box_x, box_y):
	quarter =	int(BOX_SIZE * 0.25)	# syntactic sugar
	half =		int(BOX_SIZE * 0.5)		# syntactic sugar
	left, top = left_top_coords_of_box(box_x, box_y)
	# Draw the shapes.
	if shape == DONUT:
		pygame.draw.circle(DISPLAY_SURF, color, (left + half, top + half), half - 5)
		pygame.draw.circle(DISPLAY_SURF, BG_COLOR, (left + half, \
		top + half), quarter - 5)
	elif shape == SQUARE:
		pygame.draw.rect(DISPLAY_SURF, color, \
		(left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))
	elif shape == DIAMOND:
		pygame.draw.polygon(DISPLAY_SURF, color, ((left + half, top), (left + \
		BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), \
		(left, top + half)))
	elif shape == LINES:
		for i in range(0, BOX_SIZE, 4):
			pygame.draw.line(DISPLAY_SURF, color, (left, top + i), \
			(left + i, top))
			pygame.draw.line(DISPLAY_SURF, color, (left + i, top + BOX_SIZE\
			- 1),(left + BOX_SIZE - 1, top + i))
	elif shape == OVAL:
		pygame.draw.ellipse(DISPLAY_SURF, color, (left, top + quarter,\
		BOX_SIZE, half))
		
def get_shape_and_color(main_board, box_x, box_y):
	""" Shape value for x, y spot is stored in board[x][y][0],
	color value for x, y spot is stored in board [x][y][1]
	"""
	return main_board[box_x][box_y][0], main_board[box_x][box_y][1]
	
def draw_box_covers(board, boxes, coverage):
	""" Draw boxes being covered/revealed. "boxes" is a list of 
	two-item lists, which have the x & y spot of the box.
	"""
	for box in boxes:
		left, top = left_top_coords_of_box(box[0], box[1])
		pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (left, top, BOX_SIZE,
		BOX_SIZE))
		shape, color = get_shape_and_color(board, box[0], box[1])
		draw_icon(shape, color, box[0], box[1])
		if coverage > 0: # draw cover if there is an coverage
			pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left, top, coverage,
			BOX_SIZE))
	pygame.display.update()
	FPS_CLOCK.tick(FPS)
	
def reveal_boxes_animation(board, boxes_to_cover):
	""" Box reveal animation."""
	for coverage in range(BOX_SIZE, (-REVEAL_SPEED) - 1, -REVEAL_SPEED):
		draw_box_covers(board, boxes_to_cover, coverage)
		
def cover_boxes_animation(board, boxes_to_cover):
	""" Box cover animation."""
	for coverage in range(0, BOX_SIZE + REVEAL_SPEED, REVEAL_SPEED):
		draw_box_covers(board, boxes_to_cover, coverage)
		
def draw_board(board, revealed):
	""" Draws all of the boxes in their covered or revealed state."""
	for box_x in range(BOARD_WIDTH):
		for box_y in range(BOARD_HEIGHT):
			left, top = left_top_coords_of_box(box_x, box_y)
			if not revealed[box_x][box_y]:
			# Draw covered box.
				pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left,\
			top, BOX_SIZE, BOX_SIZE))
			else:
				# Draw the (revealed) icon.
				shape, color = get_shape_and_color(board, box_x, box_y)
				draw_icon(shape, color, box_x, box_y)
				
def draw_highlight_box(box_x, box_y):
	left, top = left_top_coords_of_box(box_x, box_y)
	pygame.draw.rect(DISPLAY_SURF, HIGHLIGHT_COLOR, (left - 5, top - 5,\
	BOX_SIZE + 10, BOX_SIZE + 10), 4)
	
def start_game_animation(board):
	""" Randomly reveal the boxes, 8 at a time."""
	covered_boxes = generate_revealed_boxes_data(False)
	boxes = []
	for x in range(BOARD_WIDTH):
		for y in range(BOARD_HEIGHT):
			boxes.append((x, y))
	random.shuffle(boxes)
	box_groups = split_into_groups_of(8, boxes)
	draw_board(board, covered_boxes)
	for box_group in box_groups:
		reveal_boxes_animation(board, box_group)
		cover_boxes_animation(board, box_group)
	global tries
	global score
	tries = 0
	scpre = 0
		
def game_won_animation(board):
	"""flash the bg color when the player has won"""
	covered_boxes = generate_revealed_boxes_data(True)
	color1 = LIGHT_BG_COLOR
	color2 = BG_COLOR
	for i in range(13):
		color1, color2 = color2, color1 # swap colors
		DISPLAY_SURF.fill(color1)
		draw_board(board, covered_boxes)
		pygame.display.update()
		pygame.time.wait(300)
		
def has_won(revealed_boxes):
	""" Return True if all the boxes have been revealed, otherwise False"""
	for i in revealed_boxes:
		if False in i:
			return False # return False if any boxes are covered
	return True
	
if __name__ == '__main__':
	main()