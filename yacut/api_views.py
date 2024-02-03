import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .views import get_unique_short_id
from .constants import (
    PATTERN,
    EMPTY_REQUEST,
    EMPTY_URL,
    SHORT_LINK_EXIST,
    NOT_VALID_LINK,
    LINK_NOT_EXIST
)


@app.route('/api/id/<string:link>/', methods=['GET'])
def get_original_link(link):
    url = URLMap.query.filter_by(short=link).first()
    if url is None:
        raise InvalidAPIUsage(LINK_NOT_EXIST, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def add_short_link():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(EMPTY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage(EMPTY_URL)
    if 'custom_id' in data:
        # Python 3.9:
        if data['custom_id'] in ('', None):
            data['custom_id'] = get_unique_short_id()
        elif re.fullmatch(PATTERN, data['custom_id']) is None:
            raise InvalidAPIUsage(NOT_VALID_LINK, HTTPStatus.BAD_REQUEST)
        elif URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage(SHORT_LINK_EXIST, HTTPStatus.BAD_REQUEST)
        # Python 3.10+:
        # match data['custom_id']:
        #     case '' | None:
        #         data['custom_id'] = get_unique_short_id()
        #     case id if re.fullmatch(PATTERN, id) is None:
        #         raise InvalidAPIUsage(NOT_VALID_LINK, HTTPStatus.BAD_REQUEST)
        #     case id if URLMap.query.filter_by(short=id).first():
        #         raise InvalidAPIUsage(SHORT_LINK_EXIST, HTTPStatus.BAD_REQUEST)
    else:
        data['custom_id'] = get_unique_short_id()
    url_map = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify(
        {
            'url': url_map.original,
            'short_link': url_for(
                'redirect_view',
                link=url_map.short,
                _external=True
            )
        }
    ), HTTPStatus.CREATED
