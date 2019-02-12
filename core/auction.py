from core.schemas import BiddersSchema, AuctionSchema
from core.bidder import Bidders


class AllPayAuction:
    raise_step = 1

    def __init__(self, auction, bidders, random_start=True):
        """
        Αρχικοποιεί την δημοπρασία (διαγωνισμό) με προσφορές για τον κάθε πλειοδότη.
        Η αρχική προσφορά μπορεί είτε να ξεκινάει για όλους από το 0 είτε να είναι τυχαία.
        :param auction:
        :param bidders:
        :param random_start:
        """
        self.auction = auction
        self.bidders = Bidders(bidders, auction['global_item_values'], random_start)
        self.auction_status = [bidder.user_id for bidder in self.bidders]

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
            for bidder in self.bidders:
                old_position = self.find_bidder_auction_position(bidder.user_id)
                self.auction_status.pop(old_position)

                old_bid = bidder.bid
                bidder.bid = bidder.user_action(self.auction_status, self.bidders)

                self.auction_status.append(bidder.user_id)
                self.auction_status.sort(
                    key=lambda user_id: self.bidders.get_bidder(user_id).bid, reverse=True
                )

                if old_bid != bidder.bid:
                    changes = True

            if not changes:
                break

            avg_values.append(sum(bidder.bid for bidder in self.bidders) / len(self.bidders))

        return avg_values

    def find_bidder_auction_position(self, user_id):
        """
        Βρίσκει την προσφορά ενός χρήστη με βάση το id του.
        :param user_id:
        :return:
        """
        for position, bidder_id in enumerate(self.auction_status):
            if bidder_id == user_id:
                return position


def create_auction(auction_payload, random_start):
    bidders = BiddersSchema().load(auction_payload).data
    auction = AuctionSchema().load(auction_payload).data
    return AllPayAuction(auction, bidders, random_start)

