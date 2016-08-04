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
    question = interpreter.interprete(line)
    if(question == None):
        continue

    if(len(users) == 0 or (users[-1].id != question.userId)):
        users.append(User.user(question.userId))

    users[-1].addQuestion(question)


dataFile.close()

for user in users:
    excelFile.printUser(user)

excelFile.close()

