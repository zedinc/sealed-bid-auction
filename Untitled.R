highest_uniq <- function(x) {
  x <- sort(x, decreasing = TRUE)
  highest = 1
  if (x[1] == x[2]) {
    if (x[3] == x[4]) {
      return(-1)
    }
    else if (x[2] == x[3]) {
      highest = 4
    }
    else {
      highest = 3
    }
  }
  return(x[highest])
}

library(readr)
library(data.table)
library(ggplot2)

results <- read_csv("Contests/with_miserly_heurist.txt") # read in simulation results
results$bot <- as.factor(results$bot)
dt = as.data.table(results)

# dt[, winning_bid := .SD[bid==highest_uniq(bid)][1]$bid , by=.(auction,round), .SDcols=c("bid")]
dt[, c("winner","winning_bid") := .SD[bid==highest_uniq(bid)] , by=.(auction,round), .SDcols=c("bot","bid")]
dt[, won := ifelse(is.na(winner),FALSE,bot == winner) ,]
dt[, spent := ifelse(is.na(winner),0,bid*(bot==winner)), ]
dt[, net := 500*round - cumsum(spent), by=.(auction,bot), ]
dt[, net_start := 500 + c(0, net[1:length(net)-1]), by=.(auction,bot)]
dt[, ratio := bid/net_start, ]

competition_summary <- dt[ bot == winner , .(victories = .N, spend = sum(spent)) , by=.(winner) ][order(victories, decreasing = TRUE)]

winners_summary <- dt[ bot == winner , .(victories = .N, spend = sum(spent), avg_bid = mean(spent), min_bid = min(spent), max_bid = max(spent), std_dev_bid = sd(spent), avg_ratio = mean(spent/net_start) ) , by=.(winner,round) ]
winners_summary[round<=4, .(victories=sum(.SD$victories)), by=.(winner)][order(victories,decreasing = TRUE)]
winning_round_stats <- winners_summary[ , .SD[victories==max(victories)] , by=.(round) ]
winning_round_stats[, .( min=ceiling(unique(max(min_bid,avg_bid-2*std_dev_bid))), avg=ceiling(unique(avg_bid)), max=ceiling(unique(min(max_bid,avg_bid+2*std_dev_bid))), ratio=unique(avg_ratio) ), by=.(round) ]

winners <- dt[dt[,.I[bid==highest_uniq(bid)], by=.(auction,round)]$V1]

first_round <- dt[round == 1,.( average_bid = mean(bid), sd = sd(bid) ),by=.(round,bot)]
first_round_summary <- summary(factor(apply(combn(c(first_round$average_bid),4),2,FUN=highest_uniq)))
recommended_first_round_bid <- labels(first_round_summary[first_round_summary==max(first_round_summary)])

# Compare matchup between two bots ====

bot.a <- "heurist"
bot.b <- "AverageMine"
relevant_auctions <- dt[,.(relevant = any(bot==bot.a) & any(bot==bot.b)),by=.(auction)][relevant==TRUE]$auction
showdown.summary <- dt[auction %in% relevant_auctions, .(
  bot.a.bid = .SD[bot == bot.a]$bid,
  bot.b.bid = .SD[bot == bot.b]$bid,
  winning.bid = winning_bid[1],
  winner = winner[1]
), by = .(auction, round), .SDcols = c("bot", "bid", "winner")]
showdown.summary[winner %in% c(bot.a, bot.b), .(
  bot.a.wins = sum(winner == bot.a),
  bot.b.wins = sum(winner == bot.b),
  avg.a.win = mean(bot.a.bid[winner == bot.a]),
  avg.b.win = mean(bot.b.bid[winner == bot.b]),
  avg.a.loss = mean(bot.a.bid[winner != bot.a]),
  avg.b.loss = mean(bot.b.bid[winner != bot.b])
), by = .(round)][order(round)]

# Showdown plots ====
ggplot(showdown.summary[winner %in% c(bot.a, bot.b)], aes(x = as.factor(round))) + geom_histogram(stat="count") + facet_wrap( ~ winner )
ggplot(dt[bot %in% c(bot.a,bot.b)], aes(x = as.factor(bot), y = bid, color = (bot == winner))) + geom_violin() + facet_wrap( ~ as.factor(round) )

ggplot(showdown.summary[winner %in% c(bot.a,bot.b)], aes(x = bot.a.bid, y = bot.b.bid, color = (bot.a == winner))) + geom_point(alpha = 0.3, size = 3) + facet_wrap( ~ as.factor(round), nrow = 2, ncol = 5) + theme_bw()

