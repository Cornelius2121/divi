import os, sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from unittest import TestCase
from app import app
import json
from unittest.mock import patch


class Test(TestCase):
    def test_create_no_absolute_rules(self):
        with patch("app.session", dict()) as self.session:
            self.client = app.test_client()
            # send data as POST form to endpoint
            sent = json.dumps([{'people': ['T', 'K', 'C', 'M']}, {'count': '1'}, {
                'rules': [{'personA': 'T', 'personB': 'K', 'Year': 2022},
                          {'personA': 'K', 'personB': 'T', 'Year': 2022},
                          {'personA': 'C', 'personB': 'M', 'Year': 2022},
                          {'personA': 'M', 'personB': 'C', 'Year': 2022}]}])
            result = self.client.post(
                '/create',
                data=sent,
                content_type='application/json'
            )
            # check result from server with expected data
            self.assertEqual(
                self.session.get('assignments'),
                ['T is buying for C', 'K is buying for M', 'C is buying for T', 'M is buying for K']
            )

    def test_create_absolute_rules(self):
        with patch("app.session", dict()) as self.session:
            self.client = app.test_client()
            # send data as POST form to endpoint
            sent = json.dumps([{'people': ['T', 'K', 'M', 'C']}, {'count': '1'}, {
                'rules': [{'personA': 'T', 'personB': 'C', 'Year': '2022'},
                          {'personA': 'K', 'personB': 'M', 'Year': '2022'},
                          {'personA': 'M', 'personB': 'T', 'Year': '2022'},
                          {'personA': 'C', 'personB': 'K', 'Year': '2022'},
                          {'personA': 'T', 'personB': 'K'},
                          {'personA': 'K', 'personB': 'T'},
                          {'personA': 'C', 'personB': 'M'},
                          {'personA': 'M', 'personB': 'C'}]}])
            result = self.client.post(
                '/create',
                data=sent,
                content_type='application/json'
            )
            # check result from server with expected data
            self.assertEqual(
                self.session.get('assignments'),
                ['T is buying for M', 'K is buying for C', 'M is buying for K', 'C is buying for T']
            )
