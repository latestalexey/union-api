# server/tests/functional/test_interacting_from_brandery_staff.py

import json
from tests.base import BaseTestClass
from tests.sample_data import data1, data2, data3


class InterfacingFromBranderyTest(BaseTestClass):

    def test_get_all_companies(self):
        # The PM heard their interns just build a really
        # solid API server for retrieving startups' data from
        # the Union dashboard.
        # Hoping the salary budget won't go to waste, he firsthand
        # decides to try fetching all the companies' info to see
        # if the tech interns are any good.

        # First, he needs to enters some mock data.
        self.send_POST('/companies', data1)
        self.send_POST('/companies', data2)
        self.send_POST('/companies', data3)

        # Now he queries for all the companies' data
        response = self.client.get('/companies')
        response_ = json.loads(response.data.decode())
        companies = response_['companies']

        # He gets an array of length 3, which is neat
        self.assertEqual(response_['total'], 3)
        self.assertEqual(len(companies), 3)

        # In every entry of the array there is
        # sufficient data including name, bio, website,
        # and founders' info
        for company in companies:
            self.assertIn('name', company)
            self.assertIn('founders', company)
            self.assertIn('bio', company)
            self.assertIn('website', company)

        # Then he realizes shit gets real and he
        # has never been mistaken to hand over the
        # grandiose job of humanity to the interns
