#Question is the basic data of the system. each line in the file represent one question
class Question:
    def isDummy(self):
        if(self.lastCategory == '.'):
            return True
        return False

    def isSwitch(self):
        if(self.category == self.lastCategory):
            return False
        return True
