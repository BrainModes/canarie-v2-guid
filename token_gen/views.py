from flask import Blueprint

from token_gen.api import TokenAPI, TokenAPI_2Keys, TokenAPI_digits

token_app = Blueprint('token_app', __name__)

token_view = TokenAPI.as_view('tokenizer_api')
token_app.add_url_rule('/1key/<table>/<key>', view_func=token_view, methods=['GET',])

token_view_2keys = TokenAPI_2Keys.as_view('tokenizer_api_2keys')
token_app.add_url_rule('/2keys/<table>', view_func=token_view_2keys, methods=['GET',])

token_view_digits = TokenAPI_digits.as_view('tokenizer_api_digits')
token_app.add_url_rule('/digits/<table>', view_func=token_view_digits, methods=['GET',])