from some_bots import * 

bot_list = [
    # zero_bot, all_in_bot, random_bot, average_bot, fortytwo_bot,
    above_average, I_Dont_Even, one_upper, copycat_or_sad,
    forgetful_bot, one_dollar_bob, distributer, half_in,
    meanie, patient_bot, escalating, AntiMaxer,
    AverageMine, Almost_All_In, BeatTheWinner,
    slow_starter, FiveFiveFive, Showoff, simple_bot,
    blacklist_mod, Graylist, below_average, bid_higher,
    HighHorse, minus_one, Wingman_1, wingman_2,
    average_joe, Swapper,
    #fill_bot,
    heurist 
    #  heurist_bot, 
]

import hashlib

def decide_order(ls):
    hash = int(hashlib.sha1(str(ls).encode()).hexdigest(), 16) % 24
    nls = []
    for i in range(4, 0, -1):
        nls.append(ls[hash % i])
        del ls[hash % i]
        hash //= i
    return nls

N = len(bot_list)
score = [0] * N
total = [0] * N
hist = []
auction_no = 0

def auction(ls):
    global score, total, auction_no
    auction_no += 1
    pl = decide_order(sorted(ls))
    bots = [bot_list[i]() for i in pl]
    # for bot in bots: print(bot.__class__.__name__)
    dollar = [0] * 4
    prev_win, prev_bid = -1, -1
    for rounds in range(10):
        # print(rounds)
        bids = []
        round = [auction_no]
        round.append(rounds)
        for i in range(4): dollar[i] += 500
        # print( *dollar, sep=', ')
        for i in range(4):
            entry = list(round)
            tmp_win = prev_win
            if prev_win == i: tmp_win = 0
            elif prev_win != -1 and prev_win < i: tmp_win += 1
            bid = int(bots[i].play_round(tmp_win, prev_bid))
            if bid < 0 or bid > dollar[i]: raise ValueError(pl[i])
            bids.append((bid, i))
            entry.append(bid)
            entry.append(bots[i].__class__.__name__)
            hist.append(entry)
        # print( *bidz, sep=', ')
        bids.sort(reverse = True)
        winner = 0
        if bids[0][0] == bids[1][0]:
            if bids[2][0] == bids[3][0]: winner = -1
            elif bids[1][0] == bids[2][0]: winner = 3
            else: winner = 2
        # print('Winner = %s, Bid = %d' % ( bots[bids[winner][1]].__class__.__name__, bids[winner][0] ))
        if winner == -1:
            prev_win, prev_bid = -1, -1
        else:
            prev_bid, prev_win = bids[winner]
            score[pl[prev_win]] += 1
            total[pl[prev_win]] += prev_bid
            dollar[prev_win] -= prev_bid
        # print( *dollar, sep=', ')
        # round.append(bids[winner][0])
        # round.append(bots[bids[winner][1]].__class__.__name__)
        # hist.append(round)

for a in range(N - 3):
    for b in range(a + 1, N - 2):
        for c in range(b + 1, N - 1):
            for d in range(c + 1, N): auction([a, b, c, d])

res = sorted(map(list, zip(score, total, bot_list)), key = lambda k: (-k[0], k[1]))

class TIE_REMOVED: pass

for i in range(N - 1):
    if (res[i][0], res[i][1]) == (res[i + 1][0], res[i + 1][1]):
        res[i][2] = res[i + 1][2] = TIE_REMOVED
# for sc, t, tp in res:
#     print('%-20s Score: %-6d Total: %d' % (tp.__name__, sc, t))

# print("auction,round,a,b,c,d,bot_a,bot_b,bot_c,bot_d,winning_bid,winner")
print("auction,round,bid,bot")
for auction_no, round, bid, bot in hist:
    print('%d, %d, %d, %s' % ( auction_no, (round+1), bid, bot ))
    # print('%d, %d, %d, %d, %d, %d, %s, %s, %s, %s, %d, %s' % ( auction_no, (round+1), a, b, c, d, bot_a, bot_b, bot_c, bot_d, winning_bid, winner ))
