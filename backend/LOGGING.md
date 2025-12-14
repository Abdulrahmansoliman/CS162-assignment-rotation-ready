# Logging Configuration

## Overview

This application implements 12-factor compliant logging that treats logs as event streams written to stdout.

## Configuration

Log levels can be configured via environment variable:

```bash
export LOG_LEVEL=DEBUG  # Development
export LOG_LEVEL=INFO   # Production (default)
export LOG_LEVEL=WARNING
export LOG_LEVEL=ERROR
```

## Log Formats

**Development**: Human-readable format
```
[2025-12-14 10:30:45] INFO in registration_service: New user registered: user@example.com
```

**Production**: JSON format for log aggregation systems
```json
{"time":"2025-12-14 10:30:45", "level":"INFO", "name":"app.services.auth.registration_service", "message":"New user registered: user@example.com"}
```

## Usage in Code

```python
from flask import current_app

# Log at different levels
current_app.logger.debug('Detailed debugging information')
current_app.logger.info('General informational messages')
current_app.logger.warning('Warning messages')
current_app.logger.error('Error messages')
current_app.logger.critical('Critical issues')

# Example with context
current_app.logger.info(f'User {user_id} performed action: {action}')
```

✅ **Logs as event streams**: All logs write to stdout  
✅ **Environment-based config**: Log level via `LOG_LEVEL` env var  
✅ **No file writing**: Application doesn't manage log files  
✅ **Structured output**: JSON format in production for parsing
