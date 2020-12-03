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