# import use_model
import src.use_model_5 as use_model
import src.roberta_mnli as roberta_mnli
import src.roberta_sts as roberta_sts
from flask import render_template, jsonify, request
from flask import Flask
import numpy as np
import json


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["CACHE_TYPE"] = "null"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api_get_result', methods=["POST"])
def api_get_result():

    question = request.form['question']
    target = request.form['target']
    answer = request.form['answer']

    u_question_target, u_question_pred, u_target_pred = use_model.get_similarity(question, target, answer)
    roberta_question_target, roberta_question_pred, roberta_target_pred = roberta_sts.get_similarity(question, target, answer)
    r_pred = roberta_mnli.get_similarity(question, target, answer)

    # check contradiction
    use_score = np.round(u_target_pred * 100)
    roberta_score = np.round(roberta_target_pred[0, 0] * 100)
    status = 0

    if r_pred[0] >= 0.5:
        msg = f'Answer seems in CONTRADICTION with the target answer, even with {use_score}% similarity'
        status = -1
    elif r_pred[0] < 0.5:
        if use_score < 50:
            if roberta_score > 40:
                msg = f'The answer seems incorrect, even though they are referring about the same subject with {roberta_score}% similarity.'
                status = -1
            else:
                msg = f'The answer seems incorrect, with {use_score}% similarity.'
                status = -1

        elif use_score < 70 and use_score > 50:
            msg = f'The answer seems partialy correct, with {use_score}% similarity.'
            status = 0
        elif use_score >= 70:
            msg = f'It seems the answer is CORRECT, as it has {use_score}% similarity with the target, and it is not in contradiction with the target answer.'
            status = 1

    r = {
        'msg': msg,
        'status': status,

        'u_question_x_target': str(np.round(u_question_target, 3)),
        'u_question_x_answer': str(np.round(u_question_pred, 3)),
        'u_answer_x_target': str(np.round(u_target_pred, 3)),

        'r_question_x_target': str(np.round(roberta_question_target[0, 0], 3)),
        'r_question_x_answer': str(np.round(roberta_question_pred[0, 0], 3)),
        'r_answer_x_target': str(np.round(roberta_target_pred[0, 0], 3)),

        'r_contradicao': str(np.round(r_pred[0], 3)),
        'r_neutro': str(np.round(r_pred[1], 3)),
        'r_implicacao': str(np.round(r_pred[2], 3)),
        'score_final': str(np.round(u_target_pred, 3))

    }

    return jsonify({"status": "success", "response": r})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, use_reloader=False)
