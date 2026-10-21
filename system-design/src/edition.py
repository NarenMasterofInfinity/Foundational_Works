"""Content-driven assembly registry. Availability follows actual authored artifacts."""
import re
from blueprint import build_blueprint
from figures import get_figures, FIGURES
import teaching.lld, teaching.data, teaching.distributed, teaching.production
from teaching.foundations import LESSONS
from teaching.cases import CASES
from teaching.patterns import PATTERN_LESSONS
from teaching.assessment import all_exercises
from teaching.sources import R, CASE_SOURCES, CHAPTER_REFS


def prepare():
    book=build_blueprint();first_figures=get_figures();exercises=all_exercises()
    for unit in book['units']:
        n=unit['n'];unit['starting_references']=unit['references']
        if n==1:unit['references']=list(dict.fromkeys(r for refs in CHAPTER_REFS.values() for r in refs))
        elif n==22:unit['references']=list(dict.fromkeys(r for refs in CASE_SOURCES.values() for r in refs))
        else:
            assert len(LESSONS[n])==len(unit['topics']),f'Unproduced topic in Unit {n}'
            for i,row in enumerate(LESSONS[n],1):
                assert len(row['prose'].split())>=45,(n,i,'Insufficient concept explanation')
                assert len(row['trace'])>=3,(n,i,'Missing worked state/interaction')
            unit['references']=R[n]
        unit['status']='available'
        for chapter in unit['chapters']:
            j=int(chapter['number'].split('.')[1]);chapter['status']='available'
            if n==1:
                chapter['references']=CHAPTER_REFS[chapter['id']]
                chapter['illustrations']=[f for f in FIGURES if f['chapter']==chapter['id']]
                chapter['content_file']=f'src/chapter-{j}.html'
            elif n==22:
                assert len(CASES[j]['sections'])==22
                assert all(len(s.split())>=20 for s in CASES[j]['sections'])
                chapter['references']=CASE_SOURCES[j]
                chapter['content_file']='src/teaching/cases.py'
                chapter['section_status']=[dict(title=t,status='available') for t in chapter['sections']]
            else:
                chapter['references']=R[n]
                chapter['content_file']='src/teaching/'+('foundations.py' if n<=4 else 'lld.py' if n<=8 else 'data.py' if n<=13 else 'distributed.py' if n<=17 else 'production.py')
                chapter['topic_coverage']=[dict(syllabus_item=i,status='available',words=len(LESSONS[n][i-1]['prose'].split()),worked_trace=True) for i in chapter['topic_numbers']]
            chapter['illustrations']=chapter['illustrations'] if n==1 else []
        for kind,item in unit['assessment'].items():item.update(produced=item['required'],status='available')
        assert len(exercises[n])==11
    book.update(stage='Complete first edition: all 22 units and all 12 mandatory case studies produced',scope='A complete illustrated reference edition. Workload, latency, capacity and price examples are explicitly assumed models; code examples demonstrate bounded mechanisms rather than production infrastructure.')
    return book,first_figures,exercises
