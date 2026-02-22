# EventPulse — Scalable Order Ingestion & Analytics Backend:

EventPulse is a production-grade backend system designed to handle large-scale order ingestion, asynchronous processing, and real-time analytics.

The system supports bulk inserts, duplicate handling, distributed rate limiting, background computation, caching, and containerized deployment.

## 🚀 Key Features:

- High-throughput ingestion API

- Bulk processing with chunking

- Duplicate order handling

- Async MongoDB operations

- Rate limiting using Redis

- Background analytics via Celery workers

- Precomputed analytics storage

- Cached read endpoints for fast responses

- Fully containerized using Docker Compose


## 🏗 Tech Stack:

- FastAPI (Async API framework)

- MongoDB (NoSQL database)

- Redis (Cache & broker)

- Celery (Task queue)

- Docker & Docker Compose (Deployment)

## What This Project Demonstrates

- Building async APIs with FastAPI

- Handling large data ingestion safely

- Designing idempotent endpoints

- Using Redis for rate limiting and caching

- Offloading heavy work to background workers

- Integrating multiple services in a single system
