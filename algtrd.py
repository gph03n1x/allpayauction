#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import os
import math
import json
import random
import argparse
import matplotlib.pyplot as plt

RESULTS_DIR = "results"


class Bidder:
    def __init__(self, user_id, budget, starting_bid, trophies):
        self.user_id = user_id
        self.budget = budget
        self.bid = starting_bid
        self.trophies = trophies

    def __lt__(self, other):
        if self.bid == other.bid:
            return self.user_id < other.user_id
        return self.bid < other.bid

    def get_utility(self, trophy_id):
        if self.bid > self.budget:
            return -math.inf
        return self.trophies[trophy_id] - self.bid

    def __str__(self):
        return "user: {0} budget: {1} trophies: {2} current-bid: {3}".format(
            str(self.user_id), str(self.budget), str(self.trophies), str(self.bid)
        )


class AllPayAuction:
    def __init__(self, input_dictionary, random_start=True):
        """
        Αρχικοποιεί την δημοπρασία (διαγωνισμό) με προσφορές για τον κάθε πλειοδότη.
        Η αρχική προσφορά μπορεί είτε να ξεκινάει για όλους από το 0 είτε να είναι τυχαία.
        :param input_dictionary:
        :param random_start:
        """
        self.experiment = input_dictionary
        self.bidders = len(self.experiment["bidders"])
        self.k = len(self.get_values(0))

        if random_start:
            self.bids = [
                Bidder(user_id, self.get_budget(user_id),
                       random.randint(0, self.get_budget(user_id)), self.get_values(user_id))
                for user_id in range(self.bidders)
            ]
        else:
            self.bids = [
                Bidder(user_id, self.get_budget(user_id), 0, self.get_values(user_id))
                for user_id in range(self.bidders)
            ]

    def get_budget(self, user_id):
        return self.experiment["bidders"][user_id]["budget"]

    def get_values(self, user_id):
        if "values" in self.experiment["bidders"][user_id]:
            return self.experiment["bidders"][user_id]["values"]
        return self.experiment["values"]

    def iterative_best_response(self):
        """
        Υλοποίηση του IBR. Σε κάθε iterate αφαιρεί έναν πλειοδότη από την λίστα των προσφορών ο οποίος μέσα από την
        μέθοδο user_action αποφασίζει την επόμενη του προσφορά. Στην συνέχεια γίνεται μια ταξινόμηση των προσφορών.
        Αν οι προσφορές δεν αλλάξουν σε έναν κύκλο είναι ένδειξη ότι έχουμε ισορροπία Nash και while loop σταματάει.
        :return:
        """

        avg_values = []

        while True:
            changes = False
            for bidder in range(self.bidders):

                selected_bidder = self.bids.pop(self.find_bid(bidder))
                old_bid = selected_bidder.bid
                selected_bidder.bid = self.user_action(selected_bidder)

                self.bids.append(selected_bidder)
                self.bids.sort(key=lambda bid: bid.bid, reverse=True)

                if old_bid != selected_bidder.bid:
                    changes = True

            if not changes:
                break

            avg_values.append(sum(bidder.bid for bidder in self.bids) / self.bidders)

        return avg_values

    def user_action(self, bidder):
        """
        Ο χρήστης έχει μια σειρά από αποφάσεις από τις οποίες διαλέγει εκείνη που του αποδίδει το μεγαλύτερο
        utility. Η αποφάσεις του λαμβάνονται σε σχέση με το κάθε τρόπαιο.
        :param bidder:
        :return:
        """

        # utility, bid
        attempts = [(0, 0)]

        for i in range(self.k):
            # Κοιτάει αν η προσφορά του ξεπερνάει την προσφορά του πλειοδότη που κερδίζει το συγκεκριμένο τρόπαιο.
            if bidder.bid > self.bids[i].bid:
                attempts.insert(0, (bidder.get_utility(i), bidder.bid))

            # Αν όχι και το id του είναι μεγαλύτερο από το id του πλειοδότη που κερδίζει κάνει την προσφορά του ίση με
            # με την προσφορά του άλλου.
            elif self.bids[i].bid <= bidder.budget and self.bids[i].bid <= bidder.trophies[i] \
                    and self.bids[i].user_id > bidder.user_id:

                attempts.insert(0, (bidder.get_utility(i), self.bids[i].bid))

            # Αν πάλι δεν έχει πιο δυνατο id τότε προσφέρει 1 παραπάνω αξία σε σχέση με τον άλλο.
            elif self.bids[i].bid + 1 <= bidder.budget and self.bids[i].bid + 1 <= bidder.trophies[i]:
                attempts.insert(0, (bidder.get_utility(i), self.bids[i].bid+1))

        # Επιστρέφει την προσφορά που του δίνει το πιο πολύ utility.
        return max(attempts, key=lambda attempt: attempt[0])[1]

    def find_bid(self, user_id):
        """
        Βρίσκει την προσφορά ενός χρήστη με βάση το id του.
        :param user_id:
        :return:
        """
        for position, bidder in enumerate(self.bids):
            if bidder.user_id == user_id:
                return position


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorithmic trading iterative best response.")
    parser.add_argument("-d", "--data")
    parser.add_argument("-rs", "--random-start", action="store_true", default=False)

    pathlib.Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)

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

            au = AllPayAuction(series, random_start=args.random_start)
            data = au.iterative_best_response()

            result[series["name"]] = {"effort": data,
                                      "final_bids": [str(bid) for bid in au.bids]}

            plt.plot(range(len(data)), data, label=series["name"])

        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.tight_layout()
        plt.savefig(experiment+'.png')

        plt.close()
        experiment_filename = experiment.split("\\")[-1]
        with open(RESULTS_DIR + "/" + str(experiment_filename), 'w') as result_file:
            json.dump(result, result_file)
