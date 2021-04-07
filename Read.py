#!/usr/bin/env python
import RPi.GPIO as GPIO
from mrfc522 import SimpleMRFC522
usuario = SimpleMRFC522
try:
    UUID = usuario.read_id()
    print(UUID)
finally:
    GPIO.cleaup()
    