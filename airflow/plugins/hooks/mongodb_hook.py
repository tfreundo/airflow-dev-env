from ssl import CERT_NONE
from airflow.hooks.base_hook import BaseHook
from pymongo import MongoClient

class MongoDbHook(BaseHook):
    """
    Hook for connecting against a MongoDB using pymongo
    """
    conn_type = 'MongoDb'

    def __init__(self, conn_id='mongo_default', *args, **kwargs):
        super().__init__(source='mongo')
        self.mongo_conn_id = conn_id
        self.connection = self.get_connection(conn_id)
        self.extras = self.connection.extra_dejson

    def get_mongo_client(self):
        """
        Creates a PyMongo Client
        """
        conn = self.connection

        uri = 'mongodb://{creds}{host}{port}/{database}'.format(
            creds='{}:{}@'.format(
                conn.login, conn.password
            ) if conn.login is not None else '',

            host=conn.host,
            port='' if conn.port is None else ':{}'.format(conn.port),
            database='' if conn.schema is None else conn.schema
        )

        # MongoDB Connection Options 
        options = self.extras
        if options.get('ssl', False):
            options.update({'ssl_cert_reqs': CERT_NONE})
        return MongoClient(uri, **options)