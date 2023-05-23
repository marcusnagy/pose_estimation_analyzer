
from itertools import compress
from matplotlib.cbook import boxplot_stats
import numpy as np
import pandas as pd


def mu_and_sigma(data):
    mu = np.nanmean(data)
    sigma = np.nanstd(data)
    return mu, sigma


def in_range(x, l, u):
    return (x >= l) and (x <= u)


def make_table_column(data, prefix):
    m, s = mu_and_sigma(data)
    liers = len(boxplot_stats(data)[0]["fliers"])
    return {
        f"{prefix}_min": np.min(data),
        f"{prefix}_max": np.max(data),
        f"{prefix}_mean": m,
        f"{prefix}_std": s,
        f"{prefix}_n_liers": liers
    }


def copy_to(source: dict, target: dict):
    for k, v in source.items():
        target[k] = v


def make_row(label, N, pick, place):
    row = dict()
    copy_to({
        "label": label,
        "n_points": N,
        "n_pick": len(pick),
        "p_pick": len(pick) / N,
        "n_place": len(place),
        "p_place": len(place) / N
    }, row)
    copy_to(make_table_column(pick, "pick"), row)
    copy_to(make_table_column(place, "place"), row)
    return row


def f(l, b):
    return list(compress(l, b))


def filter_set_bools(data):
    return [not np.isnan(x) for x in data]


def adjust_set_boolean(data):
    m, s = mu_and_sigma(data)
    return [
        (x >= m - s) and (x <= m + s)
        for x in data
    ]


def adjust_set(data):
    return list(compress(data, adjust_set_boolean(data)))


def bool_and(a, b):
    return [
        a[i] and b[i] if i < len(a) and i < len(b) else False
        for i in range(len(a))
    ]


data_file_base_path = "~/Documents/LTH_Exjobb"
data_files = [
    "pick_juice_lying.0deg.csv",
    "pick_juice_vertical.csv",
    "pick_stout_test.csv",
    "pick_tall.csv",
    "pick_tall_lying.csv",
    "pick_tall_lying.90.csv",
    "pick_tall_lying.180.csv",
    "pick_tall_lying.bottom_left.csv",
    "pick_tall_lying.bottom_right.csv",
    "pick_tall_lying.top_left.csv",
    "pick_tall_lying.top_right.csv",
]
data_labels = [
    "Juice, lying",
    "Juice, standing",
    "Stout, test",
    "Tall, standing",
    "Tall, lying 0 degrees",
    "Tall, lying 90 degrees",
    "Tall, lying 180 degrees",
    "Tall, bottom left",
    "Tall, bottom right",
    "Tall, top left",
    "Tall, top right",
]
adjust_indices = [
    3,
    4,
    5,
    6
]

table = pd.DataFrame()
for i in range(len(data_files)):
    path = f"{data_file_base_path}/{data_files[i]}"
    data = pd.read_csv(path, index_col=0)

    pick_raw = data["lookout"] - data["start"]
    pick_bools = filter_set_bools(pick_raw)
    place_raw = data["finished"] - data["lookout"]
    place_bools = filter_set_bools(place_raw)

    place = f(pick_raw, pick_bools)
    pick = f(place_raw, place_bools)

    label = data_labels[i]

    row = make_row(label, len(data), pick, place)
    table = pd.concat([
        table,
        pd.DataFrame([row]),
    ], ignore_index=True)

    if i in adjust_indices:
        adjusted_label = f"{label} - Adjusted"
        adjusted_pick_bools = adjust_set_boolean(pick_raw)
        adjusted_place_bools = adjust_set_boolean(place_raw)

        common = bool_and(
            bool_and(adjusted_pick_bools, adjusted_place_bools),
            bool_and(pick_bools, place_bools)
        )
        N = sum(common)

        adjusted_pick = f(pick_raw, common)
        adjusted_place = f(place_raw, common)

        row = make_row(
            adjusted_label,
            N,
            adjusted_pick,
            adjusted_place
        )
        table = pd.concat([
            table,
            pd.DataFrame([row]),
        ], ignore_index=True)


print(table)

table.to_csv("pick_table.csv", mode="w")
