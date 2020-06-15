import pygame
import argparse
import math
import random
import os

list_of_colors = [(145, 185, 141), (229, 192, 121), (210, 191, 88), (140, 190, 178), (255, 183, 10), (189, 190, 220), (221, 79, 91), (16, 182, 98), (227, 146, 80), (241, 133, 123),
                  (110, 197, 233), (235, 205, 188), (197, 239, 247), (190, 144, 212), (41, 241, 195), (101, 198, 187), (255, 246, 143), (243, 156, 18), (189, 195, 199), (243, 241, 239)]


def draw_filled_circle(img, position, radius, color, ):
    pygame.draw.circle(img, color, position, radius, 0)


def draw_orbit(img, line_thickness, position, radius, color):
    arc_rectangle = (position[0]-radius, position[1] -
                     radius, 2*radius, 2*radius)
    pygame.draw.arc(img, color, arc_rectangle, 0, 2*math.pi, line_thickness)


def draw_background(img, color):
    img.fill(color)


def draw_border(img, size, color, width, height):
    pygame.draw.rect(img, color, (0, 0, size, height), 0)
    pygame.draw.rect(img, color, (0, 0, width, size), 0)
    pygame.draw.rect(img, color, (0, height-size, width, size), 0)
    pygame.draw.rect(img, color, (width-size, 0, size, height), 0)


def main():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="Specify Width",
                        default=3000, type=int)
    parser.add_argument("--height", help="Specify Height",
                        default=2000, type=int)
    parser.add_argument(
        "-o", "--orbit", help="Actual Orbits", action="store_true")
    parser.add_argument("-l", "--line", help=".", action="store_true")
    parser.add_argument("-s", "--sunsize", help=".",
                        default=random.randint(200, 400), type=int)
    parser.add_argument("-bs", "--bordersize", help=".", default=50, type=int)
    parser.add_argument(
        "-c", "-center", help="solar system centered on image", action="store_true")
    parser.add_argument("-co", "--colororbit", help="orbit lines same color as planet", action="store_true")
    args = parser.parse_args()

    width = args.width
    height = args.height
    border_size = args.bordersize
    sun_size = args.sunsize
    sun_center = height - border_size
    orbit_pos = (int(width/2), sun_center)
    screen = pygame.display.set_mode((width, height))

    background_color = (76, 76, 76)
    orbit_color = (153, 153, 153)
    draw_background(screen, background_color)

    sun_color = random.choice(list_of_colors)
    sun_position = (int(width/2), sun_center)
    draw_filled_circle(screen, sun_position, sun_size, sun_color)
    distance_between_planets = 20
    last_center = sun_center
    last_size = sun_size
    last_color = sun_color

    min_size = 5
    max_size = 70

    for x_pos in range(1, 20):
        rand_color = random.choice(list_of_colors)
        while (rand_color is last_color):
            rand_color = random.choice(list_of_colors)
        if (args.colororbit):
            orbit_color = rand_color
        next_size = random.randint(min_size, max_size)
        next_center = last_center - last_size - \
            (next_size * 2) - distance_between_planets
        if not(next_center - next_size < border_size):
            if(args.orbit):
                draw_orbit(screen, 4, orbit_pos, height -
                           next_center - border_size, orbit_color)
            elif(args.line):
                pygame.draw.line(screen, orbit_color,
                                 (border_size * 2, next_center), (width-(border_size*2), next_center), 4)
            draw_filled_circle(screen, (int(width/2), next_center),
                               int(next_size*1.3), background_color)
            last_color = rand_color
            draw_filled_circle(
                screen, (int(width/2), next_center), next_size, rand_color)
            last_center = next_center
            last_size = next_size

            min_size += 5
            max_size += 5 * x_pos
    draw_border(screen, border_size, sun_color, width, height)
    pygame.display.update()
    fname = "solar_system-" + "width-" + str(width) + "-height-" + str(height)
    if(args.orbit):
        fname += '-orbit'
    elif(args.line):
        fname += '-flat'
    fname += ".png"
    path_to_save = os.path.join('generated_img', fname)
    pygame.image.save(screen, path_to_save)


if __name__ == "__main__":
    main()
