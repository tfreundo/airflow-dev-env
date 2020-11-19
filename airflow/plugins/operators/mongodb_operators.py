from bson import json_util
import json
import logging
from airflow.models import BaseOperator
from hooks.mongo_hook import MongoHook

# See as reference: https://github.com/airflow-plugins/mongo_plugin/blob/master/operators/mongo_to_s3_operator.py


class MongoDbOperator(BaseOperator):
    """
    MongoDbOperator
    :param mongo_conn_id:           The connection id.
    :type mongo_conn_id:            string
    :param mongo_collection:        The collection.
    :type mongo_collection:         string
    :param mongo_database:          The database.
    :type mongo_database:           string
    :param mongo_query:             The query.
    :type mongo_query:              string
    :param log_result:              Whether the first 1000 characters of the result should be logged or not (default False).
    :type log_result:               bool
    """

    # Allow templating for those fields
    template_fields = ['mongo_query']

    def __init__(self,
                 mongo_conn_id,
                 mongo_collection,
                 mongo_database,
                 mongo_query,
                 log_result=False,
                 *args, **kwargs):
        super(MongoDbOperator, self).__init__(*args, **kwargs)
        self.mongo_conn_id = mongo_conn_id
        self.mongo_db = mongo_database
        self.mongo_collection = mongo_collection
        self.mongo_query = mongo_query
        self.log_result = log_result
        # Amount of characters to log
        self.log_result_len = 2000
        # KWARGS
        self.replace = kwargs.pop('replace', False)

    def execute(self, context):
        """
        Executed by task instance at runtime
        """
        connection = MongoHook(self.mongo_conn_id).get_conn()
        logging.info("Connecting to database ...")
        collection = connection.get_database(
            self.mongo_db).get_collection(self.mongo_collection)
        logging.info("Executing query ...")
        # Pymongo cursor object
        results = collection.find(self.mongo_query)
        logging.info("Found {} entries".format(results.count()))
        if self.log_result:
            logging.info("Transforming result to string ...")
            docs_str = self._cursor_to_string(self._cursor_to_array(results))
            logging.info(
                "Result (first {} characters)\n{} ...".format(self.log_result_len, docs_str[0:self.log_result_len]))

        # TODO Now you got the data, so actually do something with it ;)

    def _cursor_to_string(self, iter, joinable='\n'):
        """
        Create a string from an array (transform pymongo Cursor to array beforehand)
        """
        return joinable.join([json.dumps(doc, default=json_util.default) for doc in iter])

    def _cursor_to_array(self, docs):
        """
        Converts a pymongo cursor object to an array
        """
        return [doc for doc in docs]
