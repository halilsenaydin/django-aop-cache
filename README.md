# Django AOP Cache

A modular Django project demonstrating aspect-oriented programming (AOP) techniques for caching, messaging, context handling, and signal-based automation. This project is built to serve as a reusable foundation for scalable Django microservices.

## Author

**Halil İbrahim ŞENAYDIN**  
E-mail: halilsenaydin@gmail.com  
GitHub: [github.com/halilsenaydin](https://github.com/halilsenaydin)

## Dependencies

Ensure you have the following software installed on your machine:

- [Docker Desktop](https://www.docker.com/get-started)

## Project Overview

- **AOP-style Caching**: Clean and reusable `@cache_update`, `@cache_invalidate` decorators.
- **Context Handling**: Request-local and thread-local context propagation.
- **Localization**: Built-in `.po` file support and structured message keys.
- **Signals**: Automatic handling of user model changes (`post_save`, `post_delete`, `m2m_changed`).
- **Redis Integration**: High-performance distributed cache backend.
- **RabbitMQ Integration**: Event publishing using fanout exchange via abstracted messaging layer.
- **Celery Ready**: Async event dispatch using Celery tasks.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL (one per microservice)
- **Containerization & Orchestration**: Docker, Docker Compose

## Getting Started

To build and start all services:

```bash
docker-compose up --build
```

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this code for both personal and commercial purposes.

See the [LICENSE](./LICENSE) file for full license text.
