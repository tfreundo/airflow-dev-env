from bson import json_util
import json
import logging
from airflow.models import BaseOperator
from hooks.mongodb_hook import MongoDbHook

# See as reference: https://github.com/airflow-plugins/mongo_plugin/blob/master/operators/mongo_to_s3_operator.py

class MongoDbExtractAndLoadOperator(BaseOperator):
    """
    MongoDbExtractAndLoadOperator
    :param mongo_source_conn_id:        The connection id of source.
    :type mongo_source_conn_id:         string
    :param mongo_source_collection:     The collection of the source.
    :type mongo_source_collection:      string
    :param mongo_source_database:       The source database.
    :type mongo_source_database:        string
    :param mongo_source_query:          The query to use on the source.
    :type mongo_source_query:           string
    :param mongo_sink_conn_id:          The connection id of sink.
    :type mongo_sink_conn_id:           string
    :param mongo_sink_collection:       The collection of the sink.
    :type mongo_sink_collection:        string
    :param mongo_sink_database:         The sink database.
    :type mongo_sink_database:          string
    :param log_result:                  Whether the first 1000 characters of the query result should be logged or not (default False).
    :type log_result:                   bool
    """

    # Allow templating for those fields
    template_fields = ['mongo_source_query']

    def __init__(self,
                 mongo_source_conn_id,
                 mongo_source_collection,
                 mongo_source_database,
                 mongo_source_query,
                 mongo_sink_conn_id,
                 mongo_sink_collection,
                 mongo_sink_database,
                 log_result=False,
                 *args, **kwargs):
        super(MongoDbExtractAndLoadOperator, self).__init__(*args, **kwargs)
        self.mongo_source_conn_id = mongo_source_conn_id
        self.mongo_source_collection = mongo_source_collection
        self.mongo_source_database = mongo_source_database
        self.mongo_source_query = mongo_source_query
        self.mongo_sink_conn_id = mongo_sink_conn_id
        self.mongo_sink_collection = mongo_sink_collection
        self.mongo_sink_database = mongo_sink_database
        self.log_result = log_result
        # Amount of characters to log
        self.log_result_len = 2000
        # KWARGS
        self.replace = kwargs.pop('replace', False)

    def execute(self, context):
        """
        Executed by task instance at runtime
        """
        logging.info("Creating Mongo Clients for source and sink databases ...")
        mongoclient_source = MongoDbHook(
            self.mongo_source_conn_id).get_mongo_client()
        mongoclient_sink = MongoDbHook(
            self.mongo_sink_conn_id).get_mongo_client()
        counter = 0
        for doc in mongoclient_source[self.mongo_source_database][self.mongo_source_collection].find(
                self.mongo_source_query):
            counter+=1
            # Remove internal id 
            del doc["_id"]
            mongoclient_sink[self.mongo_sink_database][self.mongo_sink_collection].insert_one(
                doc)
        logging.info("Copied {} documents from source to sink".format(counter))

    def _cursor_to_string(self, docs, joinable='\n'):
        """
        Create a string from an array (transform pymongo Cursor to array beforehand)
        """
        return joinable.join([json.dumps(doc, default=json_util.default) for doc in docs])

    def _cursor_to_array(self, docs):
        """
        Converts a pymongo cursor object to an array
        """
        return [doc for doc in docs]
