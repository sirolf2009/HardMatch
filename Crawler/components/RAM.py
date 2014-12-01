__author__ = 'Rene'


from Crawler.components import Component


class RAM(Component):

    memorySize = None
    moduleSize = None
    memoryType = None

    def setMemorySize(self, memorySize):
        self.memorySize = memorySize

    def getMemorySize(self, memorySize):
        self.memorySize = memorySize

    def setModuleSize(self, moduleSize):
        self.moduleSize = moduleSize

    def getModuleSize(self, moduleSize):
        self.moduleSize = moduleSize

    def setMemoryType(self, memoryType):
        self.memoryType = memoryType

    def getMemoryType(self, memoryType):
        self.memoryType = memoryType


    memorySpec = None
    lowVoltage = None
    CASLatency = None
    volt = None
    warranty = None
