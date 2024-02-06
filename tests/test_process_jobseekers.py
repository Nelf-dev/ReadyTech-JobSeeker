import pytest
import pandas
import source.jobseeker as jobseeker

test_df = pandas.DataFrame(columns=['id', 'name', 'skills'])
df_jobs = pandas.read_csv('source/jobs.csv')

test_data = [
    {'id': 12, 'name': 'Jane Smith', 'skills': 'Java, JavaScript'},
    {'id': 11, 'name': 'John Doe', 'skills': 'Python    ,     SQL   '}
]

test_df = test_df.append(test_data, ignore_index=True)

result = jobseeker.process_jobseekers(test_df, df_jobs)

def test_complete_data_in_process_jobseekers():
    assert result.iloc[0].jobseeker_id == 11
    assert result.iloc[0].jobseeker_name == 'John Doe'
    assert result.iloc[0].job_id == 7
    assert result.iloc[0].matching_skill_count == 2
    assert result.iloc[0].matching_skill_percent == '50%'

def test_jobseeker_id_in_ascending_order():
    assert result.iloc[0].jobseeker_id < result.iloc[10].jobseeker_id

def test_matching_percent_in_descending_order():
    assert float(result.iloc[0].matching_skill_percent.strip('%')) > float(result.iloc[2].matching_skill_percent.strip('%'))

def test_matching_percent_in_ascending_order_based_on_job_id():
    assert result.iloc[0].job_id < result.iloc[1].job_id
