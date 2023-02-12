#!/usr/bin/python3
"""A module that initializes an instance of `FileStorage` class.
"""
from models.engine import file_storage
storage = file_storage.FileStorage()
storage.reload()
