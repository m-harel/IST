import Settings
import Interpreter
import User
import Excel

settings = Settings.settings()
settings.readSettingsFile()

dataFile = open(settings.dataFileName,'r',encoding=settings.dataFileEncoding)
dataFileLines = dataFile.readlines()

interpreter = Interpreter.Interpreter(dataFileLines[settings.dataFileVariablesLine])

excelFile = Excel.Excel(settings.excelFileName)

users = []

for line in dataFileLines[settings.dataFileVariablesLine+1:]:
    trail = interpreter.interprete(line)
    if(trail == None):
        continue

    if(len(users) == 0 or (users[-1].id != trail.userId)):
        users.append(User.user(trail.userId))

    users[-1].addTrail(trail)


dataFile.close()

for user in users:
    for block in user.blocks:
        block.findStandardDeviation()

listOfStandardDeviation = [2, 2.5, 3, 4, 5]
standard = 0
for standardDeviation in listOfStandardDeviation:
    countStandard = 0
    countTotal = 0
    for user in users:
        for block in user.blocks:
            countTotal += len(block.trials)
            for trial in block.trials:
                if(trial.standard < standardDeviation):
                    countStandard += 1
    if(countStandard/countTotal > 0.95):
        standard = standardDeviation
        break

if(standard == 0):
    print("standart devition problem - not found one")
    exit()

for user in users:
    user.getStandradMeans(standard)

for user in users:
    excelFile.printUser(user)

excelFile.close()

