import re
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/5"
model = hub.load(module_url)


def embed(input):
    return np.array(model(input))


def cosine(A, B):
    return np.dot(A, B.T) / (np.sqrt(np.sum(A * A)) * np.sqrt(np.sum(B * B)))


def get_similarity(question, target, evall):
    question = re.sub('[\n\r]+', '', question)
    target = re.sub('[\n\r]+', '', target)
    evall = re.sub('[\n\r]+', '', evall)
    q = embed([question])
    s1 = embed([target])
    s2 = embed([evall])
    print('====== USE ======')
    print(cosine(q, s1))
    print(cosine(q, s2))
    print(cosine(s1, s2))
    return cosine(q, s1)[0][0], cosine(q, s2)[0][0], cosine(s1, s2)[0][0]
