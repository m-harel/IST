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

    def addTrail(self, trail):
        self.trials.append(trail)
        self.addWord(trail.category)

    def findMean(self):
        sum = 0
        for trail in self.trials:
            sum += trail.timing

        self.mean = sum / len(self.trials)


    def findStandardDeviation(self):
        if(not hasattr(self, 'mean')):
            self.findMean()
        sum = 0
        for trail in self.trials:
            sum += (trail.timing - self.mean)**2

        self.standardDeviation = (sum/len(self.trials)) ** 0.5

        for trail in self.trials:
            trail.standard = abs(trail.timing - self.mean) /self.standardDeviation