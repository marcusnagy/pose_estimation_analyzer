from typing import List
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pandas as pd

from utils.tools import euler_std_dev_from_quaternion_data


def plot_std_bell_curves(df_pose: pd.DataFrame, df_std: pd.DataFrame, limits_translation: List[float], limits_rotation: List[float]):
    """Plot the standard deviation of the pose estimates."""

    def plot_bell_curve(mean, std_dev, label, color):
        # Using 4 standard deviations away from the mean in both directions
        # will capture approximately 99.7% of the distribution,
        # while using 3 standard deviations will capture approximately 99.3%
        x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 100)
        y = norm.pdf(x, mean, std_dev)
        plt.plot(x, y, label=label, color=color)

    # Calculate the mean of the pose estimates per axis
    mean_pose_x = df_pose['pos_x'].mean()
    mean_pose_y = df_pose['pos_y'].mean()
    mean_pose_z = df_pose['pos_z'].mean()

    num_data_points = df_pose.shape[0]

    translation_mean = {'x': mean_pose_x,
                        'y': mean_pose_y,
                        'z': mean_pose_z}

    # Calculate the mean of the quaternion estimates per axis
    # TODO: Change this into Euler Angles. Use the function
    data = df_pose.to_numpy()
    data_quat = data[:, 3:]
    euler_mean, euler_std = euler_std_dev_from_quaternion_data(data_quat)
    # Euler angles from quaternion data and then use mean.
    mean_quat_w = df_pose['quat_w'].mean()
    mean_quat_x = df_pose['quat_x'].mean()
    mean_quat_y = df_pose['quat_y'].mean()
    mean_quat_z = df_pose['quat_z'].mean()

    print(euler_std)
    euler_stds = euler_std[-1]  # Get the last column
    euler_stds = {axis: std for axis,
                  std in zip(['x', 'y', 'z'], euler_stds)}

    quaternion_mean = {'x': mean_quat_x,
                       'y': mean_quat_y,
                       'z': mean_quat_z,
                       'w': mean_quat_w}

    measurements = df_std.shape[0]
    plt.figure(figsize=(measurements, 3))
    for axis, color in zip(['x', 'y', 'z'], ['r', 'g', 'b']):
        plot_bell_curve(mean=translation_mean[axis],
                        std_dev=df_std[f'pose_std_{axis}'].iloc[-1],
                        label=f"Translation {axis.upper()}",
                        color=color)
    plt.xlabel('Meters')
    plt.ylabel('Probability density')
    if not limits_translation[0] == [0, 0] or not limits_translation[1] == [0, 0] or not limits_translation[2] == [0, 0]:
        max_value = max(max(sublist) for sublist in limits_translation)
        min_value = min(min(sublist) for sublist in limits_translation)
        plt.xlim((min_value, max_value))
    plt.title('Bell Curves for Translation Components')
    plt.legend()
    plt.show()

    # plt.figure(figsize=(measurements, 4))
    # for component, color in zip(['x', 'y', 'z', 'w'], ['r', 'g', 'b', 'k']):
    #     plot_bell_curve(mean=quaternion_mean[component],
    #                     std_dev=df_std[f'quat_std_{component}'].iloc[-1],
    #                     label=f"Quaternion {component.upper()}",
    #                     color=color)
    # plt.xlabel('Value')
    # plt.ylabel('Probability')
    # plt.title('Bell Curves for Quaternion Components')
    # plt.legend()
    # plt.show()

    plt.figure(figsize=(measurements, 3))
    for component, color in zip(['x', 'y', 'z'], ['r', 'g', 'b']):
        plot_bell_curve(mean=euler_mean[component],
                        std_dev=euler_stds[component],
                        label=f"Euler {component.upper()}",
                        color=color)
    plt.xlabel('Degrees')
    plt.xlim((-180, 180))
    plt.ylabel('Probability density')
    plt.title('Bell Curves for Euler Angles')
    plt.legend()
    plt.show()
