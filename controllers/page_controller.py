from flask import request, Blueprint

from services.page_service import PageService

page_service = PageService()
page_bp = Blueprint('page', __name__)


@page_bp.route('/get-page', methods=['POST'])
def get_page():
    data = request.json

    application_id = data.get('application_id')
    text = data.get('text')

    return page_service.get_page(application_id, text)