import unittest
from airflow.models import DagBag


class TestDagIntegrity(unittest.TestCase):
    LOAD_SECOND_THRESHOLD = 1

    def setUp(self):
        self.dagbag = DagBag()

    def test_import_dags(self):
        self.assertFalse(
            len(self.dagbag.import_errors),
            'DAG import failures. Errors: {}'.format(
                self.dagbag.import_errors
            )
        )

    def test_import_time(self):
        stats = self.dagbag.dagbag_stats
        slow_dags = list(filter(lambda d: d.duration > 2, stats))
        res = ', '.join(map(lambda d: d.file[1:], slow_dags))

        self.assertEqual(0, len(slow_dags),
                          'The following files take more than {threshold}s to load: {res}'.format(
                              threshold=self.LOAD_SECOND_THRESHOLD, res=res)
                          )

    def test_alert_email_present(self):
        for dag_id, dag in self.dagbag.dags.items():
            emails = dag.default_args.get('email', [])
            msg = 'Alert email not set for DAG {id}'.format(id=dag_id)
            self.assertIn('hello@world.com', emails, msg)
