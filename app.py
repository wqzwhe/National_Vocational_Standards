from flask import Flask, request, jsonify
import requests
import uuid
import time
import random
import io
import base64
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Referer': 'http://osta.mohrss.gov.cn/skillStandard',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

API_SEARCH_URL = 'http://osta.mohrss.gov.cn/api/public/skillStandardList'
DOWNLOAD_PREFIX = 'http://osta.mohrss.gov.cn/api/sys/downloadFile/decrypt?fileName='

captcha_store = {}


def _rand_text(length=5):
    alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return ''.join(random.choice(alphabet) for _ in range(length))


def _get_font(size):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/Library/Fonts/Arial.ttf',
        'DejaVuSans.ttf',
        'Arial.ttf',
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _make_captcha_image(text, width=180, height=60):
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for _ in range(6):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill=(200, 200, 200), width=1)
    font = _get_font(34)
    try:
        bx = draw.textbbox((0, 0), text, font=font)
        tw, th = bx[2] - bx[0], bx[3] - bx[1]
    except Exception:
        tw, th = font.getsize(text)
    tx = (width - tw) // 2
    ty = (height - th) // 2
    draw.text((tx, ty), text, font=font, fill=(34, 34, 34))
    for _ in range(100):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        img.putpixel((x, y), (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return 'data:image/png;base64,' + b64


@app.route('/')
def index():
    return jsonify({'msg': 'backend_ok'})


@app.route('/api/captcha/new', methods=['GET', 'OPTIONS'])
def captcha_new():
    if request.method == 'OPTIONS':
        return ('', 204)
    text = _rand_text(5)
    cid = uuid.uuid4().hex
    captcha_store[cid] = {'answer': text.lower(), 'expires': time.time() + 120}
    image_b64 = _make_captcha_image(text)
    return jsonify({'code': 200, 'msg': 'OK', 'body': {'id': cid, 'image': image_b64}})


@app.route('/api/search', methods=['GET', 'OPTIONS'])
def search():
    if request.method == 'OPTIONS':
        return ('', 204)
    cid = request.args.get('captchaId', '').strip()
    cans = request.args.get('captchaAnswer', '').strip()
    if not cid or not cans:
        return jsonify({'code': 400, 'msg': 'captcha_required'}), 400
    info = captcha_store.get(cid)
    if not info or time.time() > info.get('expires', 0) or info.get('answer') != cans.lower():
        return jsonify({'code': 400, 'msg': 'captcha_invalid'}), 400
    q = request.args.get('q', '').strip()
    page_num = request.args.get('pageNum', '1')
    page_size = request.args.get('pageSize', '10')

    params = {
        'pageSize': page_size,
        'pageNum': page_num,
        'nameCode': q,
        'status': '1',
    }

    try:
        resp = requests.get(API_SEARCH_URL, params=params, headers=HEADERS, timeout=10)
        data = resp.json()
    except Exception as e:
        return jsonify({'code': 500, 'msg': 'search_failed', 'error': str(e)}), 500

    body = data.get('body', {})
    items = body.get('list', []) or []
    for item in items:
        std = item.get('standardInfo')
        if std:
            item['downloadUrl'] = f"{DOWNLOAD_PREFIX}{std}"
        else:
            item['downloadUrl'] = None

    return jsonify({'code': 200, 'msg': 'OK', 'body': {**body, 'list': items}})


@app.after_request
def add_cors_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
