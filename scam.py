import sys
import agent_based_simulation.frame as window
import agent_based_simulation.simulator as simulator
from matplotlib import pyplot as plt

observed_objects = dict()
observ_callbacks = dict()

def add_observer(name, toObserve):
    observed_objects[name] = []
    observ_callbacks[name] = toObserve

def observe():
    for key in observed_objects.keys():
        observation = observ_callbacks[key]()
        observed_objects[key].append(observation)

def plot_array(array): 
    plt.plot(range(len(array)), array)

def plot_observed():
    for key in observed_objects.keys():
        plot_array(observed_objects[key])

def plot_strategies(strat_array, title):
    # Extract unique keys
    unique_keys = set()
    for dictionary in strat_array:
        unique_keys.update(dictionary.keys())

    # Sort the unique keys
    sorted_keys = sorted(unique_keys)

    # Create a list to store values for each key at each time point
    values_by_key = {key: [] for key in sorted_keys}

    # Populate the values list
    for dictionary in strat_array:
        for key in sorted_keys:
            value = dictionary.get(key, 0)
            values_by_key[key].append(value)

    fig, ax = plt.subplots(figsize=(10, 6))
    # Plot the values for each key
    for key, values in values_by_key.items():
        ax.plot(range(len(strat_array)), values, label=key)

    # Set the x-axis ticks and labels
    x_ticks = range(0, len(strat_array), 5)  # Set ticks every 5th step
    ax.set_xticks(x_ticks)

    # Add legend and labels
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title(title)

    plt.tight_layout()

    # Show the plot
    plt.show()

if len(sys.argv) > 1:
    print(sys.argv[1:])

    ratio = (int(sys.argv[1]), int(sys.argv[2]))
    
    simulation = simulator.Simulation([50, 50, 20, 30, sys.argv[4]])
    win_tuple = window.init(ratio, simulation)
    i = 0
    max_steps = int(sys.argv[3])
    add_observer("m_strategies", simulation.STATE.get_macrophage_strategies)
    add_observer("p_strategies", simulation.STATE.get_pathogen_strategies)
    observe()
    while True:
        if i < max_steps:
            simulation.step()
            observe()
            i += 1
        else:
            break
            #plt.plot()
        window.update(win_tuple[0], ratio, win_tuple[1], simulation)
    plot_strategies(observed_objects["m_strategies"], "Macrophage Strategies")
    plot_strategies(observed_objects["p_strategies"], "Pathogen Strategies")
    #window.run(ratio)
else:
    simulation = simulator.Simulation([100, 100, 70, 30])
    #window.run()