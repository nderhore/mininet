import requests
import json
import time

targetedSwitch = '00:00:00:00:00:00:00:03'
sFlow_RT = 'http://localhost:8008'
floodlight = 'http://192.168.91.147:8080'
defense = {'icmp': True, 'syn': False, 'dns_amplifier': False, 'udp': False}
black_list = []
block_time = 360
fw_priority = '32767'
groups = {'external': ['0.0.0.0/0'], 'internal': ['0.0.0.0/0']} #
value = 'bytes' # set to 'bytes' and multiply 8 to get bits/second
# define ICMP flood attack attributes #
icmp_flood_keys = 'inputifindex,ethernetprotocol,macsource,macdestination,ipprotocol,ipsource,ipdestination'
icmp_flood_metric_name = 'icmp_flood'
icmp_flood_threshold_value = 50
#icmp_flood_filter = 'group:ipsource:lf=external&group:ipdestination:lf=internal&outputifindex!=discard&ipprotocol=1'
icmp_flood_flows = {'keys': icmp_flood_keys, 'value': value} # No filter, the script will monitor every host
icmp_flood_threshold = {'metric': icmp_flood_metric_name, 'value': icmp_flood_threshold_value}
events = '';

while True:
    r = -1
    #r = requests.put(sFlow_RT + '/group/json', data=json.dumps(groups))
    r = requests.put(sFlow_RT + '/group/lf/json', data=json.dumps(groups))
    if defense['icmp']:
        # define flows and threshold of ICMP flood
        r = requests.put(sFlow_RT + '/flow/' + icmp_flood_metric_name + '/json', data=json.dumps(icmp_flood_flows))
        r = requests.put(sFlow_RT + '/threshold/' + icmp_flood_metric_name + '/json', data=json.dumps(icmp_flood_threshold))
        event_url = sFlow_RT + '/events/json?maxEvents=10&timeout=60'
        eventID = -1
    if black_list.__len__() > 0 and black_list[0][0] < time.time():
        r = requests.delete(floodlight + '/wm/static/flowpusher/', data=black_list.pop(0)[1])
        print (r.json()['status'])
    r = requests.get(event_url + '&eventID=' + str(eventID))
    events = r.json()
    if events.__len__() > 0:
        eventID = events[0]["eventID"]
        events.reverse()
        for e in events:
            if e['metric'] == icmp_flood_metric_name:
                r = requests.get(sFlow_RT + '/metric/' + e['agent'] + '/' + e['dataSource'] + '.' + e['metric'] + '/json')
                metrics = r.json()
                if metrics and metrics.__len__() > 0:
                    metric = metrics[0]
                    if metric.__contains__("metricValue") and metric['metricValue'] > icmp_flood_threshold_value and metric['topKeys'] and metric['topKeys'].__len__() > 0:
                        for topKey in metric['topKeys']:
                            if topKey['value'] > icmp_flood_threshold_value:
                                key = topKey['key']
                                parts = key.split(',')
                                message = {
                                    'switch':targetedSwitch,
                                    'name': 'ICMP_block_'+str(parts[5]),
                                    "cookie":"0",
                                    "priority": fw_priority,
                                    'ipv4_src': str(parts[5]),
                                    'ipv4_dst': str(parts[6]),
                                    "active":"true",
                                    "eth_type":"0x0800",
                                }
                                print(message)
                                push_data = json.dumps(message)
                                r = requests.post(floodlight + '/wm/staticflowpusher/', data=push_data)
                                black_list.append([time.time()+block_time, push_data])
                                break
                            else:
                                continue
                                break

    time.sleep(3)