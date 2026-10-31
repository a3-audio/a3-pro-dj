"""Hand-written SVG for the MJ Lab report. Colours are CSS custom properties
(set by report.html for light and dark), with light fallbacks so a file also
opens on its own."""

import math

SHIP = ["var(--s1,#2a78d6)", "var(--s2,#eb6834)", "var(--s3,#1baf7a)", "var(--s4,#eda100)"]
INK = "var(--ink,#0b0b0b)"
INK2 = "var(--ink2,#52514e)"
MUTED = "var(--muted,#8a8984)"
GRID = "var(--grid,#e4e3df)"
SURF = "var(--surf,#fcfcfb)"
BODY = "var(--body,#4a3aa7)"
DANGER = "var(--danger,#e34948)"
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(w, h, body, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
            'aria-label="%s" style="width:100%%;height:auto;font-family:inherit">'
            '<title>%s</title>%s</svg>' % (w, h, esc(title), esc(title), body))


def _f(x):
    return "%.1f" % x


class Floor:
    """Maps floor units (room edge radius 1) to a square of side `size`."""

    def __init__(self, size, ox=0.0, oy=0.0, pad=8):
        self.size, self.ox, self.oy, self.pad = size, ox, oy, pad
        self.r = size / 2 - pad

    def xy(self, x, y):
        c = self.size / 2
        return self.ox + c + x * self.r, self.oy + c - y * self.r

    def room(self, label_front=True, speakers=True):
        c = self.size / 2
        cx, cy = self.ox + c, self.oy + c
        out = ['<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1"/>'
               % (_f(cx), _f(cy), _f(self.r), GRID)]
        out.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1" stroke-dasharray="2 3"/>'
                   % (_f(cx), _f(cy), _f(self.r * 0.85), GRID))
        if speakers:
            for k in range(8):
                x, y = self.xy(math.cos(k * math.pi / 4), math.sin(k * math.pi / 4))
                out.append('<rect x="%s" y="%s" width="5" height="5" rx="1" fill="%s"/>'
                           % (_f(x - 2.5), _f(y - 2.5), MUTED))
        if label_front:
            x, y = self.xy(0, 1)
            out.append('<text x="%s" y="%s" font-size="9" text-anchor="middle" fill="%s">DJ</text>'
                       % (_f(x), _f(y + 14), INK2))
        return "".join(out)

    def path(self, pts, colour, width=1.5, opacity=0.9):
        if not pts:
            return ""
        d = "M" + " L".join("%s %s" % tuple(map(_f, self.xy(*p))) for p in pts)
        return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-opacity="%s" '
                'stroke-linejoin="round" stroke-linecap="round"/>' % (d, colour, width, opacity))

    def bodies(self, bodies, label=True):
        out = []
        for i, (x, y, m) in enumerate(bodies):
            X, Y = self.xy(x, y)
            rad = 4 + 3.5 * math.sqrt(abs(m))
            if m > 0:
                out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="0.25" stroke="%s" stroke-width="1"/>'
                           % (_f(X), _f(Y), _f(rad), BODY, BODY))
            else:
                out.append('<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-width="1.5"/>'
                           % (_f(X), _f(Y), _f(rad), DANGER))
            if label:
                out.append('<text x="%s" y="%s" font-size="8" fill="%s">G%d</text>'
                           % (_f(X + rad + 1), _f(Y + 3), INK2, i + 1))
        return "".join(out)

    def people(self, crowd, colour=INK2, r=1.6, by_fatigue=False):
        out = []
        for p in crowd:
            X, Y = self.xy(p[0], p[1])
            col = colour
            if by_fatigue and p[2] > 0.5:
                col = DANGER
            out.append('<circle cx="%s" cy="%s" r="%s" fill="%s" fill-opacity="0.75"/>' % (_f(X), _f(Y), r, col))
        return "".join(out)

    def heat(self, crowd, cells=14, vmax=None):
        k = 2.0 / cells
        grid = {}
        for p in crowd:
            gx, gy = int((p[0] + 1) / k), int((p[1] + 1) / k)
            grid[(gx, gy)] = grid.get((gx, gy), 0) + 1
        vmax = vmax or max(grid.values())
        out = []
        for (gx, gy), v in grid.items():
            x0, y1 = self.xy(-1 + gx * k, -1 + gy * k)
            x1, y0 = self.xy(-1 + (gx + 1) * k, -1 + (gy + 1) * k)
            step = min(len(SEQ) - 1, int(v / vmax * (len(SEQ) - 1) + 0.5))
            out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"><title>%d people</title></rect>'
                       % (_f(x0), _f(y0), _f(x1 - x0 - 0.5), _f(y1 - y0 - 0.5), SEQ[step], v))
        return "".join(out)


