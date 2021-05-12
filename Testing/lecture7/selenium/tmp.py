import os
import pathlib
import unittest

from selenium import webdriver

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

print(file_uri('counter.html'))