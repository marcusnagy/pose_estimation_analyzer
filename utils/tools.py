from typing import Dict, List, Tuple
import numpy as np
from scipy.spatial.transform import Rotation as R


def euler_std_dev_from_quaternion_data(quaternion_data) -> Tuple[Dict[str, float], List[float]]:
    """Function to convert quaternion standard deviation to Euler angle standard deviation."""
    # Convert quaternions to Euler angles
    euler_angles = [R.from_quat(quat).as_euler(
        'xyz', degrees=True) for quat in quaternion_data]

    # Compute the standard deviations and mean of the Euler angles
    euler_mean = {axis: np.mean(
        [euler_angle[i] for euler_angle in euler_angles]) for i, axis in enumerate('xyz')}

    euler_std_dev = []
    for i in range(len(euler_angles)):
        euler_std_dev.append(np.std(euler_angles[: i+1], axis=0))

    # euler_std_dev= {axis: np.std(
    #     [euler_angle[i] for euler_angle in euler_angles]) for i, axis in enumerate('xyz')}

    return euler_mean, euler_std_dev
