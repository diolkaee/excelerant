import json


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


def handleEvent(excelerant, event):
    (type, value, chamber) = parseEvent(event)
    match type:
        case 'power':
            handlePowerChange(excelerant, value, chamber)
        case 'exposure':
            handleExposure(excelerant, value, chamber)
        case 'fanSpeed':
            handleFanSpeedChange(excelerant, value)


def handlePowerChange(excelerant, isPowered, chamber):
    match chamber:
        case 'grow':
            excelerant.setGrowLight(isPowered)
        case 'bloom':
            excelerant.setBloomLight(isPowered)
        case _:
            raise ValueError


def handleExposure(excelerant, exposure, chamber):
    # TODO Implement me & define API spec
    print('Exposure is not implemented yet')


def handleFanSpeedChange(excelerant, fanSpeed):
    excelerant.setFanSpeed(fanSpeed)
