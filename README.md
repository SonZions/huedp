# huedp
Docker Container um Änderungen an hue Sensoren und Remotes per UDP-Nachricht zu melden.
Mein Usecase: Status des Motion Sensors (Presens, Lightlevel) und der Fernbedienung (Button 1-n) nutzen zu können.

Nach entsprechner Konfiguration fragt der Container die Bridge zwei mal in der Sekunde nach den Entsprechenden Sensoren/Objekten/Lichtern und beobachtet je nach Typ die vorkonfigurierten Stati. Wenn eine Änderung eines Status erkannt wird, wird diese an den Server geschickt. 

## Vorkonfigurierte Stati

| Typ | Beobachteter Status | Rückgabe |
|-----|---------------------|----------|
| ZLLTemperature | temperature | <int> |
| ZLLPresence | presence | <bool int> |
| ZLLLightLevel | lightlevel | <int>
| ZLLSwitch | buttonevent | <int> |
| Dimmable light | on | <bool int> |
| Extended color light | on | <bool int> |


## build

```
 docker build -t dudanski/huedp:latest .
```

Das Image ist auch auf Dockerhub verfügbar

## run 

### Vorbereitung

Zuerst muss ein User für den Container an der Hue-Bridge angelegt werden:
https://developers.meethue.com/develop/get-started-2/

### Mit .env File 

Der Container legt großen wert auf Großschreibung. 
```
BRIDGE_IP=<<Your Hue Bridge IP>>
BRIDGE_USERNAME=<<User Name: Siehe Vorbereitung>>>
UDP_TARGET_IP=<<IP des Smarthome Servers>>
UDP_PORT=<<Frei wählbare Nummer>>
SENSORS=<<Liste der Sensoren>>>
```

```
docker run --detach \
           --env-file .env \
           --name huedp_sensors \
           dudanski/huedp:latest
```

### Mit Environment-Variablen

```
docker run --detach \
           --env-file .env \
           --name huedp_sensors \
           --env BRIDGE_IP=<<Your Hue Bridge IP>>
           --env BRIDGE_USERNAME=<<User Name: Siehe Vorbereitung>>>
           --env UDP_TARGET_IP=<<IP des Smarthome Servers>>
           --env UDP_PORT=<<Frei wählbare Nummer>>
           --env SENSORS=<<Liste der Sensoren als JSON Array>>
           dudanski/huedp:latest
```

### Beispiel

```
docker run --detach \
           --restart always \
           --name huedp_sensors \
           --env BRIDGE_IP=192.168.178.3
           --env BRIDGE_USERNAME=QWErtzuioPasdfghjkl-yxcvbNm12-34567890ab
           --env UDP_TARGET_IP=192.168.178.4
           --env UDP_PORT 4711
           --env SENSORS=["Kinderzimmer Schalter","Arbeitszimmer Sensor"]
           dudanski/huedp:latest
```



## Konfiguration

| Parameter Name | Beschreibung |
|----------------|--------------|
| BRIDGE_IP | IP-Adresse, die der Hue-Bridge gegeben wurde |
| BRIDGE_USERNAME | Für die Hue-API generierter User-Name/Token zur Authentifizierung |
| UDP_TARGET_IP | IP-Adresse des Servers, der die UDP-Nachrichten entgegennehmen soll. In meinem Fall die IP des Miniservers. |
| UDP_PORT | Portnummer unter der die Nachrichten empfangen weden. Im Falle des Miniservers frei wählbar |
| SENSORS | Liste der Namen der Sensoren, die betrachtet werden sollen. (!) im JSON-Format. |
| API_ENDPOINT | [optional] default: sensors) Knoten auf dem Objekte abgefragt werden sollen. z.B. lights | 
| POLLING_FREQUENCY | [optional] (default: .500) Millisekunden, um die die Abfragen an die Bridge verzögert werden. bei zu großer Belastung der Bridge oder des Netzes sollte dad erhöht werden.| 

## Button Events Rückabe

Ein Auszug aus der API:

```
"events": [
						{
							"buttonevent": 3000,
							"eventtype": "initial_press"
						},
						{
							"buttonevent": 3001,
							"eventtype": "repeat"
						},
						{
							"buttonevent": 3002,
							"eventtype": "short_release"
						},
						{
							"buttonevent": 3003,
							"eventtype": "long_release"
						}
					]
				},
				{
					"repeatintervals": [
						800
					],
					"events": [
						{
							"buttonevent": 4000,
							"eventtype": "initial_press"
						},
						{
							"buttonevent": 4001,
							"eventtype": "repeat"
						},
						{
							"buttonevent": 4002,
							"eventtype": "short_release"
						},
						{
							"buttonevent": 4003,
							"eventtype": "long_release"
						}
					]
```