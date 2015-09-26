from miller_knowles import SocialNetwork

GEN = 2000
POP = 1000
REP = 10
SAMPLE = 20

def run_one_attrition(sn):
    while (len(sn.g) < POP and sn.gen <= GEN):
        sn.play_games()
        sn.update_strategies()
        sn.growth()
    while (sn.gen <= GEN-SAMPLE):
        sn.play_games()
        sn.update_strategies()
        if(len(sn.g) < POP):
            sn.growth()
        else:
            sn.attrition()
    ave = 1.0
    while (sn.gen < GEN):
        sn.play_games()
        sn.update_strategies()
        if(len(sn.g) < POP):
            sn.growth()
        else:
            sn.attrition()
        ave += sn.count_coop() / (1.0 * len(sn.g))
    ave = ave / SAMPLE
    return ave

def run_one_no_attrition(sn):
    while (len(sn.g) < POP and sn.gen <= GEN):
        sn.play_games()
        sn.update_strategies()
        sn.growth()
    while (sn.gen <= GEN-SAMPLE):
        sn.play_games()
        sn.update_strategies()
    ave = 1.0
    while (sn.gen < GEN):
        sn.play_games()
        sn.update_strategies()
        ave += sn.count_coop() / (1.0 * len(sn.g))
    ave = ave / SAMPLE
    return ave
        

for i in range(REP):

    for b in [1.0,1.3,1.6,1.9,2.2,2.5,2.8]:

        sn = SocialNetwork(b=b,epsilon=0, max=POP)
        ave = run_one_attrition(sn)
        sn.print_results(i,"cra+",b,ave)

        sn = SocialNetwork(b=b, max=POP)
        ave = run_one_attrition(sn)
        sn.print_results(i,"epa+",b,ave)


        sn = SocialNetwork(b=b,epsilon=0, max=POP)
        ave = run_one_no_attrition(sn)
        sn.print_results(i,"cra", b,ave)
        
        sn = SocialNetwork(b=b, max=POP)
        ave = run_one_no_attrition(sn)
        sn.print_results(i,"epa", b,ave)



#sn.draw_random()
#sn.draw()