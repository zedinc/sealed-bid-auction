class one_dollar_bob:
  def play_round(x,y,z):
    return 1

class forgetful_bot:
  def play_round(self, winner, amt):
    return 500

class patient_bot:
    def __init__(self):
        self.round = 0
        self.money = 0
    def rand(self, seed, max):
        return (394587485 - self.money*self.round*seed) % (max + 1)
    def play_round(self, winner, amount):
        self.round += 1
        self.money += 500
        if winner == 0:
            self.money -= amount
        if self.round < 6:
            return 0
        else:
            bid = 980 + self.rand(amount, 35)
            if self.money < bid or self.round == 10:
                bid = self.money
            return bid

class above_average:
  def __init__(self):
    self.round = 0
    self.player_money = [0] * 4
  def play_round(self, winner, winning_bid):
    self.round += 1
    self.player_money = [x+500 for x in self.player_money]
    if winner != -1:
      self.player_money[winner] -= winning_bid
    if self.round == 10:
      return self.player_money[0]
    bid = sum(self.player_money[1:]) / 3 + 1
    if bid > self.player_money[0]:
      return self.player_money[0]
    return min(self.player_money[0], bid)

class I_Dont_Even:
	def __init__(self):
		self.money = 0
		self.round = 0
	def play_round(self, loser, bid):
		self.money += 500 - (not loser) * bid
		self.round += 1
		return self.money * (self.round & 1 or self.round == 10)

class one_upper:
    def __init__(self): 
        self.money = 0
        self.round = 0
    def play_round(self, winner, win_amount):
        self.money += 500
        if winner == 0: self.money -= win_amount
        self.round += 1
        bid = win_amount + 1
        if self.money < bid or self.round == 10:
            bid = self.money
        return bid

class half_in:
  def __init__(self):
    self.money = 0
    self.round = -1
  def play_round(self, winner, win_amount):
    # Default actions:
    #  Collect 500 dollars
    self.money += 500
    #  If it was the winner: subtract the win_amount from his money
    if winner == 0:
      self.money -= win_amount
    #  One round further
    self.round += 1

    # If it's the final round: bid all in
    if self.round == 9:
      return self.money
    # Else: Bid half what it has left:
    return self.money / 2

class slow_starter:
  def __init__(self):
    self.money = 0
    self.round = -1
  def play_round(self, winner, win_amount):
    # Default actions:
    #  Collect 500 dollars
    self.money += 500
    #  If it was the winner: subtract the win_amount from his money
    if winner == 0:
      self.money -= win_amount
    #  One round further
    self.round += 1

    # If it's the final round or if it doesn't have enough money left: bid all in
    if self.round == 9 or self.round * 200 > self.money:
      return self.money
    # Else: bid 200 multiplied with the current round we're playing
    #  (Note: It bids 0 the first round)
    return self.round * 200

class copycat_or_sad:
  def __init__(self):
    self.money = 0
    self.round = -1
  def play_round(self, winner, win_amount):
    # Default actions:
    #  Collect 500 dollars
    self.money += 500
    #  If it was the winner: subtract the win_amount from his money
    if winner == 0:
      self.money -= win_amount
    #  One round further
    self.round += 1

    # If it's the final round: bid all-in
    if self.round == 9:
      return self.money
    # Else-if there was no previous winner, or it doesn't have enough money left: bid 1
    if win_amount < 1 or self.money < win_amount:
      return 1
    # Else: bid the exact same as the previous winner
    return win_amount

class distributer:
  def __init__(self):
    self.money = 0
    self.rounds = 11
  def play_round(self, winner, amt):
    self.money += 500
    self.rounds -= 1
    if self.rounds == 10:
      return 499
    if winner == 0:
      self.money -= amt
    return ((self.rounds - 1) * 500 + self.money) / self.rounds

