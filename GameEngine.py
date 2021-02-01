import pygame, math, noise, os, random
from pygame.locals import *


def load_animation(path, frame_durations, animation_frame_database):
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        animation_image.set_colorkey((255, 255, 255))
        animation_frame_database[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


def generate_chunk(x, y, CHUNK_SIZE): # generates chunks for plattformers to infinity
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0
            height = int(noise.pnoise1(target_x * 0.1, repeat=99999999) * 7)
            if target_y > 8 - height:
                tile_type = 2
            elif target_y == 8 - height:
                tile_type = 1
            elif target_y == 8 - height - 1:
                if random.randint(1, 5) == 1:
                    tile_type = 3
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data


def collision_test(rect, tiles):  # checks collision with !!!TILES!!!
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def flip(character_flip_value):
    pass


class Entity():
    def __init__(self, width: int, height: int, location: list):
        self.location = location
        self.width = width
        self.height = height
        self.movement = [0, 0]
        self.speed = 2
        self.flip = False
        self.rect = pygame.Rect(self.movement[0], self.movement[1], self.width, self.height)
        self.action = 'idle'
        self.frame = 0
        self.y_momentum = 0
        self.air_timer = 0
        self.moving_left = False
        self.moving_right = False

    def move(self):
        if self.moving_right:
            self.movement[0] += 2
        if self.moving_left:
            self.movement[0] -= 2
