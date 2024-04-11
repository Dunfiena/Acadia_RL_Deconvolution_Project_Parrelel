
class feedback_DS:
    def __init__(self, time, num_it, name):
        self.time = time
        self.num_iterations = num_it
        self.name = name

    def getTime(self):
        return self.time
    def getNumIterations(self):
        return self.num_iterations
    def setTime(self, time):
        self.time = time
    def setNumIterations(self, num_it):
        self.num_iterations = num_it
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name