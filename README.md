# pose_estimation_analyzer

## How to use

The csv 6D files looks as the following.

Raw position data.

```csv
,pos_x,pos_y,pos_z,quat_x,quat_y,quat_z,quat_w
0,1.1470097845583935,0.27074916612768934,0.7138396938250094,0.007412328877736154,-0.09723488661806344,0.6789833078582825,0.7276483366673804
1,1.1446601612577394,0.2819086006582481,0.7312431183490687,-0.018487856037125563,-0.11484841349819565,0.6734387092895168,0.7300331128973313
```

Standard deviation data.

```csv
,pose_std_x,pose_std_y,pose_std_z,quat_std_x,quat_std_y,quat_std_z,quat_std_w
0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
```

First Column is indexes.

To recover the **min** and **max** values of the data files you can run the *min_max.py* with all the files as input which gives you the minimum and maximum value of each column, the code will warn if the files does not match in columns.

```shell
python max_min.py <file_1> <file_2> <file_3> ...
```

To plot the different plots supplied by this library you can use e.g.

```shell
python plot_sphere_pose -h # To get help and information
python plot_sphere_pose -fpos <file_name of raw position data> -fstd <file_name of standard deviation data> -<method> true -xt '[<min>, <max>]' -yt '[<min>, <max>]' -zt '[<min>, <max>]' -xq '[<min>, <max>]' -yq '[<min>, <max>]' -zq '[<min>, <max>]' -wq '[<min>, <max>]'
```

 The `<min>` and `<max>` values should be the ones returned by the `min_max.py` or **if not** provided the axises will scale with the data, using same min and max values between multiple files makes for better analyzing when comparing plots. The `-*t` stand for *translation* and `-*q` for quaternion.

 The `<method>` are the different plot methods available by the script. Which can be viewed by the `-h` (help) call.
