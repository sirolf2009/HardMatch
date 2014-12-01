__author__ = 'Rene'

from Crawler.components import Component


class CPU(Component):
    brand = None
    series = None
    name = None
    Socket = None

    amountOfCores = None
    specNumber = None
    GHz = None
    GHZ_Turbo = None
    memorySPec = None
    BusSpeed = None
    #Procestechnologie
    ThermalDesignPower = None
    IntegratedGraphics = None
    InternalGPU = None
    videochipSpeed = None
    videochipSpeedMax = None
    cacheLvl1 = None
    cacheLvl2 = None
    cacheLvl3 = None
    threads = None
    threads_old = None
    visualisation = None
    visualisationType = None
    CPUMultiplier = None
    CPUstepping = None
    CPUInstructionset = None
    TypeCooling = None
    EAN = None
    SKU = None
