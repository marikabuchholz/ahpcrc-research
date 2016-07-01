from pylab import *
from scipy.linalg import toeplitz
import matplotlib.animation as animation
import matplotlib.patches as patches

arr = genfromtxt("infwell_results.txt")

print arr

x = linspace(0, 1, len(arr))
fs = 36
f, ax = subplots(figsize=(9,9))
grid()
xlabel(r'$x$', fontsize=fs)
ylabel(r'$|\psi(x,t)|^2$', fontsize=fs)
title('Animation of $|\psi(x,t)|^2$', fontsize=fs, y=1.03)
line, = ax.plot(x, arr[0, :], linewidth = 6) 
def animate(i):
    line.set_ydata(arr[i, :])
    return line,

ani = animation.FuncAnimation(f, animate, 100, repeat = True, interval = 50, blit = False)
show()
