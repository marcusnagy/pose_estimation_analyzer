from typing import List
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from utils.tools import euler_std_dev_from_quaternion_data


def plot_std_bar_graph(df_pose: pd.DataFrame,
                       df_std: pd.DataFrame,
                       limits_translation: List[float],
                       limits_rotation: List[float]):
    """Plot the standard deviation of the pose estimates.

    Should be used with the standard deviation csv file and
    with the raw data csv file.
    """
    def plot_bar_chart(ax, std_devs: np.ndarray, title, color):
        """Plot bar chart of standard deviations."""
        if isinstance(std_devs, list):
            std_devs = np.array(std_devs)
        num_measurements = std_devs.shape[0]
        bar_width = 1 / (num_measurements + 1)
        x_labels = ['X', 'Y', 'Z']
        x = np.arange(len(x_labels))

        for i, std_dev in enumerate(std_devs):
            ax.bar(x + i * bar_width, std_dev,
                   width=bar_width,
                   color=color[i % len(color)],
                   label=f"Measurement {i+1}")
        ax.set_xticks(x + bar_width * (num_measurements - 1) / 2)
        ax.set_xticklabels(x_labels)
        ax.set_title(title)
        ax.legend()

    def generate_colors(num_colors):
        colormap = plt.cm.viridis
        color_indices = np.linspace(0, 1, num_colors)
        return colormap(color_indices)

    # Convert to numpy array
    data_std = df_std.to_numpy()
    data_pose = df_pose.to_numpy()

    # Extract translations and quaternions
    translations_std = data_std[:, :3]
    # unused, Better to look and the standard deviation of the euler angles
    quaternion_std = data_std[:, 3:]

    translations_pose = data_pose[:, :3]  # unused
    quaternions_pose = data_pose[:, 3:]

    measurements = translations_std.shape[0]
    colors = generate_colors(measurements)

    fig, ax = plt.subplots(figsize=(measurements, 6))
    plot_bar_chart(ax, translations_std,
                   "Translation Standard Deviation", colors)
    plt.xlabel('Axis')
    plt.ylabel('Standard Deviation')
    plt.show()

    _, euler_std_dev = euler_std_dev_from_quaternion_data(quaternions_pose)
    fig, ax = plt.subplots(figsize=(measurements, 6))
    plot_bar_chart(ax, euler_std_dev,
                   "Euler Angles Standard Deviation", colors)
    plt.xlabel('Angle')
    plt.ylabel('Standard Deviation')
    plt.show()
