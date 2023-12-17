"""Pipe Module"""
import random
import pygame


class Pipe:
    """
    Class representing the pipe objects.
    """

    GAP = 180
    VEL = 5

    def __init__(self, x, pipe_img):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_img, False, True)
        self.pipe_bottom = pipe_img

        self.passed = False
        self.set_height()

    def set_height(self):
        """
        Set randome pipe heights.
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """
        Move pipes based on velocity.
        """
        self.x -= self.VEL

    def collide(self, bird):
        """
        Collision detection with the bird
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True
        return False

    def draw(self, win):
        """
        Draw pipes on the game window.
        """
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))
