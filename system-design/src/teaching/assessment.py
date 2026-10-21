"""Assemble separate questions and explained answers; preserve Unit 1."""
from resources import EXERCISES
from teaching.review import QUESTIONS,TASKS,DESIGN,THOUGHT,THOUGHT_ANSWERS,CASE_ASSESSMENT


def all_exercises():
    result={1:list(EXERCISES)}
    for n,items in QUESTIONS.items():
        rows=[]
        for j,(question,answer) in enumerate(items):
            kind='conceptual' if j<5 else 'scenario'
            ident='C'+str(j+1) if j<5 else 'S'+str(j-4)
            rows.append((kind,ident,question,answer))
        rows.append(('design','D1',*DESIGN[n]))
        rows.append(('implementation','I1',*TASKS[n]))
        rows.append(('thought_experiment','T1',THOUGHT[n],THOUGHT_ANSWERS[n]))
        result[n]=rows
    result[22]=list(CASE_ASSESSMENT)
    return result
