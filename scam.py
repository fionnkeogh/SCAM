import sys
import agent_based_simulation.frame as window
import agent_based_simulation.simulator as simulator

if len(sys.argv) > 1:
    print(sys.argv[1:])

    ratio = (int(sys.argv[1]), int(sys.argv[2]))
    
    simulation = simulator.Simulation([50, 50, 70, 30])
    win_tuple = window.init(ratio, simulation)
    i = 0
    max_steps = int(sys.argv[3])
    while True:
        if i < max_steps:
            simulation.step()
            i += 1
        window.update(win_tuple[0], win_tuple[1], simulation)
    #window.run(ratio)
else:
    simulation = simulator.Simulation([100, 100, 70, 30])
    #window.run()