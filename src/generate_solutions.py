import re
from chat_with_gpt import chat_with_gpt
from prompts.solution_generation_prompt import solution_generation_prompt

PROBLEM_PATH = ""
SOLUTION_PATH = ""

out = ""
with open(PROBLEM_PATH, 'r', encoding='utf-8') as problems:
    temp_solution_generation_prompt = solution_generation_prompt
    for problem in problems:
        if problem == '':
            continue
        domain_topic_subtopic = re.findall(r'([^:]+)', problem)[0].split('->')
        domain = domain_topic_subtopic[0]
        if domain == 'science':
            domain = domain_topic_subtopic[1]
        question = re.findall(r':\s*(.*)', problem)[0]
        solution_generation_prompt = solution_generation_prompt.replace('<QUESTION>', question)
        solution_generation_prompt = solution_generation_prompt.replace('<DOMAIN>', domain)
        with open(SOLUTION_PATH, 'a', encoding='utf-8') as outfile:
            while True:
                # gpt4o
                response = chat_with_gpt(solution_generation_prompt)

                print("\n======================================================\n")
                print(response)
                
                if re.findall(r'\[<EXP#>:\s*(.*?)<ED#>\]', repr(response).strip('\'"')):
                    temp = repr(response).strip('\'"')
                    solution = temp[temp.find('[')+len('['):temp.find('<ED#>]')].strip() # .replace(r'\\\\', '\\')
                    # print("\n--------------------Solution---------------------\n")
                    if 'ED#' in solution:
                        continue
                    elif solution.count("<ANS#>:") != 1 or solution.count("<EXP#>:") != 1:
                        continue
                    solution = solution.replace("<ANS#>:", "The correct answer:")
                    solution = solution.replace("<EXP#>:", "Here's the step-by-step justification:")
                    outfile.write(solution[solution.find('The correct answer:'):]+r'\n'+solution[:solution.find('The correct answer:')]+'\n')
                    # print(solution[solution.find('The correct answer:'):]+' '+solution[:solution.find('The correct answer:')]+'\n')
                    break
                else:
                    continue
            solution_generation_prompt = temp_solution_generation_prompt