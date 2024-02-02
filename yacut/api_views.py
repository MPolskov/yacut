from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .views import get_unique_short_id
from .constants import (
    VALID_VALUE,
    EMPTY_REQUEST,
    EMPTY_URL,
    SHORT_LINK_EXIST,
    TOO_LONG_LINK,
    NOT_VALID_LINK,
    LINK_NOT_EXIST
)


@app.route('/api/id/<string:link>/', methods=['GET'])
def get_opinion(link):
    url = URLMap.query.filter_by(short=link).first()
    if url is None:
        raise InvalidAPIUsage(LINK_NOT_EXIST, 404)
    return jsonify({'url': url.original}), 200


@app.route('/api/id/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL)
    if 'custom_id' in data:
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(SHORT_LINK_EXIST, 400)
        elif len(data['custom_id']) > 16:
            raise InvalidAPIUsage(TOO_LONG_LINK)
        elif not all([True if i in VALID_VALUE else False for i in data['custom_id']]):
            raise InvalidAPIUsage(NOT_VALID_LINK)
    else:
        data['custom_id'] = get_unique_short_id()
    url_map = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify({'url': url_map.original, 'short_link': url_map.short}), 201
