#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import pathlib

import click
import matplotlib.pyplot as plt

from core.auction import create_auction
from core.settings import IMAGES_DIRECTORY, RESULTS_DIRECTORY
from core.utils import load_experiments

pathlib.Path(RESULTS_DIRECTORY).mkdir(parents=True, exist_ok=True)
pathlib.Path(IMAGES_DIRECTORY).mkdir(parents=True, exist_ok=True)


@click.command()
@click.option('--data', type=str, required=True, help="JSON file containing the experiment")
@click.option(
    '--random_start', is_flag=True, default=False,
    help="Selecting this option makes the bidders start with a random bid"
)
def main(data, random_start):
    for experiment, experiment_filename in load_experiments(data):

        plt.subplot(121)
        result = {}
        for series in experiment:
            au = create_auction(series, random_start)
            data = au.iterative_best_response()

            result[series["name"]] = {
                "effort": data,
                "final_bids": [str(bidder.bid) for bidder in au.bidders]
            }

            plt.plot(range(len(data)), data, label=series["name"])

        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.tight_layout()
        experiment_filename = experiment_filename.replace('/', '.')
        with open(RESULTS_DIRECTORY + "/" + str(experiment_filename) + '.json',
                  'w') as result_file:
            json.dump(result, result_file)

        plt.savefig(IMAGES_DIRECTORY + "/" + str(experiment_filename) + '.png')

        plt.close()


if __name__ == "__main__":
    main()
