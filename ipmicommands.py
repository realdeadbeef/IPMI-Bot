import os


def powerOn(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} chassis power on')
    osStr = stream.read()
    if osStr == '':
        return 'Server is already online.'
    else:
        return osStr


def powerOff(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} chassis power off')
    osStr = stream.read()
    if osStr == '':
        return 'Server is already offline'
    else:
        return osStr


def powerCycle(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} chassis power cycle')
    osStr = stream.read()
    return osStr


def powerUsage(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} sdr | grep "Power"')
    osStr = stream.read()
    return osStr


def powerStatus(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} power status')
    osStr = stream.read()
    return osStr


def sdrList(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} sdr')
    osStr = stream.read()
    return osStr


def fanStatus(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} sdr | grep "Fan"')
    osStr = stream.read()
    return osStr
