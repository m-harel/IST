import Settings
import Interpreter
import Task
import Excel
import subprocess
import easygui
import chardet

dataFileName = easygui.fileopenbox(default="*.txt")

settings = Settings.Settings()
settings.readSettingsFile()

if dataFileName == None:
    dataFileName = settings.dataFileName

dataFile = open(dataFileName,'r',encoding=settings.dataFileEncoding)
dataFileLines = dataFile.readlines()

try:
    interpreter = Interpreter.Interpreter(dataFileLines[settings.dataFileVariablesLine])
except:
    print("Bad data file :(")
    exit()

task = Task.Task()

for line in dataFileLines[settings.dataFileVariablesLine+1:]:
    trial = interpreter.interprete(line)
    if(trial is None):
        continue

    task.addTrial(trial)

dataFile.close()

task.analyse()

excelFile = Excel.Excel(settings.excelFileName)
excelFile.metaSheet.write(1,0,'data file name')
excelFile.metaSheet.write(1,1,settings.dataFileName)
excelFile.metaSheet.write(2,0,'git version')
excelFile.metaSheet.write(2,1,str(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii')))

excelFile.printTask(task)

excelFile.close()

