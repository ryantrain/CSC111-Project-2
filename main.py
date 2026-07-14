"""Pygame Maze Visualization.

Main display module for solving and visualizing maze traversal algorithms
using Pygame. Provides interactive algorithm selection and animated solution playback.

Copyright (c) 2026 [Ryan Tran, Jenny Bian, Raymond Wu, Soltan Isgandar]. All rights reserved.
"""

import pygame
from typing import Type
from timeit import timeit

from maze_generation import generate_mazes, number_maze
from graph import Graph
from player import Player
from random_player import RandomPlayer
from compass_algorithm_player import CompassPlayer
from dfs_player import DFSPlayer
from bfs_player import BFSPlayer
from handonwall_player import HandOnWallPlayer
from deadend_filling_player import DeadEndFillingPlayer

# Constants
ALGORITHMS = {
    "Hand On Wall":  HandOnWallPlayer,
    "Compass":       CompassPlayer,
    "Random":        RandomPlayer,
    "BFS":           BFSPlayer,
    "DFS":           DFSPlayer,
    "Dead-end fill": DeadEndFillingPlayer
}

W, H = 600, 500
WALL = 3
CELL = 40
GRID_N = COLS = ROWS = 10
HEADER = 45
FOOTER = 30
MAZE_W = GRID_N * CELL + WALL
MAZE_H = GRID_N * CELL + WALL
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (50, 100, 200)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
LTBLU = (180, 210, 255)

screen: pygame.Surface
clock: pygame.time.Clock
FONT: pygame.font.Font


# Helpers
def draw_text(text, x, y, color=BLACK):
    """
    Display the specified text on the screen at the specified coordinates

    """
    screen.blit(FONT.render(text, True, color), (x, y))


def id_to_rc(vid):
    """
    Convert the input coordinates to a tuple of rows and columns
    """
    return divmod(vid - 1, COLS)


def run_game(player: Type[Player], start: int, end: int, graph: Graph) -> list:
    """
    Run one instance of the game of the given Player.
    Returns a list of vertex IDs representing the path taken by the player.
    """
    return player(graph).run_game(start, end)


def draw_maze(maze, path, step):
    """Draw the maze walls, the animated path, and start/end markers.
    Uses connection_list from maze-dataset:
      cl[0, r, c] = True  →  passage DOWN  (r,c)→(r+1,c)
      cl[1, r, c] = True  →  passage RIGHT (r,c)→(r,c+1)
    """
    cl = maze.connection_list

    # White background
    screen.fill(WHITE, (0, 0, W, H))

    # Visited path highlight
    for vid in set(path[:step]):
        r, c = id_to_rc(vid)
        pygame.draw.rect(screen, LTBLU,
                         (c * CELL + WALL, HEADER + r * CELL + WALL, CELL - WALL, CELL - WALL))

    if 0 < step <= len(path):
        r, c = id_to_rc(path[step - 1])
        pygame.draw.rect(screen, BLACK,
                         (c * CELL + WALL, HEADER + r * CELL + WALL, CELL - WALL, CELL - WALL))

    # Walls
    for r in range(GRID_N):
        for c in range(GRID_N):
            x = c * CELL
            y = r * CELL + HEADER
            # South wall
            if r < GRID_N - 1:
                if not cl[0, r, c]:
                    pygame.draw.rect(screen, BLACK, (x, y + CELL, CELL + WALL, WALL))
            else:
                pygame.draw.rect(screen, BLACK, (x, y + CELL, CELL + WALL, WALL))
            # East wall
            if c < GRID_N - 1:
                if not cl[1, r, c]:
                    pygame.draw.rect(screen, BLACK, (x + CELL, y, WALL, CELL + WALL))
            else:
                pygame.draw.rect(screen, BLACK, (x + CELL, y, WALL, CELL + WALL))

    # Top and left borders
    pygame.draw.rect(screen, BLACK, (0, HEADER, W, WALL))
    pygame.draw.rect(screen, BLACK, (0, HEADER, WALL, MAZE_H))

    # Start (green) and end (red) markers
    sr, sc = int(maze.start_pos[0]), int(maze.start_pos[1])
    er, ec = int(maze.end_pos[0]), int(maze.end_pos[1])
    pygame.draw.rect(screen, GREEN, (sc * CELL + WALL + 4, HEADER + sr * CELL + WALL + 4, CELL - WALL - 8,
                                     CELL - WALL - 8))
    pygame.draw.rect(screen, RED,   (ec * CELL + WALL + 4, HEADER + er * CELL + WALL + 4, CELL - WALL - 8,
                                     CELL - WALL - 8))


