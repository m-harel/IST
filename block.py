class Block:
    def __init__(self, userId,id,type):
        self.userId = userId
        self.type = type
        self.id = id
        self.neutCount = 0
        self.emoCount = 0
        self.verbCount = 0
        self.nounCount = 0

        self.questions = []

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

    def addQuestion(self,question):
        self.questions.append(question)
        self.addWord(question.category)