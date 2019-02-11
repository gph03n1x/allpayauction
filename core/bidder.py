import math


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