# ── Screen 1: menu ────────────────────────────────────────────────────────────
def screen_menu(maze, maze_num: int):
    """
    Display the menu screen. Contains clickable buttons for each algorithm (colour-coded). Display the Maze number
    and a clickable button to generate a new maze.
    """
    BTN_W, BTN_H = 300, 40
    ox = (W - BTN_W) // 2

    buttons = [
        (pygame.Rect(ox, 80 + i * 48, BTN_W, BTN_H), name, player, RED if i < 3 else BLUE)
        for i, (name, player) in enumerate(ALGORITHMS.items())
    ]

    new_maze_btn = pygame.Rect(ox, 40, BTN_W, 34)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, maze, maze_num
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_maze_btn.collidepoint(event.pos):
                    dataset = generate_mazes()
                    maze = dataset[maze_num % len(dataset)]
                    maze_num += 1
                    return "NEW_MAZE", maze, maze_num

                for rect, name, player, _ in buttons:
                    if rect.collidepoint(event.pos):
                        return (name, player), maze, maze_num

        screen.fill(WHITE)
        draw_text(f"Maze #{maze_num}  — Select an algorithm:", ox, 12)

        pygame.draw.rect(screen, GRAY, new_maze_btn)
        pygame.draw.rect(screen, BLACK, new_maze_btn, 2)
        draw_text("New Maze", new_maze_btn.x + 10, new_maze_btn.y + 8)

        for rect, name, _, colour in buttons:
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            draw_text(name, rect.x + 10, rect.y + 10)
# Draw the legend
        legend_y = H - 28
        pygame.draw.rect(screen, RED, (ox, legend_y, 14, 14))
        pygame.draw.rect(screen, BLACK, (ox, legend_y, 14, 14), 1)
        draw_text("Blind Algos", ox + 18, legend_y)

        pygame.draw.rect(screen, BLUE, (ox + 130, legend_y, 14, 14))
        pygame.draw.rect(screen, BLACK, (ox + 130, legend_y, 14, 14), 1)
        draw_text("Omniscient Algos", ox + 148, legend_y)

        pygame.display.flip()
        clock.tick(60)


# Screen 2: run & animate
def screen_run(algorithm: str, player: Type[Player], maze):
    """
    Generate the maze and animate the path of the algorithm. Display the step progress and time taken to find the path.
    """

    start = int(maze.start_pos[0] * 10 + maze.start_pos[1] + 1)
    end = int(maze.end_pos[0] * 10 + maze.end_pos[1] + 1)
    numbered_maze = number_maze(maze)
    path = run_game(player, start, end, numbered_maze)

    step, last = 0, pygame.time.get_ticks()
    back = pygame.Rect(10, 10, 80, 30)
    status_y = GRID_N * CELL + WALL + 10 + HEADER

    steps_per_tick = max(1, len(path) // 300)

    # Calculate the time taken for the algorithm to find its path in milliseconds
    elapsed_time = timeit(
        lambda: run_game(player, start, end, numbered_maze),
        number=100
    ) * 10

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    return True

        if step < len(path) and pygame.time.get_ticks() - last > 60:
            step = min(step + steps_per_tick, len(path))
            last = pygame.time.get_ticks()

        draw_maze(maze, path, step)

        pygame.draw.rect(screen, GRAY, back)
        pygame.draw.rect(screen, BLACK, back, 2)
        draw_text("Back", back.x + 10, back.y + 5)
        draw_text(algorithm, GRID_N * CELL // 2 - 40, 10)

        if step >= len(path):
            status = f"Done. {len(path)} steps. | Time taken to find path: {elapsed_time:.5f} ms"
        else:
            status = f"Step {step}/{len(path)} | Time taken to find path: {elapsed_time:.5f} ms"
        draw_text(status, 10, status_y, BLUE if step >= len(path) else BLACK)

        pygame.display.flip()
        clock.tick(60)


# Main
def main():
    """Run the main Pygame loop. Monitor for input and exit when the user quits
    Generate the first maze that all algorithms run on.
    """
    global screen, clock, FONT

    pygame.init()
    pygame.display.set_caption("Maze Solver")
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont(None, 28)

    dataset = generate_mazes()
    maze = dataset[0]
    maze_num = 1

    while True:
        result, maze, maze_num = screen_menu(maze, maze_num)
        if result is None:
            break
        if result == "NEW_MAZE":
            continue
        name, cls = result
        if not screen_run(name, cls, maze):
            break
    pygame.quit()


if __name__ == "__main__":
    main()

