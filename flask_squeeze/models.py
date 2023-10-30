from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
	from flask import Config
	from werkzeug.datastructures import Headers


class ResourceType(Enum):
	static = "static"
	dynamic = "dynamic"


class Encoding(Enum):
	gzip = "gzip"
	deflate = "deflate"
	br = "br"


class Minifcation(Enum):
	js = "js"
	css = "css"
	html = "html"


def choose_encoding_from_headers_and_config(
	headers: Headers,
	config: Config,
) -> Union[Encoding, None]:
	"""
	If the client supports brotli, gzip, or deflate, return the best encoding.
	If the client does not accept any of these encodings, or if the config
	variable SQUEEZE_COMPRESS is False, return None.
	"""
	if not config.get("SQUEEZE_COMPRESS") or headers is None:
		return None
	encoding = headers.get("Accept-Encoding", "").lower()
	if "br" in encoding:
		return Encoding.br
	if "deflate" in encoding:
		return Encoding.deflate
	if "gzip" in encoding:
		return Encoding.gzip
	return None


def choose_minification_from_mimetype_and_config(
	mimetype: Union[str, None],
	config: Config,
) -> Union[Minifcation, None]:
	"""
	Based on the response mimetype:
	- `js` or `json`, and `SQUEEZE_MINIFY_JS=True`: return `Minifcation.js`
	- `css` and `SQUEEZE_MINIFY_CSS=True`: return `Minifcation.css`
	-  `html` and `SQUEEZE_MINIFY_HTML=True`: return `Minifcation.html`
	- Otherwise, return `None`
	"""
	if mimetype is None:
		return None
	is_js_or_json = mimetype.endswith("javascript") or mimetype.endswith("json")
	if is_js_or_json and config.get("SQUEEZE_MINIFY_JS"):
		return Minifcation.js
	if mimetype.endswith("css") and config.get("SQUEEZE_MINIFY_CSS"):
		return Minifcation.css
	if mimetype.endswith("html") and config.get("SQUEEZE_MINIFY_HTML"):
		return Minifcation.html
	return None
