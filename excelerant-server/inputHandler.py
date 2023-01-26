import json

from pixtendController import setBloomLight, setFanSpeed, setGrowLight


def parseEvent(event):
    jsonData = json.loads(event)

    eventChamber = jsonData['chamber'] if 'chamber' in jsonData else None

    eventType = jsonData['type']
    if eventType is None:
        print("No event type given")

    eventValue = jsonData['value']
    if eventValue is None:
        print("No event value given")

    return (eventType, eventValue, eventChamber)


def handleEvent(event):
    (type, value, chamber) = parseEvent(event)
    match type:
        case 'power':
            handlePowerChange(value, chamber)
        case 'exposure':
            handleExposure(value, chamber)
        case 'fanSpeed':
            handleFanSpeedChange(value)


def handlePowerChange(isPowered, chamber):
    match chamber:
        case 'grow':
            setGrowLight(isPowered)
        case 'bloom':
            setBloomLight(isPowered)
        case _:
            raise ValueError


def handleExposure(exposure, chamber):
    # TODO Implement me & define API spec
    print('Exposure is not implemented yet')


def handleFanSpeedChange(fanSpeed):
    setFanSpeed(fanSpeed)
