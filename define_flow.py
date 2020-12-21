import json
import requests

flow_defination = {'keys': 'ipsource,ipdestination,tcpsourceport,tcpdestinationport,ip_offset,tcp_offset,tcpwindow,tcppayloadbytes', 
                   'value': 'bytes', 'log': True}
response = requests.put('http://localhost:9999/flow/test/json', data=json.dumps(flow_defination))
print(response.status_code)