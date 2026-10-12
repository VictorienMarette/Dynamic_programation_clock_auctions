from random import uniform


def uniforme_valuation_vector(zmax, m, nb_opponents=1):
    Z = []
    for j in range(m*nb_opponents):
        Z.append(zmax * uniform(0, 1))
    Z.sort(reverse=True)
    return Z


def action_from_valuation_vector(valuation_vector, price):
    i = 0
    while i < len(valuation_vector) and valuation_vector[i] > price:
        i += 1
    return i


def valuation_from_vector(valuation_vector, price, k):
    v = 0
    for i in range(k):
        v += valuation_vector[i]
    return v - price*k


def perfectly_informed_action(player_valuation_vector, opponent_valuation_vector, p_init, delta_p, m, epsi):
    max_value = 0
    i = 0

    for k in range(m + 1):
        pk = p_init
        while action_from_valuation_vector(opponent_valuation_vector, pk) + k > m:
            pk += delta_p

        v = valuation_from_vector(player_valuation_vector, pk, k)
        if v > max_value + epsi:
            max_value = v
            i = k

    return i
