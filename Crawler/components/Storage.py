__author__ = 'Rene'

from Crawler.components import Component


class Storage(Component):
    type = None
    electricityUseRead = None
    electricityUseWrite = None
    width = None
    depth = None
    interface = None

    #HDD
    capacity = None
    rotationSpeed = None
    driveCache = None
    commandQueuing = None
    warrantyInYears = None

    #SSD
    SSDType = None
    SSDController = None
    SSDProperties = None
    connection = None
    meanTimeBetweenFailures = None
    sequentialReadSpeed = None
    sequentialWriteSpeed = None
