import math
import random


class Bidder:
    def __init__(self, user_id, budget, starting_bid, trophies, raise_step):
        self.user_id = user_id
        self.budget = budget
        self.bid = starting_bid
        self.trophies = trophies
        self.raise_step = raise_step

    def __lt__(self, other):
        if self.bid == other.bid:
            return self.user_id < other.user_id
        return self.bid < other.bid

    def get_utility(self, bid, trophy_id):
        if bid > self.budget:
            return -math.inf
        return self.trophies[trophy_id] - bid

    def __str__(self):
        return "user: {0} budget: {1} trophies: {2} current-bid: {3}".format(
            str(self.user_id), str(self.budget), str(self.trophies), str(self.bid)
        )

    def user_action(self, auction_status, bidders):
        """
        Ο χρήστης έχει μια σειρά από αποφάσεις από τις οποίες διαλέγει εκείνη
        που του αποδίδει το μεγαλύτερο utility. Η αποφάσεις του λαμβάνονται σε
        σχέση με το κάθε τρόπαιο.
        :param bidders:
        :return:
        """
        # utility, bid
        attempts = [(0, 0)]

        auctions_that_matter = auction_status[:len(self.trophies)]

        for trophy_position, bidder_id in enumerate(auctions_that_matter):
            bidder = bidders.get_bidder(bidder_id)

            if bidder.user_id == self.user_id:
                continue

            # Κοιτάει αν η προσφορά του ξεπερνάει την προσφορά του
            # πλειοδότη που κερδίζει το συγκεκριμένο τρόπαιο.
            if self.bid > bidder.bid:
                attempts.insert(0, (self.get_utility(self.bid, trophy_position), self.bid))

            # Αν όχι και το id του είναι μεγαλύτερο από το id του
            # πλειοδότη που κερδίζει κάνει την προσφορά του ίση με
            # με την προσφορά του άλλου.
            elif bidder.bid <= self.budget and bidder.bid <= self.trophies[trophy_position] \
                    and bidder.user_id > self.user_id:

                attempts.insert(0, (self.get_utility(bidder.bid, trophy_position), bidder.bid))

            # Αν πάλι δεν έχει πιο δυνατο id τότε προσφέρει 1 παραπάνω αξία σε σχέση με τον άλλο.
            elif bidder.bid + self.raise_step <= self.budget \
                    and bidder.bid + self.raise_step <= self.trophies[trophy_position]:
                new_bid = bidder.bid + self.raise_step
                attempts.insert(0, (self.get_utility(new_bid, trophy_position), new_bid))

        # Επιστρέφει την προσφορά που του δίνει το πιο πολύ utility.
        return max(attempts, key=lambda attempt: attempt[0])[1]


class Bidders:
    def __init__(self, bidders, global_item_values, random_start=True):
        """
        Αρχικοποιεί την δημοπρασία (διαγωνισμό) με προσφορές για τον κάθε πλειοδότη.
        Η αρχική προσφορά μπορεί είτε να ξεκινάει για όλους από το 0 είτε να είναι τυχαία.
        :param bidders:
        :param random_start:
        """
        self.global_item_values = global_item_values
        self.random_start = random_start

        self.bidders = [
            Bidder(
                user_id,
                bidder['budget'],
                self.get_starting_budget(bidder),
                self.get_item_values(bidder),
                bidder['raise_step']
            )
            for user_id, bidder in enumerate(bidders['bidders'])
        ]

    def __len__(self):
        return len(self.bidders)

    def __iter__(self):
        for bidder in self.bidders:
            yield bidder

    def get_starting_budget(self, bidder):
        return random.randint(0, bidder['budget']) if self.random_start else 0

    def get_item_values(self, bidder):
        if 'item_values' in bidder:
            return bidder['item_values']
        return self.global_item_values

    def get_bidder(self, user_id):
        for bidder in self.bidders:
            if bidder.user_id == user_id:
                return bidder
