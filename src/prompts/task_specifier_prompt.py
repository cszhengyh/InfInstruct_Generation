PER_QUERY_QCNT = 5

different_audiences = ['high school student', 'college student', '<DOMAIN> expert or researcher who hold or are pursuing PhD']
difficulty_level = 'and extremely difficult graduate-level '
question_type = 'objective calculation '

research_question_requirement = """2. The <TYPE>questions should be uncommon or complex applications of well-known principles in the subtopic <SUBTOPIC>.
3. The <TYPE>questions should appeal to many different concepts from <DOMAIN>, such that answering correctly requires synthesizing knowledge across a broad range of areas.
4. The <TYPE>questions should contain concepts or techniques that are often misunderstood or misused in the subtopic <SUBTOPIC>, even by professionals in <DOMAIN>.
5. The <TYPE>questions should be about difficult aspects of the subtopic <SUBTOPIC> and niche or specialized areas within <SUBTOPIC> that are not commonly addressed in general educational resources (there is likely to be less information easily available online in these areas).
6. The <TYPE>questions are impossible for non-experts (the non-experts may be experts in domains other than <DOMAIN>) to answer, even with the whole internet at their disposal. 
7. If <DOMAIN> experts want to solve these problems, they need extensive background knowledge or an understanding of multiple concepts."""

task_specifier_prompt = f"""From this <DOMAIN> subject <TOPIC> and this subtopic <SUBTOPIC> we need to write {PER_QUERY_QCNT} different high-quality <DIFFICULTY><TYPE>questions for a <ROLE> to solve. 
Here are some suggestions and strategies for writing <TYPE>questions:
1. The <TYPE>questions should have a clear, objective answer. 
<REQUIREMENTS>
Please write {PER_QUERY_QCNT} precise problems for the <ROLE> to solve and maximise the variety of question types and knowledge points. No question number required. 
Deliver your response in this format: [<BEG#>: ......<ED#>]. All the content of the problems must be put before '<ED#>]'. For example, the {PER_QUERY_QCNT} problems are "A", "B", "C", your response should be 
[<BEG#>: 
<QUES#> A
<QUES#> B
<QUES#> C
<ED#>]
"""