import pandas
import pdb

df_seekers = pandas.read_csv('jobseekersTEST.csv')
df_seekers_sorted = df_seekers.sort_values(by='id')

df_jobs = pandas.read_csv('jobs.csv')

ranked_jobs_for_seekers = pandas.DataFrame(columns=['jobseeker_id', 'jobseeker_name', 'job_id', 'job_title', 'matching_skill_count', 'matching_skill_percent'])

def process_jobseeker(jobseeker):
    global ranked_jobs_for_seekers

    seeker_skills_array = [lang.strip() for lang in jobseeker['skills'].split(",")]
    seeker_skills_set = set(seeker_skills_array)

    seeker_jobs = []

    for index, job in df_jobs.iterrows():
        job_skills_array = [lang.strip() for lang in job['required_skills'].split(",")]
        job_skills_set = set(job_skills_array)
        matching_skills = seeker_skills_set.intersection(job_skills_set)
        matching_skill_count = len(matching_skills)
        matching_skill_percent = matching_skill_count/len(job_skills_array) * 100

        new_data = {
            'jobseeker_id': jobseeker['id'],
            'jobseeker_name': jobseeker['name'],
            'job_id': job['id'],
            'job_title': job['title'],
            'matching_skill_count': matching_skill_count,
            'matching_skill_percent': matching_skill_percent
        }
        seeker_jobs.append(new_data)

    sorted_seeker_jobs = sorted(seeker_jobs, key=lambda x: (-x['matching_skill_percent'], x['job_id']))

    ranked_jobs_for_seekers = ranked_jobs_for_seekers.append(sorted_seeker_jobs, ignore_index=True)

df_seekers_sorted.apply(process_jobseeker, axis=1)
ranked_jobs_for_seekers.to_csv('output_file.csv', index=False)