class meanie:
    def __init__(self):
        self.money = [0] * 4
        self.rounds = 11
        self.total_spent = 0

    def play_round(self,winner,winning_bid):
        self.money = [x+500 for x in self.money]
        self.rounds -= 1
        if winner != -1:
            self.money[winner] -= winning_bid
            self.total_spent += winning_bid
        bid = 500
        if self.rounds > 0 and self.total_spent < 20000:
            bid = int((20000 - self.total_spent)/self.rounds/4)+1
        return min(bid,max(self.money[1:])+1,self.money[0])

class Showoff:
  def __init__(self):
      self.moneys = [0, 0, 0]
      self.roundsLeft = 10
  def play_round(self, winner, winning_bid):
      import math
      self.moneys = [self.moneys[0] + 500,
                     self.moneys[1] + 1500,
                     self.moneys[2] + 1500]
      self.roundsLeft -= 1
      if winner > 0:
          self.moneys[1] -= winning_bid
      if winner == 0:
          self.moneys[0] -= winning_bid
      if self.roundsLeft == 0:
          return self.moneys[0]
      ratio = self.moneys[1] / self.moneys[2]
      logisticized = (1 + (math.e ** (-8 * (ratio - 0.5)))) ** -1
      return math.floor(self.moneys[0] * logisticized)

class escalating:
  def __init__(self):
    self.money = 0
    self.round = 0
  def play_round(self, winner, win_amount):
    # Default actions:
    #  Collect 500 dollars
    self.money += 500
    #  If it was the winner: subtract the win_amount from his money
    if winner == 0:
      self.money -= win_amount
    #  One round further
    self.round += 1

    # bid round number in percent times remaining money, floored to integer
    return self.money * self.round // 10

class FiveFiveFive:
    nplayers = 4
    maxrounds = 10
    def __init__(self):
        self.money = [0] * self.nplayers
        self.wins = [0] * self.nplayers
        self.round = 0

    def play_round(self, winner, win_amt):
        self.round += 1
        for i in range(self.nplayers):
            self.money[i] += 500
            if i == winner:
                self.money[i] -= win_amt
                self.wins[i] += 1
        if self.round == 1:
            return 0
        elif self.round < self.maxrounds:
            return min(555, self.money[0])
        else:
            bid = self.money[0]
            return bid if self.money.count(bid) < 3 else bid-1

class AntiMaxer:
    nplayers = 4
    maxrounds = 10
    def __init__(self):
        self.money = [0] * self.nplayers
        self.wins = [0] * self.nplayers
        self.round = 0

    def play_round(self, winner, win_amt):
        self.round += 1
        for i in range(self.nplayers):
            self.money[i] += 500
            if i == winner:
                self.money[i] -= win_amt
                self.wins[i] += 1
        return max((m for m in self.money[1:] if m<=self.money[0]),
                   default=0)

class Almost_All_In:
	def __init__(self):
		self.money = 0
		self.round = 0
	def play_round(self, loser, bid):
		self.money += 500 - (not loser) * bid
		self.round += 1
		return self.money - self.round % 3 * 3 - 3

class BeatTheWinner:
    nplayers = 4
    maxrounds = 10
    def __init__(self):
        self.money = [0] * self.nplayers
        self.wins = [0] * self.nplayers
        self.round = 0

    def play_round(self, winner, win_amt):
        self.round += 1
        for i in range(self.nplayers):
            self.money[i] += 500
            if i == winner:
                self.money[i] -= win_amt
                self.wins[i] += 1
        mymoney = self.money[0]
        for w,m in sorted(zip(self.wins, self.money),reverse=True):
            if mymoney > m:
                return m+1
        #if we get here we can't afford our default strategy, so
        return int(mymoney/10)

