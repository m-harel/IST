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

    def addTrial(self, trial):
        if(trial.isDummy()):
            self.blocks.append(Block.Block(self.id, len(self.blocks) + 1, trial.type))
        self.blocks[-1].addTrial(trial)

    def calculateMeans(self, standardScore):
        for block in self.blocks:
            for trial in block.trials:
                if((not trial.isDummy()) and trial.standardScore < standardScore):
                    if(trial.type == '1'):
                        if(trial.category == 'Neut'):
                            if(trial.lastCategory == 'Neut'):
                                self.emotional_NN.add(trial.timing)
                                self.emotional_NS.add(trial.timing)
                            else:
                                self.emotional_NE.add(trial.timing)
                                self.emotional_S.add(trial.timing)
                        else:
                            if(trial.lastCategory == 'Neut'):
                                self.emotional_EN.add(trial.timing)
                                self.emotional_S.add(trial.timing)
                            else:
                                self.emotional_EE.add(trial.timing)
                                self.emotional_NS.add(trial.timing)
                    elif(trial.type == '2'):
                        if(trial.isSwitch()):
                            self.neutral_S.add(trial.timing)
                        else:
                            self.neutral_NS.add(trial.timing)

    def findMean(self):
        sum = 0
        count = 0
        for block in self.blocks:
            for trial in block.trials:
                if(not  trial.isDummy()):
                    sum +=  trial.timing
                    count += 1

        self.mean = sum / count


    def findStandardDeviation(self):
        if(not hasattr(self, 'mean')):
            self.findMean()
        sum = 0
        count = 0
        for block in self.blocks:
            for trial in block.trials:
                if(not trial.isDummy()):
                    sum += (trial.timing - self.mean)**2
                    count += 1

        self.standardDeviation = (sum/count) ** 0.5

        for block in self.blocks:
            for trial in block.trials:
                if(not trial.isDummy()):
                    trial.standardScore = abs(trial.timing - self.mean) / self.standardDeviation

