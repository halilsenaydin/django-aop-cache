# Changelog

## Version 1.0.0 · 2025-07-17 · @halilsenaydin

### Added

- Initial release of the Django AOP-based core utilities package.
- Integrated modular structure with the following components:
  - **Cache**: AOP-style caching decorators (`@cache_update`, `@cache_invalidate`) for views, signals, and services.
  - **Context**: Request-local context utilities for multi-tenant or per-request processing.
  - **Locales**: Localization and i18n support using `.po` files and a structured message key system.
  - **Signals**: User model signal listeners (`post_save`, `post_delete`, `m2m_changed`) with event publishing.
  - **Redis**: Built-in Redis support for caching and context sharing across distributed services.
  - **RabbitMQ**: Message broker integration with a `fanout`-based event publishing system via abstract factory.
- Example user service implementation demonstrating all components in action.
- Ready-to-extend architecture for microservices built with Django and Celery.
