import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from tqdm import tqdm

fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.set_facecolor('black')


def cantor(y, generations):
    y[int(len(y)/3+1):int(2*len(y)/3)] = 0
    if generations == 0: return y
    else:
        y[:int(len(y)/3)] = y[int(2*len(y)/3):] = cantor(y[:int(len(y)/3)], generations-1)
        return y

generations = 10
UPSAMPLE_RATE = 100
# upsample rate refers to how slowly should fractal be zoomed
# minimum: 2, maximum: fractal_resolution
# good value is something like 100
# rate of 2 means at single iteration frames are cut by half
# rate of 10 means every 10th sample will be cut

fractal_resolution = 3**generations
# 3 is a multiplier for resolution of generation of Cantor set: i.e.:
#    1st generation 3**1: [1, 0, 1]
#    2nd generation 3**2: [1, 0, 1, 0, 0, 0, 1, 0, 1]

# initialize datapoints
x = np.linspace(0, fractal_resolution, fractal_resolution)
y = np.ones_like(x)

print(f"fractal resolution: {fractal_resolution}")

# generate fractal
y = cantor(y, generations)

def zoom_fractal(x, y):
    for i in range(int(len(x)/UPSAMPLE_RATE)):
        y = np.insert(y, UPSAMPLE_RATE*i, y[UPSAMPLE_RATE*i])[:-1]
    return x, y

# prepare animation
artists = []
for i in tqdm(range(3*UPSAMPLE_RATE)):
    x, y = zoom_fractal(x, y)
    container = ax.plot(x, y, color="tab:blue")
    artists.append(container)

# animate :)
ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=50) # adjust interval to speed up/slow down animation
# To save the animation using Pillow as a gif
# writer = animation.PillowWriter(fps=15,
#                                 metadata=dict(artist=''),
#                                 bitrate=1800)
# ani.save('cantor.gif', writer=writer)
plt.show()
