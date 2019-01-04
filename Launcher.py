import ProceduralSolver as procedural
import DijkstraSolver as dijkstra
import RandomSolver as random
import Core as core
import time
from PIL import Image

maze=Image.open("./mazes/hardcore_maze.png")

print("\n» DIJKSTRA (dijkstra based maze solver)")
start_time = time.time()
dijkstra_response = core.Translater(maze).convert_to_coordinates(dijkstra.par_dijkstra(maze))
print("\n-> shortest path:", dijkstra.affichage(dijkstra_response),
      "\n-> solution size:", str(len(dijkstra_response)),
      "\n-> seconds taken:", time.time()-start_time)

print("\n» RANDOM (random based maze solver)")
start_time = time.time()
random_response = random.execute(maze, 50)
print("\n-> shortest path:", procedural.affichage(random_response),
      "\n-> solution size:", str(len(random_response)),
      "\n-> seconds taken:", time.time()-start_time)

print("\n» GLOUTON (procedural maze solver)")
start_time = time.time()
procedural_response = core.Translater(maze).convert_to_coordinates(procedural.par_glouton(maze))
print("\n-> shortest path:", procedural.affichage(procedural_response),
      "\n-> solution size:", str(len(procedural_response)),
      "\n-> seconds taken:", time.time()-start_time)

core.Decoder(maze).draw_path(dijkstra_response, "output_dijkstra")
core.Decoder(maze).draw_path(random_response, "output_random")
core.Decoder(maze).draw_path(procedural_response, "output_procedural")
