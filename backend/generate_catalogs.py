import pandas as pd
import random

skills = ['Python', 'SQL', 'AWS', 'NLP', 'React', 'Machine Learning', 'Data Analysis', 'DevOps', 'FastAPI', 'Docker']

projects = []
for i in range(1, 21):
    projects.append({
        'ProjectID': f'PRJ{i:03d}',
        'ProjectTitle': f'Enterprise AI Initiative {i}',
        'RequiredSkills': ', '.join(random.sample(skills, k=random.randint(2, 4))),
        'DurationMonths': random.randint(3, 12),
        'TeamSize': random.randint(3, 8)
    })
pd.DataFrame(projects).to_csv('data/projects_catalog.csv', index=False)

courses = []
for i in range(1, 26):
    target_skill = random.choice(skills)
    courses.append({
        'CourseID': f'CRS{i:03d}',
        'CourseTitle': f'Advanced {target_skill} Mastery',
        'TargetSkill': target_skill,
        'DurationHours': random.randint(10, 40)
    })
pd.DataFrame(courses).to_csv('data/training_catalog.csv', index=False)