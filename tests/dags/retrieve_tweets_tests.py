import unittest
from airflow.models import DagBag

class TestRetrieveTweets(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = 'retrieve_tweets'
        self.tasks = ['twitter_feed', 'csv_to_postgres']

    def test_task_count(self):
        """Checks task count of dag"""
        dag = self.dagbag.dags[self.dag_id]
        self.assertEqual(len(dag.tasks), 2)

    def test_contain_tasks(self):
        """Check task contains in retrieve_tweets dag"""
        dag = self.dagbag.dags[self.dag_id]
        tasks = dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(sorted(task_ids), sorted(self.tasks))