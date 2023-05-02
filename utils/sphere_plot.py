import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_sphere(df: pd.DataFrame):
    """Plots the sphere in 3D space.

    Created a heatmap on a sphere.
    Should be used to visualize the spread of the generated poses.
    """
    def random_point(r=1):
        ct = 2*np.random.rand() - 1
        st = np.sqrt(1 - ct**2)
        phi = 2 * np.pi * np.random.rand()
        x = r * st * np.cos(phi)
        y = r * st * np.sin(phi)
        z = r * ct
        return np.array([x, y, z])

    def near(p, pntList, d0):
        cnt = 0
        for pj in pntList:
            dist = np.linalg.norm(p - pj)
            if dist < d0:
                cnt += 1 - dist/d0
        return cnt
        # Convert to numpy array
    data = df.to_numpy()

    pointList = np.array([random_point(10.05) for i in range(65)])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(0, np.pi, 60)

    # create the sphere surface
    XX = 10 * np.outer(np.cos(u), np.sin(v))
    YY = 10 * np.outer(np.sin(u), np.sin(v))
    ZZ = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

    WW = XX.copy()
    for i in range(len(XX)):
        for j in range(len(XX[0])):
            x = XX[i, j]
            y = YY[i, j]
            z = ZZ[i, j]
            WW[i, j] = near(np.array([x, y, z]), pointList, 3)
    WW = WW / np.amax(WW)
    myheatmap = WW

    # ~ ax.scatter( *zip( *pointList ), color='#dd00dd' )
    ax.plot_surface(XX, YY,  ZZ, cstride=1, rstride=1,
                    facecolors=cm.jet(myheatmap))
    plt.show()
