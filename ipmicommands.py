import os


def powerOn(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} chassis power on')
    osStr = stream.read()
    return 'Server is already online.' if osStr == '' else osStr


def powerOff(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} chassis power off')
    osStr = stream.read()
    return 'Server is already offline' if osStr == '' else osStr


def powerCycle(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} chassis power cycle')
    return stream.read()


def powerUsage(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} sdr | grep "Power"')
    return stream.read()


def powerStatus(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} power status')
    return stream.read()


def sdrList(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} sdr')
    return stream.read()


def fanStatus(serverIP, userName, password):
    stream = os.popen(f'ipmitool -I lanplus -H {serverIP} -U {userName} -P {password} sdr | grep "Fan"')
    return stream.read()
