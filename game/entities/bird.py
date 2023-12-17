"""Bird Module"""
import pygame


class Bird:
    """
    Class representing the bird character in the game.
    """

    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    MAX_DISPLACEMENT = 16

    def __init__(self, x, y, bird_imgs):
        self.imgs = bird_imgs
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.imgs[0]

    def jump(self):
        """
        Make the bird perform a jump.
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        Move the bird based on its current velocity.
        """
        self.tick_count += 1

        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2
        displacement = min(displacement, self.MAX_DISPLACEMENT)

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            self.tilt = min(self.MAX_ROTATION, self.tilt + self.ROT_VEL)

        else:
            self.tilt = max(-90, self.tilt - self.ROT_VEL)

    def draw(self, win):
        """
        Draw the bird on the game window.
        """
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.imgs[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.imgs[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.imgs[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.imgs[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """
        Get the mask for collision detection.
        """
        return pygame.mask.from_surface(self.img)
