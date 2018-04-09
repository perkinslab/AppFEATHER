# force floating point division. Can still use integer with //
from __future__ import division
import os
from subprocess import call
import sys
sys.path.append("../../")
import numpy as np
import matplotlib.pyplot as plt
def run():
    # move to the script directory
    os.chdir("../")
    args=["-tau 1.5e-2 ",
          "-threshold 1e-3 ",
          "-spring_constant 6.67e-3 ",
          "-trigger_time 0.382 ",
          "-dwell_time 0.992 ",
          "-file_input ../Data/example.csv ",
          "-file_output ./output.txt "]
    call(["C:/ProgramData/Anaconda2/python.exe","main_feather.py",*args)
    events = np.loadtxt("./output.txt")
    data = np.loadtxt("../Data/example.csv", delimiter=",").T
    t, f = data[0], data[2]
    # plot the relative force
    f -= np.median(f[:f.size//10])
    f *= -1
    f *= 1e12
    plt.plot(t, f)
    for i in events:
        plt.axvline(t[int(i)])
    plt.xlabel("Time (s)")
    plt.ylabel("Force (pN")
    plt.show()
    pass


if __name__ == "__main__":
    run()
