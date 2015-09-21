
class Game(object):
    
    def __init__(self, T, R, P, S, rewards):
        self.r = rewards
        
        self.T = T
        self.R = R
        self.P = P
        self.S = S

    def play(self):
        return 0;
    
    def play(self, p1, p2):
        r = self.r
        
        # update strategies after the loop has finished
        p1_e = p1['st'] = p1['nst']
        p2_e = p2['st'] = p2['nst']

        
        if p1_e == p2_e:
            if p1_e == 'C':
                r[p1['r_index']] += self.R
                r[p2['r_index']] += self.R
            else:
                r[p1['r_index']] += self.P
                r[p2['r_index']] += self.P
        else:
            if p1_e == 'C':
                r[p1['r_index']] += self.S
                r[p2['r_index']] += self.T
            else:
                r[p1['r_index']] += self.T
                r[p2['r_index']] += self.S
        

class PD (Game):
        
    def __init__(self, b, rewards):
        super(self.__class__,self).__init__(b,1,0,0,rewards)