import unittest
from airflow.models import DagBag

class TestRetrieveTweets(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = 'retrieve_tweets_and_quotes'
        self.dag = self.dagbag.dags[self.dag_id]
        self.tasks = ['twitter_feed', 'csv_to_postgres_1', 'goodreads_quotes', 'csv_to_postgres_2']

    def test_task_count(self):
        """Checks task count of dag"""
        self.assertEqual(len(self.dag.tasks), 4)

    def test_contain_tasks(self):
        """Check task contains in retrieve_tweets dag"""
        tasks = self.dag.tasks
        task_ids = list(map(lambda task: task.task_id, tasks))
        self.assertListEqual(sorted(task_ids), sorted(self.tasks))

    def test_dependencies_of_twitter_feed_task(self):
        """Check the task dependencies of twitter_feed task"""
        dummy_task = self.dag.get_task('twitter_feed')
        upstream_task_ids = list(map(lambda task: task.task_id, dummy_task.upstream_list))
        self.assertListEqual(upstream_task_ids, [])
        downstream_task_ids = list(map(lambda task: task.task_id, dummy_task.downstream_list))
        self.assertListEqual(downstream_task_ids, ['csv_to_postgres_1'])

    def test_dependencies_of_csv_to_postgres_2_task(self):
        """Check the task dependencies of csv_to_postgres_1 task"""
        dummy_task = self.dag.get_task('csv_to_postgres_1')
        upstream_task_ids = list(map(lambda task: task.task_id, dummy_task.upstream_list))
        self.assertListEqual(upstream_task_ids, ['twitter_feed'])
        downstream_task_ids = list(map(lambda task: task.task_id, dummy_task.downstream_list))
        self.assertListEqual(downstream_task_ids, ['goodreads_quotes'])

    def test_dependencies_of_goodreads_quotes_task(self):
        """Check the task dependencies of goodreads_quotes task"""
        dummy_task = self.dag.get_task('goodreads_quotes')
        upstream_task_ids = list(map(lambda task: task.task_id, dummy_task.upstream_list))
        self.assertListEqual(upstream_task_ids, ['csv_to_postgres_1'])
        downstream_task_ids = list(map(lambda task: task.task_id, dummy_task.downstream_list))
        self.assertListEqual(downstream_task_ids, ['csv_to_postgres_2'])

    def test_dependencies_of_csv_to_postgres_1_task(self):
        """Check the task dependencies of csv_to_postgres_2 task"""
        dummy_task = self.dag.get_task('csv_to_postgres_2')
        upstream_task_ids = list(map(lambda task: task.task_id, dummy_task.upstream_list))
        self.assertListEqual(upstream_task_ids, ['goodreads_quotes'])
        downstream_task_ids = list(map(lambda task: task.task_id, dummy_task.downstream_list))
        self.assertListEqual(downstream_task_ids, [])