import unittest
from algtrd import AllPayAuction
import matplotlib.pylab as plt


class TestBiddingAllPayAuction(unittest.TestCase):
    def setUp(self):
        print()

    def test_scenario_1(self):
        self.name = "images/scenario1"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000, 1000, 1000]

    def test_scenario_2(self):
        self.name = "images/scenario2"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/2, 1000/2, 1000/2]

    def test_scenario_3(self):
        self.name = "images/scenario3"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/10, 1000/10, 1000/10]

    def test_scenario_4(self):
        self.name = "images/scenario4"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [100+i*10 for i in range(4)]

    def tearDown(self):
        for values in self.tests:
            au = AllPayAuction(values, self.budgets, random_start=False)

            x_values, plot_data = au.iterative_best_response()
            x_values = range(x_values)

            ax1 = plt.subplot2grid((2, 2), (0, 0))
            ax2 = plt.subplot2grid((2, 2), (0, 1))
            ax3 = plt.subplot2grid((2, 2), (1, 0))
            ax4 = plt.subplot2grid((2, 2), (1, 1))

            ax1.plot(x_values, plot_data[0], 'r')
            ax2.plot(x_values, plot_data[1], 'b')
            ax3.plot(x_values, plot_data[2], 'g')
            ax4.plot(x_values, plot_data[3], 'y')
            plt.savefig(self.name+"-0start-"+str(values)+'.png')


class TestMeasureAllPayAuctionEffort(unittest.TestCase):
    def setUp(self):
        print()

    def test_scenario_1(self):
        self.name = "images/scenario1"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000, 1000, 1000]

    def test_scenario_2(self):
        self.name = "images/scenario2"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/2, 1000/2, 1000/2]

    def test_scenario_3(self):
        self.name = "images/scenario3"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [1000, 1000/10, 1000/10, 1000/10]

    def test_scenario_4(self):
        self.name = "images/scenario4"
        self.tests = [(999, 1), (900, 100), (800, 200), (700, 300), (600, 400), (501, 499)]
        self.budgets = [100+i*10 for i in range(4)]

    def tearDown(self):
        x = []
        y1 = []
        y2 = []
        y3 = []
        ax1 = plt.subplot2grid((3, 1), (0, 0))
        ax2 = plt.subplot2grid((3, 1), (1, 0))
        ax3 = plt.subplot2grid((3, 1), (2, 0))
        for values in self.tests:
            au = AllPayAuction(values, self.budgets, random_start=False)

            y_max, y_avg, y_min = au.iterative_best_response(False)
            print(au.bids)
            x.append(abs(values[0] - values[1]))
            y1.append(y_max)
            y2.append(y_avg)
            y3.append(y_min)

        ax1.plot(x, y1, 'r')
        ax2.plot(x, y2, 'b')
        ax3.plot(x, y3, 'g')

        plt.savefig(self.name+"-effort.png")



if __name__ == "__main__":
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestBiddingAllPayAuction)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMeasureAllPayAuctionEffort)
    unittest.TextTestRunner(verbosity=2).run(suite)
