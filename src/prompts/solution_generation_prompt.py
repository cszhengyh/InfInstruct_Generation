solution_generation_prompt = f"""You are a domain expert in <DOMAIN>, solve the following question: <QUESTION>. 
Please explain your solution step by step.
Deliver your response in this format: [<EXP#>: ......, <ANS#>: ......<ED#>]. All the content must be put before '<ED#>]'. For example, the solution is "A", your response should be [<EXP#>: (Here you should explain your solution step by step), <ANS#>: A<ED#>] and can't be [<EXP#>: [<EXP#>: ......, <ANS#>: A<ED#>], <ANS#>: A [<EXP#>: ......, <ANS#>: A<ED#>]<ED#>].
"""