#author: Thomas Marchand (Th0rgal)
#date: 04/01/2019
from PIL import Image


class Decoder:
    def __init__(self, image):
        self.image = image

    @staticmethod
    def get_cell_type(pixel):
        r, g, b = pixel
        if r + g + b == 255 * 3:
            return 0
        elif r == 255:
            return 2
        else:
            return 1

    def draw_path(self, path, name):
        output = self.image.copy()
        for x, y in path:
            output.putpixel((x, y), (52, 152, 219))
        output.save("./outputs/" +name + ".png")

    def to_maze_list(self):
        width, height = self.image.size
        pixels = self.image.load()

        maze_list = []
        for y in range(0, height):
            line = []
            for x in range(0, width):
                line.append(self.get_cell_type(pixels[x, y]))
            maze_list.append(line)

        return maze_list


class Translater:
      def __init__(self, maze):
            self.maze = maze
            self.list = Decoder(maze).to_maze_list()
            self.height = len(self.list)
            self.width = len(self.list[0])

      def convert_to_coordinates(self, path):
            output_path = []
            for cell_id in path:
                  output_path.append((cell_id % self.width, int(cell_id/self.width)))
            return output_path
      
      def convert_to_numbers(self, path):
            output_path = []
            for x, y in path:
                  output_path.append(y*self.width + x)
            return output_path