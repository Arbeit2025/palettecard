"""きょうの配色カード palettecard

季節（春・夏・秋・冬）× 気分（元気・落ち着く・爽やか・あたたかい）の
組み合わせから、内蔵データの3色パレット（名前＋HEX）を提示するツール。
デザインやイラストの色選びのきっかけに。単一ファイル Flask（DBなし）。
"""
import os

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

SEASONS = ["春", "夏", "秋", "冬"]
MOODS = ["元気", "落ち着く", "爽やか", "あたたかい"]

# (季節, 気分) -> (パレット名, [HEX x3])
PALETTES = {
    ("春", "元気"): ("桜はじける", ["#F783AC", "#FFD43B", "#8CE99A"]),
    ("春", "落ち着く"): ("春の野原", ["#A9E5BB", "#F7D6E0", "#FFF3B0"]),
    ("春", "爽やか"): ("春風ミント", ["#63E6BE", "#A5D8FF", "#E7F5FF"]),
    ("春", "あたたかい"): ("ひだまりピーチ", ["#FFC9A3", "#FFEC99", "#F1A7A7"]),
    ("夏", "元気"): ("真夏のひまわり", ["#FFD43B", "#FF922B", "#4DABF7"]),
    ("夏", "落ち着く"): ("夕凪の海", ["#74C0FC", "#B197FC", "#FFD8A8"]),
    ("夏", "爽やか"): ("ラムネと青空", ["#339AF0", "#66D9E8", "#E3FAFC"]),
    ("夏", "あたたかい"): ("夏祭りの提灯", ["#FF6B6B", "#FFA94D", "#FFE066"]),
    ("秋", "元気"): ("収穫祭", ["#E8590C", "#FAB005", "#82C91E"]),
    ("秋", "落ち着く"): ("読書の時間", ["#A0522D", "#D6C7AE", "#748C69"]),
    ("秋", "爽やか"): ("秋晴れハイキング", ["#5C7CFA", "#FFD8A8", "#96F2D7"]),
    ("秋", "あたたかい"): ("焼き芋ホクホク", ["#B08968", "#E6CCB2", "#DDB892"]),
    ("冬", "元気"): ("雪とイルミネーション", ["#4DABF7", "#FFD43B", "#F783AC"]),
    ("冬", "落ち着く"): ("静かな雪の夜", ["#CED4DA", "#E7F5FF", "#868E96"]),
    ("冬", "爽やか"): ("冬の朝の空気", ["#A5D8FF", "#E3FAFC", "#FFFFFF"]),
    ("冬", "あたたかい"): ("こたつとみかん", ["#FF922B", "#FFE8CC", "#C2255C"]),
}

PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>きょうの配色カード</title>
<style>body{font-family:sans-serif;max-width:680px;margin:2em auto;padding:0 1em}
.card{border:1px solid #ccc;border-radius:8px;padding:1em;margin-top:1em}
.swatch{height:64px;border-radius:6px;margin:.4em 0;padding:.4em;font-family:monospace}
button{margin:.3em .2em}</style>
</head><body>
<h1>きょうの配色カード</h1>
<p>季節と気分を選ぶと、3色の配色パレットを表示します。イラストやデザインの色選びのヒントにどうぞ。</p>
<form method="get" action="{{ url_for('index') }}">
  <label>季節
    <select name="season">{% for s in seasons %}<option{% if s == season %} selected{% endif %}>{{ s }}</option>{% endfor %}</select></label>
  <label>気分
    <select name="mood">{% for m in moods %}<option{% if m == mood %} selected{% endif %}>{{ m }}</option>{% endfor %}</select></label>
  <button type="submit">配色を見る</button>
</form>

{% if palette %}
<div class="card">
  <h2>{{ season }} × {{ mood }}：「{{ palette.name }}」</h2>
  {% for hex in palette.colors %}
  <div class="swatch" style="background:{{ hex }}">{{ hex }}
    <button type="button" onclick="copyHex('{{ hex }}')">コピー</button>
  </div>
  {% endfor %}
</div>
<script>
function copyHex(hex) {
  if (navigator.clipboard) { navigator.clipboard.writeText(hex); }
}
</script>
{% endif %}
</body></html>"""


def get_palette(season, mood):
    data = PALETTES.get((season, mood))
    if data is None:
        return None
    return {"name": data[0], "colors": data[1]}


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.route("/")
def index():
    season = request.args.get("season", "")
    mood = request.args.get("mood", "")
    palette = get_palette(season, mood) if season in SEASONS and mood in MOODS else None
    return render_template_string(
        PAGE, seasons=SEASONS, moods=MOODS,
        season=season, mood=mood, palette=palette,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
