#!/usr/bin/python3
"""A module that initializes an instance of `FileStorage` class.
"""
# Task 5:
from models.engine import file_storage


storage = file_storage.FileStorage()
storage.reload()
