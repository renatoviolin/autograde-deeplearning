
import torch
from fairseq.models.roberta import RobertaModel
import re

MNLI_PATH = 'roberta.large.mnli'

roberta = RobertaModel.from_pretrained(MNLI_PATH).eval()


def get_similarity(question, target, evall):
    question = re.sub('[\n\r]+', '', question)
    target = re.sub('[\n\r]+', '', target)
    evall = re.sub('[\n\r]+', '', evall)

    tokens_q_t = roberta.encode(question, target)
    logits_q_t = roberta.predict('mnli', tokens_q_t, return_logits=True)
    pred_q_t = torch.nn.Softmax(dim=1)(logits_q_t).detach().numpy()[0]

    tokens_q_e = roberta.encode(question, evall)
    logits_q_e = roberta.predict('mnli', tokens_q_e, return_logits=True)
    pred_q_e = torch.nn.Softmax(dim=1)(logits_q_e).detach().numpy()[0]

    tokens_t_e = roberta.encode(target, evall)
    logits_t_e = roberta.predict('mnli', tokens_t_e, return_logits=True)
    pred_t_e = torch.nn.Softmax(dim=1)(logits_t_e).detach().numpy()[0]

    print('====== RoBERTa ======')
    print('Question x Target: {}'.format(pred_q_t))
    print('Question x Eval: {}'.format(pred_q_e))
    print('Target x Eval: {}'.format(pred_t_e))
    return pred_t_e
