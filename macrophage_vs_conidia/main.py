from payoff import Payoff
from simulator import Simulator
import matplotlib.pyplot as plt

macrophage_replication_rate = {'normal': 0.03, 'high': 0.059, 'maximal': 0.266} # alpha
candida_replication_rate = 0.0393 # delta
macrophage_death_rate = 0.0676 # nu
candida_death_rate = 0.0797 # lambda
fm_max = 4/4
fc_max = 4/4
ic1 = 1/4
ic2 = 1/4
im1 = 1/4
im2 = 1/4
rm = 1/4
rc = 1/4
s1 = 0.5/4
s2 = 1/4

macrophage_win_probability = candida_death_rate/(macrophage_death_rate+candida_death_rate)

mpp = fm_max - im1 - s1
mpa = fm_max - im1 - rm - s2
map = fm_max - im2
maa = macrophage_win_probability*(fm_max - im2 - rm)
cpp = fc_max - ic1
cpa = 0
cap = fc_max - ic2
caa = (1-macrophage_win_probability)*(fc_max - ic2 - rc)

payoff = Payoff(mpp,mpa,map,maa,cpp,cpa,cap,caa)

simulation = Simulator(
    100, 
    100, 
    '11', 
    '11', 
    payoff, 
    1000, 
    (5, 15), 
    2*10**-5, 
    1*10**-5, 
    macrophage_death_rate, 
    candida_death_rate, 
    macrophage_replication_rate.get("normal"), 
    candida_replication_rate
)

simulation.run()
history = simulation.get_history()

plt.figure(figsize=(12, 8))
plt.subplot(1, 1, 1)
plt.title('')
plt.plot(history[0], label ="macrophages")
plt.plot(history[1], label ="candida")
plt.legend()
plt.tight_layout()
plt.show()