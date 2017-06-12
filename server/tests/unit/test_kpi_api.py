# server/tests/unit/test_kpi_api.py

import json
from app.models import Sale, Customer, Traffic, Email
from tests.base import BaseTestClass
from tests.sample_data import data1, kpis


class KpiPOSTTest(BaseTestClass):

    def kpi_for_week(self, week=0):
        assert week < min(list(map(
            len, [
                kpis['sales'],
                kpis['customers'],
                kpis['traffic'],
                kpis['emails']
            ]
        )))
        return {
            'sales': kpis['sales'][week],
            'customers': kpis['customers'][week],
            'traffic': kpis['traffic'][week],
            'emails': kpis['emails'][week],
        }

    def test_post_empty_metrics(self):
        company_id = self.get_id_from_POST(data1)

        response = self.send_POST(
            f'/companies/{company_id}',
            data=''
        )

        response_ = json.loads(response.data.decode())

        self.assert400(response)
        self.assertIn('failure', response_['status'])
        self.assertIn('empty metrics', response_['message'])

    def test_one_of_the_metrics_is_empty(self):
        company_id = self.get_id_from_POST(data1)

        # The assumption is that it's okay to add only 2 or 3
        # fields out of 4, but if there are 4 fields and there is
        # blank data for one of the fields then return an error
        response = self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': kpis['sales'][0],
                'customers': '',
                'traffic': kpis['traffic'][0],
                'emails': kpis['emails'][0],
            }
        )
        response_ = json.loads(response.data.decode())

        self.assert400(response)
        self.assertIn('failure', response_['status'])
        self.assertIn(
            'one of the metrics is empty',
            response_['message']
        )

    def test_post_to_invalid_company(self):
        response = self.send_POST('/companies/1233', data=self.kpi_for_week(0))

        self.assert404(response)

        response_ = json.loads(response.data.decode())
        self.assertIn('failure', response_['status'])
        self.assertIn('company not found', response_['message'])

    def test_post_all_kpis_to_company_message(self):
        """>\tPOST all the KPIs successfully and returns the correct message"""
        company_id = self.get_id_from_POST(data1)
        data = self.kpi_for_week()
        response = self.send_POST(
            f'/companies/{company_id}',
            data=data
        )
        response_ = json.loads(response.data.decode())
        self.assert200(response)
        self.assertIn('success', response_['status'])
        self.assertIn('metrics added', response_['message'])
        self.assertIn('metrics_added', response_)
        for metric in response_['metrics_added']:
            self.assertEqual(response_['metrics_added'][metric], data[metric])

    def test_post_one_kpi_to_company_message(self):
        """>\tPOST just one KPI successfully and returns the correct message"""
        company_id = self.get_id_from_POST(data1)
        response = self.send_POST(
            f'/companies/{company_id}',
            data={
                'sales': 123
            }
        )
        response_ = json.loads(response.data.decode())
        self.assert200(response)
        self.assertIn('success', response_['status'])
        self.assertIn('metrics added', response_['message'])
