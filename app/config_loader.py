#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configparser import ConfigParser

def get_config(section, key):
    ini_file = 'config.ini'
    config = ConfigParser()
    config.read(ini_file)
    return config.get(section, key)