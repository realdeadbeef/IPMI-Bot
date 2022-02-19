import os


def powerOn(server_ip, user_name, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {user_name} -P {password} chassis power on')
    osStr = stream.read()
    return 'Server is already online.' if osStr == '' else osStr


def powerOff(server_ip, user_name, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {user_name} -P {password} chassis power off')
    osStr = stream.read()
    return 'Server is already offline' if osStr == '' else osStr


def powerCycle(server_ip, user_name, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {user_name} -P {password} chassis power cycle')
    return stream.read()


def powerUsage(server_ip, user_name, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {user_name} -P {password} sdr | grep "Power"')
    return stream.read()


def powerStatus(server_ip, user_name, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {user_name} -P {password} power status')
    return stream.read()


def sdrList(server_ip, user_name, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {user_name} -P {password} sdr')
    return stream.read()


def fanStatus(server_ip, user_name, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {user_name} -P {password} sdr | grep "Fan"')
    return stream.read()


def soft_shutdown(server_ip, username, password):
    stream = os.popen(f'ipmitool -I lanplus -H {server_ip} -U {username} -P {password} chassis power on')
    osStr = stream.read()
    return 'Server is already offline.' if osStr == '' else osStr
