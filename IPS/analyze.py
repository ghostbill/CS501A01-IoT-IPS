import datetime
import json
import copy
import sys


macs_to_add = []	
with open('ips.json', 'r') as f:	
    for line in f:	
        data = json.loads(line)	
        for c in data['cellphones']:	
            if c['rssi'] > -80 and c['mac'] not in macs_to_add:	
                macs_to_add.append(c['mac'])	
 print(macs_to_add)	
mac_data = {}	
for mac in macs_to_add:	
    mac_data[mac] = {'y': []}	
 num = {'x': [], 'y': []}	
 with open('ips.json', 'r') as f:	
    for line in f:	
        data = json.loads(line)	
        rssi = {}	
        for mac in macs_to_add:	
            rssi[mac] = -100	
            for c in data['cellphones']:	
                if c['mac'] in rssi:	
                    rssi[c['mac']] = c['rssi']	
        for mac in mac_data:	
            mac_data[mac]['y'].append(str(rssi[mac] + 100))	
        num['x'].append("'" + datetime.datetime.fromtimestamp(	
                data['time']).isoformat().split('.')[0].replace('T', ' ') + "'")	
        num['y'].append(str(len(data['cellphones'])))	
 mac_names = copy.deepcopy(macs_to_add)	
for i, mac in enumerate(mac_names):	
    mac_names[i] = 'mac' + mac.replace(':', '')	
 # remove pings	
for mac in mac_data:	
    for i, y in enumerate(mac_data[mac]['y']):	
        if y == "0" and i > 2:	
            if mac_data[mac]['y'][i - 3] == "0" and (mac_data[mac]['y'][i - 1] != "0" or mac_data[mac]['y'][i - 2] != "0"):	
                mac_data[mac]['y'][i - 1] = "0"	
                mac_data[mac]['y'][i - 2] = "0"	
 js = ""	
js += ('timex = [%s]' % ', '.join(num['x']))	
for i, mac in enumerate(macs_to_add):	
    js += ('\nvar %s = {' % mac_names[i])	
    js += ('\n  x: timex,')	
    js += ('\n  y: [%s],' % ', '.join(mac_data[mac]['y']))	
    js += ("\n name: '%s', mode: 'lines', type:'scatter' };\n\n" % mac)	
js += ('\n\nvar data = [%s];' % ', '.join(mac_names))	
js += ("\n\nPlotly.newPlot('myDiv',data);")	
js += ('\nvar num_cellphones = {')	
js += ('\n  x: timex,')	
js += ('\n  y: [%s],' % ', '.join(num['y']))	
js += ("\n name: 'N', mode: 'lines', type:'scatter' };\n\n")	
js += ("\n\nPlotly.newPlot('myDiv2',[num_cellphones]);")	
 with open('index.html','w') as f:	
    f.write("""<head>	
    <!-- Plotly.js -->	
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>	
</head>	
 <body>	
    <div id="myDiv2" style="width: 950px; height: 400px;">	
        <!-- Plotly chart will be drawn inside this DIV -->	
    </div>	
     <div id="myDiv" style="width: 950px; height: 400px;">	
        <!-- Plotly chart will be drawn inside this DIV -->	
    </div>	
    <script>	
%s	
    </script>	
</body>""" % js)