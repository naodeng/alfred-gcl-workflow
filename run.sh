#!/usr/bin/env bash
# Wrapper so Alfred can run the Python script without execute permission on .py
cd "$(dirname "$0")"
exec /usr/bin/env python3 generate_number.py "$@"
