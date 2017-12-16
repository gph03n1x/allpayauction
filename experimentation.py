import unittest
from algtrd import AllPayAuction
import matplotlib.pyplot as plt


class TestBiddingAllPayAuction(unittest.TestCase):
    RANDOM_START = True
    PATH = ""

    def test_scenario_1(self):
        self.name = "scenario1/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000, 1000, 1000]

    def test_scenario_2(self):
        self.name = "scenario2/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/2, 1000/2, 1000/2]

    def test_scenario_3(self):
        self.name = "scenario3/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/10, 1000/10, 1000/10]

    def test_scenario_4(self):
        self.name = "scenario4/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [100+i*10 for i in range(4)]

    def tearDown(self):
        self.base = "images/" + self.PATH

        for values in self.tests:
            au = AllPayAuction(values, self.budgets, random_start=self.RANDOM_START)

            x_values, plot_data = au.iterative_best_response(True)
            x_values = range(x_values)

            fig = plt.figure()
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)

            ax1.plot(x_values, plot_data[0], 'r')
            ax2.plot(x_values, plot_data[1], 'b')
            ax3.plot(x_values, plot_data[2], 'g')
            ax4.plot(x_values, plot_data[3], 'y')

            ax1.set_xlabel("Iterations")
            ax1.set_ylabel("Bid")
            ax1.set_title("Bidder 0")

            ax2.set_xlabel("Iterations")
            ax2.set_ylabel("Bid")
            ax2.set_title("Bidder 1")

            ax3.set_xlabel("Iterations")
            ax3.set_ylabel("Bid")
            ax3.set_title("Bidder 2")

            ax4.set_xlabel("Iterations")
            ax4.set_ylabel("Bid")
            ax4.set_title("Bidder 3")

            plt.tight_layout()
            plt.savefig(self.base + self.name + str(values) + '.png')
            plt.close(fig)


class TestMeasureAllPayAuctionEffort(unittest.TestCase):
    RANDOM_START = True
    PATH = ""

    def test_scenario_1(self):
        self.name = "scenario1/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000, 1000, 1000]

    def test_scenario_2(self):
        self.name = "scenario2/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/2, 1000/2, 1000/2]

    def test_scenario_3(self):
        self.name = "scenario3/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/10, 1000/10, 1000/10]

    def test_scenario_4(self):
        self.name = "scenario4/"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [100+i*10 for i in range(4)]

    def tearDown(self):
        self.base = "images/" + self.PATH
        x = []
        y1 = []
        y2 = []
        y3 = []
        fig = plt.figure()
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)

        for values in self.tests:
            au = AllPayAuction(values, self.budgets, random_start=self.RANDOM_START)

            y_max, y_avg, y_min = au.iterative_best_response()
            x.append(abs(values[0] - values[1]))
            y1.append(y_max)
            y2.append(y_avg)
            y3.append(y_min)

        ax1.plot(x, y1, 'r')
        ax2.plot(x, y2, 'b')
        ax3.plot(x, y3, 'g')

        ax1.set_xlabel("abs(Value[0] - Value[1])")
        ax2.set_xlabel("abs(Value[0] - Value[1])")
        ax3.set_xlabel("abs(Value[0] - Value[1])")

        ax1.set_title("Maximum")
        ax2.set_title("Average")
        ax3.set_title("Minimum")
        plt.tight_layout()
        plt.savefig(self.base + self.name + "effort.png")


if __name__ == "__main__":
    START_POINTS = [(True, "rstart/"), (False, "0start/")]
    for _boolean, _path in START_POINTS:
        TestBiddingAllPayAuction.RANDOM_START = _boolean
        TestMeasureAllPayAuctionEffort.RANDOM_START = _boolean
        TestBiddingAllPayAuction.PATH = _path
        TestMeasureAllPayAuctionEffort.PATH = _path
        #suite = unittest.TestLoader().loadTestsFromTestCase(TestBiddingAllPayAuction)
        #unittest.TextTestRunner(verbosity=2).run(suite)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMeasureAllPayAuctionEffort)
        unittest.TextTestRunner(verbosity=2).run(suite)
