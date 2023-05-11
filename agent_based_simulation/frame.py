import tkinter
import time
import random
from directions import directions
from agent import Agent
 
# width of the window
window_width=700

# height of the window
window_height=700

# row count
rows = 100

# column count
columns = 100

# number of agents
n_agents = 50
position_dict = dict()

# the pixel movement of ball for each iteration
animation_ball_min_movement = 5

# delay between successive frames in seconds
refresh_rate = 0.1

# init agents
def initialise_agents():
  _agents = list()
  y_pos = dict.fromkeys(range(rows), None)
  x_pos = dict.fromkeys(range(columns), None)
  for i in range(n_agents):
    x = None
    y = None
    while x == None:
      _x = random.choice(range(columns))
      if x_pos[_x] == None:
        x = _x
        x_pos[_x] = _x
    
    while y == None:
      _y = random.choice(range(rows))
      if y_pos[_y] == None:
        y = _y
        y_pos[_y] = _y
    agent = Agent(i, x, y, random.choice(list(directions)), bounds_x=100, bounds_y=100)
    key = f'({x},{y})'
    position_dict.update({key: [i]})
    _agents.append(agent)
  return _agents

agents = initialise_agents()
canvas_agents = list()

def create_grid(canvas):
  for x in range(columns):
    canvas.create_line(window_width/columns*x,-5, window_width/columns*x, window_height+5)
  for y in range(rows):
    canvas.create_line(-5, window_height/rows*y, window_width+5, window_height/rows*y)

# The main window of the animation
def create_window():
  window = tkinter.Tk()
  window.title("Tkinter Animation Demo")
  window.geometry(f'{window_width}x{window_height}')
  return window
 
# Create a canvas for animation and add it to main window
def create_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="lightgrey")
  canvas.pack(fill="both", expand=True)
  create_grid(canvas)
  return canvas

def spawn_agents(canvas):
  for agent in agents:
    agent_width = window_width/columns
    agent_height = window_height/rows
    x = agent.x_pos*agent_width
    y = agent.y_pos*agent_height
    canvas_agent = canvas.create_rectangle(x+1, y+1, x+agent_width-1, y+agent_height-1, fill=agent.color)
    canvas_agents.append(canvas_agent)

def update_agents(canvas):
  for i in range(len(agents)):
    agent = agents[i]
    canvas_agent = canvas_agents[i]
    key = f'({agent.x_pos},{agent.y_pos})'
    #print(len(position_dict))
    values = position_dict.pop(key)
    if len(values) > 1:
      values.remove(agent.ID)
      position_dict.update({key: values})
    agent.move()
    key_next = f'({agent.x_pos},{agent.y_pos})'
    if position_dict.get(key_next):
      position_dict.update({key_next:[*position_dict.get(key_next),agent.ID]})
    else:
      position_dict.update({key_next:[agent.ID]})
    agent_x_1, agent_y_1, agent_x_2, agent_y_2 = canvas.coords(canvas_agent)
    agent_x_1 = agent.x_pos*(window_width/columns) - agent_x_1
    agent_y_1 = agent.y_pos*(window_height/rows) - agent_y_1
    canvas.move(canvas_agent, agent_x_1, agent_y_1)
  # if len(position_dict) < n_agents:
  #   print(position_dict)
    
def check_collision():
  keys = position_dict.keys()
  for key in keys:
    values = position_dict.get(key)
    if len(values) > 1:
      print(f'COLLISION: {values}')

# Create and simulate
def simulate(window, canvas):
  # ball = canvas.create_oval(animation_ball_start_xpos-animation_ball_radius,
  #           animation_ball_start_ypos-animation_ball_radius,
  #           animation_ball_start_xpos+animation_ball_radius,
  #           animation_ball_start_ypos+animation_ball_radius,
  #           fill="blue", outline="white", width=4)
  while True:
    # canvas.move(ball,xinc,yinc)
    window.update()
    time.sleep(refresh_rate)
    update_agents(canvas)
    check_collision()
    # ball_pos = canvas.coords(ball)
    # unpack array to variables
    # xl,yl,xr,yr = ball_pos
    # if xl < abs(xinc) or xr > window_width-abs(xinc):
    #   xinc = -xinc
    # if yl < abs(yinc) or yr > window_height-abs(yinc):
    #   yinc = -yinc
 
# The actual execution starts here
window = create_window()
window_canvas = create_canvas(window)
spawn_agents(window_canvas)
simulate(window, window_canvas)