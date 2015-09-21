from miller_knowles import SocialNetwork

GEN = 2000
POP = 1000
REP = 10

#1.6 is incomplete

for i in range(REP):

    for b in [2.2,2.5,2.8]:

        sn = SocialNetwork(b=b, max=POP)
        while (len(sn.g) < POP and sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
            sn.growth()
        while (sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
            if(len(sn.g) < POP):
                sn.growth()
            else:
                sn.attrition()
        sn.print_results(i,"epa+",b)

        sn = SocialNetwork(b=b,epsilon=0, max=POP)
        while (len(sn.g) < POP and sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
            sn.growth()
        while (sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
            if(len(sn.g) < POP):
                sn.growth()
            else:
                sn.attrition()
        sn.print_results(i,"cra+",b)

        
        sn = SocialNetwork(b=b, max=POP)
        while (len(sn.g) < POP and sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
            sn.growth()
        while (sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
        sn.print_results(i,"epa", b)

        sn = SocialNetwork(b=b,epsilon=0, max=POP)
        while (len(sn.g) < POP and sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
            sn.growth()
        while (sn.gen <= GEN):
            sn.play_games()
            sn.update_strategies()
        sn.print_results(i,"cra", b)




#sn.draw_random()
#sn.draw()