def legend_ships(n, x, y):
    out = []
    for i in range(n):
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2"/>'
                   % (_f(x + i * 52), _f(y), _f(x + i * 52 + 14), _f(y), SHIP[i]))
        out.append('<text x="%s" y="%s" font-size="9" fill="%s">ship %d</text>'
                   % (_f(x + i * 52 + 17), _f(y + 3), INK2, i + 1))
    return "".join(out)


def trajectories(trace, from_sample, to_sample, n_ships, title, size=300, bar=None, extra_note=""):
    f = Floor(size, 0, 0, pad=14)
    body = [f.room()]
    b_idx = bar if bar is not None else min(len(trace["bodies"]) - 1, int(to_sample * 0.25 / 4))
    body.append(f.people(trace["crowd"][b_idx]))
    body.append(f.bodies(trace["bodies"][b_idx]))
    for ch in range(n_ships):
        pts = [trace["ships"][s][ch] for s in range(from_sample, to_sample)]
        body.append(f.path(pts, SHIP[ch]))
        X, Y = f.xy(*pts[-1])
        body.append('<circle cx="%s" cy="%s" r="3.5" fill="%s" stroke="%s" stroke-width="2"/>' % (_f(X), _f(Y), SHIP[ch], SURF))
    body.append(legend_ships(n_ships, 14, size + 10))
    if extra_note:
        body.append('<text x="14" y="%s" font-size="9" fill="%s">%s</text>' % (size + 26, MUTED, esc(extra_note)))
    return wrap(size, size + 32, "".join(body), title)


def heat_series(trace, bars, title, size=120, cols=4):
    rows = (len(bars) + cols - 1) // cols
    W, H = cols * (size + 6), rows * (size + 20)
    body = []
    allmax = 1
    for b in bars:
        crowd = trace["crowd"][b]
        k = 2.0 / 14
        g = {}
        for p in crowd:
            key = (int((p[0] + 1) / k), int((p[1] + 1) / k))
            g[key] = g.get(key, 0) + 1
        allmax = max(allmax, max(g.values()))
    for i, b in enumerate(bars):
        ox, oy = (i % cols) * (size + 6), (i // cols) * (size + 20)
        f = Floor(size, ox, oy, pad=4)
        body.append(f.heat(trace["crowd"][b], vmax=allmax))
        body.append(f.room(label_front=False, speakers=False).replace(GRID, MUTED))
        body.append(f.bodies(trace["bodies"][b], label=False))
        body.append('<text x="%s" y="%s" font-size="10" text-anchor="middle" fill="%s">bar %d</text>'
                    % (_f(ox + size / 2), _f(oy + size + 13), INK2, b))
    return wrap(W, H, "".join(body), title)


def dot_chart(rows, metric, title, unit="", width=520, better="higher", fmt="%.2f"):
    """rows: list of (label, [values per seed]). Mean as a dot, seeds as ticks,
    +-1 sd as a bar. Horizontal layout reads on a phone."""
    pad_r, row_h = 46, 22
    longest = max(len(str(l)) for l, _ in rows)
    lab_w = int(min(300, 16 + 5.3 * longest))
    width = max(width, lab_w + 300)
    vals = [v for _, vs in rows for v in vs]
    lo, hi = min(vals + [0.0]), max(vals)
    if hi - lo < 1e-9:
        hi = lo + 1
    span = hi - lo
    lo -= span * 0.05
    hi += span * 0.05
    plot_w = width - lab_w - pad_r
    X = lambda v: lab_w + (v - lo) / (hi - lo) * plot_w
    H = 30 + row_h * len(rows) + 18
    out = ['<text x="0" y="12" font-size="11" font-weight="600" fill="%s">%s</text>' % (INK, esc(metric + (" (" + unit + ")" if unit else "")))]
    out.append('<text x="%d" y="12" font-size="9" text-anchor="end" fill="%s">%s is better</text>'
               % (width, MUTED, better) if better else "")
    if lo < 0 < hi:
        out.append('<line x1="%s" y1="22" x2="%s" y2="%s" stroke="%s"/>' % (_f(X(0)), _f(X(0)), H - 18, GRID))
    for i, (label, vs) in enumerate(rows):
        y = 30 + i * row_h + row_h / 2
        m = sum(vs) / len(vs)
        sd = math.sqrt(sum((v - m) ** 2 for v in vs) / max(1, len(vs) - 1))
        out.append('<text x="%d" y="%s" font-size="10" text-anchor="end" fill="%s">%s</text>' % (lab_w - 8, _f(y + 3.5), INK2, esc(label)))
        out.append('<line x1="%d" y1="%s" x2="%d" y2="%s" stroke="%s"/>' % (lab_w, _f(y), width - pad_r, _f(y), GRID))
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-opacity="0.35"/>'
                   % (_f(X(m - sd)), _f(y), _f(X(m + sd)), _f(y), SHIP[0]))
        for v in vs:
            out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-opacity="0.5"/>' % (_f(X(v)), _f(y - 5), _f(X(v)), _f(y + 5), MUTED))
        out.append('<circle cx="%s" cy="%s" r="4.5" fill="%s" stroke="%s" stroke-width="2"><title>%s: %s ± %s</title></circle>'
                   % (_f(X(m)), _f(y), SHIP[0], SURF, esc(label), fmt % m, fmt % sd))
        out.append('<text x="%d" y="%s" font-size="10" text-anchor="end" fill="%s">%s</text>' % (width, _f(y + 3.5), INK, fmt % m))
    yb = H - 6
    for v in (lo + (hi - lo) * k / 4 for k in range(5)):
        out.append('<text x="%s" y="%d" font-size="8" text-anchor="middle" fill="%s">%s</text>' % (_f(X(v)), yb, MUTED, fmt % v))
    return wrap(width, H, "".join(out), title)


