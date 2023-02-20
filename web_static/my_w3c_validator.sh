#!/usr/bin/env zsh
# Validates all web files (html/css/svg) files for the Airbnb Clone project

alias w3c_validator='~/W3C-Validator/w3c_validator.py'
w3c_validator ./*.html ./styles/*.css
