import unittest
from airflow.models import DagBag

class TestRetrieveTweets(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag()

    def test_task_count(self):
        """Checks task count of dag"""
        dag_id = 'retrieve_tweets'
        dag = self.dagbag.get_dag(dag_id)
        self.assertEqual(len(dag.tasks), 2)