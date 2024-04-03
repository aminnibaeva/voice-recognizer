from flask import request, Blueprint

from services.query_service import QueryService

query_bp = Blueprint('query', __name__)

query_service = QueryService()


@query_bp.route('/update_query', methods=['POST'])
def update_query():
    user_query_id = request.form['userQueryId']
    query_service.update_query(user_query_id)
    return user_query_id

@query_bp.route('/delete_query', methods=['POST'])
def delete_query():
    user_query_id = request.form['userQueryId']
    query_service.delete_query(user_query_id)
    return user_query_id
