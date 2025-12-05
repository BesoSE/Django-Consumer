# Django Consumer

Django Consumer is a Django-based microservice responsible for consuming **Order** and **User** events from Apache Pulsar. It listens to Pulsar topics, validates messages using Avro schemas, and processes them into Django models for persistence and business logic.

## Features

- Consumes Order and User events from Apache Pulsar
- Validates messages using Avro schemas
- Automatic background consumer loop with reconnection
- Persists events into Django models
- Supports Docker-based deployment (Pulsar started separately)

## Running the Project

Start the Django Consumer using Docker Compose:

docker-compose up

After startup, the application (if it exposes endpoints) will be available at:
http://localhost:8001

Note: Apache Pulsar is not included in docker-compose and must be started manually.

## Running Pulsar Manually

Start Apache Pulsar standalone using Docker:

docker run -it -p 6650:6650 -p 8080:8080 \
  --mount source=pulsardata,target=/pulsar/data \
  --mount source=pulsarconf,target=/pulsar/conf \
  apachepulsar/pulsar:4.0.0 bin/pulsar standalone

This will run Pulsar standalone on:
- Pulsar protocol port: 6650
- Admin/API port: 8080

Make sure Pulsar is running before starting the Django Consumer.

## Pulsar Integration

The service integrates with Apache Pulsar to consume structured domain events.

Workflow:
1. A new event (Order or User) is published upstream.
2. Django Consumer subscribes to the topic and receives the message.
3. The Avro schema validates the structure.
4. The data is transformed into Django models.
5. The event is persisted or processed internally.
6. Logs or side effects are triggered as needed.

Pulsar schemas are located in:
pulsar_schemas/schemas/
