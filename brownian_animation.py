# Importing Packages Used In This Project

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Animation Settings; Number Of Molecules, Frames, Axes Limits, Time Steps

molecules = 100
frames = 800
(xmin, xmax, ymin, ymax) = (0, 1, 0, 1)
(fig, ax) = plt.subplots(dpi=190)
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
dt = 0.001

# Initial Conditions For Velocity Of Grain/Molecule And Position Of Grain

m = 1
M = 20
vx = 5*np.random.randn(molecules)
vy = 5*np.random.randn(molecules)
Gx = np.array([0.5])
Gy = np.array([0.5])
vgx = np.array([0])
vgy = np.array([0])

# Insures That No Molecule Is Created Inside The Grain

flag = 1
while flag != 0:
    x = np.random.rand(molecules)
    y = np.random.rand(molecules)

    # Indices where x and y are within the area of the grain with radius (r=0.03 m)
    ind = np.where((x ** 2) + (y ** 2) <= (0.03 ** 2))
    flag = ind[0].size

# A Function That Updates Velocity/Position Of Molecules/Grain:


def update_point(num):

    # Allows The Use Of Variables Outside The Function
    global m, M
    global x, y, vx, vy
    global Gx, Gy, vgx, vgy


# Inversing Direction Of Molecule'S Velocity When It Hits Axes Limits

    indx = np.where((x <= xmin) | (x >= xmax))
    indy = np.where((y <= ymin) | (y >= ymax))
    vx[indx] = -vx[indx]
    vy[indy] = -vy[indy]


# Inversing Direction Of Grain'S Velocity When It Hits Axes Limits

    indGx = np.where((Gx <= xmin) | (Gx >= xmax))
    indGy = np.where((Gy <= ymin) | (Gy >= ymax))
    vgx[indGx] = -vgx[indGx]
    vgy[indGy] = -vgy[indGy]

# Updates Molecule Position and Distance from Grain

    dx = dt * vx
    dy = dt * vy
    x = x + dx
    y = y + dy
    x_distance = Gx - x
    y_distance = Gy - y

# Magnitude of Molecule's Distance from the Grain And Velocity

    distance = np.sqrt(x_distance ** 2 + y_distance ** 2)
    v = np.sqrt(vx ** 2 + vy ** 2)


# Defining The Indices At Which The Collisions Occur

    collision = np.where(distance <= 0.03)

# alpha: angle between molecule velocity and prime coordinate axis
# theta: angle of rotation of the prime axis

    alpha = np.arctan2(vy[collision], vx[collision])
    theta = np.arctan2(y_distance[collision], x_distance[collision])

# Projection of molecule's velocity onto the X' axis and reversing it's Direction

    vxA = -np.abs(v[collision] * np.cos(alpha))

# Projection of Molecule's velocity Onto the X' axis

    vyA = v[collision] * np.sin(alpha)

# Projecting The Velocity Components Onto The X And Y Axes
    vx[collision] = np.cos(theta) * vxA + np.sin(theta) * vyA
    vy[collision] = np.sin(theta) * vxA + np.cos(theta) * vyA


# Updates Grain's Position And Velocity

    dxg = dt * vgx
    dyg = dt * vgy
    Gx = Gx + dxg
    Gy = Gy + dyg
    vgx = np.sum(-2*(m/M)*vx[collision]) + vgx
    vgy = np.sum(-2*(m/M)*vy[collision]) + vgy

# Stacks Molecule/Grain Position Coordinates And Updates Image With
# New Coordinates

    data = np.stack((x, y), axis=-1)
    im.set_offsets(data)
    dataG = np.stack((Gx, Gy), axis=-1)
    im2.set_offsets(dataG)

    return (Gx, Gy)


# Plotting Particles On A Scatter Plot Images

im = ax.scatter(x, y, color='#892cdc', s=10)
im2 = ax.scatter(Gx, Gy, c='#F5D300', s=165)

ax.set_facecolor('#000000')

# Animating Images Over A 1ms Interval

anim = animation.FuncAnimation(fig, update_point, frames,
                               interval=30, repeat=False)

# Showing Animation
plt.show()

'''
# The writer will write the video to a file
# This is where properties of the video should be (fps, bitrate, codec ...etc)
writervideo = animation.FFMpegWriter(fps=30, bitrate=-1)

# You have to include this to tell python where the ffmpeg path is:
plt.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\unive\\Downloads\\Programs\\ffmpeg-4.3.1-win64-static\\bin\\ffmpeg.exe'


anim.save("browniananimation3.mp4",
          writer=writervideo)
'''
