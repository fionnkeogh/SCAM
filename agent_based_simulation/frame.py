import tkinter
from PIL import Image, ImageTk
import time
import math
import random
from agent_based_simulation.agent import Agent
from agent_based_simulation.candida import Candida
from agent_based_simulation.macrophage import Macrophage
from agent_based_simulation.directions import directions

canvas_agents = list()
canvas_cytokines = list()
images = []

def create_grid(canvas, width, height, columns, rows):
  for x in range(columns):
    canvas.create_line(width/columns*x,-5, width/columns*x, height+5)
  for y in range(rows):
    canvas.create_line(-5, height/rows*y, width+5, height/rows*y)

# The main window of the animation
def create_window(width, height):
  window = tkinter.Tk()
  window.title("Tkinter Simulation Demo")
  window.geometry(f'{width}x{height}')
  return window
 
# Create a canvas for animation and add it to main window
def create_canvas(window, width, height, size):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="lightgrey") # 211, 211, 211
  canvas.pack(fill="both", expand=True)
  create_grid(canvas, width, height, size[0], size[1])
  return canvas

def spawn_agents(canvas, size, n_candida, n_macrophages, simulation):
  for agent in simulation.STATE.get_agents():
    agent_width = size[0]/simulation.size[0]
    agent_height = size[1]/simulation.size[1]
    x = agent.x_pos*agent_width
    y = agent.y_pos*agent_height
    canvas_agent = canvas.create_oval(x+0.05, y+0.05, x+(agent_width*agent.size)-0.05, y+(agent_height*agent.size)-0.05, fill=agent.color)
    canvas_agents.append(canvas_agent)

def lerp_color(start, end, t):
  r = int(start[0] + (end[0] - start[0]) * t**t)
  g = int(start[1] + (end[1] - start[1]) * t**t)
  b = int(start[2] + (end[2] - start[2]) * t**t)
  return (r,g,b)

def get_moore_neighbors(grid, row, col, neighborhood_size):
    rows = grid[0]
    cols = grid[0]
    neighbors = []
    
    for i in range(-neighborhood_size+1, neighborhood_size + 2):
        for j in range(-neighborhood_size+1, neighborhood_size + 2):
            if i == 0 and j == 0:  # Skip the central cell
                continue
            
            neighbor_row = row + i
            neighbor_col = col + j
            
            if neighbor_row >= 0 and neighbor_row < rows and neighbor_col >= 0 and neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    
    return neighbors

def spawn_cytokines(canvas, size, simulation):
  global canvas_cytokines
  for cytokine_tile in canvas_cytokines:
    canvas.delete(cytokine_tile)
  canvas_cytokines = list()
  for cytokine in simulation.STATE.get_cytokine_objects():
    width = size[0]/simulation.size[0]
    height = size[1]/simulation.size[1]
    x, y = cytokine.get_position()
    x = x*width
    y = y*height
    gauss = cytokine.compute_gaussian_kernal()
    m = int(((len(gauss)-1)/2))
    color = "#%02x%02x%02x" % lerp_color(cytokine.color, (211,211,211), gauss[m])
    canvas_cytokine = canvas.create_rectangle(x, y, x+(width*cytokine.size), y+(height*cytokine.size), fill=color)
    canvas.tag_lower(canvas_cytokine)
    canvas_cytokines.append(canvas_cytokine)
    neighbors = get_moore_neighbors(simulation.size, cytokine.get_position()[1], cytokine.get_position()[0], 6)
    for neighbor in neighbors:
      mid = (cytokine.get_position()[0] + cytokine.size*0.5, cytokine.get_position()[1] + cytokine.size*0.5)
      dist = int(math.sqrt(abs(neighbor[1]-mid[0])**2+abs(neighbor[0]-mid[1])**2))
      t = 0
      if m+dist < len(gauss):
        t = gauss[m+dist]
        if gauss[m+dist] > 0:
          color = "#%02x%02x%02x" % lerp_color(cytokine.color, (211,211,211), 1-t)
          ny = neighbor[0]*height
          nx = neighbor[1]*width
          cytokine_neighbor = canvas.create_rectangle(nx, ny, nx+(width*1), ny+(height*1), fill=color)
          canvas.tag_lower(cytokine_neighbor)
          canvas_cytokines.append(cytokine_neighbor)

def update_agents(window, ratio, canvas, simulation):
  spawn_cytokines(canvas, ratio, simulation)
  for i, agent in enumerate(simulation.STATE.get_agents()):
    canvas_agent = canvas_agents[i]
    agent_x_1, agent_y_1, agent_x_2, agent_y_2 = canvas.coords(canvas_agent)
    agent_x_1 = agent.x_pos*(window.winfo_width()/simulation.size[0]) - agent_x_1
    agent_y_1 = agent.y_pos*(window.winfo_height()/simulation.size[1]) - agent_y_1
    canvas.move(canvas_agent, agent_x_1, agent_y_1)


# Create and simulate
def update(window, ratio, canvas, simulation):
  window.update()
  time.sleep(0.1)
  update_agents(window, ratio, canvas, simulation)

def init(ratio, simulation):
  global canvas_cytokines
  canvas_cytokines = list()
  # row and column count
  rows = simulation.size[1]
  columns = simulation.size[0]
  # number of agents
  n_candida = simulation.num_phages
  n_macrophages = simulation.num_path
  # delay between successive frames in seconds
  refresh_rate = 0.1
  # The actual execution starts here
  window = create_window(ratio[0], ratio[1])
  window_canvas = create_canvas(window, ratio[0], ratio[1], simulation.size)
  spawn_agents(window_canvas, ratio, n_candida, n_macrophages, simulation)
  #simulate(window, window_canvas)
  return (window, window_canvas)