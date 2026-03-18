import pygame
import numpy

from scripts.sprites.basesprite import *
from scripts.sprites.sheet import *
from scripts.sprites.gui import *


def multiply_image(
    input_image: pygame.Surface,
    tile_size: pygame.typing.IntPoint,
    target_size: pygame.typing.IntPoint
) -> pygame.Surface:
    """
    utility to produce an image with a size of target_size, contains repeated copies of the image from tile_size
    """

    output_image = pygame.Surface(target_size, pygame.SRCALPHA)

    for y in range(0, int(target_size[1]), int(tile_size[1])):
        for x in range(0, int(target_size[0]), int(tile_size[0])):
            output_image.blit(input_image, (x, y))

    return output_image


def mode7(
    image: pygame.Surface,
    target_size: pygame.typing.IntPoint,
    cam: pygame.Vector3 = pygame.Vector3(0, 0, 10),
    angle: int = 0,
    fov: int = 250,
    scale: int = 10
) -> pygame.Surface:
    """
    utility to produce a mode 7 effect on an image.
    dont call this every frame.
    might have to do some numba njit wizardry so that its faster.
    """

    new_image = pygame.Surface(target_size)

    for y in range(target_size[1]):
        pz = y + cam.z
        sy = fov / pz

        for x_screen in range(target_size[0]):
            px = x_screen - image.size[0] / 2
            sx = px / pz

            rotated_sx = sx * numpy.cos(angle) - sy * numpy.sin(angle)
            rotated_sy = sx * numpy.sin(angle) + sy * numpy.cos(angle)

            texture_x = (rotated_sx * scale + cam.x) % image.size[0]
            texture_y = (rotated_sy * scale + cam.y) % image.size[1]

            color = image.get_at((int(texture_x), int(texture_y)))
            new_image.set_at((x_screen, y), color)

    return new_image
