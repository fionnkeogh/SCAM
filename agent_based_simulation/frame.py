import tkinter
import time
import random
from agent_based_simulation.agent import Agent
from agent_based_simulation.candida import Candida
from agent_based_simulation.macrophage import Macrophage
from agent_based_simulation.directions import directions

canvas_agents = list()

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
  canvas.configure(bg="lightgrey")
  canvas.pack(fill="both", expand=True)
  create_grid(canvas, width, height, size[0], size[1])
  return canvas

def spawn_agents(canvas, size, n_candida, n_macrophages, simulation):
  for agent in simulation.STATE.get_objects():
    agent_width = size[0]/simulation.size[0]
    agent_height = size[1]/simulation.size[1]
    x = agent.x_pos*agent_width
    y = agent.y_pos*agent_height
    canvas_agent = canvas.create_oval(x+0.05, y+0.05, x+(agent_width*agent.size)-0.05, y+(agent_height*agent.size)-0.05, fill=agent.color)
    canvas_agents.append(canvas_agent)

def update_agents(window, canvas, simulation):
  for i, agent in enumerate(simulation.STATE.get_objects()):
    canvas_agent = canvas_agents[i]
    agent_x_1, agent_y_1, agent_x_2, agent_y_2 = canvas.coords(canvas_agent)
    agent_x_1 = agent.x_pos*(window.winfo_width()/simulation.size[0]) - agent_x_1
    agent_y_1 = agent.y_pos*(window.winfo_height()/simulation.size[1]) - agent_y_1
    canvas.move(canvas_agent, agent_x_1, agent_y_1)


# Create and simulate
def update(window, canvas, simulation):
  window.update()
  time.sleep(0.1)
  update_agents(window, canvas, simulation)

def init(ratio, simulation):
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