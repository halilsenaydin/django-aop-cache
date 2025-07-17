# Core

Reusable core components for Django-based projects and microservices.

## Author

**Halil İbrahim ŞENAYDIN**  
E-mail: halilsenaydin@gmail.com  
GitHub: [github.com/halilsenaydin](https://github.com/halilsenaydin)

## Project Overview

The `core` package is a lightweight and modular Python library that provides foundational building blocks for Django projects. It consolidates common functionalities — such as caching, messaging, constants, utilities, and standardized API responses — into a single, reusable location. This improves consistency and eliminates code duplication across services.

- **Cache**: Reusable caching strategies and helpers (e.g., Redis-backed logic).
- **Context**: Thread-local and context-aware utilities for multi-tenant or request-aware operations.
- **Constants**: Centralized definition of constants and localization keys.
- **Locales**: Translation support with `.po` and `.mo` files.
- **Messaging**: Event/message abstraction for service communication (e.g., Kafka, RabbitMQ).
- **Results**: Standardized success/error response wrappers for APIs.
- **Serializers**: Shared DRF serializer logic across apps or services.
- **Tasks**: Common background task logic for Celery.
- **Utils**: General-purpose utility functions and helpers.
- **Views**: Abstract base views and reusable API mixins for DRF.

## Installation

Install via pip (from PyPI or your private package index):

```bash
pip install core
```

## Usage

Import and use the modules in your Django or DRF projects:

```python
from core.cache.factory import CacheManagerFactory
from core.constants import MessageConstant
from core.context.cache_context import CacheContext
from core.messaging.factory import MessageBrokerFactory
from core.results import SuccessResult
from core.serializers import SuccessResultSerializer
from core.utils import CacheUtil
from core.views import BaseModelViewSet
```

## Localization

`core` includes localization support with `.po` files in the `locales/` directory.
To use these translations in your Django project, add the core locale path to your `LOCALE_PATHS` setting:

```python
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locales'),
    os.path.join(BASE_DIR, 'path_to_core/core/locales'),
]
```

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this code for both personal and commercial purposes.

See the [LICENSE](../LICENSE) file for full license text.