def line_chart(series, title, xlabel, ylabel, width=520, height=200, xs=None, xticks=None):
    """series: list of (label, [y]) on a shared x. Direct labels at the right end,
    nudged apart so they never overlap."""
    lab_r, pad_l, pad_b, pad_t = 92, 44, 30, 18
    ys = [v for _, s in series for v in s]
    lo, hi = min(ys + [0.0]), max(ys)
    if hi - lo < 1e-9:
        hi = lo + 1
    n = len(series[0][1])
    xs = xs or list(range(n))
    X = lambda x: pad_l + (x - xs[0]) / max(1e-9, xs[-1] - xs[0]) * (width - pad_l - lab_r)
    Y = lambda v: pad_t + (hi - v) / (hi - lo) * (height - pad_t - pad_b)
    out = []
    for k in range(5):
        v = lo + (hi - lo) * k / 4
        out.append('<line x1="%d" y1="%s" x2="%d" y2="%s" stroke="%s"/>' % (pad_l, _f(Y(v)), width - lab_r, _f(Y(v)), GRID))
        out.append('<text x="%d" y="%s" font-size="8" text-anchor="end" fill="%s">%s</text>' % (pad_l - 4, _f(Y(v) + 3), MUTED, "%.0f" % v if abs(hi - lo) > 20 else "%.2f" % v))
    for xt in (xticks or []):
        out.append('<text x="%s" y="%d" font-size="8" text-anchor="middle" fill="%s">%s</text>' % (_f(X(xt)), height - pad_b + 12, MUTED, xt))
    ends = []
    for j, (label, s) in enumerate(series):
        d = "M" + " L".join("%s %s" % (_f(X(xs[i])), _f(Y(v))) for i, v in enumerate(s))
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (d, SHIP[j % 4]))
        ends.append([Y(s[-1]) + 3, label, j])
    ends.sort()
    for k in range(1, len(ends)):
        if ends[k][0] - ends[k - 1][0] < 11:
            ends[k][0] = ends[k - 1][0] + 11
    for y, label, j in ends:
        out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="2"/>' % (_f(width - lab_r + 4), _f(y - 3), _f(width - lab_r + 12), _f(y - 3), SHIP[j % 4]))
        out.append('<text x="%s" y="%s" font-size="9" fill="%s">%s</text>' % (_f(width - lab_r + 15), _f(y), INK2, esc(label)))
    out.append('<text x="%s" y="%d" font-size="9" text-anchor="middle" fill="%s">%s</text>' % (_f((width - lab_r + pad_l) / 2), height - 4, MUTED, esc(xlabel)))
    out.append('<text x="%d" y="10" font-size="9" fill="%s">%s</text>' % (pad_l, MUTED, esc(ylabel)))
    return wrap(width, height, "".join(out), title)
