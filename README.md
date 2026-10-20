# Dynamic Programming for Clock Auctions

This project implements the clock auction model and bidding strategies described in J. Zeroual et al., *“Dynamic programming for optimal bidding strategies in clock auctions”*.

The objective is to implement the computational framework described in the paper, compute an optimal bidding strategy for a player using dynamic programming, and simulate auctions under the assumptions of the model.

The implementation considers opponents who follow a straightforward bidding strategy and whose marginal valuations are drawn from a uniform distribution. It also allows the results of different bidding strategies to be compared.

## 1. Auction model

### Clock auction mechanism

The auction allocates a fixed supply of \(m\) identical items among several bidders. The model is inspired by the French 5G spectrum auction, where bidders compete for spectrum blocks.

The auction proceeds in discrete rounds:

1. The price starts at an initial value \(p_{\mathrm{init}}\).
2. At each round, bidders choose how many items they wish to acquire at the current price.
3. If aggregate demand exceeds the available supply, the price increases by a fixed increment \(\Delta p\).
4. The process continues until total demand no longer exceeds supply, at which point the auction terminates.

Each bidder has a vector of marginal valuations. If bidder \(i\)'s marginal valuations are \(v_{i,1},\ldots,v_{i,m}\), their value for acquiring \(k\) items is

\[
V_i(k)=\sum_{j=1}^{k}v_{i,j},
\qquad V_i(0)=0.
\]

At price \(p\), the utility associated with demanding \(k\) items is

\[
U_i(k,p)=V_i(k)-kp.
\]

### Player valuations and opponent model

Each player is characterized by a vector of marginal valuations representing their willingness to pay for successive items.

In the uniform valuation model, marginal valuations are drawn from a uniform distribution on \([0,z_{\max}]\) and arranged in decreasing order. This ensures that the marginal value of an additional item does not exceed that of the preceding item.

The strategic player's valuation vector is generated using `uniforme_valuation_vector(zmax, m)`. The opponents' valuations are generated using `uniforme_valuation_vector(zmax, m, nb_opponents=nb_e - 1)`.

Once generated, valuations remain fixed throughout an auction. The uncertainty comes from the strategic player's lack of direct access to the opponents' valuations, rather than from valuations changing over time.

### Opponent bidding strategy

The opponents follow the **straightforward bidding (SB)** strategy. At each price \(p\), each opponent chooses the quantity that maximizes their current utility:

\[
\delta_i(p)\in
\underset{k\in\{0,\ldots,m\}}{\arg\max}
\left\{V_i(k)-kp\right\}.
\]

Their individual demands can be aggregated into a single total opponent demand. As the clock price increases, this aggregate demand generally decreases.

The strategic player observes the aggregate opponent demand but does not directly know the individual valuations that generated it. The dynamic programming algorithm uses the observed auction state and the probabilistic model of opponent demand to determine an optimal bidding decision.

This setup makes it possible to study how a strategic player can exploit the information revealed throughout the auction to improve its decisions against straightforward bidders.

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

The method

`optimal_controle(t, k, delta, epsi)`

computes the optimal control for a given auction state, according to the dynamic programming model implemented in the project.

The state contains information about the current round, the player's demand, and the observed aggregate demand of the opponents. The parameter `epsi` specifies the numerical tolerance used by the algorithm.

The method `simulate_auction_bellman(epsi)` simulates the auction using the dynamic programming strategy.

### Straightforward bidding

The method `simulate_auction_SB(epsi)` simulates the auction when the strategic player also follows straightforward bidding, choosing the quantity that maximizes its current utility at each price.

This provides a baseline for evaluating the benefits of strategic planning.

### Perfect-information benchmark

The method `simulate_auction_perfectly_informed(epsi)` simulates the auction under the perfect-information benchmark implemented in the project.

This benchmark provides a comparison with the strategies operating under incomplete information, helping assess the effect of uncertainty about opponents' valuations.

### Simulation outputs

The simulation methods return the resulting utility and auction sequence. These outputs can be used to compare the strategies in terms of their resulting payoffs and auction dynamics.

## 3. Example

For a complete example showing how to initialize an auction, compute an optimal bidding decision, and simulate the auction using the three strategies, see [`example.py`](example.py).
