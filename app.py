# In[]:
import requests, json, socket
from time import sleep
import constants as c
from config import Config

# In[]:

bridge_ip = Config.BRIDGE_IP
bridge_username = Config.BRIDGE_USERNAME
udp_target_ip = Config.UDP_TARGET_IP
udp_port = Config.UDP_PORT
print(Config.SENSORS)
sensors = json.loads(Config.SENSORS)
api_endpoint = Config.API_ENDPOINT
poll_freq = Config.POLLING_FREQUENCY

print(sensors)

# dict to store and detect changes
sensordata={}

# counter für anzahl msg
cntmsg=0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# In[]
def get_sensor_cnt(sensor):
    global sensordata
    if sensor in sensordata:
        return sensordata[sensor][c.msgcounter]
    return 0

def incr_sensor_cnt(sensor):
    global sensordata
    if sensor not in sensordata:
        sensordata[sensor][c.msgcounter] = 0    
    sensordata[sensor][c.msgcounter] = sensordata[sensor][c.msgcounter]+1
    

# In[]

def get_sensor_data(jsonr,sensor):

    for node in jsonr:
        name = jsonr[node][c.name]
        if name == sensor:
            # nachschlagen wie der status heißt
            # dann den Status nachschlagen und lastupdate für sensors
            sstatetype =c.keymapping[jsonr[node][c.jtype]]
            state = jsonr[node][c.state][sstatetype]
            # Translate bool to int
            if state == False:
                state = 0
            if state == True:
                state = 1
            if c.lastupdated in jsonr[node][c.state]:
                # Es gibt machmal kein LastUpate z.B. bei Lampen
                lastupdt = jsonr[node][c.state][c.lastupdated]
                return {name: {c.state:state, c.lastupdated:lastupdt, c.msgcounter:get_sensor_cnt(sensor)}}
            return {name: {c.state : state}}
            
# In[]

def send_udp_message(sensordata):
    # es gibt nur einen Key und den brauchen wir
    sname = list(sensordata.keys())[0]
    udpmessage = str({ sname:sensordata[sname][c.state], c.msgcounter: get_sensor_cnt(sname)})
    return sock.sendto(bytes(udpmessage, c.encoding), (udp_target_ip, udp_port))


# In[]
while True:
    # response von der Bridge holen und jasonizen
    response = requests.get("http://"+bridge_ip+"/api/"+bridge_username+"/"+api_endpoint)
    jsonr = json.loads(response.text)

    # sensordaten raussuchen
    for sensor in sensors:
        try:
            new_sensordata = get_sensor_data(jsonr,sensor)
        except:
            print(" Error while retreiving data for {} ".sensor)
            pass
        if (     (   sensor not in sensordata 
                  or sensordata[sensor] != new_sensordata[sensor])
             and new_sensordata != None):
            # nur wenn es eine Änderung gab müssen wir den Miniserver anpingen
            send_udp_message(new_sensordata)
            sensordata.update(new_sensordata)
            print(new_sensordata)
            incr_sensor_cnt(sensor)

    sleep(poll_freq)

  
# %%
