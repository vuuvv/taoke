#!/usr/bin/env python
import os
import sys

vendor_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "vendor"
)

sys.path.insert(0, os.path.abspath(vendor_path))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
