import airflow
from operators.mongodb_operators import MongoDbOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago

args = {
    'owner': 'tfreundo',
    'start_date': days_ago(1),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False
}
dag = DAG(dag_id='mongodb_dag', default_args=args, schedule_interval=None, concurrency=1, max_active_runs=1,
          catchup=False)

t_query_data = MongoDbOperator(
    task_id='mongo_query',
    mongo_conn_id="mongo_default",
    mongo_collection="zips",
    mongo_database="test",
    mongo_query={},
    # Activated for debugging
    log_result=True,
    dag=dag
)

t_query_data