from src.auction import AuctionUniformCase, Observation
from src.utils import action_from_valuation_vector, uniforme_valuation_vector
import pickle


# Parameters
m = 11
p_init = 70
delta_p = 3
nb_e = 4

N = 1000
epsi = 0.0001

data = {}

for zmax in [110, 121, 132, 143, 154, 165]:
    print(zmax)
    print("")

    u_informed = 0
    u_bellman = 0
    u_sb = 0
    u_b_over_u_i = 0
    u_sb_over_u_i = 0
    compt_sb_eq_i = 0

    for n in range(N):
        player_valuation_vector = uniforme_valuation_vector(zmax, m)
        opponent_valuation_vector = uniforme_valuation_vector(zmax, m, nb_opponents=nb_e-1)
        V = AuctionUniformCase(player_valuation_vector, opponent_valuation_vector, nb_e - 1, m, p_init, delta_p, zmax)
        v_b, seq_b = V.simulate_auction_bellman(0.0001)
        v_sb, _ = V.simulate_auction_SB(0.0001)
        v_i, seq_i = V.simulate_auction_perfectly_informed(0.0001)

        if v_i != 0:
            u_informed += v_i
            u_bellman += v_b
            u_sb += v_sb
            u_b_over_u_i += v_b/v_i
            u_sb_over_u_i += v_sb/v_i

        if v_i - v_b <= epsi:
            compt_sb_eq_i += 1


    data[zmax] = [u_informed/N, u_bellman/N, u_sb/N, u_b_over_u_i/N, u_sb_over_u_i/N, compt_sb_eq_i/N]

# Sauvegarder
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Recharger plus tard
with open("data.pkl", "rb") as f:
    data = pickle.load(f)
