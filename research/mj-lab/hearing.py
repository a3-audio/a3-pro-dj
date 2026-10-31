"""How one listener hears a moving band in the dome. A MODEL, built from the
research note (knowledge/spatial/motion-perception.md, part A). Every constant lives in
HearingTuning with the row it comes from; nothing here is measured on a real system.

Coordinates: floor units, speaker ring at radius 1 on the ear plane (z = 0),
an upper ring of 4 at 45 deg. A ship at floor point p is rendered at the dome
point S = dome_point(p) on the unit sphere,
which is how a dragged blob maps onto the hemisphere (HeightMap::mapTo3D,
default ElevationParams; see dome_point).
"""

import math
from dataclasses import dataclass

DEG = 180.0 / math.pi


@dataclass
class HearingTuning:
    # Room: 6 m from centre to the speaker ring (only used for talk, not maths).
    roomRadiusM: float = 6.0
    floorEdge: float = 0.85          # listeners stay inside this radius
    # MAMA vs speed, front, broadband (Perrott & Musicant 1977; Saberi & Perrott 1990)
    mamaTable: tuple = ((1.8, 1.7), (20.0, 4.0), (90.0, 8.3), (180.0, 13.0),
                        (360.0, 21.2), (900.0, 40.0))
    mamaScale: float = 1.0           # global knob for robustness checks
    # MAMA vs angle from the facing direction: 5 deg front -> >30 deg at the side
    # (Grantham 1986): factor 1 + kSide * sin^2(alpha)
    kSide: float = 5.0
    # vertical MAMAs are larger at every speed (Saberi & Perrott 1990)
    verticalPenalty: float = 1.8
    # integration windows: 336 ms minimum (Chandler & Grantham 1992),
    # ~1 s velocity integration (Locke et al. 2016)
    windowShortS: float = 0.336
    windowLongS: float = 1.0
    # off-centre: 3rd-order sweet area covers almost the whole array
    # (Zotter & Frank): blur grows with (r / sweet)^2 -- MJ hypothesis for the shape
    sweetRadius: float = 0.75
    offCentreBlur: float = 0.6
    # precedence pulls transients towards the nearest speaker off centre
    # (Stitt et al. 2017): weight = kPrecedence * (r / floorEdge) * transient
    kPrecedence: float = 0.5
    transient: float = 0.6
    # salience saturates when the angle moved is (1 + zSat) x threshold
    zSat: float = 2.0
    levelRef: float = 0.45
    # front/back confusion and the upper limit of rotation (Feron 2010; Roggerone 2019)
    ulBroadband: float = 2.5         # rot/s, white noise
    fbBase: float = 0.05
    fbLowBand: float = 0.4
    # habituation: steady motion keeps this share of its interest -- MJ hypothesis
    novelFloor: float = 0.2
    surpriseDecayBeats: float = 4.0
    expectationBeats: float = 2.0
    turnEventDeg: float = 45.0       # a change of heading this large is "it bent"
    speedUpRatio: float = 2.0        # speed-ups need ~2x (Carlile & Best; Locke 2016)
    slowDownRatio: float = 1.5
    onBeatWindow: float = 0.15       # beats either side of an onset -- MJ hypothesis
    offBeatEventValue: float = 0.7   # an event off the beat is worth less -- MJ hypothesis
    # attention follows about one stream, others count less -- MJ hypothesis
    attention: tuple = (1.0, 0.4, 0.15, 0.05)
    # fatigue (no published threshold exists; all MJ hypothesis)
    loadComfort: float = 1.2
    kLoad: float = 0.04
    vectionOnsetDegS: float = 90.0
    vectionRangeDegS: float = 360.0
    kVection: float = 0.05
    kBlur: float = 0.03
    eventComfortPerBeat: float = 0.5
    kOverload: float = 0.05
    recoveryBeats: float = 16.0
    blurPenalty: float = 0.5
    fatiguePenalty: float = 0.3
    # robustness switches: speaker layout and where listeners face
    layout: str = "8+4"              # 8+4 | 8 | 16+8
    facing: str = "dj"               # dj | centre | random
    proxMax: float = 2.0                 # how much louder a band gets when it passes close
    elevationLikeAzimuth: bool = False  # robustness: hear overhead motion as well as horizontal


@dataclass
class Band:
    """The moving band of the 3D filter: centre in Hz, width in octaves."""
    freq: float = 3000.0
    octaves: float = 2.0

    @property
    def low(self):
        return self.freq / 2 ** (self.octaves / 2)

    @property
    def high(self):
        return self.freq * 2 ** (self.octaves / 2)


def _octaves_above(band, f):
    lo, hi = math.log2(band.low), math.log2(band.high)
    edge = math.log2(f)
    return max(0.0, hi - max(lo, edge))


