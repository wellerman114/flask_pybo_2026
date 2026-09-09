from flask import Blueprint

# 라우팅 함수를 체계적으로 관리해줌 = blueprint

bp = Blueprint('main', __name__,url_prefix='/')

@bp.route('/')
def hello_pybo():
    return 'Hello pybo!'

@bp.route('/hello')
def hello():
    return 'Hello page!'

