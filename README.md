# Dynamic Programming for Clock Auctions

This project implements the clock auction model and bidding strategies described in J. Zeroual et al., *“Dynamic programming for optimal bidding strategies in clock auctions”*.

The objective is to implement the computational framework described in the paper, compute an optimal bidding strategy for a strategic player using dynamic programming, and simulate auctions under the assumptions of the model.

The implementation considers opponents who follow a straightforward bidding strategy and whose marginal valuations are drawn from a uniform distribution.

## 1. Auction model

### Clock auction mechanism

The auction allocates a fixed supply of `m` identical items among several bidders. The model is inspired by the French 5G spectrum auction.

The auction proceeds in discrete rounds:

1. The price starts at an initial value, `p_init`.
2. At each round, bidders choose how many items they wish to acquire at the current price.
3. If aggregate demand exceeds the available supply, the price increases by a fixed increment, `delta_p`.
4. The process continues until total demand no longer exceeds supply, at which point the auction terminates.

Each bidder has a marginal valuation vector. For bidder \(i\), let \(v_{i,j}\) denote the marginal valuation of item \(j\). Their total value for acquiring \(k\) items is

$$
\Large
V_i(k)=\sum_{j=1}^{k}v_{i,j},
\qquad V_i(0)=0.
$$

At price \(p\), the utility associated with demanding \(k\) items is

$$
\Large
U_i(k,p)=V_i(k)-kp.
$$

### Opponent valuation assumptions

The model makes specific assumptions about the opponents' valuations and behavior.

Each opponent's marginal valuations are drawn from a uniform distribution on the interval \([0,z_{\max}]\). The sampled marginal valuations are arranged in decreasing order, so that the marginal value of an additional item does not exceed that of the preceding item.

For each opponent \(i\), the marginal valuations satisfy

$$
\Large
v_{i,1}\geq v_{i,2}\geq\cdots\geq v_{i,m}.
$$

Once sampled, the valuations remain fixed throughout the auction.

The strategic player does not directly observe the opponents' valuation vectors. It observes their aggregate demand during the auction and uses this information to make its own bidding decisions.

### Opponent bidding strategy

All opponents follow the **straightforward bidding (SB)** strategy. At each price \(p\), opponent \(i\) demands a quantity that maximizes their current utility:

$$
\Large
\delta_i(p)\in
\underset{k\in\{0,\ldots,m\}}{\arg\max}
\left\{V_i(k)-kp\right\}.
$$

The total demand of the opponents is the sum of their individual demands:

$$
\Large
\Delta(p)=\sum_{i=1}^{n-1}\delta_i(p),
$$

where \(n\) is the total number of bidders, including the strategic player.

The strategic player observes this aggregate demand but does not know the individual valuations that generated it. The dynamic programming algorithm uses the observed auction state and the probabilistic model of opponent demand to determine its optimal bidding decisions.

The strategic player's valuation vector is supplied separately to the auction model; the uniform-distribution assumption above describes the opponents' valuations.

The model is inspired by the French 5G spectrum auction but is a simplified computational model, not a full reproduction of the official auction rules.

## 2. Implemented functionalities

### Auction initialization

The `AuctionUniformCase` class initializes an auction using:

- The strategic player's marginal valuations.
- The opponents' marginal valuations.
- The number of opponents.
- The available supply.
- The initial price and price increment.
- The upper bound on marginal valuations.

### Optimal bidding using dynamic programming

The method `optimal_controle(t, k, delta, epsi)` computes the optimal control for a given auction state, according to the dynamic programming model implemented in the project.

The state describes the current round, the strategic player's demand, and the observed aggregate demand of the opponents. The parameter `epsi` specifies the numerical tolerance used by the algorithm.

The method `simulate_auction_bellman(epsi)` simulates the auction using the dynamic programming strategy.

### Straightforward bidding

The method `simulate_auction_SB(epsi)` simulates the auction when the strategic player also follows straightforward bidding, choosing the quantity that maximizes its current utility at each price.

This provides a baseline for evaluating the benefits of strategic planning.

### Perfect-information benchmark

The method `simulate_auction_perfectly_informed(epsi)` simulates the auction under the perfect-information benchmark implemented in the project.

This benchmark allows comparison with strategies operating under incomplete information and helps illustrate the effect of uncertainty about opponents' valuations.

### Simulation outputs

The simulation methods return the resulting utility and auction sequence. These outputs can be used to compare the strategies in terms of their resulting payoffs and auction dynamics.

## 3. Example

For a complete example showing how to initialize an auction, compute an optimal bidding decision, and simulate the auction using the three strategies, see [`example.py`](example.py).
