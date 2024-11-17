
# MQTT Agent for Monitoring CPU and RAM Usage

This MQTT agent collects CPU and RAM usage metrics from the host machine and sends them to an MQTT broker. It runs in a Docker container with elevated permissions (`--privileged`) to access system resources.

---

## Features

- Monitors **CPU** and **RAM** usage using the `psutil` library.
- Sends metrics to an **MQTT broker**.
- Configurable publish interval.

---

## Requirements

- **Docker** (for running the agent in a container)
- **Python 3**
- **MQTT Broker** (e.g., Mosquitto)
- Python dependencies:
  - `psutil`
  - `paho-mqtt`

---

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/agent-mqtt.git
cd agent-mqtt
```

### 2. Build the Docker Image

Build the Docker image for the MQTT agent:

```bash
docker build -t agent-mqtt .
```

### 3. Run the Docker Container

Run the Docker container with the `--privileged` flag, which grants the container access to system resources. The host machine's name is passed to the container via an environment variable:

```bash
docker run -d --name agent-mqtt-container --privileged -e HOSTNAME=$(hostname) agent-mqtt
```

- `--privileged`: Grants the container elevated permissions.
- `-e HOSTNAME=$(hostname)`: Passes the host machine's name as an environment variable to the container.

### 4. Verify the Container is Running

To verify that the container is running and sending metrics to the MQTT broker, check the container logs:

```bash
docker logs agent-mqtt-container
```

You should see output similar to:

```json
Sent: {'hostname': 'HOSTNAME', 'cpu_percent': 10.0, 'ram_percent': 50.0}
```

### 5. Configure Your MQTT Broker

Ensure your MQTT broker is running and listening on the default port (1883). You can use any MQTT broker, such as **Mosquitto**.

### 6. Monitor Metrics

The agent will publish CPU and RAM metrics every **5 seconds** to the MQTT topic `home/computer/metrics`.

You can monitor the metrics in real-time using any MQTT client, such as [MQTT Explorer](https://mqtt-explorer.com/).

---

## Python Script

Below is the Python script used by the MQTT agent to collect CPU and RAM usage and send it to the MQTT broker.

```python
import psutil
import paho.mqtt.client as mqtt
import time
import json
import os

BROKER = "YOUR_BROKER_IP"  # MQTT broker IP address
PORT = 1883                # MQTT broker port
TOPIC = "home/computer/metrics"  # MQTT topic to send the metrics
INTERVAL = 5               # Time interval (in seconds) between each publication

def get_metrics():
    hostname = os.getenv('HOSTNAME', 'default-hostname')  # Get the host machine's name
    metrics = {
        "hostname": hostname,
        "cpu_percent": psutil.cpu_percent(interval=1),  # CPU usage
        "ram_percent": psutil.virtual_memory().percent,  # RAM usage
    }
    return metrics

def main():
    client = mqtt.Client()  # Create a new MQTT client
    client.connect(BROKER, PORT)  # Connect to the MQTT broker
    
    while True:
        metrics = get_metrics()  # Get system metrics
        client.publish(TOPIC, json.dumps(metrics))  # Send metrics to the MQTT broker
        print(f"Sent: {metrics}")
        time.sleep(INTERVAL)  # Wait for the next publication

if __name__ == "__main__":
    main()
```

---

## Customization

You can customize the agent by modifying the following variables in the script:

- **`BROKER`**: Set this variable to the IP address or hostname of your MQTT broker.
- **`INTERVAL`**: Adjust the time interval (in seconds) between each publication of metrics.

---

## Integration with Home Assistant

You can easily integrate this MQTT agent with Home Assistant. For detailed instructions on how to set up MQTT sensors and use the data published by this agent, refer to the official [Home Assistant MQTT documentation](https://www.home-assistant.io/integrations/mqtt/).


## Troubleshooting

- If you encounter any issues with the Docker container not having the necessary permissions, make sure you are using the `--privileged` flag when running the container.
- Check the container logs to ensure that the agent is successfully connecting to the MQTT broker and publishing metrics.

---
