from konlpy.tag import Okt
from . import mongo_connection
 
def analysis():
    okt = Okt()
    doc = mongo_connection.post_find()
    
    doc_list = []
    for i in doc :
        doc = {}
        doc['post_id'] = i['post_id']
        doc['person_id'] = i['person_id']
        doc['keyword'] = okt.nouns(i['post'])
        doc_list += [doc]
        # print(okt.nouns(i['post']))
    mongo_connection.textmining_result_insert(doc_list)
 