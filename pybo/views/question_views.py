from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from pybo import db
from pybo.forms import QuestionForm,AnswerForm
from pybo.models import Question

# 라우팅 함수를 체계적으로 관리
bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    page = request.args.get('page', default=1, type=int) # url parameter ?page=1
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10) # 한페이지에 보여야할 갯수
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form = AnswerForm()  # 질문 상세 템플릿에 폼 추가
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question, form=form)

@bp.route('/create/', methods=['GET', 'POST'])
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)
