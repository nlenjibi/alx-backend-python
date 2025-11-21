#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

This minimal `manage.py` points to the bundled settings module used in this
exercise: `messaging_app.messaging_app.settings`.
"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.messaging_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
