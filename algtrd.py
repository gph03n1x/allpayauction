#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math
import unittest
import argparse
from copy import copy

def zeros(x, y):
    return [[0 for j in range(y)] for i in range(x)]


class AllPayAuction:
    def __init__(self, values, budgets):
        self.k = len(values)
        self.bidders = len(budgets)
        self.values = values
        self.budgets = budgets
        self.bids = [(user_id, 0) for user_id in range(self.bidders)]

        self.decision = zeros(self.bidders, self.k)

    def iterative_best_response(self):
        count = 0
        old_bids = []
        while True:
            old_bids = copy(self.bids)
            print("O", old_bids)
            for bidder in range(0, self.bidders):
            #for bidder in range(self.bidders - 1, -1, -1):
                bid = self.bids.pop(self.find_bid(bidder))
                self.bids.append((bid[0], self.user_action(bid[0], bid[1])))
                self.bids.sort(key=lambda bid: bid[1], reverse=True)

            if (old_bids == self.bids):
                break

            print("N", self.bids)


        print("done")
        print(self.bids)

    def user_action(self, user_id, previous_bid):
        # TODO: there #1 seems to let #2 dominate him, i don't understand why
        # TODO: ok so it doesnt understand the second price thing
        # LOG:
        # O [(0, 80), (1, 80), (2, 0), (3, 0)]
        # UID 0 FA [(20, 0), (80, 80), (0, 0)]
        # (80, 80)
        # UID 1 FA [(20, 0), (0, 0)]
        # (20, 0)
        # UID 2 FA [(20, 0), (0, 0)]
        # (20, 0)
        # UID 3 FA [(19, 1), (0, 0)]
        # (19, 1)
        # N [(0, 80), (3, 1), (1, 0), (2, 0)]

        # utility, bid
        attempts = [(0, 0)]

        for i in range(self.k):

            bid_to_overcome = self.bids[next_price(self.bidders, i)]


            if self.bids[i][1] <= self.budgets[user_id] and self.bids[i][1] <= self.values[i] and self.bids[i][0] > user_id:
                #print("using id to overcome")
                attempts.insert(0, (self.utility_function_targeted(bid_to_overcome[1], user_id, i), self.bids[i][1]))

            elif self.bids[i][1] + 1 <= self.budgets[user_id] and self.bids[i][1] + 1 <= self.values[i] :
                #print("using budget to overcome")
                attempts.insert(0, (self.utility_function_targeted(bid_to_overcome[1] + 1, user_id, i), self.bids[i][1] + 1))

        print("UID", user_id, "FA", attempts)
        print(max(attempts, key=lambda attempt: attempt[0]))
        return max(attempts, key=lambda attempt: attempt[0])[1]

    def find_bid(self, user_id):
        for position, bid in enumerate(self.bids):
            if bid[0] == user_id:
                return position

    def utility_function_targeted(self, bid, user_id, value_id):
        if bid > self.budgets[user_id]:
            return -math.inf
        return self.values[value_id] - bid

    def utility_function(self, user_id):
        user_bid = self.bids[self.find_bid(user_id)][1]
        if user_bid > self.budgets[user_id]:
            return -math.inf
        return sum(self.decision[user_id][l] * self.values[l] for l in range(self.k)) - self.bids[user_id]




def next_price(bidders, user_id):
    if user_id + 1 >= bidders:
        return user_id
    return user_id + 1


class TestAllPayAuction(unittest.TestCase):

    def test_scenario_1(self):
        values = [80, 20]
        budgets = [100, 100, 100, 100]
        au = AllPayAuction(values, budgets)
        au.iterative_best_response()

    """
    def test_scenario_2(self):
        pass

    def test_scenario_3(self):
        pass

    def test_scenario_4(self):
        pass
    """

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
