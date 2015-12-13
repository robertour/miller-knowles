import random
from sortedcontainers import SortedSet, SortedDict


# each certain amount of generations there is an attack to the elite 
def tournament_least_fit(sn):  
    f_of = sn.fitness_of
    f = sn.fitness
    node_set = sn.node_set
    g = sn.g
    
    winners = []
    for i in range(round(sn.size*sn.X)):

        # avoid repetitions randomly select the participants
        tombola = random.sample(node_set,round(sn.size*sn.tourn))

        # search for the "winners" (or really "losers")
        min_fit = float("inf")
        ties = []
        for t in tombola:
            cur_fit = f[g.node[t]['r_index']]
            if cur_fit < min_fit:
                min_fit = cur_fit
                ties=[t]
            elif cur_fit == min_fit:
                ties.append(t)

        # in case of tie, select one randomly
        w = random.choice(ties)
        winners.append(w)
        # we already know this node won't exist,
        # so we can remove it forever
        f_of[g.node[w]['r_index']] = -1
        node_set.discard(w)
    
    return winners
    
        
def tournament_fittest2(sn):
        f_of = sn.fitness_of
        f = sn.fitness
        node_set = sn.node_set
        g = sn.g
        
        winners = []
         
        for i in range(round(sn.size*sn.X2)):

            # avoid repetitions randomly select the participants
            tombola = random.sample(node_set,round(sn.size*sn.tourn))
    
            # search for the "winners" (or really "losers")
            max_fit = -1
            ties = []
            for t in tombola:
                cur_fit = f[g.node[t]['r_index']]
                if cur_fit > max_fit:
                    max_fit = cur_fit
                    ties=[t]
                elif cur_fit == max_fit:
                    ties.append(t)
    
            # in case of tie, select one randomly
            w = random.choice(ties)
            winners.append(w)
            # we already know this node won't exist,
            # so we can remove it forever
            f_of[g.node[w]['r_index']] = -1
            node_set.discard(w)

        return winners

def tournament_fittest(sn):
    f_of = sn.fitness_of
    f = sn.fitness
    node_set = sn.node_set
    g = sn.g
    
    winners = []
    for i in range(round(sn.size*sn.X)):

        # avoid repetitions randomly select the participants
        tombola = random.sample(node_set,round(sn.size*sn.tourn))

        # search for the "winners" (or really "losers")
        max_fit = -1
        ties = []
        for t in tombola:
            cur_fit = f[g.node[t]['r_index']]
            if cur_fit > max_fit:
                max_fit = cur_fit
                ties=[t]
            elif cur_fit == max_fit:
                ties.append(t)

        # in case of tie, select one randomly
        w = random.choice(ties)
        winners.append(w)
        # we already know this node won't exist,
        # so we can remove it forever
        f_of[g.node[w]['r_index']] = -1
        node_set.discard(w)

    return winners


def at_random(sn):
    return random.sample(sn.node_set,round(sn.size*sn.X))


def least_fit(sn):  
    f_of = sn.fitness_of
    f = sn.fitness
    node_set = sn.node_set
    g = sn.g
    
    sorted_fit = SortedDict()
    for i in range(sn._max):
        if f_of[i] != -1:
            if f[i] in sorted_fit:
                sorted_fit[f[i]].append(f_of[i])
            else:
                sorted_fit[f[i]] = [f_of[i]]

    shrink_size = round(sn.size*sn.X)
    winners = []
    for key in iter(sorted_fit):
        value = sorted_fit[key]
        if len(value) + len(winners) < shrink_size:
            winners.extend(value) 
        elif len(value) + len(winners) == shrink_size:
            winners.extend(value)
            break
        else:
            for v in value:
                winners.append(v)
                if len(winners) == shrink_size:
                    break
            break
    
    return winners


def fittest(sn):  
    f_of = sn.fitness_of
    f = sn.fitness
    node_set = sn.node_set
    g = sn.g
    
    sorted_fit = SortedDict()
    for i in range(sn._max):
        if f_of[i] != -1:
            if f[i] in sorted_fit:
                sorted_fit[f[i]].append(f_of[i])
            else:
                sorted_fit[f[i]] = [f_of[i]]

    shrink_size = round(sn.size*sn.X)
    winners = []
    for key in reversed(sorted_fit):
        value = sorted_fit[key]
        if len(value) + len(winners) < shrink_size:
            winners.extend(value) 
        elif len(value) + len(winners) == shrink_size:
            winners.extend(value)
            break
        else:
            for v in value:
                winners.append(v)
                if len(winners) == shrink_size:
                    break
            break
        
    return winners
