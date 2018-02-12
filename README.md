## All Pay Auction

University project for the algorithmic trading class. I was tasked with creating a simple version of an All pay second price auction. This auction is implemented over an Iterative Best Response where each bidder looks at each others bids and decides his own best choice for the next turn.

### Requirements

```bash
pip install -r requirements.txt
```

### Help

Simply running the following command in the terminal presents the help menu:
```bash
python algtrd.py -h
```


### Examples

You can simply run the example experiment in example.json by using the following
command:

```bash
python algtrd.py -d example.json
```

Or you can run every experiment in the experiments folder by using the following
command:

```bash
python algtrd.py -d experiments
```

You are going to notice two new directories showing up images/ and results/ .

Results has a json with the average price ("effort") history during each iteration and the results of the auction ("final_bids").

Inside the images there are the graphs indicating the average effort over each iteration.
