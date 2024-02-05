from fastapi import APIRouter
from models import UserText
from crud.crud_document import query_pinecone_document, search_document_by_id, query_pinecone_law, search_law_by_id
from util.reference import make_reference

router = APIRouter()


@router.post('/similar_document')
def query_sim_doc(user_text: UserText):
    try:
        text = user_text.text

        sim_doc_id = query_pinecone_document(text, top_k=5)
        if sim_doc_id is None:
            raise Exception
        print(sim_doc_id)
        res_list = []
        for item in sim_doc_id:
            id = int(item['id'])
            score = item['score']
            table_data = search_document_by_id(id)
            if table_data is None:
                continue
            reference = make_reference(table_data['title'], table_data['writer'], table_data['date'],
                                       table_data['from_'], table_data['url'])
            data = {'title': table_data['title'], 'writer': table_data['writer'], 'date': table_data['date'],
                    'from': table_data['from_'], 'url': table_data['url'], 'reference': reference}
            res_list.append(data)

        return {'success': True, 'documents': res_list}
    except Exception as e:
        print(e)
        return {'success': False}
    

@router.post('/similar_law')
def query_sim_law(user_text: UserText):
    try:
        text = user_text.text

        sim_law_id = query_pinecone_law(text, top_k=5)
        if sim_law_id is None:
            raise Exception
        print(sim_law_id)
        res_list = []
        for item in sim_law_id:
            id = int(item['id'])
            table_data = search_law_by_id(id)
            if table_data is None:
                continue
            data = {'title': table_data['title'].strip(), 'url': table_data['url']}
            res_list.append(data)

        return {'success': True, 'laws': res_list}
    except Exception as e:
        print(e)
        return {'success': False}