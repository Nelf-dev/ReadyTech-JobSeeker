import pytest
import pandas as pd
import source.jobseeker as jobseeker

df_large_seekers = pd.read_csv('source/jobseekersLarge.csv')
df_jobs = pd.read_csv('source/jobs.csv')

result = jobseeker.process_jobseekers(df_large_seekers,df_jobs)

def test_complete_process_jobseekers():
    assert len(result) == 1000
