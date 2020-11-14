from sentence_transformers import SentenceTransformer
import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')


def get_similarity(question, target, evall):
    question = re.sub('[\n\r]+', '', question)
    target = re.sub('[\n\r]+', '', target)
    evall = re.sub('[\n\r]+', '', evall)

    sentences = [question, target, evall]

    encoder = model.encode(sentences)

    bert_q_t = cosine_similarity(encoder[0].reshape(1, -1), encoder[1].reshape(1, -1))
    bert_q_e = cosine_similarity(encoder[0].reshape(1, -1), encoder[2].reshape(1, -1))
    bert_t_e = cosine_similarity(encoder[1].reshape(1, -1), encoder[2].reshape(1, -1))

    print('====== ROBERTA_STS ======')
    print('Question x Target: {}'.format(bert_q_t))
    print('Question x Eval: {}'.format(bert_q_e))
    print('Target x Eval: {}'.format(bert_t_e))
    return bert_q_t, bert_q_e, bert_t_e
