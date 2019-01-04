#author: Thomas Marchand (Th0rgal)
#date: 04/01/2019
from PIL import Image
import Core as core
import random
import time


class Maze:
    def __init__(self, maze_list):
        self.maze = {"lines": maze_list,
                     "width": len(maze_list[0]),
                     "height": len(maze_list)}

    @staticmethod
    def count_items(maze_list):
        item_count = 0
        for line in maze_list:
            item_count += len(line)
        return item_count


class Solver:
    def __init__(self, maze_instance):
        self.maze_instance = maze_instance
        self.solution = []
        self.start_pos = None

    def find_way_out(self, enter_position):  # Ici enter_position prend un tuple (x,y)
        self.start_pos = enter_position
        current_position = enter_position
        self.solution.append(enter_position)
        while True:
            air_cells, solution_cells = self.find_way(current_position)
            if solution_cells:
                self.solution.append(solution_cells[0])
                return self.solution, True
            elif air_cells:
                current_position = self.move_to(random.choice(air_cells))
            # Si c'est un cul de sac
            else:
                return self.solution, False

    def move_to(self, cell_pos):
        self.solution.append(cell_pos)
        return cell_pos

    def find_way(self, current_pos):

        cells = []

        for x in range(current_pos[0] - 1, current_pos[0] + 2):
            cells.append((x, current_pos[1]))
        for y in range(current_pos[1] - 1, current_pos[1] + 2):
            cells.append((current_pos[0], y))

        air_cells = []
        solution_cells = []

        for x, y in cells:
            if x < 0 or y < 0 or x >= self.maze_instance.maze["width"] or y >= self.maze_instance.maze["height"]:
                continue
            cell_type = self.maze_instance.maze["lines"][y][x]
            if cell_type == 0 and (self.solution is None or (x, y) not in self.solution):
                air_cells.append((x, y))
            elif cell_type == 2 and (x, y) != self.start_pos:
                solution_cells.append((x, y))

        return air_cells, solution_cells


def execute(maze_image, tries):
    decoder = core.Decoder(maze_image)
    maze = Maze(decoder.to_maze_list())

    solutions = []
    for _ in range(tries):
        solver = Solver(maze)
        solution, is_working = solver.find_way_out((5, 0))
        if is_working:
            solutions.append(solution)

    solutions.sort(key=lambda v: len(v))
    return solutions[0]