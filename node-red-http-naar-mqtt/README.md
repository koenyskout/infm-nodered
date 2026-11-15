# Node-RED: HTTP to MQTT

A small demo of using Node-RED as a bridge between an HTTP device and an MQTT
broker. A simulated temperature sensor POSTs readings over HTTP, Node-RED
converts them into MQTT messages, and a client prints whatever arrives.

```
temp-sensor --HTTP POST--> node-red --MQTT publish--> mqtt-broker --> mqtt-client
                /devices/123            /tsensor/123                 (prints)
```

## Services

Defined in [docker-compose.yml](docker-compose.yml):

| Service       | What it does                                                                                   |
| ------------- | ---------------------------------------------------------------------------------------------- |
| `temp-sensor` | Python script ([temperature-sensor/](temperature-sensor/)) that POSTs a random-walk temperature (starting at 20 °C) to `http://node-red:1880/devices/123` every 2 seconds. |
| `node-red`    | Receives `POST /devices/:id`, validates the id (must be > 0, otherwise HTTP 400), wraps the body as `{"temperature": <value>}`, publishes it to MQTT topic `/tsensor/<id>`, and answers HTTP 200. |
| `mqtt-broker` | Eclipse Mosquitto broker (anonymous access allowed).                                           |
| `mqtt-client` | Python script ([mqtt-listener/](mqtt-listener/)) subscribed to `/tsensor/#` that prints each message. |

The Node-RED flow is stored in [data/node-red-data/flows.json](data/node-red-data/flows.json).

## Requirements

- Docker with Docker Compose

## Run

```sh
docker compose up --build
```

Rebuild with `--build` whenever you change a `Dockerfile` or `requirements.txt`.

You should see output like this:

```
temp-sensor  | Sent 21.4°C (HTTP 200)
mqtt-client  | /tsensor/123: {"temperature":"21.4"}
```

Stop with `Ctrl+C`, or `docker compose down` if you ran it detached (`-d`).

### Live reload while developing

```sh
docker compose watch
```

Edits to the files in `temperature-sensor/` or `mqtt-listener/` are synced into
the containers, which then restart. Dependency changes still need a rebuild.

## Ports

| Port | Purpose                                        |
| ---- | ---------------------------------------------- |
| 1880 | Node-RED editor and HTTP endpoints, http://localhost:1880 |
| 1883 | MQTT                                           |
| 8083 | MQTT over WebSockets                           |

## Try it yourself

Send a reading by hand:

```sh
curl -X POST -d 23.5 http://localhost:1880/devices/42   # -> published to /tsensor/42
curl -X POST -d 23.5 http://localhost:1880/devices/0    # -> HTTP 400
```

Watch the MQTT traffic from your own machine (needs Mosquitto's CLI tools):

```sh
mosquitto_sub -h localhost -t '/tsensor/#' -v
```

Open http://localhost:1880 to inspect or edit the flow. Changes are saved to
`data/node-red-data/`.

## Troubleshooting

- **`temp-sensor` prints `Failed to send: ...`**: Node-RED is probably still
  starting. The sensor retries every 2 seconds, so it recovers by itself.
- **Nothing shows up in `mqtt-client`**: check that the flow is deployed in the
  Node-RED editor and that `docker compose ps` shows all four services running.
