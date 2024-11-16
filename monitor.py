import psutil
import paho.mqtt.client as mqtt
import time
import json
import os

BROKER = "YOUR_BROKER_IP"
PORT = 1883
TOPIC = "home/computer/metrics"
INTERVAL = 5

def get_metrics():
    hostname = os.getenv('HOSTNAME', 'default-hostname')
    metrics = {
        "hostname": hostname,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "ram_percent": psutil.virtual_memory().percent,
    }
    return metrics

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT)
    
    while True:
        metrics = get_metrics()
        client.publish(TOPIC, json.dumps(metrics))
        print(f"Enviado para o MQTT: {metrics}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
