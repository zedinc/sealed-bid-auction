# Sealed Bid Auction

This culminated in my [first ever Python3 entry](https://codegolf.stackexchange.com/a/148708/2771) for a King-of-the-Hill competition on codegolf.SE, where I placed a respectable 5th out of 33.

The overall winner adopted a similar strategy in which they hard-coded the bids for each round.

## Competition Rules

From the [original post](https://codegolf.stackexchange.com/q/147576/2771)

> In this game, we will simulate a sealed-bid auction.
  
>  Each auction is a 4-player game, consists of 10 rounds. Initially, players have no money. At the start of each round, each player will get $500, and then make their own bids. The bid can be any non-negative integer less or equal than the amount they have. Usually, one who bid the highest win the round. However, to make things more interesting, if several players bid the same price, their bid won't be taken into account (thus can't win the round). For example, if four players bid 400 400 300 200, the one bids 300 wins; if they bid 400 400 300 300, no one wins. The winner should pay what they bid.
  
>  Since it is a "sealed-bid" auction, the only information player will know about the bidding is the winner and how much they paid when next round starts (so player can know how much everyone has).

## My Approach

I went down a probabilistic route, in which I simulated in the competition all available bots in order to ascertain statistical bounds on the winning bids for each round.

`RStudio`, `data.table` and `ggplot2` made light work of the analysis :)
