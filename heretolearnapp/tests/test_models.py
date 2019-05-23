# JSON
import json
from pprint import pprint

# HTTP testing
from vcr_unittest import VCRTestCase
import requests
import vcr

my_vcr = vcr.VCR(
    serializer='json',
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)

from django.test import TestCase
from django.utils import timezone

from heretolearnapp.models import Question # tutorial stuff
# from .models import Iris
# from .serializers import IrisSerializer

class IrisesApiTests(VCRTestCase):

    with my_vcr.use_cassette('fixtures/vcr_cassettes/irises/all.yaml'):
        def test_get_all_irises(self):
            """
            This test ensures that all irises stored in database from rails
            app are received in a GET request to the irises/ endpoint
            """
            response = requests.get('http://localhost:3000/api/v1/irises').json()

            iris_attributes = response['data'][0]['attributes'].values()

            self.assertEqual(150, len(response['data']))
            self.assertEqual(5, len(iris_attributes))
