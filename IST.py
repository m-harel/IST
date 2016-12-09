import Settings
import Interpreter
import User
import Excel
import subprocess


settings = Settings.settings()
settings.readSettingsFile()

dataFile = open(settings.dataFileName,'r',encoding=settings.dataFileEncoding)
dataFileLines = dataFile.readlines()

interpreter = Interpreter.Interpreter(dataFileLines[settings.dataFileVariablesLine])

users = []

for line in dataFileLines[settings.dataFileVariablesLine+1:]:
    trial = interpreter.interprete(line)
    if(trial == None):
        continue

    if(len(users) == 0 or (users[-1].id != trial.userId)):
        users.append(User.user(trial.userId))

    users[-1].addTrial(trial)

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
            for trial in block.trials:
                if(not trial.isDummy()):
                    countTotal+=1
                    if(trial.standardScore < standardDeviation):
                        countStandard += 1

    if(countStandard/countTotal > 0.95):
        standardScore = standardDeviation
        standardScoreRate = countStandard / countTotal
        break

if(standardScore == 0):
    print("standard deviation problem - not found standard score with more then 95% trials available")
    exit()

for user in users:
    user.calculateMeans(standardScore)

excelFile = Excel.Excel(settings.excelFileName)
excelFile.metaSheet.write(1,0,'data file name')
excelFile.metaSheet.write(1,1,settings.dataFileName)
excelFile.metaSheet.write(2,0,'git version')
excelFile.metaSheet.write(2,1,str(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii')))

excelFile.metaSheet.write(4,0,'standard score')
excelFile.metaSheet.write(4, 1, standardScore)

excelFile.metaSheet.write(5,0,'rate')
excelFile.metaSheet.write(5, 1, standardScoreRate)

for user in users:
    excelFile.printUser(user)

excelFile.close()

