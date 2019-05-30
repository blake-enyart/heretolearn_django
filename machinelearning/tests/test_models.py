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

# Debugging
import IPython
from IPython import embed

from machinelearning.predict import SinatraApi, ParseSurveyData

class MachineLearningTests(TestCase):
    with my_vcr.use_cassette('fixtures/vcr_cassettes/predict/responses.json', record_mode='none'):
        def test_parse_response_correctly(self):
            """
            This test ensures that all responses are from sinatra app are
            parsed correctly in a GET request to the aqueous-caverns-33840.herokuapp.com/api/v1/responses
            endpoint
            """
            url = 'https://aqueous-caverns-33840.herokuapp.com/api/v1/responses'

            self.assertTrue(isInstance(ParseSurveyData.__get_json(cls,url)), Dictionary)
