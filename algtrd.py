#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math
import random
import unittest
import argparse
from copy import copy
from collections import defaultdict



class AllPayAuction:
    def __init__(self, values, budgets, random_start=True):
        self.k = len(values)
        self.bidders = len(budgets)
        self.values = values
        self.budgets = budgets


        if random_start:
            self.bids = [(user_id, random.randint(0, self.budgets[user_id])) for user_id in range(self.bidders)]
        else:
            self.bids = [(user_id, 0) for user_id in range(self.bidders)]
        print(self.bids)

    def iterative_best_response(self, return_bids=True):
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

                count+=1

            if old_bids == self.bids:
                break

        if return_bids:
            return count, plot_data

        return max(self.bids, key=lambda bid: bid[1])[1],\
               sum(j for i, j in self.bids) / self.bidders,\
               min(self.bids, key=lambda bid: bid[1])[1]

    def user_action(self, user_id, previous_bid):

        # utility, bid
        attempts = [(0, 0)]

        for i in range(self.k):

            if previous_bid > self.bids[i][1]:
                attempts.insert(0, (self.utility_function_targeted(self.bids[i][1], user_id, i), previous_bid))

            elif self.bids[i][1] <= self.budgets[user_id] and self.bids[i][1] <= self.values[i] \
                    and self.bids[i][0] > user_id:
                # print("using id to overcome")
                attempts.insert(0, (self.utility_function_targeted(self.bids[i][1], user_id, i), self.bids[i][1]))

            elif self.bids[i][1] + 1 <= self.budgets[user_id] and self.bids[i][1] + 1 <= self.values[i]:
                # print("using budget to overcome")
                attempts.insert(0, (self.utility_function_targeted(self.bids[i][1], user_id, i), self.bids[i][1] + 1))

        # print("ID", user_id, "FA", attempts, "RE", max(attempts, key=lambda attempt: attempt[0]))
        return max(attempts, key=lambda attempt: attempt[0])[1]

    def find_bid(self, user_id):
        for position, bid in enumerate(self.bids):
            if bid[0] == user_id:
                return position

    def utility_function_targeted(self, bid, user_id, value_id):
        if bid > self.budgets[user_id]:
            return -math.inf
        return self.values[value_id] - bid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorithmic trading iterative best response.")
    args = parser.parse_args()

