import os
import pickle
import pygame
import neat
from entities.ground import Ground
from entities.pipe import Pipe
from entities.bird import Bird

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 900

GEN = 0

STAT_FONT = pygame.font.SysFont("comicsans", 50)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Blappy Fird")
pygame.display.set_icon(pygame.image.load("game/images/bird_icon.ico"))

PLAYER_BIRD_IMGS = [
    pygame.transform.scale2x(
        pygame.image.load("game/images/redbird-downflap.png").convert_alpha()
    ),
    pygame.transform.scale2x(
        pygame.image.load("game/images/redbird-midflap.png").convert_alpha()
    ),
    pygame.transform.scale2x(
        pygame.image.load("game/images/redbird-upflap.png").convert_alpha()
    ),
]
BIRD_IMGS = [
    pygame.transform.scale2x(
        pygame.image.load("game/images/bluebird-downflap.png").convert_alpha()
    ),
    pygame.transform.scale2x(
        pygame.image.load("game/images/bluebird-midflap.png").convert_alpha()
    ),
    pygame.transform.scale2x(
        pygame.image.load("game/images/bluebird-upflap.png").convert_alpha()
    ),
]
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load("game/images/pipe.png").convert_alpha()
)
GROUND_IMG = pygame.transform.scale2x(
    pygame.image.load("game/images/ground.png").convert_alpha()
)
BACKGROUND_IMG = pygame.transform.scale(
    pygame.image.load("game/images/background.png").convert_alpha(), (600, 900)
)
MESSAGE_IMG = pygame.transform.scale2x(
    pygame.image.load("game/images/message.png").convert_alpha()
)


def draw_menu_window(win):
    win.blit(BACKGROUND_IMG, (0, 0))
    win.blit(MESSAGE_IMG, (113, 183))
    pygame.display.update()


def draw_train_window(win, birds, pipes, ground, score, gen):
    win.blit(BACKGROUND_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Bird Cnt: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(text, (10, 50))

    ground.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def draw_play_window(win, bird, pipes, ground, score):
    win.blit(BACKGROUND_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    ground.draw(win)

    bird.draw(win)

    pygame.display.update()


def draw_verse_window(win, ai_bird, player_bird, pipes, ground, score):
    win.blit(BACKGROUND_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    ground.draw(win)

    ai_bird.draw(win)
    player_bird.draw(win)

    pygame.display.update()


def eval_genome(genomes, config):
    global WIN, GEN
    win = WIN
    GEN += 1

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350, BIRD_IMGS))
        g.fitness = 0
        ge.append(g)

    ground = Ground(730, GROUND_IMG)
    pipes = [Pipe(600, PIPE_IMG)]

    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        pipe_index = 0
        if len(birds) > 0:
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
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

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600, PIPE_IMG))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        if score >= 15:
            print("score: ", score)
            run = False

        ground.move()
        draw_train_window(win, birds, pipes, ground, score, GEN)


def load_train_bird():
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

    winner = p.run(eval_genome, 50)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    with open("best_bird.obj", "wb") as output:
        pickle.dump(winner_net, output)


def play_bird():
    global WIN, GEN
    win = WIN

    bird = Bird(230, 350, BIRD_IMGS)
    ground = Ground(730, GROUND_IMG)
    pipes = [Pipe(600, PIPE_IMG)]

    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.move()

        if ground.collide(bird):
            run = False

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600, PIPE_IMG))

        for r in rem:
            pipes.remove(r)

        ground.move()
        draw_play_window(win, bird, pipes, ground, score)


def verse_bird():
    global WIN, GEN
    win = WIN

    print("in here")
    with open("best_bird.obj", "rb") as best_bird:
        net = pickle.load(best_bird)

    ai_bird = Bird(230, 350, BIRD_IMGS)
    player_bird = Bird(230, 350, PLAYER_BIRD_IMGS)
    ground = Ground(730, GROUND_IMG)
    pipes = [Pipe(600, PIPE_IMG)]

    clock = pygame.time.Clock()

    player_win = False
    ai_win = False
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_bird.jump()

        pipe_index = 0

        if len(pipes) > 1 and ai_bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_index = 1

        ai_bird.move()
        player_bird.move()

        output = net.activate(
            (
                ai_bird.y,
                abs(ai_bird.y - pipes[pipe_index].height),
                abs(ai_bird.y - pipes[pipe_index].bottom),
                abs(pipes[pipe_index].x),
            )
        )

        if output[0] > 0.5:
            ai_bird.jump()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(ai_bird):
                player_win = True
                run = False
            if pipe.collide(player_bird):
                ai_win = True
                run = False

            if not pipe.passed and pipe.x < ai_bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600, PIPE_IMG))

        for r in rem:
            pipes.remove(r)

        if ai_bird.y + ai_bird.img.get_height() >= 730 or ai_bird.y < 0:
            player_win = True
            run = False
        if player_bird.y + player_bird.img.get_height() >= 730 or player_bird.y < 0:
            ai_win = True
            run = False

        if score >= 50:
            run = False

        ground.move()
        draw_verse_window(win, ai_bird, player_bird, pipes, ground, score)


def load_verse_bird():
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

    # winner = p.run(verse_bird, 10)

    verse_bird()


def menu():
    global WIN
    win = WIN

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    play_bird()
                if event.key == pygame.K_UP:
                    load_train_bird()
                if event.key == pygame.K_RIGHT:
                    load_verse_bird()
        draw_menu_window(win)


if __name__ == "__main__":
    menu()
