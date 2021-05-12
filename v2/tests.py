import unittest
import json
import sys, os.path

from api import *

class TestAPI1(unittest.TestCase): 

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_pred24(self):
        response = self.app.get('/servicio/v2/prediccion/24horas/')
        self.assertEqual(response.status_code, 200)

    def test_pred48(self):
        response = self.app.get('/servicio/v2/prediccion/48horas/')
        self.assertEqual(response.status_code, 200)

    def test_pred72(self):
        response = self.app.get('/servicio/v2/prediccion/72horas/')
        self.assertEqual(response.status_code, 200)