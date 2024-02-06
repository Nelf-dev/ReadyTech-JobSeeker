import pandas as pd
import math

def process_jobseeker(jobseeker, df_jobs, ranked_jobs_for_seekers):
    seeker_skills_array = [lang.strip() for lang in jobseeker['skills'].split(",")]
    seeker_skills_set = set(seeker_skills_array)

    seeker_jobs = []

    for index, job in df_jobs.iterrows():
        job_skills_array = [lang.strip() for lang in job['required_skills'].split(",")]
        job_skills_set = set(job_skills_array)

        matching_skills = seeker_skills_set.intersection(job_skills_set)
        matching_skill_count = len(matching_skills)

        matching_skill_value = matching_skill_count / len(job_skills_array)
        matching_skill_percent = '{:.0%}'.format(matching_skill_value)

        new_data = {
            'jobseeker_id': jobseeker['id'],
            'jobseeker_name': jobseeker['name'],
            'job_id': job['id'],
            'job_title': job['title'],
            'matching_skill_count': matching_skill_count,
            'matching_skill_percent': matching_skill_percent
        }
        seeker_jobs.append(new_data)

    sorted_seeker_jobs = sorted(seeker_jobs, key=lambda x: (-float(x['matching_skill_percent'].strip('%')), x['job_id']))

    ranked_jobs_for_seekers = ranked_jobs_for_seekers.append(sorted_seeker_jobs, ignore_index=True)

    return ranked_jobs_for_seekers

def process_jobseekers(jobseekers, df_jobs):
    ranked_jobs_for_seekers = pd.DataFrame(columns=[
        'jobseeker_id',
        'jobseeker_name',
        'job_id',
        'job_title',
        'matching_skill_count',
        'matching_skill_percent'
    ])

    jobseekers_sorted = jobseekers.sort_values(by='id')
    for index, jobseeker in jobseekers_sorted.iterrows():
        ranked_jobs_for_seekers = process_jobseeker(jobseeker, df_jobs, ranked_jobs_for_seekers)

    print(ranked_jobs_for_seekers)
    return ranked_jobs_for_seekers

if __name__ == '__main__':
    df_seekers = pd.read_csv('source/jobseekers.csv')
    df_jobs = pd.read_csv('source/jobs.csv')
    process_jobseekers(df_seekers, df_jobs)
