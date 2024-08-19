PROBLEMS_PATH = ""
SOLUTIONS_PATH = ""
DATASET_DIR = ""

import re
import os
import json
from collections import defaultdict

domains, topics, subtopics, problems, solutions = [], [], [], [], []

with open(PROBLEMS_PATH, 'r', encoding='utf-8') as problems_file:
    for line in problems_file:
        domain_topic_subtopic = re.findall(r'([^:]+)', line)[0].split('->')
        # print(domain_topic_subtopic)
        # print(line)
        domain = domain_topic_subtopic[0]
        topic = domain_topic_subtopic[1]
        subtopic = domain_topic_subtopic[2]
        question = re.findall(r': \s*(.*)', line)[0]
        domains.append(domain)
        topics.append(topic)
        subtopics.append(subtopic)
        problems.append(question)

with open(SOLUTIONS_PATH, 'r', encoding='utf-8') as solutions_file:
    for solution in solutions_file:
        solutions.append(solution)

if len(domains) == len(topics) == len(subtopics) == len(problems) == len(solutions):
    for idx in range(0, len(domains)):
        data = defaultdict(lambda: -1)
        data['domain'] = domains[idx]
        data['topic'] = topics[idx]
        data['subtopic'] = subtopics[idx]
        data['problem'] = problems[idx]
        data['solution'] = solutions[idx]
        data_path = os.path.join(DATASET_DIR, f"{str(idx).zfill(6)}.json")
        with open(data_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
else:
    print("domains, problems, solutions length is not equal")
    print(f"length- domains: {len(domains)}, topics: {len(topics)}, subtopics: {len(subtopics)}, problems: {len(problems)}, solutions: {len(solutions)}")