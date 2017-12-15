#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import json
import random
import argparse
from copy import copy
from collections import defaultdict



class AllPayAuction:
    def __init__(self, values, budgets, random_start=True):
        """
        Αρχικοποιεί την δημοπρασία (διαγωνισμό) με προσφορές για τον κάθε πλειοδότη.
        Η αρχική προσφορά μπορεί είτε να ξεκινάει για όλους από το 0 είτε να είναι τυχαία.
        :param values:
        :param budgets:
        :param random_start:
        """
        self.k = len(values)
        self.bidders = len(budgets)
        self.values = values
        self.budgets = budgets

        if random_start:
            self.bids = [(user_id, random.randint(0, self.budgets[user_id])) for user_id in range(self.bidders)]
        else:
            self.bids = [(user_id, 0) for user_id in range(self.bidders)]

    def iterative_best_response(self, return_bids=False):
        """
        Υλοποίηση του IBR. Σε κάθε iterate αφαιρεί έναν πλειοδότη από την λίστα των προσφορών ο οποίος μέσα από την
        μέθοδο user_action αποφασίζει την επόμενη του προσφορά. Στην συνέχεια γίνεται μια ταξινόμηση των προσφορών.
        Αν οι προσφορές δεν αλλάξουν σε έναν κύκλο είναι ένδειξη ότι έχουμε ισορροπία Nash και while loop σταματάει.
        :param return_bids: boolean, ενδυκνύει αν θέλει να επιστρέψει τις αλλαγές των bids ανά iteration
        :return:
        """
        if return_bids:
            plot_data = defaultdict(list)
            for bidder in range(self.bidders):
                plot_data[bidder].append(self.bids[self.find_bid(bidder)][1])
            count = 1

        while True:

            old_bids = copy(self.bids)

            for bidder in range(self.bidders):

                selected_bid = self.bids.pop(self.find_bid(bidder))
                self.bids.append((selected_bid[0], self.user_action(selected_bid[0], selected_bid[1])))
                self.bids.sort(key=lambda bid: bid[1], reverse=True)

            if return_bids:
                for bidder in range(self.bidders):
                    position = self.find_bid(bidder)
                    plot_data[bidder].append(self.bids[position][1])

                count += 1

            if old_bids == self.bids:
                break

        if return_bids:
            return count, plot_data

        return max(self.bids, key=lambda bid: bid[1])[1],\
               sum(j for i, j in self.bids) / self.bidders,\
               min(self.bids, key=lambda bid: bid[1])[1]

    def user_action(self, user_id, previous_bid):
        """
        Ο χρήστης έχει μια σειρά από αποφάσεις από τις οποίες διαλέγει εκείνη που του αποδίδει το μεγαλύτερο
        utility. Η αποφάσεις του λαμβάνονται σε σχέση με το κάθε τρόπαιο.
        :param user_id:
        :param previous_bid:
        :return:
        """

        # utility, bid
        attempts = [(0, 0)]

        for i in range(self.k):
            # Κοιτάει αν η προσφορά του ξεπερνάει την προσφορά του πλειοδότη που κερδίζει το συγκεκριμένο τρόπαιο.
            if previous_bid > self.bids[i][1]:
                attempts.insert(0, (self.utility_function_targeted(self.bids[i][1], user_id, i), previous_bid))

            # Αν όχι και το id του είναι μεγαλύτερο από το id του πλειοδότη που κερδίζει κάνει την προσφορά του ίση με
            # με την προσφορά του άλλου.
            elif self.bids[i][1] <= self.budgets[user_id] and self.bids[i][1] <= self.values[i] \
                    and self.bids[i][0] > user_id:

                attempts.insert(0, (self.utility_function_targeted(self.bids[i][1], user_id, i), self.bids[i][1]))

            # Αν πάλι δεν έχει πιο δυνατο id τότε προσφέρει 1 παραπάνω αξία σε σχέση με τον άλλο.
            elif self.bids[i][1] + 1 <= self.budgets[user_id] and self.bids[i][1] + 1 <= self.values[i]:
                attempts.insert(0, (self.utility_function_targeted(self.bids[i][1], user_id, i), self.bids[i][1] + 1))

        # Επιστρέφει την προσφορά που του δίνει το πιο πολύ utility.
        return max(attempts, key=lambda attempt: attempt[0])[1]

    def find_bid(self, user_id):
        """
        Βρίσκει την προσφορά ενός χρήστη με βάση το id του.
        :param user_id:
        :return:
        """
        for position, bid in enumerate(self.bids):
            if bid[0] == user_id:
                return position

    def utility_function_targeted(self, bid, user_id, value_id):
        """
        Επιστρέφει το utility ενός πλειδότη εφόσον τα λεφτά που θα προσφέρει στο τέλος
        είναι μικρότερα της αξίας του τρόπαιου που θέλει να αποκτήσει.
        :param bid:
        :param user_id:
        :param value_id:
        :return:
        """
        if bid > self.budgets[user_id]:
            return -math.inf
        return self.values[value_id] - bid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorithmic trading iterative best response.")
    parser.add_argument("-d", "--data")
    parser.add_argument("-rs", "--random-start", action="store_true", default=False)

    args = parser.parse_args()

    if not args.data:
        parser.print_help()

    with open(args.data, "r") as data_file:
        json_data = json.load(data_file)
        au = AllPayAuction(json_data["values"], json_data["budgets"], random_start=args.random_start)
        max_effort, avg_effort, min_effort = au.iterative_best_response()
        print("Maximum effort: ", max_effort)
        print("Average effort: ", avg_effort)
        print("Minimum effort: ", min_effort)
        for bid in au.bids:
            print("User id:{0} made a bid of {1}".format(bid[0], bid[1]))
