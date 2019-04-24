"""Script to start the ingestion gateway."""

from ingestion_gateway import Gateway

if __name__ == '__main__':
    gateway = Gateway()
    gateway.run()