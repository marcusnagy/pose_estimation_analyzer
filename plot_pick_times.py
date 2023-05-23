# If you think this file is ugly as hell
# Well, yes. Cause it is a sketch!

import argparse
from itertools import compress
import os
from typing import List

import matplotlib.pyplot as plot
import numpy as np
import pandas
from matplotlib.axes import Axes


class Dataset:
    label: str
    data: np.ndarray
    raw_data: np.ndarray

    def __init__(self, label, data, raw_data) -> None:
        self.label = label
        self.data = data
        self.raw_data = raw_data


def plot_steps_to(index: int, axes: Axes, dataset: Dataset):
    data = dataset.data
    title = dataset.label

    axes.bar(range(len(data)), data, width=0.90, align='center')
    axes.axhline(np.mean(data), color='black', label="Mean")
    axes.legend()
    axes.set_xlabel("Nth successful run")
    # sharey hides ticks and automatically sets ylim but ylabel will still show
    if index < 1:
        axes.set_ylabel("Time, seconds")
    axes.set_title(title)


def plot_box_plots(values, labels, ylim):
    plot.boxplot(values)
    plot.ylim(ylim)
    plot.xticks(
        ticks=range(1, len(values) + 1),
        labels=labels
    )
    plot.xlabel("Skill")
    plot.ylabel("Time, seconds")


def bool_and(a, b):
    return [
        a[i] and b[i] if i < len(a) and i < len(b) else False
        for i in range(len(a))
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "plot_pick_times"
    )
    parser.add_argument('-i', '--in_file', type=str)
    parser.add_argument('-o', '--out', type=str, default=".")
    parser.add_argument('-yr', '--yrange', type=float, nargs="*")
    parser.add_argument('-yh', '--yhist', type=int)
    parser.add_argument('-nb', '--nbins', type=int, default=40)
    parser.add_argument('-a', '--adjust', type=bool, default=False)
    args = parser.parse_args()

    def save(f):
        if not os.path.exists(args.out):
            os.mkdir(args.out)
        plot.savefig("{}/{}".format(args.out, f))

    data = pandas.read_csv(
        args.in_file,
        index_col=0
    )
    n_points = len(data)

    pick_raw = np.array(data["lookout"]) - np.array(data["start"])
    pick_bools = [not np.isnan(x) for x in pick_raw]
    pick = [pick_raw[i] for i in range(n_points) if pick_bools[i]]

    place_raw = np.array(data["finished"]) - np.array(data["lookout"])
    place_bools = [not np.isnan(x) for x in place_raw]
    place = [place_raw[i] for i in range(n_points) if place_bools[i]]

    datasets = [
        Dataset("Pick", pick, pick_raw),
        Dataset("Place", place, place_raw)
    ]
    vals = [np.array(ds.data) for ds in datasets]

    # If the ylim is given, check whether it is within the data
    # otherwise warn the user about data exclusion
    ylim = args.yrange
    if ylim is not None:
        vs = np.concatenate(vals, axis=None)
        dmin = np.nanmin(vs)
        dmax = np.nanmax(vs)
        if ylim[0] > dmin:
            print(
                "Warning: %.3f is higher than the data minimum %.3f" %
                (ylim[0], dmin)
            )
        if ylim[1] < dmax:
            print(
                "Warning: %.3f is lower than the data maximum %.3f" %
                (ylim[1], dmax)
            )

    fig, axes = plot.subplots(1, 2, sharey=True)
    fig.set_figwidth(8)  # in inches
    fig.set_figheight(5)  # in inches
    for i, ds in enumerate(datasets):
        plot_steps_to(i, axes[i], ds)
    save("pick_times_steps.png")

    plot.clf()  # clear

    plot_box_plots(vals, [ds.label for ds in datasets], ylim)
    save("pick_times_box.png")

    plot.clf()  # clear

    if args.adjust:
        # Find common indices
        common = list()
        for ds in datasets:
            dat = ds.raw_data
            # Remove nans
            a = [not np.isnan(x) for x in dat]

            # Remove outliers
            m = np.nanmean(dat)
            s = np.nanstd(dat)
            b = [
                (x >= m - s) and (x <= m + s)
                for x in dat
            ]

            # Compute the AND list
            c = bool_and(a, b)
            if len(common) < 1:
                common = c
            else:
                common = bool_and(common, c)

        cleaned = list()
        for ds in datasets:
            d = list(compress(ds.data, common))
            cleaned.append(Dataset(f"{ds.label}, Adjusted", d, None))

        l: List[Dataset] = list()
        l.extend(cleaned)
        l.extend(datasets)
        plot_box_plots([ds.data for ds in l], [ds.label for ds in l], ylim)
        save("pick_times_box_noliers.png")

        plot.clf()  # clear

    counts, _, _ = plot.hist(
        vals,
        stacked=True,
        align='mid',
        label=[ds.label for ds in datasets],
        bins=args.nbins,
        range=ylim
    )
    if args.yhist is not None:
        hist_max = np.max(counts)
        if hist_max > args.yhist:
            print(
                "Warning: yhist %i is lower than histogram maximum %i" %
                (args.yhist, hist_max)
            )
        plot.ylim(0.0, args.yhist + 0.5)
    plot.legend()
    plot.xlabel("Time, seconds")
    plot.ylabel("Count of successful runs")
    save("pick_times_hist.png")