class AverageMine:
    nplayers = 4
    maxrounds = 10
    def __init__(self):
        self.money = [0] * self.nplayers
        self.wins = [0] * self.nplayers
        self.round = 0
        self.average = 0
    def play_round(self, winner, win_amt):
        self.round += 1
        for i in range(self.nplayers):
            if i == winner:
                self.average = (self.average * (self.round - 2) + (win_amt / self.money[i])) / (self.round - 1)
                self.money[i] -= win_amt
                self.wins[i] += 1
            self.money[i] += 500
        if self.round == 1:
            return int(0.991 * self.money[0])
        elif self.round < self.maxrounds:
            if self.money[0] > self.money[1] + 1 and self.money[0] > self.money[2] + 1 and self.money[0] > self.money[3] + 1:
                return max(self.money[1],self.money[2],self.money[3]) + 1
            bid = int(self.average * self.money[0]) + max(self.round - 4,4 - self.round)
            return min(self.money[0],bid)
        else:
            bid = self.money[0]
            return bid

class simple_bot:
    def __init__(self):
        self.round = 0
        self.money = 0
    def rand(self, seed, max):
        return (394587485 - self.money*self.round*seed) % (max + 1)
    def play_round(self, winner, amount):
        self.round += 1
        self.money += 500
        if winner == 0:
            self.money -= amount
        bid = 980 + self.rand(amount, 135)
        if self.money < bid or self.round == 10:
            bid = self.money
        return bid

class below_average:
  def __init__(self):
    self.round = 0
    self.player_money = [0] * 4
  def play_round(self, winner, winning_bid):
    self.round += 1
    self.player_money = [x+500 for x in self.player_money]
    if winner != -1:
      self.player_money[winner] -= winning_bid
    if self.round == 10:
      return self.player_money[0]
    bid = sum(self.player_money[1:]) / 3 - 2
    if bid > self.player_money[0]:
      return self.player_money[0]
    return min(self.player_money[0], bid)

class blacklist_mod:
  def __init__(self):
    self.round = 0
    self.player_money = [0] * 4
    self.blacklist = {0, 499}
  def play_round(self, winner, winning_bid):
    self.round += 1
    self.player_money = [x+500 for x in self.player_money]
    if winner != -1:
      self.player_money[winner] -= winning_bid
      self.blacklist.add(winning_bid % 500)
      self.blacklist |= {x % 500 for x in self.player_money[1:]}
    tentative_bid = self.player_money[0]
    autowin = max(self.player_money[1:])+1
    if tentative_bid < autowin:
      while tentative_bid and (tentative_bid % 500) in self.blacklist:
        tentative_bid = tentative_bid - 1
    else:
      tentative_bid = autowin
    self.blacklist.add(tentative_bid % 500)
    return tentative_bid

