from unittest import TestCase
from app import app
import json
from unittest.mock import patch


class Test(TestCase):
    def test_create(self):
        with patch("app.session", dict()) as session:
            client = app.test_client()
            # send data as POST form to endpoint
            sent = json.dumps([{'people': ['T', 'K', 'C', 'M']}, {'count': '1'}, {
                'rules': [{'personA': 'T', 'personB': 'K', 'Year': 2022},
                          {'personA': 'K', 'personB': 'T', 'Year': 2022},
                          {'personA': 'C', 'personB': 'M', 'Year': 2022},
                          {'personA': 'M', 'personB': 'C', 'Year': 2022}]}])
            result = client.post(
                '/create',
                data=sent,
                content_type='application/json'
            )
            # check result from server with expected data
            self.assertEqual(
                session.get('assignments'),
                ['T is buying for C', 'K is buying for M', 'C is buying for T', 'M is buying for K']
            )
