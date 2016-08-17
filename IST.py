import Settings
import Interpreter
import User
import Excel
import statistics

settings = Settings.settings()
settings.readSettingsFile()

dataFile = open(settings.dataFileName,'r',encoding=settings.dataFileEncoding)
dataFileLines = dataFile.readlines()


interpreter = Interpreter.Interpreter(dataFileLines[settings.dataFileVariablesLine])

users = []

for line in dataFileLines[settings.dataFileVariablesLine+1:]:
    trail = interpreter.interprete(line)
    if(trail == None):
        print('failed interpret line - ' + line)
        continue

    if(len(users) == 0 or (users[-1].id != trail.userId)):
        users.append(User.user(trail.userId))

    users[-1].addTrail(trail)


dataFile.close()


for user in users:
    user.findStandardDeviation()

listOfStandardScores = [2.5, 3, 3.5]
standardScore = 0
standardScoreRate = 0
for standardDeviation in listOfStandardScores:
    countStandard = 0
    countTotal = 0
    for user in users:
        for block in user.blocks:
            for trail in block.trials:
                if(not trail.isDummy()):
                    countTotal+=1
                    if(trail.standardScore < standardDeviation):
                        countStandard += 1

    if(countStandard/countTotal > 0.95):
        standardScore = standardDeviation
        standardScoreRate = countStandard / countTotal
        break

if(standardScore == 0):
    print("standard deviation problem - not found standard score with more then 95% trails available")
    exit()

for user in users:
    user.calculateMeans(standardScore)

excelFile = Excel.Excel(settings.excelFileName)

excelFile.metaSheet.write(1,0,'data file name')
excelFile.metaSheet.write(1,1,settings.dataFileName)

excelFile.metaSheet.write(3,0,'standard score')
excelFile.metaSheet.write(3, 1, standardScore)

excelFile.metaSheet.write(4,0,'rate')
excelFile.metaSheet.write(4, 1, standardScoreRate)

for user in users:
    excelFile.printUser(user)

excelFile.close()

