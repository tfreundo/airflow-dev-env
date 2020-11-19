import airflow
from airflow.operators.bash_operator import BashOperator
from airflow.models import DAG
from airflow.utils.dates import days_ago

args = {
    'owner': 'tfreundo',
    'start_date': days_ago(1),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False
}
dag = DAG(dag_id='example_dag', default_args=args, schedule_interval=None, concurrency=1, max_active_runs=1,
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