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

    def addQuestion(self,question):
        if(question.isDummy()):
            self.blocks.append(Block.Block(self.id, len(self.blocks) + 1, question.type))
        self.blocks[-1].addQuestion(question)

        if(question.type == '1'):
            if(question.category == 'Neut'):
                if(question.lastCategory == 'Neut'):
                    self.emotional_NN.add(question.timing)
                    self.emotional_NS.add(question.timing)
                else:
                    self.emotional_NE.add(question.timing)
                    self.emotional_S.add(question.timing)
            else:
                if(question.lastCategory == 'Neut'):
                    self.emotional_EN.add(question.timing)
                    self.emotional_S.add(question.timing)
                else:
                    self.emotional_EE.add(question.timing)
                    self.emotional_NS.add(question.timing)
        elif(question.type == '2'):
            if(question.isSwitch()):
                self.neutral_S.add(question.timing)
            else:
                self.neutral_NS.add(question.timing)