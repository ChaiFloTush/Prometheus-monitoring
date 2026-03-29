import prometheus_client
import os
import time

HOST_TYPE = prometheus_client.Gauge('host_type', 'Type of host', ['type'])

def detect_host_type():
    if os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv'):
        return 'container'

    if os.path.exists('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo =f.read()
            if 'hypervisor' in cpuinfo.lower():
                return 'virtual_machine'
        
    return 'physical_server'

host_type = detect_host_type()
HOST_TYPE.labels(type=host_type).set(1)

if __name__ == '__main__':
    prometheus_client.start_http_server(8080)
    while True:
        time.sleep(1)