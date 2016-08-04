class Mean:
    def __init__(self):
        self.count = 0
        self.sum = 0
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

    def __sub__(self, other):
        if(self.count == 0 or other.count == 0):
            return 'N\A'
        return self.getMean(1) - other.getMean(1)