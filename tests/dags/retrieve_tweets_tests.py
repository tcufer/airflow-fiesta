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

    # def test_contain_tasks(self):
    #     """Check task contains in hello_world dag"""
    #     dag_id='retrieve_tweets'
    #     dag = self.dagbag.get_dag(dag_id)
    #     tasks = dag.tasks
    #     task_ids = list(map(lambda task: task.task_id, tasks))
    #     self.assertListEqual(task_ids, ['twitter_feed', 'csv_to_postgres'])