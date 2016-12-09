class Trial:
    def isDummy(self):
        if(self.lastCategory == '.'):
            return True
        return False

    def isSwitch(self):
        if(self.category == self.lastCategory):
            return False
        return True
