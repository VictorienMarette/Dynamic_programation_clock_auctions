from src.auction import AuctionUniformCase
from src.utils import uniforme_valuation_vector

# French 5G spectrum clock auction
m = 11
p_init = 70
delta_p = 3
nb_e = 4
zmax = 132
epsi = 1e-4

# Generate marginal valuations
player_values = uniforme_valuation_vector(zmax, m)
opponent_values = uniforme_valuation_vector(
    zmax, m, nb_opponents=nb_e - 1
)

# Initialize the auction
auction = AuctionUniformCase(
    player_values,
    opponent_values,
    nb_e - 1,
    m,
    p_init,
    delta_p,
    zmax,
)

# Compute the optimal bid at the initial state
t = 0
k = m
delta = None  # Initial aggregate opponent demand, according to the implementation
optimal_bid = auction.optimal_controle(t, k, delta, epsi)

# Simulate the auction with the three strategies
utility_optimal, sequence_optimal = auction.simulate_auction_bellman(epsi)
utility_sb, sequence_sb = auction.simulate_auction_SB(epsi)
utility_informed, sequence_informed = auction.simulate_auction_perfectly_informed(epsi)
