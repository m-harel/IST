#Task is the highest module in this system. it contain a list of users that each user of list of blocks and each block have list of trials
import User

class Task:
    ListOfStandardScores = [2.5, 3, 3.5]
    MinimumStandaraRate = 0.95

    def __init__(self):
        self.users = []
        self.standardScore = 0
        self.standardScoreRate = 0
        self.accuracyRate = 0
        self.accuracySwitchRate = 0
        self.accuracy01Rate = 0
        self.accuracySwitch01Rate = 0

    def addTrial(self,trial):
        if(len(self.users) == 0 or (self.users[-1].id != trial.userId)):
            self.users.append(User.user(trial.userId))

        self.users[-1].addTrial(trial)

    def analyse(self):
        blocksCounter = 0
        for user in self.users:
            for block in user.blocks:
                block.calcAccuracy()
                self.accuracyRate += (int)(block.accuracy)
                self.accuracySwitchRate += (int)(block.accuracySwitch)
                self.accuracy01Rate += (int)(block.accuracy01)
                self.accuracySwitch01Rate += (int)(block.accuracySwitch01)
                blocksCounter += 1

            user.calcAccuracyRates()
            user.findStandardDeviation()

        self.accuracyRate /= blocksCounter
        self.accuracySwitchRate /= blocksCounter
        self.accuracy01Rate /= blocksCounter
        self.accuracySwitch01Rate /= blocksCounter

        for standardDeviation in Task.ListOfStandardScores:
            countStandard = 0
            countTotal = 0
            for user in self.users:
                for block in user.blocks:
                    for trial in block.trials:
                        if(not trial.isDummy()):
                            countTotal+=1
                            if(trial.standardScore < standardDeviation):
                                countStandard += 1

            if(countStandard/countTotal > Task.MinimumStandaraRate):
                self.standardScore = standardDeviation
                self.standardScoreRate = countStandard / countTotal
                break

        if(self.standardScore == 0):
            print("standard deviation problem - not found standard score with more then 95% trials available")
            exit()

        for user in self.users:
            user.calculateMeans(self.standardScore)