def band_profile(band: Band, h: HearingTuning):
    """Everything about the band that does not depend on where it is."""
    bw = band.octaves
    # localisation blur: >1 oct ~6.5 deg rms whatever the CF; narrower worse,
    # worst around 1.5-2 kHz (Yost & Zhong 2014; Mills 1958)
    mid = math.exp(-(math.log2(band.freq / 1750.0) ** 2) / (2 * 0.7 ** 2))
    narrow = max(0.0, 1.0 - bw)
    sigma = 6.5 * (1 + 1.5 * narrow) * (1 + 0.6 * mid * (1 if bw < 1.5 else 0.3))
    # club bass: room modes and shared subs -- practice (4DSOUND, Rex Club)
    low_pen = 1 + 3 * min(1.0, max(0.0, math.log2(400.0 / band.high) / 1.5))
    m_band = sigma / 6.5 * low_pen
    # upper limit of rotation rises with CF and bandwidth (Roggerone 2019)
    cf_term = min(1.0, max(0.1, math.log2(band.freq / 125.0) / 5.0))
    bw_term = min(1.0, 0.35 + 0.65 * min(bw, 3.0) / 3.0)
    ul = h.ulBroadband * cf_term * bw_term
    # front/back confusion: needs energy at 8-16 kHz (Langendijk & Bronkhorst 2002)
    hf = min(1.0, _octaves_above(band, 3000.0) / 1.5)
    p_fb = h.fbBase + h.fbLowBand * (1 - hf)
    # elevation cue: 6-12 kHz (Langendijk & Bronkhorst); a narrow high band sits
    # at its own height (Middlebrooks 1992, directional bands)
    elev = 0.2 + 0.8 * min(1.0, _octaves_above(band, 5000.0) / 1.0)
    if bw < 1.0 and band.freq > 4000:
        elev *= 0.3
    if h.elevationLikeAzimuth:
        elev = h.verticalPenalty
    # share of club-music energy in the band, relative to full band -- guess
    energy = bw / (bw + 1.5)
    if band.high < 300:
        energy *= 1.4
    return dict(m_band=m_band, ul=ul, p_fb=p_fb, elev=elev, energy=energy,
                clarity_fb=1 - p_fb)


def mama(omega, h: HearingTuning):
    tab = h.mamaTable
    if omega <= tab[0][0]:
        return tab[0][1]
    for (x0, y0), (x1, y1) in zip(tab, tab[1:]):
        if omega <= x1:
            return y0 + (y1 - y0) * (omega - x0) / (x1 - x0)
    (x0, y0), (x1, y1) = tab[-2], tab[-1]
    return y1 + (y1 - y0) * (omega - x1) / (x1 - x0)


# Speakers: 8 on the ear plane, 4 at 45 deg (the default layout).
def speaker_layout(ring, upper):
    out = [(math.cos(k * 2 * math.pi / ring), math.sin(k * 2 * math.pi / ring), 0.0) for k in range(ring)]
    out += [(math.cos(k * 2 * math.pi / upper + math.pi / upper) * 0.7071,
             math.sin(k * 2 * math.pi / upper + math.pi / upper) * 0.7071, 0.7071) for k in range(upper)]
    return out


LAYOUTS = {"8+4": None, "8": speaker_layout(8, 0), "16+8": speaker_layout(16, 8)}

SPEAKERS = [(math.cos(k * math.pi / 4), math.sin(k * math.pi / 4), 0.0) for k in range(8)] + \
           [(math.cos(k * math.pi / 2 + math.pi / 4) * 0.7071,
             math.sin(k * math.pi / 2 + math.pi / 4) * 0.7071, 0.7071) for k in range(4)]


def dome_point(px, py, reach=0.5):
    """HeightMap::mapTo3D with default ElevationParams (centre at the pole):
    the polar angle grows linearly with the floor radius, reaching
    reach * pi at r = sqrt(2) (reach 0.5: the corner sits on the equator,
    the room edge r = 1 at 26 deg elevation)."""
    r = math.hypot(px, py)
    if r < 1e-9:
        return 0.0, 0.0, 1.0
    polar = reach * math.pi * min(r, math.sqrt(2.0)) / math.sqrt(2.0)
    s = math.sin(polar) / r
    return px * s, py * s, math.cos(polar)


LAYOUTS["8+4"] = SPEAKERS


def nearest_speaker(sx, sy, sz, speakers=None):
    speakers = speakers or SPEAKERS
    best, bd = speakers[0], -9.0
    for s in speakers:
        d = s[0] * sx + s[1] * sy + s[2] * sz
        if d > bd:
            bd, best = d, s
    return best


def perceived_direction(qx, qy, S, h: HearingTuning, r_q):
    """Unit vector from the listener to where the band is heard."""
    sx, sy, sz = S
    dx, dy, dz = sx - qx, sy - qy, sz
    dl = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / dl, dy / dl, dz / dl
    w = h.kPrecedence * min(1.0, r_q / h.floorEdge) * h.transient
    if w > 0.0:
        kx, ky, kz = nearest_speaker(sx, sy, sz, LAYOUTS[h.layout])
        ex, ey, ez = kx - qx, ky - qy, kz
        el = math.sqrt(ex * ex + ey * ey + ez * ez)
        dx = (1 - w) * dx + w * ex / el
        dy = (1 - w) * dy + w * ey / el
        dz = (1 - w) * dz + w * ez / el
        n = math.sqrt(dx * dx + dy * dy + dz * dz)
        dx, dy, dz = dx / n, dy / n, dz / n
    return dx, dy, dz, dl


def az_el(d):
    return math.atan2(d[1], d[0]), math.asin(max(-1.0, min(1.0, d[2])))


def wrap(a):
    while a > math.pi:
        a -= 2 * math.pi
    while a < -math.pi:
        a += 2 * math.pi
    return a
