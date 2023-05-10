# If you think this file is ugly as hell
# Well, yes. Cause it is a sketch!

import argparse

import matplotlib.pyplot as plot
import numpy as np
import pandas
from matplotlib.axes import Axes


class Dataset:
    label: str
    data: np.ndarray

    def __init__(self, label, data) -> None:
        self.label = label
        self.data = data


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "plot_pick_times"
    )
    parser.add_argument('-f', '--file', type=str)
    parser.add_argument('-yr', '--yrange', type=float, nargs="*")
    parser.add_argument('-yh', '--yhist', type=int)
    parser.add_argument('-nb', '--nbins', type=int, default=40)
    args = parser.parse_args()

    data = pandas.read_csv(
        args.file,
        index_col=0
    )

    pick = np.array(data["lookout"]) - np.array(data["start"])
    pick = [x for x in pick if not np.isnan(x)]
    place = np.array(data["finished"]) - np.array(data["lookout"])
    place = [x for x in place if not np.isnan(x)]

    datasets = [
        Dataset("Pick", pick),
        Dataset("Place", place)
    ]
    vals = [np.array(ds.data) for ds in datasets]

    # If the ylim is given, check whether it is within the data
    # otherwise warn the user about data exclusion
    ylim = args.yrange
    if ylim is not None:
        vs = np.concatenate(vals, axis=None)
        dmin = np.min(vs)
        dmax = np.max(vs)
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
    fig.savefig("pick_times_steps.png")

    plot.clf()  # clear

    plot_box_plots(vals, [ds.label for ds in datasets], ylim)
    plot.savefig("pick_times_box.png")

    plot.clf()  # clear

    cleaned = list()
    for ds in datasets:
        mu = np.mean(ds.data)
        sigma = np.std(ds.data)

        cleaned.append([
            x
            for x in ds.data
            if (x >= mu - sigma) and (x <= mu + sigma)
        ])

    plot_box_plots(cleaned, [ds.label for ds in datasets], ylim)
    plot.savefig("pick_times_box_noliers.png")

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
    plot.savefig("pick_times_hist.png")
