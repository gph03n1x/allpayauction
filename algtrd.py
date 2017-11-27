#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math
import random
import unittest
import argparse
from copy import copy


class AllPayAuction:
    def __init__(self, values, budgets):
        self.k = len(values)
        self.bidders = len(budgets)
        self.values = values
        self.budgets = budgets
        self.bids = [(user_id, 0) for user_id in range(self.bidders)]

    def iterative_best_response(self):
        while True:
            old_bids = copy(self.bids)

            for bidder in range(0, self.bidders):

                selected_bid = self.bids.pop(self.find_bid(bidder))
                self.bids.append((selected_bid[0], self.user_action(selected_bid[0], selected_bid[1])))
                self.bids.sort(key=lambda bid: bid[1], reverse=True)

            if old_bids == self.bids:
                break

        print(self.bids)
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


class TestAllPayAuction(unittest.TestCase):
    def setUp(self):
        print()

    def test_scenario_1(self):
        tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        budgets = [1000, 1000, 1000, 1000]
        for values in tests:
            au = AllPayAuction(values, budgets)
            print(au.iterative_best_response())

    def test_scenario_2(self):
        tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        budgets = [1000, 1000/2, 1000/2, 1000/2]
        for values in tests:
            au = AllPayAuction(values, budgets)
            print(au.iterative_best_response())

    def test_scenario_3(self):
        tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        budgets = [1000, 1000/10, 1000/10, 1000/10]
        for values in tests:
            au = AllPayAuction(values, budgets)
            print(au.iterative_best_response())

    def test_scenario_4(self):
        tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        budgets = [100+i*10 for i in range(4)]
        for values in tests:
            au = AllPayAuction(values, budgets)
            print(au.iterative_best_response())


def trophy_generation(k, V, n):
    values = []
    for i in range(n):
        upper_limit = V
        lower_limit = V//2
        trophies = []
        for g in range(k-1):
            trophies.append(
                random.randint(lower_limit, upper_limit)
            )
            upper_limit = lower_limit-1
            lower_limit = lower_limit//2
        trophies.append(V - sum(trophies))
        trophies.sort()
        values.append(trophies)
    return values






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorithmic trading iterative best response.")
    key_group = parser.add_mutually_exclusive_group()
    key_group.add_argument("-f", "--first-price")
    key_group.add_argument("-n", "--next-price")
    parser.add_argument("-t", "--tests", action="store_true")

    args = parser.parse_args()

    if args.tests:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestAllPayAuction)
        unittest.TextTestRunner(verbosity=2).run(suite)
        sys.exit()

    print(trophy_generation(10, 10000, 5))
