"""Page scaffolding for report.html: tokens, light/dark, phone width."""

import html
import math
import os

import svg
from lab import load, paired

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """
:root{
  color-scheme: light;
  --bg:#f6f5f2; --surf:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#8a8984; --grid:#e4e3df;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --body:#4a3aa7; --danger:#e34948;
  --good:#008300; --warn:#a86b00; --card:#ffffff; --line:#dedcd6; --code:#efeee9;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme: dark;
    --bg:#121211; --surf:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#8f8e86; --grid:#33332f;
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --body:#9085e9; --danger:#e66767;
    --good:#4fb34f; --warn:#e0a030; --card:#1a1a19; --line:#33332f; --code:#24241f;
  }
}
:root[data-theme="dark"]{
  color-scheme: dark;
  --bg:#121211; --surf:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#8f8e86; --grid:#33332f;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --body:#9085e9; --danger:#e66767;
  --good:#4fb34f; --warn:#e0a030; --card:#1a1a19; --line:#33332f; --code:#24241f;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:860px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:2rem;line-height:1.15;margin:.2em 0 .1em;letter-spacing:-.01em}
h2{font-size:1.35rem;margin:2.2em 0 .5em;padding-top:.6em;border-top:1px solid var(--line)}
h3{font-size:1.05rem;margin:1.6em 0 .4em}
p,li{color:var(--ink)}
.lede{font-size:1.1rem;color:var(--ink2);margin:.4em 0 1em}
.meta{color:var(--muted);font-size:.85rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:14px 0}
.warn{border-left:4px solid var(--warn)}
.figs{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:12px 0}
.figs.two{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.figs.one{grid-template-columns:1fr}
figure{margin:0;background:var(--surf);border:1px solid var(--line);border-radius:10px;padding:10px}
figcaption{font-size:.85rem;color:var(--ink2);margin-top:6px}
.wide{overflow:hidden}
table{border-collapse:collapse;width:100%;font-size:.88rem;margin:10px 0}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--ink2);font-weight:600}
.tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.tablewrap table{min-width:560px}
code{background:var(--code);padding:1px 5px;border-radius:4px;font-size:.88em}
.tag{display:inline-block;font-size:.72rem;font-weight:600;padding:1px 7px;border-radius:999px;
  border:1px solid currentColor;white-space:nowrap}
.tag.sim{color:var(--good)} .tag.res{color:var(--s1)} .tag.guess{color:var(--warn)} .tag.no{color:var(--danger)}
.find{counter-increment:f;position:relative;padding-left:2.2em}
.find::before{content:counter(f);position:absolute;left:0;top:.1em;width:1.6em;height:1.6em;border-radius:50%;
  background:var(--s1);color:#fff;font-weight:700;font-size:.85rem;display:flex;align-items:center;justify-content:center}
ol.finds{list-style:none;padding:0;counter-reset:f}
ol.finds li{margin:.9em 0}
.yes{color:var(--good);font-weight:700} .nope{color:var(--danger);font-weight:700}
details summary{cursor:pointer;color:var(--ink2)}
@media (max-width:520px){ h1{font-size:1.6rem} body{font-size:15px} th,td{padding:5px 5px} }
"""


def esc(s):
    return html.escape(str(s))


def page(title, description, body):
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>%s</title><meta name=\"description\" content=\"%s\"><style>%s</style></head>"
            "<body><main>%s</main></body></html>" % (esc(title), esc(description), CSS, body))


def fig(name, caption):
    with open(os.path.join(HERE, "figs", name + ".svg")) as f:
        s = f.read()
    return "<figure>%s<figcaption>%s</figcaption></figure>" % (s, caption)


def chart(round_name, metric, title, conds=None, better="higher", fmt="%.3f", labels=None):
    out = load(round_name)
    rows = []
    for n, runs in out.items():
        if conds and n not in conds:
            continue
        rows.append(((labels or {}).get(n, n), [r[metric] for r in runs]))
    if conds:
        order = {c: i for i, c in enumerate(conds)}
        rows.sort(key=lambda r: order.get(next((c for c in conds if (labels or {}).get(c, c) == r[0]), r[0]), 0))
    return svg.dot_chart(rows, title, title, better=better, fmt=fmt)


def chart_fig(round_name, metric, title, caption, **kw):
    return "<figure>%s<figcaption>%s</figcaption></figure>" % (chart(round_name, metric, title, **kw), caption)


def paired_rows(round_name, ref, keys=("engagement", "bottomQuarter", "boredom", "fatigue")):
    out = load(round_name)
    ps = {k: paired(out, ref, k) for k in keys}
    head = "<tr><th>vs %s</th>%s</tr>" % (esc(ref), "".join("<th>Δ %s</th>" % esc(k) for k in keys))
    body = []
    for n in out:
        if n == ref:
            continue
        cells = []
        for k in keys:
            m, se, up, tot = ps[k][n]
            cells.append("<td style=\"white-space:nowrap\">%+.3f <span class=\"meta\">±%.3f (%d/%d)</span></td>" % (m, se, up, tot))
        body.append("<tr><td>%s</td>%s</tr>" % (esc(n), "".join(cells)))
    return "<div class=\"tablewrap\"><table>%s%s</table></div>" % (head, "".join(body))


def mean(round_name, cond, key):
    runs = load(round_name)[cond]
    return sum(r[key] for r in runs) / len(runs)
