import pygame


class Ground:
    VEL = 5

    def __init__(self, y, ground_img):
        self.img = ground_img
        self.width = ground_img.get_width()

        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def collide(self, bird):
        bird_mask = bird.get_mask()
        ground_mask = pygame.mask.from_surface(self.img)

        ground_offset = (0, self.y - round(bird.y))

        g_point = bird_mask.overlap(ground_mask, ground_offset)

        if g_point:
            return True
        return False

    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))
