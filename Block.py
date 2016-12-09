class Block:
    def __init__(self, userId,id,type):
        self.userId = userId
        self.type = type
        self.id = id
        self.neutCount = 0
        self.emoCount = 0
        self.verbCount = 0
        self.nounCount = 0

        self.trials = []

    def addWord(self,word):
        if(word == 'Neut'):
            self.neutCount+=1
        elif(word == 'Emo'):
            self.emoCount+=1
        elif(word == 'Verb'):
            self.verbCount+=1
        elif(word == 'Noun'):
            self.nounCount+=1
        else:
            print("unknown - " + word)

    def addTrial(self, trial):
        self.trials.append(trial)
        self.addWord(trial.category)

    def calcAccuracy(self): #check if the user return the right answers of how many types of words in each category
        if(self.type == '1'): # emo - neut block
            if(self.trials[0].firstQuestionSlide == '1'): #the question can be presented in both ways
                self.emoDiff = abs(self.emoCount -  self.trials[0].firstQuestionAnswer)
                self.neutDiff = abs(self.neutCount - self.trials[0].secondQuestionAnswer)
                self.emoDiffSwitch = abs(self.emoCount -  self.trials[0].secondQuestionAnswer)
                self.neutDiffSwitch = abs(self.neutCount - self.trials[0].firstQuestionAnswer)
            else:
                self.emoDiff = abs(self.emoCount -  self.trials[0].secondQuestionAnswer)
                self.neutDiff = abs(self.neutCount - self.trials[0].firstQuestionAnswer)
                self.emoDiffSwitch = abs(self.emoCount -  self.trials[0].firstQuestionAnswer)
                self.neutDiffSwitch = abs(self.neutCount - self.trials[0].secondQuestionAnswer)

            self.accuracy = (self.emoDiff == 0 and self.neutDiff == 0)
            self.accuracySwitch = ((self.emoDiff == 0 and self.neutDiff == 0) or (self.emoDiffSwitch ==0 and self.neutDiffSwitch ==0))
            self.accuracy01 = (self.emoDiff <= 1 and self.neutDiff <= 1)
            self.accuracySwitch01 = ((self.emoDiff <= 1 and self.neutDiff <= 1) or (self.emoDiffSwitch <=1 and self.neutDiffSwitch <= 1))

        else: # verb - noun block
            if(self.trials[0].firstQuestionSlide == '3'):
                self.verbDiff = abs(self.verbCount -  self.trials[0].firstQuestionAnswer)
                self.nounDiff = abs(self.nounCount - self.trials[0].secondQuestionAnswer)
                self.verbDiffSwitch = abs(self.verbCount -  self.trials[0].secondQuestionAnswer)
                self.nounDiffSwitch = abs(self.nounCount - self.trials[0].firstQuestionAnswer)
            else:
                self.verbDiff = abs(self.verbCount -  self.trials[0].secondQuestionAnswer)
                self.nounDiff = abs(self.nounCount - self.trials[0].firstQuestionAnswer)
                self.verbDiffSwitch = abs(self.verbCount -  self.trials[0].firstQuestionAnswer)
                self.nounDiffSwitch = abs(self.nounCount - self.trials[0].secondQuestionAnswer)

            self.accuracy = (self.verbDiff == 0 and self.nounDiff == 0)
            self.accuracySwitch = ((self.verbDiff == 0 and self.nounDiff == 0) or (self.verbDiffSwitch ==0 and self.nounDiffSwitch ==0))
            self.accuracy01 = (self.verbDiff <= 1 and self.nounDiff <= 1)
            self.accuracySwitch01 = ((self.verbDiff <= 1 and self.nounDiff <= 1) or (self.verbDiffSwitch <=1 and self.nounDiffSwitch <= 1))




