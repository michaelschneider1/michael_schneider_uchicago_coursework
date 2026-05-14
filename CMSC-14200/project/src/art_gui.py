import click
import pygame
from abc import ABC
from ui import ArtGUIBase

class ArtGUI9Slice(ArtGUIBase):
    def __init__(self, frame_width: int):
        self.frame_width = frame_width

    def draw_background(self, surface: pygame.Surface) -> None:
        width, height = surface.get_width(), surface.get_height()
        f = self.frame_width
        colors = {
            "tl": (255,165,0), "t": (255,0,0), "tr": (128,0,128),
            "l": (0,255,255), "c": (0,255,0), "r": (255,0,255),
            "bl": (255,255,0), "b": (0,0,255), "br": (0,100,0)
        }
        pygame.draw.rect(surface, colors["tl"], (0, 0, f, f))
        pygame.draw.rect(surface, colors["tr"], (width - f, 0, f, f))
        pygame.draw.rect(surface, colors["bl"], (0, height - f, f, f))
        pygame.draw.rect(surface, colors["br"], (width - f, height - f, f, f))

        pygame.draw.rect(surface, colors["t"], (f, 0, width - 2*f, f))
        pygame.draw.rect(surface, colors["b"], (f, height - f, width - 2*f, f))
        pygame.draw.rect(surface, colors["l"], (0, f, f, height - 2*f))
        pygame.draw.rect(surface, colors["r"], (width - f, f, f, height - 2*f))

        pygame.draw.rect(surface, colors["c"], (f, f, width - 2*f, height - 2*f))


class PolkaDotsGUI(ArtGUIBase):
    def __init__(self, frame_width):
        self.fw = frame_width

    def draw_background(self, surface):
        w, h = surface.get_size()
        f = self.fw
        surface.fill((255, 255, 255))
        r = f // 2
        dot_col = (255, 100, 100)
        gap = 2*r + 10

        for x in range(f, w - f, gap):
            for y in range(f, h - f, gap):
                pygame.draw.circle(surface, dot_col, (x, y), r)


class HoneycombGUI(ArtGUIBase):
    def __init__(self, fw):
        self.fw = fw

    def draw_background(self, surface):
        w, h = surface.get_size()
        f = self.fw
        surface.fill((240,240,240))
        hc = (200,160,0)
        r = f
        dy = int(r * 1.5)
        dx = int((3**0.5) * r)

        for row in range(0, h, dy):
            offset = dx//2 if (row//dy)%2 else 0
            for col in range(offset, w, dx):
                pygame.draw.circle(surface, hc, (col, row), r, 1)


class PokemonGUI(ArtGUIBase):
    def __init__(self, fw):
        self.fw = fw
        self.pokemon = [
            pygame.image.load("assets/PIKACHU.png"),
            pygame.image.load("assets/PSYDUCK.png"),
            pygame.image.load("assets/POKEBALL.png")
        ]
        self.pokemon = [pygame.transform.scale(image, (100, 100)) for image in self.pokemon]
        pokeball_img = self.pokemon[2]
        pokeball_img = pygame.transform.scale(pokeball_img, (80, 80))
        self.pokemon[2] = pokeball_img


        self.positions_of_images = [(5, 310), (225, 475), (355, 2)]

    def draw_background(self, surface):
        f = self.fw
        surface.fill((255, 255, 255))
        for image, position in zip(self.pokemon, self.positions_of_images):
            surface.blit(image, position)


@click.command()
@click.option('-a', '--art', required=True, help='frame type: cat0, cat1, cat3, special, etc')
@click.option('-f', '--frame', type=int, default=20, help='frame width in pixels')
@click.option('-w', '--width', type=int, default=400, help='total window width in pixels')
@click.option('-h', '--height', type=int, default=300, help='total window height in pixels')
def main(art, frame, width, height):
    pygame.init()

    if art == 'cat0':
        gui = ArtGUI9Slice(frame)
    elif art == 'cat1':
        gui = PolkaDotsGUI(frame)
    elif art == 'cat3':
        gui = HoneycombGUI(frame)
    elif art == 'special':
        gui = PokemonGUI(frame)
    elif art in ('cat2', 'cat4'):
        click.echo("cat not implemented")
        return
    else:
        click.echo(f"unknown frame type: {art}")
        return

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("custom GUI")
    gui.draw_background(screen)
    pygame.display.flip()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == '__main__':
    main()
