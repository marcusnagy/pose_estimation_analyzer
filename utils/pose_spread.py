from typing import List
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from pyquaternion import Quaternion
import seaborn as sns


def visualize_pose_estimate_spread(df: pd.DataFrame, df_std: pd.DataFrame, limits_translation: List[float], limits_rotation: List[float]):
    """Visualizes the spread of the estimated poses.

    Should be used to visualize the spread of the estimated poses. (raw data)
    """

    def quaternion_to_rotation_matrix(quaternion: Quaternion) -> np.ndarray:
        """Converts quaternion to rotation matrix.

        Args:
            quaternion (Quaternion): Quaternion to convert to rotation matrix.

        Returns:
            np.ndarray: Rotation matrix.
        """
        return quaternion.rotation_matrix

    def plot_coordinate_frame(ax, R, T, scale=0.01) -> None:
        """Plot coordinate frame on given plot object.

        Args:
            ax: Plot object
            R (np.ndarray): Rotation vector
            T (np.ndarray): Translation vector
            scale (float, optional): Length of arrows for coordinate frame.
                                     Defaults to 0.01.
        """
        colors = ["r", "g", "b"]
        labels = ["X", "Y", "Z"]
        for i, (color, label) in enumerate(zip(colors, labels)):
            ax.quiver(
                *T,
                *scale*R[:, i],
                color=color,
                label=label,
                lw=2
            )

    # Convert to numpy array
    data = df.to_numpy()

    mean_pose_x = df['pos_x'].mean()
    mean_pose_y = df['pos_y'].mean()
    mean_pose_z = df['pos_z'].mean()

    # Extract translations and quaternions
    translations = data[:, :3]
    quaternions = data[:, [6, 3, 4, 5]]  # [x, y, z, w] -> [w, x, y, z]
    num_data_points = translations.shape[0]

    # Get the x, y, z coordinates of the translations [Used for histogram]
    translations_x = [t[0] for t in translations]
    translations_y = [t[1] for t in translations]
    translations_z = [t[2] for t in translations]

    # TODO: Get the x, y, z coordinates of the euler angles [Used for histogram]
    # Get the x, y, z, w coordinates of the quaternions [Used for histogram]
    quaternion_w = [q[0] for q in quaternions]
    quaternion_x = [q[1] for q in quaternions]
    quaternion_y = [q[2] for q in quaternions]
    quaternion_z = [q[3] for q in quaternions]

    # Convert quaternions to rotation matrices
    rotation_matrices = np.apply_along_axis(
        lambda quaternion: quaternion_to_rotation_matrix(
            Quaternion(*quaternion).normalised
        ),
        1,
        quaternions
    )

    # Plot the 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the coordinate frame
    for t, R in zip(translations, rotation_matrices):
        ax.scatter(*t, marker="o")
        plot_coordinate_frame(ax, R, t)

    # Set the labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Set the limits
    if not limits_translation[0] == [0, 0]:
        ax.set_xlim(tuple(limits_translation[0]))
    if not limits_translation[1] == [0, 0]:
        ax.set_ylim(tuple(limits_translation[1]))
    if not limits_translation[2] == [0, 0]:
        ax.set_zlim(tuple(limits_translation[2]))

    # Show
    plt.show()

    # Plot the histograms with kernel density estimation (KDE)
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    sns.histplot(translations_x, kde=True, ax=axes[0])
    axes[0].set_title("Translation X")
    sns.histplot(translations_y, kde=True, ax=axes[1])
    axes[1].set_title("Translation Y")
    sns.histplot(translations_z, kde=True, ax=axes[2])
    axes[2].set_title("Translation Z")
    for ax in axes:
        ax.set_ylim(0, num_data_points)
    if not limits_translation[0] == [0, 0]:
        axes[0].set_xlim(tuple(limits_translation[0]))
    if not limits_translation[1] == [0, 0]:
        axes[1].set_xlim(tuple(limits_translation[1]))
    if not limits_translation[2] == [0, 0]:
        axes[2].set_xlim(tuple(limits_translation[2]))
    plt.show()

    fig, axes = plt.subplots(1, 4, figsize=(20, 4))
    for ax in axes:
        ax.set_ylim(0, num_data_points)
    sns.histplot(quaternion_w, kde=True, ax=axes[0])
    axes[0].set_title("Quaternion W")
    sns.histplot(quaternion_x, kde=True, ax=axes[1])
    axes[1].set_title("Quaternion X")
    sns.histplot(quaternion_y, kde=True, ax=axes[2])
    axes[2].set_title("Quaternion Y")
    sns.histplot(quaternion_z, kde=True, ax=axes[3])
    axes[3].set_title("Quaternion Z")
    if not limits_rotation[3] == [0, 0]:
        axes[0].set_xlim(tuple(limits_rotation[3]))
    if not limits_rotation[0] == [0, 0]:
        axes[1].set_xlim(tuple(limits_rotation[0]))
    if not limits_rotation[1] == [0, 0]:
        axes[2].set_xlim(tuple(limits_rotation[1]))
    if not limits_rotation[2] == [0, 0]:
        axes[3].set_xlim(tuple(limits_rotation[2]))

    plt.show()
