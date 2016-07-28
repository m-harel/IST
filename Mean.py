class Mean:
    count = 0
    sum = 0
    def getMean(self,reset = 0):
        if self.count == 0:
            return 'N\A'
        m = (int)(self.sum/self.count)
        if(reset == 1):
            self.reset()
        return m
    def reset(self):
        self.count = 0
        self.sum = 0
    def add(self, num):
        self.count += 1
        self.sum += num