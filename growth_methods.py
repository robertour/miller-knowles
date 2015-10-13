import random

def growth_cra(sn):
    g = sn.g
    node_set = sn.node_set
    e_per_gen = sn.e_per_gen
    
    # this are the existent nodes before the growth process
    # miller's nodes doesn't attach to new nodes, that hasn't
    # play yet
    range_of_existent_nodes = range(len(node_set))        
     
            
    for i in range(sn.n_per_gen):
        
        # add the node to the network
        n_id = sn.add_node(random.choice(sn.__class__.strategies))
        
        # select the nodes to be connected with            
        selected = random.sample(range_of_existent_nodes,e_per_gen)
        
        # connect the node to e_per_gen nodes (edges)
        for node_index in selected:
      
            # add the edge
            g.add_edge(n_id, node_set[node_index])
            

def growth_epa(sn):
    f_of = sn.fitness_of
    ef = sn.eps_fitness     
    node = sn.g.node
    node_set = sn.node_set
    
    """
    Poncela et. al suggested to use an epsilon of 0.99. No reason is 
    given, but we assumed it is to avoid divisions by 0. However, this 
    is an unnecessary expensive calculation. We avoid this by using the
    __choice_r_index
    survival[f_of != -1] = 1 - 0.99 + \
                          0.99 * sn.fitness[f_of != -1]     
    survival /= sum(survival[f_of != -1])
    """
    g = sn.g
    n_per_gen = sn.n_per_gen
    e_per_gen = sn.e_per_gen
    total_efit = sn.total_efit
    
    for i in range(n_per_gen):
        
        # add the node to the network
        n_id = sn.add_node(random.choice(sn.__class__.strategies))
                  
        # keep the temporal nodes already selected
        temp_efitness = []
            
        # connect the node to e_per_gen nodes (edges)
        for e in range(e_per_gen):
            
            # pick a random value from 0 to max_fitness
            picked_value = random.uniform(0, total_efit)
                                
            # use the pick value to select a node to connect
            current_value = 0
            selected_node = -1
            for n in node_set:
                current_value += ef[node[n]['r_index']]
                if current_value > picked_value:
                    selected_node = n
                    r_index = node[n]['r_index']
                    break;
    
            # add the edge
            g.add_edge(n_id, selected_node)
            
            # temporarily store the r index and fitness values
            temp_efitness.append((r_index, ef[r_index]))
                            
            # reduce the fitness to 0 so the node won't be selected
            # again. also reduce the fitness
            total_efit -= ef[r_index]
            ef[r_index] = 0                
    
        # restore the fitness array after adding the edges
        for r_index, val in temp_efitness:
            ef[r_index] = val
            
        # restart the max sum
        total_efit = sn.total_efit


def growth_pa(sn):
    f_of = sn.fitness_of
    node_set = sn.node_set
    degrees = sn.degrees     
    node = sn.g.node
    g = sn.g
    n_per_gen = sn.n_per_gen
    e_per_gen = sn.e_per_gen
    total_degrees = sn.total_degrees
    
    for i in range(n_per_gen):
        
        # add the node to the network
        n_id = sn.add_node(random.choice(sn.__class__.strategies))
                  
        # keep the temporal nodes already selected
        temp_degrees = []
            
        # connect the node to e_per_gen nodes (edges)
        for e in range(e_per_gen):
            
            # pick a random value from 0 to max_fitness
            picked_value = random.uniform(0, total_degrees)
                                
            # use the pick value to select a node to connect
            current_value = 0
            selected_node = -1
            for n in node_set:
                current_value += degrees[node[n]['r_index']]
                if current_value > picked_value:
                    selected_node = n
                    r_index = node[n]['r_index']
                    break;
    
            if selected_node == -1:
                print ("this shouldn't ever happen")
                import ipdb; ipdb.set_trace()
                            
            # add the edge
            g.add_edge(n_id, selected_node)
            
            # temporarily store the r index and fitness values
            temp_degrees.append((r_index, degrees[r_index]))
                            
            # reduce the fitness to 0 so the node won't be selected
            # again. also reduce the fitness
            total_degrees -= degrees[r_index]
            degrees[r_index] = 0                
    
        # restore the fitness array after adding the edges
        for r_index, val in temp_degrees:
            degrees[r_index] = val
            
        # restart the max sum
        total_degrees = sn.total_degrees
