#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import os
import json
import random
import argparse
import matplotlib.pyplot as plt

from core.settings import IMAGES_DIRECTORY, RESULTS_DIRECTORY
from core.auction import create_auction


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorithmic trading iterative best response.")
    parser.add_argument("-d", "--data")
    parser.add_argument("-rs", "--random-start", action="store_true", default=False)

    pathlib.Path(RESULTS_DIRECTORY).mkdir(parents=True, exist_ok=True)
    pathlib.Path(IMAGES_DIRECTORY).mkdir(parents=True, exist_ok=True)

    args = parser.parse_args()

    if not args.data:
        parser.print_help()

    if os.path.isdir(args.data):
        experiments = [os.path.join(args.data, f) for f in os.listdir(args.data)
                       if os.path.isfile(os.path.join(args.data, f)) and f.endswith(".json")]
    else:
        experiments = [args.data]

    for experiment in experiments:
        with open(experiment, "r") as data_file:
            json_data = json.load(data_file)

        if type(json_data) is not list:
            json_data = [json_data]

        plt.subplot(121)
        result = {}
        for series in json_data:

            au = create_auction(series, args.random_start)
            data = au.iterative_best_response()

            result[series["name"]] = {"effort": data,
                                      "final_bids": [str(bidder.bid) for bidder in au.bidders]}

            plt.plot(range(len(data)), data, label=series["name"])

        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.tight_layout()

        experiment_filename = experiment.replace('/', '.')
        with open(RESULTS_DIRECTORY + "/" + str(experiment_filename)+ '.json', 'w') as result_file:
            json.dump(result, result_file)

        plt.savefig(IMAGES_DIRECTORY + "/" + str(experiment_filename) + '.png')

        plt.close()
