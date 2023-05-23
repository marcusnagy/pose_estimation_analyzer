
import os
import subprocess
from typing import List
import yaml


class InputDataset:
    path: str
    label: str
    adjust: bool

    def __init__(self, path, label, adjust) -> None:
        self.path = path
        self.label = label
        self.adjust = adjust

    def __str__(self) -> str:
        return f"<{self.path}, {self.label}, {self.adjust}>"


if __name__ == "__main__":
    input_data = yaml.safe_load(open("input.yaml"))

    imin = input_data["min"]
    imax = input_data["max"]

    datasets: List[InputDataset] = list()
    collections = input_data["input"]
    for collection in collections:
        path = collection["base"]
        files = collection["files"]

        for file in files:
            datasets.append(
                InputDataset(
                    "{}/{}".format(path, file["file"]),
                    file["label"],
                    file["adjust"] if "adjust" in file else False
                )
            )

    for i in datasets:
        _, of = os.path.split(i.path)
        of, _ = os.path.splitext(of)

        o = "{}/{}".format(input_data["output"], of)

        args = [
            "python",
            "plot_pick_times.py",
            "--yrange", imin, imax,
            "--yhist", 20,
            "--nbins", 40,
            "-i", i.path,
            "-o", o
        ]
        if i.adjust:
            args.extend(["-a", True])
        args = [str(a) for a in args if not a == None]

        p = subprocess.Popen(args)
        p.wait()
