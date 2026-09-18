from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, g, flash

from pybo import db
from pybo.forms import QuestionForm,AnswerForm
from pybo.models import Answer, Question, User
from pybo.views.auth_views import login_required

# 라우팅 함수를 체계적으로 관리
bp = Blueprint('question', __name__, url_prefix='/question')


def _list_legacy():
    page = request.args.get('page', default=1, type=int) # url parameter ?page=1
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page=page, per_page=10) # 한페이지에 보여야할 갯수
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/list/')
def _list():
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw', default='', type=str)
    question_list = Question.query.order_by(Question.create_date.desc())

    if kw:
        search = f'%{kw}%'
        answer_subquery = db.session.query(
            Answer.question_id,
            Answer.content,
            User.username,
        ).join(User, Answer.user_id == User.id).subquery()
        question_list = question_list.join(User).outerjoin(
            answer_subquery,
            answer_subquery.c.question_id == Question.id,
        ).filter(
            Question.subject.ilike(search) |
            Question.content.ilike(search) |
            User.username.ilike(search) |
            answer_subquery.c.content.ilike(search) |
            answer_subquery.c.username.ilike(search)
        ).distinct()

    question_list = question_list.paginate(page=page, per_page=10)
    return render_template(
        'question/question_list.html', question_list=question_list, page=page, kw=kw
    )

@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form = AnswerForm()  # 질문 상세 템플릿에 폼 추가
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html',question=question, form=form)

@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=['GET', 'POST'])
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method=='POST':  # POST요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
