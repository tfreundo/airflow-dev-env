import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from datetime import datetime, timedelta
args = {
    'owner': 'Yourself',
    'start_date': datetime(2018, 12, 2, 16, 40, 0),
    'email': ['Yourself@mail.tech'],
    'email_on_failure': False,
    'email_on_retry': False
}
dag = DAG(dag_id='example_dag', default_args=args, schedule_interval='@daily', concurrency=1, max_active_runs=1,
          catchup=False)
task_1 = BashOperator(
    task_id='task_1',
    bash_command='echo Wow, your first DAG ...',
    dag=dag
)
task_2 = BashOperator(
    task_id='task_2',
    bash_command='echo ... which even has two operators! So much wow!',
    dag=dag
)
task_1 >> task_2