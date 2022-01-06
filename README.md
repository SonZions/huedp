# huedp
Docker Container um Änderungen an hue Sensoren und Remotes per UDP-Nachricht zu melden.
Mein Usecase: Status des Motion Sensors (Presens, Lightlevel) und der Fernbedienung (Button 1-n) nutzen zu können.

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

## Mit Environment-Variablen

```
docker run --detach \
           --env-file .env \
           --name huedp_sensors \
           --env BRIDGE_IP=<<Your Hue Bridge IP>>
           --env BRIDGE_USERNAME=<<User Name: Siehe Vorbereitung>>>
           --env UDP_TARGET_IP=<<IP des Smarthome Servers>>
           --env UDP_PORT=<<Frei wählbare Nummer>>
           --env SENSORS=<<Liste der Sensoren>>>
           dudanski/huedp:latest
```

## Konfiguration

| Parameter Name | Beschreibung |
---------------------------------
| Bla | Blub |