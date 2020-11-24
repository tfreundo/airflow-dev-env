import airflow
from operators.mongodb_operators import MongoDbExtractAndLoadOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago

args = {
    'owner': 'tfreundo',
    'start_date': days_ago(1),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False
}
dag = DAG(dag_id='mongodb_extract_and_load_dag', default_args=args, schedule_interval=None, concurrency=1, max_active_runs=1,
          catchup=False)

t_extract_and_load_data = MongoDbExtractAndLoadOperator(
    task_id='mongo_extract_and_load',
    mongo_source_conn_id="mongo_default",
    mongo_source_collection="zips",
    mongo_source_database="test",
    mongo_source_query={},
    mongo_sink_conn_id="mongo_default",
    mongo_sink_collection="zips",
    mongo_sink_database="analytics",
    # Activated for debugging
    log_result=True,
    dag=dag
)

t_extract_and_load_data