import sys
import agent_based_simulation.frame as window

if len(sys.argv) > 1:
    print(sys.argv[1:])

    ratio = (int(sys.argv[1]), int(sys.argv[2]))

    window.run(ratio)
else:
    window.run()