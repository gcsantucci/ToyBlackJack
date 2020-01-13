# Toy BlackJack

Simulation of a BlackJack Toy Model. It follows the same idea as standard BlackJack,
but with simplified rules.
There is no splitting of pairs or doubling up bets, thus, the only
allowed plays are Stand or Hit.

## Simulated Players:

The class "Players" provide 3 different kinds of player plus the dealer,
each of them following a different strategy.

### Basic:
The Basic player always makes the same bet and follows a simple strategy
that takes into account the current value of the hand and the dealer's card that is public.
More details can be found here:     
https://bicyclecards.com/how-to-play/blackjack/

### Simplest Player:
There is also a Bad player simulation that will always make the same bet and
always follow the pattern:
1. If hand total >= 17: Stand
2. Else: Hit

### Chart Player:
And finally a player that follows the chart here:

https://www.blackjackapprenticeship.com/blackjack-strategy-charts/

### Dealer:
The dealer will always follow the steps:

1. If hand total > 17: Stand
2. If hand total < 17: Hit
3. If hand total = soft 17 (with an Ace): Hit
4. If hand total = hard 17 (without and Ace): Stand

## Payouts:
The payout is as follows:

1. If players have a BlackJack and the Dealer does not,
the players are awarded 1.5x their initial bets.
2. If the players beat the dealer without a BlackJack, they receive 1x their initial bets.
3. If the players bust (>21) or if the dealer wins, they lose their initial bets.
3. In case of a draw (BlackJack draw also), the initial bet is returned to each player.
