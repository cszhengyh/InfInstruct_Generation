import re
import math
from chat_with_gpt import chat_with_gpt
from tqdm import tqdm
from prompts.task_specifier_prompt import task_specifier_prompt, PER_QUERY_QCNT, different_audiences, difficulty_level, research_question_requirement, question_type

TOPICS_PATH = ""
PROBLEM_OUT_PATH = ""
PER_TOPIC_PER_ROLE_PROBLEM_CNT = 35

def generate_questions(query):
    with open(PROBLEM_OUT_PATH, 'a', encoding='utf-8') as outfile:
        while True:
            # gpt4o
            response = chat_with_gpt(query)

            print(response)

            if re.findall(r'\[<BEG#>:\s*(.*?)<ED#>\]', repr(response).strip('\'"')):
                temp = repr(response).strip('\'"')
                questions = temp[temp.find('[<BEG#>:')+len('[<BEG#>:'):temp.find('<ED#>]')].strip()
                if 'BEG#' in questions or 'ED#' in questions:
                    continue
                questions = questions.split("<QUES#>")

                cnt = 0
                for question in questions:
                    question = question.strip()
                    question = question.strip(r'\n')
                    if question == '':
                        continue
                    cnt += 1
                
                if cnt != PER_QUERY_QCNT:
                    print(cnt)
                    continue            

                for question in questions:
                    question = question.strip()
                    question = question.strip(r'\n')
                    if question == '':
                        continue
                    outfile.write(f"{domain}->{topic}->{subtopic}: {question}\n")
                break           
            else:
                continue     

def mmlu_problems(domain, topic, subtopic):
    for i in range(0, math.ceil(PER_TOPIC_PER_ROLE_PROBLEM_CNT/PER_QUERY_QCNT)):
        for role in different_audiences:    
            temp_task_specifier_prompt = task_specifier_prompt
            temp_research_question_requirement = research_question_requirement

            if role == 'high school student':
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<TYPE>', '')
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<DIFFICULTY>', '')
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<REQUIREMENTS>', '')
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<ROLE>', role)
            elif role == 'college student':
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<TYPE>', question_type)
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<DIFFICULTY>', '')
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<REQUIREMENTS>', '')
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<ROLE>', role)                
            else:
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<DIFFICULTY>', difficulty_level)

                role = role.replace('<DOMAIN>', domain)
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<ROLE>', role)

                temp_research_question_requirement = temp_research_question_requirement.replace('<TYPE>', question_type)
                temp_research_question_requirement = temp_research_question_requirement.replace('<DOMAIN>', domain)
                temp_research_question_requirement = temp_research_question_requirement.replace('<SUBTOPIC>', subtopic)
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<REQUIREMENTS>', temp_research_question_requirement)
            
            temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<DOMAIN>', domain)
            temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<TOPIC>', topic)
            temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<SUBTOPIC>', subtopic)

            print(role)
            print(temp_task_specifier_prompt)
            generate_questions(temp_task_specifier_prompt)            

def gpqa_problems(domain, topic, subtopic):
    for i in range(0, math.ceil(PER_TOPIC_PER_ROLE_PROBLEM_CNT/PER_QUERY_QCNT)):
        for role in different_audiences:
            temp_task_specifier_prompt = task_specifier_prompt
            temp_research_question_requirement = research_question_requirement

            temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<TYPE>', '')
            if role == 'high school student' or role == 'college student':
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<DIFFICULTY>', '')
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<REQUIREMENTS>', '')
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<ROLE>', role)
            else:
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<DIFFICULTY>', difficulty_level)

                role = role.replace('<DOMAIN>', domain)
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<ROLE>', role)

                temp_research_question_requirement = temp_research_question_requirement.replace('<TYPE>', '')
                temp_research_question_requirement = temp_research_question_requirement.replace('<DOMAIN>', domain)
                temp_research_question_requirement = temp_research_question_requirement.replace('<SUBTOPIC>', subtopic)
                temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<REQUIREMENTS>', temp_research_question_requirement)
            
            temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<DOMAIN>', domain)
            temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<TOPIC>', topic)
            temp_task_specifier_prompt = temp_task_specifier_prompt.replace('<SUBTOPIC>', subtopic)

            print("\n---------------------------------------------------\n")
            print(role)
            print(temp_task_specifier_prompt)
            generate_questions(temp_task_specifier_prompt)
        # break

out = ""
with open(TOPICS_PATH, 'r', encoding='utf-8') as topics_file:
    for line in topics_file:
        if line == '':
            continue
        subtopic = re.findall(r'label:\s*(.*?),\s*la', line)[0]
        domains_and_topics = eval(re.findall(r'label_path:\s*(.*?),\s*cou', line)[0])
        for domain_and_topic in domains_and_topics:
            if len(domain_and_topic) == 0:
                domain = 'science'
                topic = subtopic
            elif len(domain_and_topic) == 1:
                domain = 'science'
                topic = domain_and_topic[-1]
            else:
                domain = domain_and_topic[-1]
                topic = domain_and_topic[-2]
            
            gpqa_problems(domain, topic, subtopic)
            # mmlu_problems(domain, topic, subtopic)
        #     break
        # break