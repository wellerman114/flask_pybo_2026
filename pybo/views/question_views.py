from flask import Blueprint, render_template

from pybo.models import Question

# 라우팅 함수를 체계적으로 관리
bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc()).all()

    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question)