class Graylist:
  def __init__(self):
    self.round = 0
    self.player_money = [0] * 4
    self.ratios = {1}
    self.diffs = {0}
  def play_round(self, winner, winning_bid):
    self.round += 1
    if winner != -1:
      if winner >0 and winning_bid>0:
        self.ratios.add(self.player_money[winner]/winning_bid)
        self.diffs.add(self.player_money[winner]-winning_bid)
      self.player_money[winner] -= winning_bid
    self.player_money = [x+500 for x in self.player_money]
    tentative_bid = min(self.player_money[0],max(self.player_money[1:])+1, winning_bid+169, sum(self.player_money[1:])//3+169)
    while tentative_bid and (tentative_bid in (round(m*r) for m in self.player_money[1:] for r in self.ratios)) or (tentative_bid in (m-d for m in self.player_money[1:] for d in self.diffs)):
      tentative_bid = tentative_bid - 1
    return tentative_bid

class bid_higher:
    def __init__(self):
        self.dollar = 0
        self.round = 0
    def play_round(self, winner, win_amount):
        self.dollar += 500
        self.round += 1
        inc = 131
        if winner == 0: self.dollar -= win_amount
        if self.round == 10: return self.dollar
        if win_amount == 0: win_amount = 500
        if self.dollar > (win_amount + inc):
            return win_amount + inc
        else:
            if self.dollar > 1:
                return self.dollar -1
            else:
                return 0

class HighHorse:
    maxrounds = 10
    def __init__(self):
        self.money = 0
        self.round = 0
    def play_round(self, winner, win_amt):
        self.round += 1
        if 0 == winner:
            self.money -= win_amt
        self.money += 500
        if self.round < self.maxrounds:
            return self.money - self.round
        else:
            bid = self.money
            return bid

class minus_one:
    def __init__(self):
        self.money = 0
    def play_round(self, winner, amount):
        self.money += 500
        if winner == 0:
            self.money -= amount
        return self.money - 1

class Wingman_1:
    def __init__(self):
        self.dollar = 0
        self.round = 0
    def play_round(self, winner, win_amount):
        self.dollar += 500
        self.round += 1
        inc = 130
        if win_amount == 0: win_amount = 500
        if winner == 0: self.dollar -= win_amount
        if self.round == 10: return self.dollar
        if self.dollar > win_amount + inc:
            return win_amount + inc
        else:
            if self.dollar > 1: return self.dollar -1
            else:
                return 0

class wingman_2:
    def __init__(self):
        self.dollar = 0
        self.round = 0
    def play_round(self, winner, win_amount):
        self.round += 1
        self.dollar += 500
        inc = 129
        if win_amount == 0: win_amount = 500
        if winner == 0: self.dollar -= win_amount
        if self.round == 10: return self.dollar
        if self.dollar > win_amount + inc:
            return win_amount + inc
        else:
            if self.dollar > 1: return self.dollar -1
            else:
                return 0

MONEY_PER_ROUND = 500
NUM_ROUNDS = 10

class Random:
    def __init__(self, seed):
        self.val = seed
    def randint(self, a, b):
        self.val = (self.val * 6364136223846793005 + 1) % (1 << 64)
        return (self.val >> 32) % (b - a + 1) + a
    def choice(self, arr):
        return arr[self.randint(0,len(arr)-1)]

class average_joe:
    running_sum = 0

    def __init__(self):
        self.random = Random(42)

    def play_round(self, winner, winning_bid):
        if winner == -1 and winning_bid == -1:
            self.tracker = Tracker()
            self.tracker.next_round(money=MONEY_PER_ROUND)
            return 475
        else:
            self.tracker.next_round(money = MONEY_PER_ROUND)
            self.tracker.update_balance(winner, winning_bid)
            self.running_sum += winning_bid
            if self.tracker.rounds == NUM_ROUNDS:
                balance = self.tracker.get_balance(0)
                return balance
            else:
                strategy = self.random.choice([self.beat_mean_history, self.beat_mean_balance])
                return strategy()

    def beat_mean_history(self):
        mean = self.running_sum // self.tracker.rounds
        return max(min(mean + 2, self.tracker.get_balance(0)),0)

    def beat_mean_balance(self):
        mean = self.tracker.get_average_balance()
        return max(min(mean+2, self.tracker.get_balance(0)),0)

# Tracker utility class
class Tracker:
    def __init__(self):
        self.rounds = 0
        self.player_balance = dict.fromkeys(range(4), 0)

    def get_values(self):
        return [self.player_balance[player] for player in self.player_balance.keys()]

    def next_round(self, money=500):
        self.rounds += 1
        for player in self.player_balance.keys():
            self.player_balance[player] += money

    def get_balance(self, player):
        return self.player_balance[player]

    def update_balance(self, player, expense):
        self.player_balance[player] -= expense

    def get_average_balance(self):
        values = self.get_values()[1:]
        return round(sum(values) / len(values))

class Swapper:
    def __init__(self):
        self.money = 0
        self.round = 0
    def play_round(self, loser, bid):
        self.money += 500 - (not loser) * bid
        self.round += 1
        if self.round & 1:
            return self.money - 1
        return self.money

class heurist:
    def __init__(self):
        self.money = 0
        self.round = -1
        self.net_worth = [0] * 4
    def play_round(self, winner, bid):
        self.round += 1
        self.money += 500
        if winner == 0: self.money -= bid
        if winner != -1: self.net_worth[winner] -= bid
        self.net_worth = [x+500 for x in self.net_worth]
        max_bid = [498,1000,1223,1391,1250,1921,2511,1666,1600,5000][self.round]
        if self.money > max_bid:
            return 1 + min(max_bid,max(self.net_worth[1:3]))
        else:
            return self.money
