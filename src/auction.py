from dataclasses import dataclass
from functools import lru_cache
from math import ceil, comb

from src.utils import action_from_valuation_vector, perfectly_informed_action


@dataclass(frozen=True)
class Observation:
    time: int
    price: float
    player_bid: int
    opponent_bid: int


class AuctionUniformCase:

    def __init__(self, player_valuation_vector, opponent_valuation_vector, nb_opponents, m, p_init, delta_p, zmax):
        self.player_valuation_vector = player_valuation_vector
        self.opponent_valuation_vector = opponent_valuation_vector
        self.nb_opponents = nb_opponents
        self.m = m
        self.p_init = p_init
        self.delta_p = delta_p
        self.zmax = zmax
        self.r_barre = ceil((self.player_valuation(1) - self.p_init) / self.delta_p)

    def player_valuation(self, k):
        value = 0
        for i in range(k):
            value += self.player_valuation_vector[i]
        return value

    def phi_v_o0(self):
        max_value = 0

        for futur_player_bid in range(self.m + 1):
            r = 0

            for futur_opponent_bid in range(self.m + 1):
                new_observation = Observation(
                    time=1,
                    price=self.p_init + self.delta_p,
                    player_bid=futur_player_bid,
                    opponent_bid=futur_opponent_bid
                )

                r += (
                    self.proba_futur_opponent_bid(
                        futur_opponent_bid,
                        self.p_init + self.delta_p
                    )
                    * self.phi_v(new_observation)
                )

            max_value = max(r, max_value)

        return max_value

    def proba_futur_opponent_bid(self, futur_opponent_bid, futur_price):
        return (
            comb(self.m*self.nb_opponents, futur_opponent_bid)
            * (1 - futur_price / self.zmax) ** futur_opponent_bid
            * (futur_price / self.zmax) ** (
                self.m*self.nb_opponents - futur_opponent_bid
            )
        )

    @lru_cache(maxsize=None)
    def phi_v(self, observation):
        time = observation.time
        price = observation.price
        player_bid = observation.player_bid
        opponent_bid = observation.opponent_bid

        if time == self.r_barre:
            return 0

        if player_bid + opponent_bid <= self.m:
            return (
                self.player_valuation(player_bid)
                - player_bid * (price - self.delta_p)
            )

        max_value = 0

        for futur_player_bid in range(player_bid + 1):
            r = 0

            for futur_opponent_bid in range(opponent_bid + 1):
                new_observation = Observation(
                    time=time + 1,
                    price=price + self.delta_p,
                    player_bid=futur_player_bid,
                    opponent_bid=futur_opponent_bid
                )

                r += (
                    self.conditional_proba_futur_opponent_bid(
                        futur_opponent_bid,
                        price + self.delta_p,
                        opponent_bid,
                        price
                    )
                    * self.phi_v(new_observation)
                )

            max_value = max(r, max_value)

        return max_value

    def conditional_proba_futur_opponent_bid(
        self,
        futur_opponent_bid,
        futur_price,
        opponent_bid,
        price
    ):
        u = (self.zmax - futur_price) / (self.zmax - price)

        return (
            comb(opponent_bid, futur_opponent_bid)
            * u ** futur_opponent_bid
            * (1 - u) ** (opponent_bid - futur_opponent_bid)
        )

    def optimal_controle(self, t, k, delta, epsi):
        if t == 0:
            return self.__initial_optimal_controle(epsi)

        if t == self.r_barre:
            return -1

        if k + delta <= self.m:
            return -1

        max_value = 0
        i = 0

        for u in range(self.m + 1):
            r = 0

            for futur_opponent_bid in range(delta + 1):
                new_observation = Observation(
                    time=t + 1,
                    price=self.p_init + (t+1)*self.delta_p,
                    player_bid=u,
                    opponent_bid=futur_opponent_bid
                )

                r += (
                    self.conditional_proba_futur_opponent_bid(
                        futur_opponent_bid,
                        self.p_init + (t+1)*self.delta_p,
                        delta,
                        self.p_init + t*self.delta_p
                    )
                    * self.phi_v(new_observation)
                )

            if r > max_value + epsi:
                max_value = r
                i = u

        return i

    def __initial_optimal_controle(self, epsi):
        max_value = 0
        i = 0

        for u in range(self.m + 1):
            r = 0

            for futur_opponent_bid in range(self.m + 1):
                new_observation = Observation(
                    time=1,
                    price=self.p_init + self.delta_p,
                    player_bid=u,
                    opponent_bid=futur_opponent_bid
                )

                r += (
                    self.proba_futur_opponent_bid(
                        futur_opponent_bid,
                        self.p_init + self.delta_p
                    )
                    * self.phi_v(new_observation)
                )

            if r > max_value + epsi:
                max_value = r
                i = u

        return i

    def simulate_auction_bellman(self, epsi):
        time = 0
        price = self.p_init
        player_action = -1
        opponent_action = -1

        observation_sequance = []

        while time < self.r_barre:
            player_action = self.optimal_controle(time, player_action, opponent_action, epsi)
            opponent_action = action_from_valuation_vector(self.opponent_valuation_vector, price)
            observation_sequance.append((time, price, player_action, opponent_action))
            if player_action + opponent_action <= self.m:
                return (self.player_valuation(player_action) - player_action*price), observation_sequance
            time += 1
            price += self.delta_p

        return 0, observation_sequance

    def simulate_auction_SB(self, epsi):
        time = 0
        price = self.p_init
        player_action = -1
        opponent_action = -1

        observation_sequance = []

        while time < self.r_barre:
            player_action = action_from_valuation_vector(self.player_valuation_vector, price)
            opponent_action = action_from_valuation_vector(self.opponent_valuation_vector, price)
            observation_sequance.append((time, price, player_action, opponent_action))
            if player_action + opponent_action <= self.m:
                return (self.player_valuation(player_action) - player_action*price), observation_sequance
            time += 1
            price += self.delta_p

        return 0, observation_sequance

    def simulate_auction_perfectly_informed(self, epsi):
        time = 0
        price = self.p_init
        player_action = -1
        opponent_action = -1

        observation_sequance = []

        while time < self.r_barre:
            player_action = perfectly_informed_action(self.player_valuation_vector, self.opponent_valuation_vector, self.p_init, self.delta_p, self.m, epsi)
            opponent_action = action_from_valuation_vector(self.opponent_valuation_vector, price)
            observation_sequance.append((time, price, player_action, opponent_action))
            if player_action + opponent_action <= self.m:
                return (self.player_valuation(player_action) - player_action*price), observation_sequance
            time += 1
            price += self.delta_p

        return 0, observation_sequance
