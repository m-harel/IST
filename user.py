import Block
import Mean

class user:
    def __init__(self,id):
        self.id = id
        self.neutral_S = Mean.Mean() #switch
        self.neutral_NS = Mean.Mean()  #no switch

        self.emotional_NN = Mean.Mean()
        self.emotional_NE = Mean.Mean()
        self.emotional_EN = Mean.Mean()
        self.emotional_EE = Mean.Mean()
        self.emotional_S = Mean.Mean() #switch
        self.emotional_NS = Mean.Mean() #no switch
        self.blocks = []

    def addTrail(self, trail):
        if(trail.isDummy()):
            self.blocks.append(Block.Block(self.id, len(self.blocks) + 1, trail.type))
        self.blocks[-1].addTrail(trail)

    def getStandradMeans(self,standard):
        for block in self.blocks:
            for trail in block.trials:
                if(trail.standard < standard):
                    if(trail.type == '1'):
                        if(trail.category == 'Neut'):
                            if(trail.lastCategory == 'Neut'):
                                self.emotional_NN.add(trail.timing)
                                self.emotional_NS.add(trail.timing)
                            else:
                                self.emotional_NE.add(trail.timing)
                                self.emotional_S.add(trail.timing)
                        else:
                            if(trail.lastCategory == 'Neut'):
                                self.emotional_EN.add(trail.timing)
                                self.emotional_S.add(trail.timing)
                            else:
                                self.emotional_EE.add(trail.timing)
                                self.emotional_NS.add(trail.timing)
                    elif(trail.type == '2'):
                        if(trail.isSwitch()):
                            self.neutral_S.add(trail.timing)
                        else:
                            self.neutral_NS.add(trail.timing)

