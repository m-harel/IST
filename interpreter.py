#interpreter a line to question
import Question

class Interpreter:
    mustExistVariables = ['Subject','Session','StimCat','LactCategory','StimTextDisp.RT','Q1SlidePath','Q2Slide.RESP','Q1Slide.RESP']
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
        lineVariables = line.split()
        if(len(lineVariables) < 4 or lineVariables[2] == 'NULL' or lineVariables[2] == ''):
            return None
        question = Question.Question()
        question.userId = lineVariables[self.variables.index('Subject')]
        question.type = lineVariables[self.variables.index('Session')]
        question.category = lineVariables[self.variables.index('StimCat')]
        question.lastCategory = lineVariables[self.variables.index('LactCategory')]
        question.timing = int(lineVariables[self.variables.index('StimTextDisp.RT')])
        question.firstQuestionSlide = lineVariables[self.variables.index('Q1SlidePath')][-4]
        question.firstQuestionAnswer = self.questionResponse(lineVariables[self.variables.index('Q1Slide.RESP')])
        question.secondQuestionAnswer = self.questionResponse(lineVariables[self.variables.index('Q2Slide.RESP')])

        return question