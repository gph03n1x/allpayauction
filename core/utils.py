import json
import os


def load_experiments(experiment_dataset):
    if os.path.isdir(experiment_dataset):
        experiments = [
            os.path.join(experiment_dataset, f) for f in os.listdir(experiment_dataset)
            if os.path.isfile(os.path.join(experiment_dataset, f)) and f.endswith(".json")
        ]

    else:
        experiments = [experiment_dataset]

    for experiment in experiments:
        with open(experiment, "r") as data_file:
            yield json.load(data_file), experiment
