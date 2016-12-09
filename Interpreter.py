#interpreter a line to trial
import Trial

class Interpreter:
    mustExistVariables = ['Subject','Session','StimCat','LactCategory','StimTextDisp.RT','Q1SlidePath','Q2Slide.RESP','Q1Slide.RESP','isPrac']

    def __init__(self, line):
        if(line.startswith('\ufeff')):
            line= line[1:]
        self.variables = line.split()

        for var in Interpreter.mustExistVariables:
            if(not (var in self.variables)):
                print('a must exist variables missed - ' + var)
                exit()

    def questionResponse(self, response):
        if(response == '{ENTER}'):
            return 0
        return (int)(response.split('{')[0])

    def interprete(self,line):
        #print(line)
        lineVariables = line.split()
        if(len(lineVariables) < 4 or lineVariables[2] == 'NULL' or lineVariables[2] == '' or lineVariables[self.variables.index('isPrac')] == 'Y'):
            return None
        #print(lineVariables[self.variables.index('isPrac')])

        trial = Trial.Trial()
        trial.userId = lineVariables[self.variables.index('Subject')]
        trial.type = lineVariables[self.variables.index('Session')]
        trial.category = lineVariables[self.variables.index('StimCat')]
        trial.lastCategory = lineVariables[self.variables.index('LactCategory')]
        trial.timing = int(lineVariables[self.variables.index('StimTextDisp.RT')])
        trial.firstQuestionSlide = lineVariables[self.variables.index('Q1SlidePath')][-4]
        trial.firstQuestionAnswer = self.questionResponse(lineVariables[self.variables.index('Q1Slide.RESP')])
        trial.secondQuestionAnswer = self.questionResponse(lineVariables[self.variables.index('Q2Slide.RESP')])

        return trial