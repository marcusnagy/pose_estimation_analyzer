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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "plot_pick_times"
    )
    parser.add_argument('-f', '--file', type=str)
    args = parser.parse_args()

    data = pandas.read_csv(
        args.file,
        index_col=0
    )

    pick = np.array(data["lookout"]) - np.array(data["start"])
    pick = [x for x in pick if x > 0]
    place = np.array(data["finished"]) - np.array(data["lookout"])
    place = [x for x in place if x > 0]

    datasets = [
        Dataset("Pick", pick),
        Dataset("Place", place)
    ]

    fig, axes = plot.subplots(1, 2, sharey=True)
    fig.set_figwidth(8)  # in inches
    fig.set_figheight(5)  # in inches
    for i, ds in enumerate(datasets):
        plot_steps_to(i, axes[i], ds)
    fig.savefig("pick_times_steps.png")

    plot.clf()  # clear

    plot.boxplot([ds.data for ds in datasets])
    plot.xticks(
        ticks=range(1, len(datasets) + 1),
        labels=[ds.label for ds in datasets]
    )
    plot.xlabel("Skill")
    plot.ylabel("Time, seconds")
    plot.savefig("pick_times_box.png")

    plot.clf()  # clear

    plot.hist(
        [ds.data for ds in datasets],
        stacked=True,
        align='mid',
        label=[ds.label for ds in datasets],
        bins=20
    )
    plot.legend()
    plot.xlabel("Time, seconds")
    plot.ylabel("Count of successful runs")
    plot.savefig("pick_times_hist.png")
