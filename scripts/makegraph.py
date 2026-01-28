import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import csv

voltages = []
timestamps = []

index = count()

dt = 0.01

def animate(i): # makes the live graph
    global timestamps, voltages
    voltages = []
    timestamps = []
    
    try:
        with open("data.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamps.append(float(row["time"]))
                voltages.append(float(row["voltage"]))
    except FileNotFoundError:
        return
    
    plt.cla()
    plt.plot(timestamps, voltages, label = "A5")
    plt.ylim(0,5)

    plt.legend(loc ="upper left")
    plt.tight_layout()
    
    
ani = FuncAnimation(plt.gcf(), animate, interval = dt*1000)
plt.tight_layout()
plt.show()
