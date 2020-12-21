import json
import pandas as pd
import requests

# Fwd_Seg_Size_Min
fwd_seg_size_min = []
# Dst_Port
dst_port = []
# Fwd_Header_Len
fwd_header_len = []
# Init_Fwd_Win_Byts
init_fwd_win_byts = []
while len(fwd_seg_size_min) < 100:
    print(len(fwd_seg_size_min))
    response = requests.get('http://localhost:9999/activeflows/192.168.222.128/test/json')
    print(response.status_code)
    response_json = response.json()
    for i in range(len(response_json)):
        if len(fwd_seg_size_min) >= 100:
            break
        ipsource, ipdestination, tcpsourceport, tcpdestinationport, ip_offset, tcp_offset, tcpwindow, tcppayloadbytes = response_json[i]['key'].split(',')
        if ipdestination == '10.0.0.1':
            fwd_seg_size_min.append(int(tcp_offset) + int(tcppayloadbytes))
            dst_port.append(int(tcpdestinationport))
            fwd_header_len.append(int(ip_offset) + int(tcp_offset))
            init_fwd_win_byts.append(int(tcpwindow))

# Flow_Byts/s
flow_byts = []
while len(flow_byts) < 100:
    print(len(flow_byts))
    response = requests.get('http://localhost:9999/metric/192.168.222.128/avg:ifoutoctets/json')
    print(response.status_code)
    response_json = response.json()
    flow_byts.append(float(response_json[0]['metricValue']))

collected_data = pd.DataFrame({'Fwd_Seg_Size_Min': fwd_seg_size_min, 
                               'Dst_Port': dst_port, 
                               'Fwd_Header_Len': fwd_header_len,
                               'Init_Fwd_Win_Byts': init_fwd_win_byts,
                               'Flow_Byts/s': flow_byts})
collected_data.to_csv('./datasets/collected_ddos_traffic.csv', index=False)
