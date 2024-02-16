""" Flappy Bird Module"""

import os
import pickle
import pygame
import neat

try:
    from game.entities.ground import Ground
    from game.entities.pipe import Pipe
    from game.entities.bird import Bird
except ImportError:
    from entities.ground import Ground
    from entities.pipe import Pipe
    from entities.bird import Bird

from config import SCREENSHOT_FILE_PATH


class FlappyBirdGame:
    """
    Flappy Bird game class
    """

    def __init__(self, train_mode: bool = False):
        pygame.font.init()
        pygame.display.set_caption("Blappy Fird")
        pygame.display.set_icon(pygame.image.load("game/images/bird_icon.ico"))

        self.win_width, self.win_height = 1080, 1920
        self.win = pygame.display.set_mode((self.win_width, self.win_height))

        self.filepath = SCREENSHOT_FILE_PATH

        self.train_mode = train_mode
        self.gen = 0

        self.bird_imgs = [
            pygame.transform.scale2x(
                pygame.image.load(
                    f"game/images/bluebird-{state}flap.png"
                ).convert_alpha()
            )
            for state in ["down", "mid", "up"]
        ]

        self.pipe_img = pygame.transform.scale2x(
            pygame.image.load("game/images/pipe.png").convert_alpha()
        )
        self.ground_img = pygame.transform.scale2x(
            pygame.image.load("game/images/ground.png").convert_alpha()
        )
        self.background_img = pygame.transform.scale(
            pygame.image.load("game/images/background.png").convert_alpha(), (600, 900)
        )

        self.stat_font = pygame.font.SysFont("Arial", 50)

    def run(self, frames: int = 0):
        """
        Start the main game logic
        """
        if self.train_mode:
            self.train_ai()
        else:
            self.play_ai(frames)

        pygame.quit()

    def train_ai(self):
        """
        Train a new AI bird
        """
        local_dir = os.path.dirname(__file__)
        config_file = os.path.join(local_dir, "config-feedforward.txt")
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_file,
        )

        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter())
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.eval_genome, 50)
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

        with open("game/best_bird.obj", "wb") as output:
            pickle.dump(winner_net, output)

    def eval_genome(self, genomes, config):
        """Evaluate the fitness of each genome during the training phase."""
        self.gen += 1

        nets = []
        ge = []
        birds = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            birds.append(Bird(230, 350, self.bird_imgs))
            g.fitness = 0
            ge.append(g)

        ground = Ground(730, self.ground_img)
        pipes = [Pipe(600, self.pipe_img)]

        clock = pygame.time.Clock()

        score = 0

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            pipe_index = 0
            if len(birds) > 0:
                if (
                    len(pipes) > 1
                    and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width()
                ):
                    pipe_index = 1
            else:
                run = False
                break

            for x, bird in enumerate(birds):
                bird.move()
                ge[x].fitness += 0.1

                output = nets[x].activate(
                    (
                        bird.y,
                        abs(bird.y - pipes[pipe_index].height),
                        abs(bird.y - pipes[pipe_index].bottom),
                        abs(pipes[pipe_index].x),
                    )
                )

                if output[0] > 0.5:
                    bird.jump()

            add_pipe = False
            rem = []
            for pipe in pipes:
                for x, bird in enumerate(birds):
                    if pipe.collide(bird):
                        ge[x].fitness -= 2
                        birds.pop(x)
                        nets.pop(x)
                        ge.pop(x)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if pipe.x + pipe.pipe_top.get_width() < 0:
                    rem.append(pipe)

                pipe.move()

            if add_pipe:
                score += 1
                for g in ge:
                    g.fitness += 5
                pipes.append(Pipe(600, self.pipe_img))

            for r in rem:
                pipes.remove(r)

            for x, bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            if score >= 50:
                print("score: ", score)
                run = False

            ground.move()
            self.draw_game_window(self.win, birds, pipes, ground)

    def play_ai(self, frames):
        """
        Start the game with the AI
        """

        with open("game/best_bird.obj", "rb") as best_bird:
            net = pickle.load(best_bird)

        bird = Bird(230, 350, self.bird_imgs)
        ground = Ground(730, self.ground_img)
        pipes = [Pipe(600, self.pipe_img)]

        clock = pygame.time.Clock()
        count = 0

        while frames > 0:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pipe_index = 0

            if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_index = 1

            bird.move()

            output = net.activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_index].height),
                    abs(bird.y - pipes[pipe_index].bottom),
                    abs(pipes[pipe_index].x),
                )
            )

            if output[0] > 0.5:
                bird.jump()

            add_pipe = False
            rem = []
            for pipe in pipes:
                if pipe.collide(bird):
                    frames = 0

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                if pipe.x + pipe.pipe_top.get_width() < 0:
                    rem.append(pipe)

                pipe.move()

            if add_pipe:
                pipes.append(Pipe(600, self.pipe_img))

            for r in rem:
                pipes.remove(r)

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                frames = 0

            ground.move()
            self.draw_game_window(self.win, [bird], pipes, ground)
            self.save_screenshot(str(count) + ".png")
            frames -= 1
            count += 1

    def draw_game_window(self, win, birds, pipes, ground):
        """Draw the ai window."""
        self.win.blit(self.background_img, (0, 0))

        for pipe in pipes:
            pipe.draw(win)

        ground.draw(win)

        for bird in birds:
            bird.draw(win)

        pygame.display.update()

    def save_screenshot(self, filename):
        """Save a screenshot of pygame instance"""
        pygame.image.save(self.win, self.filepath + filename)


if __name__ == "__main__":
    game = FlappyBirdGame(60)
    game.run()
