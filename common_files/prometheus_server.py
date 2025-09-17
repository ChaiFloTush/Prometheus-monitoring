# import http.server
import prometheus_client
import os
import subprocess
import time

HOST_TYPE = prometheus_client.Gauge('host_type', 'Type of host', ['type'])

def detect_host_type():
    if os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv'):
        return 'container'

    try:
        virt_what = subprocess.run(['which', 'virt-what'], capture_output=True, text=True)
        if virt_what.returncode == 0:
            result = subprocess.run(['virt-what'], capture_output=True, text=True)
            if result.stdout.strip():
                return 'virtual_machine'
            
        if os.path.exists('/proc/cpuinfo'):
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo =f.read()
                if 'hypervisor' in cpuinfo.lower():
                    return 'virtual_machine'
                
        systemd_virt = subprocess.run(['systemd-detect-virt'], capture_output=True, text=True)
        if systemd_virt.returncode == 0 and systemd_virt.stdout.strip() != 'none':
            return 'virtual_machine'
        
    except Exception:
        pass

    return 'physical_server'

host_type = detect_host_type()
HOST_TYPE.labels(type=host_type).set(1)

# REQUEST_COUNT = prometheus_client.Counter('http_requests_total', 'Total HTTP Requests')

# class MetricsHandler(prometheus_client.MetricsHandler):
#     def do_GET(self):
#         REQUEST_COUNT.inc()
#         return super().do_GET()
    
if __name__ == '__main__':
    # server = http.server.HTTPServer(('', 8080), MetricsHandler)
    # server.serve_forever()

    prometheus_client.start_http_server(8080)
    while True:
        time.sleep(1)