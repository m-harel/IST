#interpreter a line to question
import Question

class Interpreter:
    mustExistVariables = ['Subject','Session','StimCat','LactCategory','StimTextDisp.RT','Q1SlidePath','Q2Slide.RESP','Q1Slide.RESP']
    variables = []
    def __init__(self,line):
        self.variables = line.split()
        for var in self.mustExistVariables:
            if(not (var in self.variables)):
                print('a must exist variables missed - ' + var)
                exit()

    def questionResponse(self,response):
        if(response == '{ENTER}'):
            return 0
        return (int)(response.split('{')[0])

    def interprete(self,line):
        lineVariables = line.split()
        if(len(lineVariables) < 3 or lineVariables[2] == 'NULL'):
            return None
        #print(line)
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