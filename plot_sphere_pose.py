from typing import Optional, Tuple, Union
import pandas as pd
import argparse
from pathlib import Path
from utils.bell_curves import plot_std_bell_curves
from utils.pose_spread import visualize_pose_estimate_spread
from utils.sphere_plot import plot_sphere
from utils.std_bar_graph import plot_std_bar_graph


def check_if_file_exists(file_path: Path) -> bool:
    if not (file_path.exists() and file_path.is_file()):
        raise ValueError(f"File {file_path} does not exist")

    if file_path.suffix != '.csv':
        raise ValueError(f"File {file_path} is not a csv file")

    return True


def check_file_path_read(file_path_one: Path,
                         file_path_two: Optional[Path],
                         expected_size: int = 7) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
    df_one = pd.read_csv(file_path_one, index_col=0)
    if df_one.shape[1] != expected_size:
        raise ValueError(
            f"File {file_path_one} does not have the correct format")

    print(df_one.shape)
    if file_path_two:
        df_two = pd.read_csv(file_path_two, index_col=0)
        print(df_two.shape)
        if df_two.shape[1] != expected_size or df_one.shape[0] != df_two.shape[0]:
            raise ValueError(
                f"File {file_path_two} does not have the correct format")

        return df_one, df_two
    else:
        return df_one


def parse_float_list(input_str):
    try:
        float_list = [float(x.strip())
                      for x in input_str.strip('[]').split(',')]
        if len(float_list) != 2:
            raise ValueError("Invalid number of elements")
        if float_list[0] >= float_list[1]:
            raise ValueError(
                "First value must be smaller than the second value")
        return float_list
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid float list format: {input_str}. Must be two comma-separated floats in square brackets, e.g. [0.1, 1].") from e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='plot_sphere_pose',
        description='Plot the poses of the sphere',
        epilog='Enjoy the program! :)'
    )
    parser.add_argument("-bell",
                        "--bell-curve",
                        default=False,
                        type=bool,
                        help="Plot the bell curve of the standard deviation"
                        )
    parser.add_argument("-pose",
                        "--pose-spread",
                        default=False,
                        type=bool,
                        help="Plot the pose spread of the sphere")
    parser.add_argument("-bar",
                        "--bar-graph",
                        default=False,
                        type=bool,
                        help="Plot the bar graph of the standard deviation")
    parser.add_argument("-fpos",
                        "--file-pose",
                        type=str,
                        nargs='?',
                        required=False,
                        help="Path to the csv file, expect csv file to have following format\n"
                        "[,pos_x,pos_y,pos_z,quat_x,quat_y,quat_z,quat_w]\n"
                        "NOTE: that first column is index column")
    parser.add_argument("-fstd",
                        "--file-std",
                        type=str,
                        nargs='?',
                        required=False,
                        help="Path to the csv file, expect csv file to have following format\n"
                        "[,pos_x,pos_y,pos_z,quat_x,quat_y,quat_z,quat_w]\n"
                        "NOTE: that first column is index column")
    parser.add_argument("-sph",
                        "--plot-sphere",
                        type=str,
                        nargs='?',
                        required=False,
                        help="Path to the csv file, expect csv file to have following format\n"
                        "[,pos_x,pos_y,pos_z,quat_x,quat_y,quat_z,quat_w]\n"
                        "NOTE: that first column is index column")
    parser.add_argument("-xt",
                        "--minmax-x-trans",
                        type=parse_float_list,
                        required=False,
                        default=[0, 0],
                        help="Minimum & Maximum x translation of the data, e.g. [0.1, 1]. Default is [0, 0].")
    parser.add_argument("-yt",
                        "--minmax-y-trans",
                        type=parse_float_list,
                        required=False,
                        default=[0, 0],
                        help="Minimum & Maximum y translation of the data, e.g. [0.1, 1]. Default is [0, 0].")
    parser.add_argument("-zt",
                        "--minmax-z-trans",
                        type=parse_float_list,
                        default=[0, 0],
                        required=False,
                        help="Minimum & Maximum z translation of the data, e.g. [0.1, 1]. Default is [0, 0].")
    parser.add_argument("-xq",
                        "--minmax-x-quat",
                        type=parse_float_list,
                        default=[0, 0],
                        required=False,
                        help="Minimum & Maximum x quaternion of the data, e.g. [0.1, 1]. Default is [0, 0].")
    parser.add_argument("-yq",
                        "--minmax-y-quat",
                        type=parse_float_list,
                        default=[0, 0],
                        required=False,
                        help="Minimum & Maximum y quaternion of the data, e.g. [0.1, 1]. Default is [0, 0].")
    parser.add_argument("-zq",
                        "--minmax-z-quat",
                        type=parse_float_list,
                        default=[0, 0],
                        required=False,
                        help="Minimum & Maximum z quaternion of the data, e.g. [0.1, 1]. Default is [0, 0].")
    parser.add_argument("-wq",
                        "--minmax-w-quat",
                        type=parse_float_list,
                        default=[0, 0],
                        required=False,
                        help="Minimum & Maximum w quaternion of the data, e.g. [0.1, 1]. Default is [0, 0].")
    args = parser.parse_args()

    # Check if only one of the file is provided
    if args.file_pose and args.plot_sphere:
        raise ValueError("Only one of the file can be provided")
    if args.file_std and args.plot_sphere:
        raise ValueError("Only one of the file can be provided")

    if not ((args.file_pose and args.file_std) or args.plot_sphere):
        raise ValueError("At least two of the file must be provided")

    # Check if the file exists
    file_path_raw: Path
    file_path_std: Path

    if args.file_pose and args.file_std:
        # Check if the file exists
        file_path_raw = Path(args.file_pose)
        file_path_std = Path(args.file_std)
        check_if_file_exists(file_path_raw)
        check_if_file_exists(file_path_std)

        # Read the file
        df_raw, df_std = check_file_path_read(file_path_raw, file_path_std)

        # Plot the data
        if args.bell_curve:
            plot_std_bell_curves(df_raw,
                                 df_std,
                                 [args.minmax_x_trans,
                                  args.minmax_y_trans,
                                  args.minmax_z_trans],
                                 [args.minmax_x_quat,
                                  args.minmax_y_quat,
                                  args.minmax_z_quat,
                                  args.minmax_w_quat])
        elif args.pose_spread:
            visualize_pose_estimate_spread(df_raw,
                                           df_std,
                                           [args.minmax_x_trans,
                                            args.minmax_y_trans,
                                            args.minmax_z_trans],
                                           [args.minmax_x_quat,
                                               args.minmax_y_quat,
                                               args.minmax_z_quat,
                                               args.minmax_w_quat])
        elif args.bar_graph:
            plot_std_bar_graph(df_raw,
                               df_std,
                               [args.minmax_x_trans,
                                args.minmax_y_trans,
                                args.minmax_z_trans],
                               [args.minmax_x_quat,
                                args.minmax_y_quat,
                                args.minmax_z_quat,
                                args.minmax_w_quat])
        exit(0)

    elif args.plot_sphere:
        file_path = Path(args.plot_sphere)
        check_if_file_exists(file_path)

    exit(0)
