"""
CEP — Controle Estatístico de Processo
Análise completa: Cp, Cpk, Cpu, Cpl, X-barra, R-barra, σ
Estabilidade + Capacidade + Repetibilidade
"""

import streamlit as st
import math
import io
import statistics
from datetime import date, datetime

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CEP — Controle Estatístico de Processo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif !important;
  background: #060810 !important;
  color: #eaf0ff !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.5rem 5rem !important; max-width: 1100px; }

/* ── APP HEADER */
.cep-header {
  background: linear-gradient(135deg, #0d1b4b 0%, #102060 40%, #0a3080 100%);
  border: 1px solid rgba(77,130,255,0.3);
  border-radius: 18px; padding: 28px 32px; margin-bottom: 28px;
  display: flex; align-items: center; gap: 20px;
}
.cep-header-icon {
  width: 60px; height: 60px; border-radius: 14px;
  background: linear-gradient(135deg,#1e5cff,#00c4ff);
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; flex-shrink: 0;
}
.cep-header-title { font-size: 22px; font-weight: 800; color: #fff; letter-spacing: -0.04em; }
.cep-header-sub   { font-size: 12px; color: rgba(180,200,255,0.7); margin-top: 4px; letter-spacing: 0.06em; text-transform: uppercase; }

/* ── SECTION HEADS */
.sec-head {
  font-size: 11px; font-weight: 700; color: rgba(120,160,255,0.8);
  text-transform: uppercase; letter-spacing: 0.12em;
  display: flex; align-items: center; gap: 8px;
  margin: 24px 0 12px;
}
.sec-head::before { content:''; width:3px; height:14px; background:#1e5cff; border-radius:2px; }

/* ── INDICATOR CARDS */
.ind-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(150px,1fr)); gap:10px; margin-bottom:20px; }
.ind-card {
  background: #0e1423; border: 1px solid rgba(77,130,255,0.15);
  border-radius: 14px; padding: 16px 18px; position: relative; overflow: hidden;
}
.ind-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background: var(--accent, #1e5cff);
}
.ind-card.ok   { --accent: #00e5a0; border-color: rgba(0,229,160,0.2); background: rgba(0,229,160,0.04); }
.ind-card.wn   { --accent: #ffb340; border-color: rgba(255,179,64,0.2);  background: rgba(255,179,64,0.04); }
.ind-card.bad  { --accent: #ff4455; border-color: rgba(255,68,85,0.25);  background: rgba(255,68,85,0.05); }
.ind-card.info { --accent: #4d9eff; border-color: rgba(77,158,255,0.2);  background: rgba(77,158,255,0.04); }
.ind-label { font-size: 10px; font-weight: 700; color: rgba(150,180,255,0.7); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
.ind-value { font-size: 28px; font-weight: 800; font-family: 'JetBrains Mono', monospace; letter-spacing: -0.04em; color: #eaf0ff; }
.ind-card.ok  .ind-value { color: #00e5a0; }
.ind-card.wn  .ind-value { color: #ffb340; }
.ind-card.bad .ind-value { color: #ff4455; }
.ind-card.info .ind-value{ color: #4d9eff; }
.ind-desc { font-size: 11px; color: rgba(150,180,255,0.55); margin-top: 5px; line-height: 1.4; }

/* ── SCALE BADGE */
.scale-badge {
  display: inline-block; padding: 2px 9px; border-radius: 20px;
  font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace; margin-top: 6px;
}
.scale-badge.bad  { background: rgba(255,68,85,0.15);  color: #ff4455; border: 1px solid rgba(255,68,85,0.3); }
.scale-badge.wn   { background: rgba(255,179,64,0.15);  color: #ffb340; border: 1px solid rgba(255,179,64,0.3); }
.scale-badge.ok   { background: rgba(0,229,160,0.12);  color: #00e5a0; border: 1px solid rgba(0,229,160,0.3); }
.scale-badge.ex   { background: rgba(0,180,255,0.12);  color: #00c4ff; border: 1px solid rgba(0,180,255,0.3); }

/* ── INSIGHT BOXES */
.ins { border-radius: 12px; padding: 13px 17px; margin-bottom: 9px; border-left: 4px solid; font-size: 13px; line-height: 1.65; }
.ins.ok  { background: rgba(0,229,160,0.07);  color: rgba(0,229,160,0.95);  border-color: #00e5a0; }
.ins.wn  { background: rgba(255,179,64,0.07);  color: rgba(255,179,64,0.95);  border-color: #ffb340; }
.ins.bad { background: rgba(255,68,85,0.07);   color: rgba(255,68,85,0.95);   border-color: #ff4455; }
.ins strong { font-weight: 700; }

/* ── CURVA NORMAL SVG */
.normal-wrap { background:#0e1423; border:1px solid rgba(77,130,255,0.15); border-radius:14px; padding:14px; }

/* ── STREAMLIT OVERRIDES */
div[data-testid="stTabs"] button {
  font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
  font-size: 13px !important;
}
.stDataFrame { border-radius: 12px !important; overflow: hidden; }
.stProgress > div > div { background: #0e1423 !important; border-radius:4px !important; }
.stProgress > div > div > div { background: linear-gradient(90deg,#1e5cff,#00c4ff) !important; border-radius:4px !important; }
label { color: rgba(150,180,255,0.7) !important; font-size: 11px !important; font-weight: 600 !important; letter-spacing: 0.04em !important; text-transform: uppercase !important; }
input, select, textarea {
  background: #0e1423 !important; border: 1px solid rgba(77,130,255,0.2) !important;
  color: #eaf0ff !important; border-radius: 8px !important;
  font-family: 'Inter', sans-serif !important;
}
input:focus { border-color: #1e5cff !important; box-shadow: 0 0 0 3px rgba(30,92,255,0.15) !important; }
.stButton > button {
  background: #0e1423 !important; color: #eaf0ff !important;
  border: 1px solid rgba(77,130,255,0.25) !important;
  border-radius: 9px !important; font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important; font-size: 13px !important;
}
.stButton > button:hover { background: #1a2540 !important; border-color: rgba(77,130,255,0.5) !important; }
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg,#1e5cff,#0044cc) !important;
  color: #fff !important; border-color: #1e5cff !important;
}
.stButton > button[kind="primary"]:hover { background: linear-gradient(135deg,#2a6aff,#0055ee) !important; }
hr { border-color: rgba(77,130,255,0.12) !important; }
.stExpander { background: #0e1423 !important; border: 1px solid rgba(77,130,255,0.15) !important; border-radius: 12px !important; }
.stSelectbox > div > div { background: #0e1423 !important; border-color: rgba(77,130,255,0.2) !important; }
div[data-testid="stNumberInput"] input { font-family: 'JetBrains Mono', monospace !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MATH ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def parse_vals(samples):
    vals = []
    for s in samples:
        try:
            if str(s).strip() not in ("", "nan", "None"):
                vals.append(float(s))
        except:
            pass
    return vals

def calc_cep(vals, lse=None, lie=None, subgroup=1):
    """Full CEP analysis: Cp, Cpk, Cpu, Cpl, Xbar, Rbar, sigma"""
    n = len(vals)
    if n < 2:
        return None

    mean = sum(vals) / n
    # Population std via sample std
    std  = statistics.stdev(vals)

    # ── Control limits (Xbar chart, individuals if subgroup=1)
    # d2 constant for subgroup size
    d2_table = {1:1.128,2:1.128,3:1.693,4:2.059,5:2.326,6:2.534,7:2.704,8:2.847,9:2.970,10:3.078}
    d2 = d2_table.get(max(1, min(subgroup, 10)), 1.128)

    # Moving range (individuals) or subgroup ranges
    if subgroup == 1:
        ranges = [abs(vals[i+1] - vals[i]) for i in range(n-1)]
    else:
        # split into subgroups
        groups = [vals[i:i+subgroup] for i in range(0, n, subgroup) if len(vals[i:i+subgroup]) == subgroup]
        ranges = [max(g) - min(g) for g in groups]

    r_bar = sum(ranges) / len(ranges) if ranges else 0
    sigma_within = r_bar / d2 if d2 else std

    # Control limits
    A2_table = {1:2.659,2:2.659,3:1.023,4:0.729,5:0.577,6:0.483,7:0.419,8:0.373,9:0.337,10:0.308}
    A2 = A2_table.get(max(1, min(subgroup, 10)), 2.659)
    UCL_x = mean + A2 * r_bar
    LCL_x = mean - A2 * r_bar

    D3_table = {1:0,2:0,3:0,4:0,5:0,6:0,7:0.076,8:0.136,9:0.184,10:0.223}
    D4_table = {1:3.267,2:3.267,3:2.574,4:2.282,5:2.114,6:2.004,7:1.924,8:1.864,9:1.816,10:1.777}
    D3 = D3_table.get(max(1,min(subgroup,10)),0)
    D4 = D4_table.get(max(1,min(subgroup,10)),3.267)
    UCL_r = D4 * r_bar
    LCL_r = D3 * r_bar

    # ── Capability indices (using sigma_within for process capability)
    sigma_use = sigma_within if sigma_within > 0 else std

    cp = cpu = cpl = cpk = None
    if lse is not None and lie is not None and sigma_use > 0:
        cp  = (lse - lie) / (6 * sigma_use)
        cpu = (lse - mean) / (3 * sigma_use)
        cpl = (mean - lie) / (3 * sigma_use)
        cpk = min(cpu, cpl)
    elif lse is not None and sigma_use > 0:
        cpu = (lse - mean) / (3 * sigma_use)
        cpk = cpu
    elif lie is not None and sigma_use > 0:
        cpl = (mean - lie) / (3 * sigma_use)
        cpk = cpl

    # ── Stability: points outside control limits
    out_ctrl = [i for i, v in enumerate(vals) if v > UCL_x or v < LCL_x]

    # ── Nelson rules (simplified: 8 consec same side, trend of 6)
    nelson_violations = []
    # Rule 1: point outside ±3σ
    for i, v in enumerate(vals):
        if abs(v - mean) > 3 * sigma_use:
            nelson_violations.append((i+1, "Ponto fora de ±3σ"))
    # Rule 2: 8 consecutive on same side
    for i in range(len(vals)-7):
        seg = vals[i:i+8]
        if all(v > mean for v in seg) or all(v < mean for v in seg):
            nelson_violations.append((i+1, "8 pontos consecutivos no mesmo lado da média"))
            break
    # Rule 3: 6 consecutive trend
    for i in range(len(vals)-5):
        seg = vals[i:i+6]
        increasing = all(seg[j] < seg[j+1] for j in range(5))
        decreasing = all(seg[j] > seg[j+1] for j in range(5))
        if increasing or decreasing:
            nelson_violations.append((i+1, "Tendência de 6 pontos consecutivos"))
            break

    # ── PPM estimate (approximate, assuming normal)
    ppm_above = ppm_below = ppm_total = None
    if lse is not None or lie is not None:
        def phi(x):  # CDF approximation
            t = 1 / (1 + 0.2316419 * abs(x))
            poly = t*(0.319381530 + t*(-0.356563782 + t*(1.781477937 + t*(-1.821255978 + t*1.330274429))))
            p = 1 - (1/(math.sqrt(2*math.pi)))*math.exp(-0.5*x*x)*poly
            return p if x >= 0 else 1 - p
        if lse is not None and sigma_use > 0:
            z_above = (lse - mean) / sigma_use
            ppm_above = round((1 - phi(z_above)) * 1_000_000)
        if lie is not None and sigma_use > 0:
            z_below = (mean - lie) / sigma_use
            ppm_below = round((1 - phi(z_below)) * 1_000_000)
        ppm_total = (ppm_above or 0) + (ppm_below or 0)

    return dict(
        n=n, mean=mean, std=std,
        sigma_within=sigma_within, r_bar=r_bar,
        ranges=ranges,
        UCL_x=UCL_x, LCL_x=LCL_x,
        UCL_r=UCL_r, LCL_r=LCL_r,
        cp=cp, cpk=cpk, cpu=cpu, cpl=cpl,
        out_ctrl=out_ctrl,
        nelson_violations=nelson_violations,
        ppm_above=ppm_above, ppm_below=ppm_below, ppm_total=ppm_total,
        vals=vals,
    )


def cpk_status(v):
    if v is None: return "info"
    if v >= 1.67: return "ex"
    if v >= 1.33: return "ok"
    if v >= 1.00: return "wn"
    return "bad"

def cpk_label(v):
    if v is None: return "—"
    if v >= 1.67: return "Excelente"
    if v >= 1.33: return "Bom"
    if v >= 1.00: return "Aceitável"
    return "Incapaz"

def card_cls(v):
    if v is None: return "info"
    if v >= 1.33: return "ok"
    if v >= 1.0:  return "wn"
    return "bad"


# ═══════════════════════════════════════════════════════════════════════════════
# SVG CHARTS
# ═══════════════════════════════════════════════════════════════════════════════

def svg_control_chart(vals, mean, ucl, lcl, lse=None, lie=None, title="Gráfico de Controle (CEP)", color="#1e5cff"):
    W, H = 700, 260
    PL, PR, PT, PB = 52, 20, 30, 40
    CW = W - PL - PR
    CH = H - PT - PB

    all_v = list(vals) + [ucl, lcl]
    if lse is not None: all_v.append(lse)
    if lie is not None: all_v.append(lie)
    vmin = min(all_v); vmax = max(all_v)
    vr = vmax - vmin or 1
    padding = vr * 0.1
    vmin -= padding; vmax += padding; vr = vmax - vmin

    def xp(i): return PL + (i / (len(vals)-1 or 1)) * CW
    def yp(v): return PT + CH - ((v - vmin) / vr) * CH

    lines = []
    # grid
    for i in range(5):
        gv = vmin + i*(vmax-vmin)/4
        gy = yp(gv)
        lines.append(f'<line x1="{PL}" y1="{gy:.1f}" x2="{W-PR}" y2="{gy:.1f}" stroke="rgba(77,130,255,0.08)" stroke-width="1"/>')
        lines.append(f'<text x="{PL-4}" y="{gy+4:.1f}" text-anchor="end" font-size="9" fill="rgba(150,180,255,0.5)" font-family="JetBrains Mono">{gv:.3f}</text>')

    # control limit bands
    band_top = min(yp(ucl), PT)
    band_bot = max(yp(lcl), PT+CH)
    lines.append(f'<rect x="{PL}" y="{PT}" width="{CW}" height="{yp(ucl)-PT:.1f}" fill="rgba(255,68,85,0.06)"/>')
    lines.append(f'<rect x="{PL}" y="{yp(lcl):.1f}" width="{CW}" height="{PT+CH-yp(lcl):.1f}" fill="rgba(255,68,85,0.06)"/>')

    # limit lines
    def hline(v, col, lbl, dash=""):
        yy = yp(v)
        da = 'stroke-dasharray="5,3"' if dash else ""
        lines.append(f'<line x1="{PL}" y1="{yy:.1f}" x2="{W-PR}" y2="{yy:.1f}" stroke="{col}" stroke-width="1.2" {da}/>')
        lines.append(f'<text x="{W-PR+3}" y="{yy+4:.1f}" font-size="8.5" fill="{col}" font-family="JetBrains Mono">{lbl}</text>')

    hline(mean, "#4d9eff", "X̄")
    hline(ucl,  "#ff4455", "UCL", "dash")
    hline(lcl,  "#ff4455", "LCL", "dash")
    if lse is not None: hline(lse, "#ffb340", "LSE", "dash")
    if lie is not None: hline(lie, "#ffb340", "LIE", "dash")

    # connecting line
    pts = " ".join(f"{xp(i):.1f},{yp(v):.1f}" for i,v in enumerate(vals))
    lines.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>')

    # points
    for i, v in enumerate(vals):
        out = (lse is not None and v > lse) or (lie is not None and v < lie) or (v > ucl) or (v < lcl)
        fc = "#ff4455" if out else color
        lines.append(f'<circle cx="{xp(i):.1f}" cy="{yp(v):.1f}" r="4" fill="{fc}" stroke="{fc}" stroke-width="0"/>')
        if out:
            lines.append(f'<circle cx="{xp(i):.1f}" cy="{yp(v):.1f}" r="7" fill="none" stroke="#ff4455" stroke-width="1.5" opacity="0.5"/>')

    # x-axis labels
    step = max(1, len(vals)//8)
    for i in range(0, len(vals), step):
        lines.append(f'<text x="{xp(i):.1f}" y="{PT+CH+14}" text-anchor="middle" font-size="9" fill="rgba(150,180,255,0.5)" font-family="JetBrains Mono">{i+1}</text>')

    # axis labels
    lines.append(f'<text x="{W//2}" y="{H}" text-anchor="middle" font-size="10" fill="rgba(150,180,255,0.5)">Amostra</text>')
    lines.append(f'<text x="10" y="{H//2}" text-anchor="middle" font-size="10" fill="rgba(150,180,255,0.5)" transform="rotate(-90,10,{H//2})">Valor</text>')

    svg = f'''<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="display:block">
  <rect width="{W}" height="{H}" fill="#0a0e1a" rx="10"/>
  <text x="{PL}" y="18" font-size="11" font-weight="700" fill="rgba(150,180,255,0.7)" font-family="Inter">{title}</text>
  {''.join(lines)}
</svg>'''
    return svg


def svg_histogram(vals, mean, std, lse=None, lie=None, n_bins=None):
    W, H = 700, 240
    PL, PR, PT, PB = 44, 20, 24, 38

    if n_bins is None:
        n_bins = max(5, min(12, int(math.sqrt(len(vals)))))
    mn = min(vals); mx = max(vals)
    bw = (mx - mn) / n_bins or 1

    bins = []
    for i in range(n_bins):
        lo = mn + i*bw; hi = mn + (i+1)*bw
        cnt = sum(1 for v in vals if v >= lo and (v < hi if i < n_bins-1 else v <= hi))
        bins.append((lo, hi, cnt))
    max_cnt = max(b[2] for b in bins) or 1

    CW = W - PL - PR
    CH = H - PT - PB

    parts = []
    # grid
    for i in range(5):
        gy = PT + i*(CH/4)
        cv = max_cnt - i*(max_cnt/4)
        parts.append(f'<line x1="{PL}" y1="{gy:.1f}" x2="{W-PR}" y2="{gy:.1f}" stroke="rgba(77,130,255,0.08)" stroke-width="1"/>')
        parts.append(f'<text x="{PL-4}" y="{gy+4:.1f}" text-anchor="end" font-size="9" fill="rgba(150,180,255,0.4)" font-family="JetBrains Mono">{int(cv)}</text>')

    bw_px = CW / n_bins
    for i, (lo, hi, cnt) in enumerate(bins):
        bh = (cnt / max_cnt) * CH if max_cnt else 0
        bx = PL + i * bw_px
        by = PT + CH - bh
        mid = (lo + hi) / 2
        # color based on spec
        out_hi = lse is not None and hi > lse
        out_lo = lie is not None and lo < lie
        if out_hi or out_lo:
            fc, oc = "rgba(255,68,85,0.5)", "#ff4455"
        else:
            fc, oc = "rgba(30,92,255,0.45)", "#1e5cff"
        parts.append(f'<rect x="{bx+1:.1f}" y="{by:.1f}" width="{bw_px-2:.1f}" height="{bh:.1f}" fill="{fc}" stroke="{oc}" stroke-width="1" rx="2"/>')
        if len(bins) <= 10:
            parts.append(f'<text x="{bx+bw_px/2:.1f}" y="{H-PT+2}" text-anchor="middle" font-size="8" fill="rgba(150,180,255,0.45)" font-family="JetBrains Mono">{mid:.2f}</text>')

    # Normal curve overlay
    sigma = std if std > 0 else 0.001
    def norm_y(x):
        return (1/(sigma*math.sqrt(2*math.pi)))*math.exp(-0.5*((x-mean)/sigma)**2)
    xrange = [mn + j*(mx-mn)/100 for j in range(101)]
    ny_vals = [norm_y(x) for x in xrange]
    ny_max = max(ny_vals) or 1
    # scale to histogram height
    scale = CH / ny_max * (max_cnt / (len(vals) * bw))
    curve_pts = []
    for j, (x, ny) in enumerate(zip(xrange, ny_vals)):
        cx = PL + (x - mn) / (mx - mn) * CW
        cy = PT + CH - ny * scale * len(vals) * bw
        cy = max(PT, min(PT+CH, cy))
        curve_pts.append(f"{cx:.1f},{cy:.1f}")
    if curve_pts:
        parts.append(f'<polyline points="{" ".join(curve_pts)}" fill="none" stroke="rgba(0,229,160,0.7)" stroke-width="1.8" stroke-linejoin="round"/>')

    # mean line
    mx_px = PL + (mean - mn) / (mx - mn + 0.001) * CW
    parts.append(f'<line x1="{mx_px:.1f}" y1="{PT}" x2="{mx_px:.1f}" y2="{PT+CH}" stroke="#4d9eff" stroke-width="1.5" stroke-dasharray="4,3"/>')
    parts.append(f'<text x="{mx_px+3:.1f}" y="{PT+12}" font-size="9" fill="#4d9eff" font-family="JetBrains Mono">X̄</text>')

    # spec limits
    if lse is not None:
        lx = PL + (lse - mn)/(mx-mn+0.001)*CW
        parts.append(f'<line x1="{lx:.1f}" y1="{PT}" x2="{lx:.1f}" y2="{PT+CH}" stroke="#ffb340" stroke-width="1.5" stroke-dasharray="3,3"/>')
        parts.append(f'<text x="{lx+2:.1f}" y="{PT+9}" font-size="8.5" fill="#ffb340" font-family="JetBrains Mono">LSE</text>')
    if lie is not None:
        lx = PL + (lie - mn)/(mx-mn+0.001)*CW
        parts.append(f'<line x1="{lx:.1f}" y1="{PT}" x2="{lx:.1f}" y2="{PT+CH}" stroke="#ffb340" stroke-width="1.5" stroke-dasharray="3,3"/>')
        parts.append(f'<text x="{lx+2:.1f}" y="{PT+9}" font-size="8.5" fill="#ffb340" font-family="JetBrains Mono">LIE</text>')

    svg = f'''<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="display:block">
  <rect width="{W}" height="{H}" fill="#0a0e1a" rx="10"/>
  <text x="{PL}" y="16" font-size="11" font-weight="700" fill="rgba(150,180,255,0.7)" font-family="Inter">Histograma + Curva Normal</text>
  {''.join(parts)}
</svg>'''
    return svg


def svg_moving_range(ranges, ucl_r, r_bar, title="Gráfico de Amplitude Móvel (MR)"):
    W, H = 700, 180
    PL, PR, PT, PB = 52, 20, 24, 36
    CW = W - PL - PR; CH = H - PT - PB

    vmin = 0
    vmax = max(max(ranges), ucl_r) * 1.1 or 1
    vr = vmax - vmin

    def xp(i): return PL + (i / (len(ranges)-1 or 1)) * CW
    def yp(v): return PT + CH - ((v - vmin) / vr) * CH

    parts = []
    # grid
    for i in range(4):
        gy = PT + i*(CH/3)
        gv = vmax - i*(vmax/3)
        parts.append(f'<line x1="{PL}" y1="{gy:.1f}" x2="{W-PR}" y2="{gy:.1f}" stroke="rgba(77,130,255,0.07)" stroke-width="1"/>')
        parts.append(f'<text x="{PL-4}" y="{gy+4:.1f}" text-anchor="end" font-size="9" fill="rgba(150,180,255,0.4)" font-family="JetBrains Mono">{gv:.3f}</text>')

    # fill area under curve
    area_pts = f"{xp(0):.1f},{PT+CH}"
    for i, r in enumerate(ranges):
        area_pts += f" {xp(i):.1f},{yp(r):.1f}"
    area_pts += f" {xp(len(ranges)-1):.1f},{PT+CH}"
    parts.append(f'<polygon points="{area_pts}" fill="rgba(30,92,255,0.08)"/>')

    # UCL and R-bar lines
    ucl_y = yp(ucl_r)
    rbar_y = yp(r_bar)
    parts.append(f'<line x1="{PL}" y1="{ucl_y:.1f}" x2="{W-PR}" y2="{ucl_y:.1f}" stroke="#ff4455" stroke-width="1.2" stroke-dasharray="4,3"/>')
    parts.append(f'<text x="{W-PR+3}" y="{ucl_y+4:.1f}" font-size="8.5" fill="#ff4455" font-family="JetBrains Mono">UCL</text>')
    parts.append(f'<line x1="{PL}" y1="{rbar_y:.1f}" x2="{W-PR}" y2="{rbar_y:.1f}" stroke="#4d9eff" stroke-width="1.2" stroke-dasharray="4,3"/>')
    parts.append(f'<text x="{W-PR+3}" y="{rbar_y+4:.1f}" font-size="8.5" fill="#4d9eff" font-family="JetBrains Mono">R̄</text>')

    # line
    pts = " ".join(f"{xp(i):.1f},{yp(r):.1f}" for i, r in enumerate(ranges))
    parts.append(f'<polyline points="{pts}" fill="none" stroke="#a855f7" stroke-width="1.8" stroke-linejoin="round"/>')
    for i, r in enumerate(ranges):
        out = r > ucl_r
        fc = "#ff4455" if out else "#a855f7"
        parts.append(f'<circle cx="{xp(i):.1f}" cy="{yp(r):.1f}" r="3.5" fill="{fc}"/>')

    # x labels
    step = max(1, len(ranges)//8)
    for i in range(0, len(ranges), step):
        parts.append(f'<text x="{xp(i):.1f}" y="{PT+CH+13}" text-anchor="middle" font-size="9" fill="rgba(150,180,255,0.4)" font-family="JetBrains Mono">{i+2}</text>')

    svg = f'''<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="display:block">
  <rect width="{W}" height="{H}" fill="#0a0e1a" rx="10"/>
  <text x="{PL}" y="16" font-size="11" font-weight="700" fill="rgba(150,180,255,0.7)" font-family="Inter">{title}</text>
  {''.join(parts)}
</svg>'''
    return svg


def svg_normal_curve(mean, std, lse=None, lie=None):
    W, H = 500, 200
    PL, PR, PT, PB = 20, 20, 20, 30
    CW = W - PL - PR; CH = H - PT - PB

    sigma_range = 4
    x_min = mean - sigma_range * std
    x_max = mean + sigma_range * std
    x_range = x_max - x_min or 1

    def xp(x): return PL + (x - x_min) / x_range * CW
    def norm(x): return (1/(std*math.sqrt(2*math.pi)))*math.exp(-0.5*((x-mean)/std)**2) if std > 0 else 0

    N = 200
    xs = [x_min + i*(x_max-x_min)/(N-1) for i in range(N)]
    ys = [norm(x) for x in xs]
    y_max = max(ys) or 1
    def yp(y): return PT + CH - (y/y_max)*CH

    parts = []
    # baseline
    parts.append(f'<line x1="{PL}" y1="{PT+CH}" x2="{W-PR}" y2="{PT+CH}" stroke="rgba(77,130,255,0.2)" stroke-width="1"/>')

    # fill zones
    def fill_zone(x0, x1, fill):
        pts_top = [(xp(x), yp(norm(x))) for x in [x0 + j*(x1-x0)/50 for j in range(51)] if x_min <= x <= x_max]
        if not pts_top: return
        poly = f"{xp(max(x0,x_min)):.1f},{PT+CH}"
        for px, py in pts_top: poly += f" {px:.1f},{py:.1f}"
        poly += f" {xp(min(x1,x_max)):.1f},{PT+CH}"
        parts.append(f'<polygon points="{poly}" fill="{fill}"/>')

    # green zone (within spec)
    lo_spec = lie if lie is not None else x_min
    hi_spec = lse if lse is not None else x_max
    fill_zone(lo_spec, hi_spec, "rgba(0,229,160,0.18)")
    # yellow zones
    fill_zone(mean - 2*std, lie if lie is not None else mean-2*std, "rgba(255,179,64,0.2)")
    fill_zone(lse if lse is not None else mean+2*std, mean + 2*std, "rgba(255,179,64,0.2)")
    # red zones
    if lie is not None: fill_zone(x_min, lie, "rgba(255,68,85,0.25)")
    if lse is not None: fill_zone(lse, x_max, "rgba(255,68,85,0.25)")

    # main curve
    curve_pts = " ".join(f"{xp(x):.1f},{yp(y):.1f}" for x, y in zip(xs, ys))
    parts.append(f'<polyline points="{curve_pts}" fill="none" stroke="#1e5cff" stroke-width="2.2" stroke-linejoin="round"/>')

    # σ labels on x-axis
    for k in range(-3, 4):
        xk = mean + k * std
        if x_min <= xk <= x_max:
            lbl = f"{'+' if k > 0 else ''}{k}σ" if k != 0 else "X̄"
            parts.append(f'<text x="{xp(xk):.1f}" y="{PT+CH+14}" text-anchor="middle" font-size="9" fill="rgba(150,180,255,0.6)" font-family="JetBrains Mono">{lbl}</text>')
            parts.append(f'<line x1="{xp(xk):.1f}" y1="{PT+CH-2}" x2="{xp(xk):.1f}" y2="{PT+CH+2}" stroke="rgba(150,180,255,0.3)" stroke-width="1"/>')

    # mean line
    parts.append(f'<line x1="{xp(mean):.1f}" y1="{PT}" x2="{xp(mean):.1f}" y2="{PT+CH}" stroke="#4d9eff" stroke-width="1.2" stroke-dasharray="4,3"/>')

    # spec limits
    if lse is not None and x_min <= lse <= x_max:
        parts.append(f'<line x1="{xp(lse):.1f}" y1="{PT}" x2="{xp(lse):.1f}" y2="{PT+CH}" stroke="#ffb340" stroke-width="1.5" stroke-dasharray="3,3"/>')
        parts.append(f'<text x="{xp(lse)+3:.1f}" y="{PT+12}" font-size="9" fill="#ffb340" font-family="JetBrains Mono">LSE</text>')
    if lie is not None and x_min <= lie <= x_max:
        parts.append(f'<line x1="{xp(lie):.1f}" y1="{PT}" x2="{xp(lie):.1f}" y2="{PT+CH}" stroke="#ffb340" stroke-width="1.5" stroke-dasharray="3,3"/>')
        parts.append(f'<text x="{xp(lie)+3:.1f}" y="{PT+12}" font-size="9" fill="#ffb340" font-family="JetBrains Mono">LIE</text>')

    svg = f'''<svg width="100%" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="display:block">
  <rect width="{W}" height="{H}" fill="#0a0e1a" rx="12"/>
  {''.join(parts)}
</svg>'''
    return svg


def build_insights(r, lse, lie):
    ins = []
    cpk = r.get("cpk")
    cp  = r.get("cp")

    # Stability
    if not r["nelson_violations"] and not r["out_ctrl"]:
        ins.append(("ok", "Processo <strong>estável</strong>. Nenhuma violação das regras de controle detectada."))
    else:
        if r["out_ctrl"]:
            pts = ", ".join(str(i+1) for i in r["out_ctrl"])
            ins.append(("bad", f"<strong>Instabilidade detectada.</strong> Pontos fora dos limites de controle: amostras {pts}."))
        for _, desc in r["nelson_violations"][:3]:
            ins.append(("bad", f"<strong>Violação de regra:</strong> {desc}."))

    # Capability
    if cpk is not None:
        lbl = cpk_label(cpk)
        if cpk >= 1.33:
            ins.append(("ok", f"<strong>Processo capaz.</strong> Cpk={cpk:.2f} — {lbl}. Processo atende às especificações com margem adequada."))
        elif cpk >= 1.00:
            ins.append(("wn", f"<strong>Capacidade marginal.</strong> Cpk={cpk:.2f} — {lbl}. Monitoramento contínuo e revisão de causas especiais recomendada."))
        else:
            ins.append(("bad", f"<strong>Processo incapaz.</strong> Cpk={cpk:.2f} — {lbl}. Risco real de produção fora de especificação. Ação corretiva imediata necessária."))

    # Centering
    if cp is not None and cpk is not None and cp > 0:
        loss = (cp - cpk) / cp * 100
        if loss > 20:
            ins.append(("wn", f"<strong>Descentramento significativo:</strong> {loss:.0f}% de capacidade perdida por deslocamento da média. Cp={cp:.2f} vs Cpk={cpk:.2f}. Ajustar ponto nominal do setup."))

    # PPM
    ppm = r.get("ppm_total")
    if ppm is not None:
        if ppm == 0:
            ins.append(("ok", "Estimativa de não conformidade: <strong>0 ppm</strong>. Processo com alta confiabilidade."))
        elif ppm < 100:
            ins.append(("ok", f"Estimativa de não conformidade: <strong>{ppm} ppm</strong>. Nível de qualidade muito bom."))
        elif ppm < 1000:
            ins.append(("wn", f"Estimativa de não conformidade: <strong>{ppm} ppm</strong>. Avaliar possibilidade de ajuste no processo."))
        else:
            ins.append(("bad", f"Estimativa de não conformidade: <strong>{ppm} ppm</strong>. Volume expressivo de peças fora de especificação esperado."))

    # CPU/CPL
    cpu = r.get("cpu"); cpl = r.get("cpl")
    if cpu is not None and cpl is not None:
        if cpu < 1 and cpl >= 1:
            ins.append(("bad", f"<strong>Risco no limite superior (LSE).</strong> Cpu={cpu:.2f} < 1,00. Média deslocada para cima."))
        elif cpl < 1 and cpu >= 1:
            ins.append(("bad", f"<strong>Risco no limite inferior (LIE).</strong> Cpl={cpl:.2f} < 1,00. Média deslocada para baixo."))

    return ins


# ═══════════════════════════════════════════════════════════════════════════════
# PDF REPORT
# ═══════════════════════════════════════════════════════════════════════════════

def generate_pdf_report(ident, r, lse, lie, param_name, unit):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.graphics.shapes import Drawing, Line, Circle, Rect, String, Polygon
    from reportlab.graphics import renderPDF

    buf = io.BytesIO()
    W, H_page = A4
    ml = mr = 13 * mm
    cw = W - ml - mr

    BG    = colors.HexColor("#060810")
    BLUE  = colors.HexColor("#1e5cff")
    CARD  = colors.HexColor("#0e1423")
    S2    = colors.HexColor("#0a0e1a")
    MUTED = colors.HexColor("#6b7db3")
    TEXT  = colors.HexColor("#eaf0ff")
    GREEN = colors.HexColor("#00e5a0")
    AMBER = colors.HexColor("#ffb340")
    RED   = colors.HexColor("#ff4455")
    PURPLE= colors.HexColor("#a855f7")

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#060810"))
        canvas.rect(0, 0, W, 11*mm, fill=1, stroke=0)
        canvas.setFillColor(BLUE)
        canvas.rect(ml, 9*mm, cw, 0.7, fill=1, stroke=0)
        canvas.setFont("Helvetica", 6.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(ml, 4.5*mm,
            f"CEP Analyzer  ·  {param_name}  ·  {ident.get('linha','—')}  ·  {ident.get('data','—')}")
        canvas.drawRightString(W-ml, 4.5*mm, f"Página {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=ml, rightMargin=mr,
                            topMargin=13*mm, bottomMargin=15*mm)

    styles = getSampleStyleSheet()
    def PS(name, **kw):
        return ParagraphStyle(name, parent=styles["Normal"], **kw)

    story = []

    # ── Header
    hdr = Table([[
        Paragraph("<b>CEP — Controle Estatístico de Processo</b>",
                  PS("ht", fontSize=16, textColor=TEXT, fontName="Helvetica-Bold")),
        Paragraph(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}",
                  PS("hd", fontSize=8, textColor=MUTED, fontName="Helvetica", alignment=2)),
    ]], colWidths=[cw*0.7, cw*0.3])
    hdr.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), BG),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
        ("LINEBELOW",(0,0),(-1,-1),2.5,BLUE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 5*mm))

    def sec(t):
        tbl = Table([[Paragraph(t.upper(),
                     PS("sh", fontSize=7.5, textColor=TEXT, fontName="Helvetica-Bold"))]], colWidths=[cw])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),CARD),
            ("LEFTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),5),
            ("RIGHTPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LINEBEFORE",(0,0),(0,-1),3,BLUE),
        ]))
        story.append(tbl)
        story.append(Spacer(1,3*mm))

    # ── Identification
    sec("1. Identificação")
    id_row = []
    for lbl, val in [("Linha",ident.get("linha","—")),("Embalagem",ident.get("emb","—")),
                     ("Parâmetro",param_name),("Unidade",unit),
                     ("N amostras",str(r["n"])),("Data",ident.get("data","—"))]:
        id_row += [Paragraph(lbl, PS("il",fontSize=7,textColor=MUTED,fontName="Helvetica")),
                   Paragraph(str(val or "—"), PS("iv",fontSize=9,textColor=TEXT,fontName="Helvetica-Bold"))]
    id_tbl = Table([id_row], colWidths=[cw/12]*12)
    id_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),S2),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(id_tbl)
    story.append(Spacer(1,4*mm))

    # ── Indicators
    sec("2. Indicadores CEP")
    cw5 = cw/5
    def ind_cell(label, value, col):
        return [Paragraph(label, PS("kl",fontSize=7,textColor=col,fontName="Helvetica-Bold")),
                Paragraph(str(value), PS("kv",fontSize=16,textColor=col,fontName="Helvetica-Bold"))]

    st_cpk = cpk_status(r.get("cpk"))
    col_cpk = {"ok":GREEN,"wn":AMBER,"bad":RED,"ex":colors.HexColor("#00c4ff")}.get(st_cpk,MUTED)

    ind_cells = []
    for lbl, val, col in [
        ("Cp",   f"{r['cp']:.3f}"  if r.get("cp")  is not None else "—", GREEN if (r.get("cp") or 0)>=1.33 else AMBER),
        ("Cpk",  f"{r['cpk']:.3f}" if r.get("cpk") is not None else "—", col_cpk),
        ("Cpu",  f"{r['cpu']:.3f}" if r.get("cpu") is not None else "—", GREEN if (r.get("cpu") or 0)>=1.33 else AMBER),
        ("Cpl",  f"{r['cpl']:.3f}" if r.get("cpl") is not None else "—", GREEN if (r.get("cpl") or 0)>=1.33 else AMBER),
        ("X̄ Média", f"{r['mean']:.4f}", colors.HexColor("#4d9eff")),
    ]:
        ind_cells += ind_cell(lbl, val, col)

    ind_tbl = Table([ind_cells], colWidths=[cw5/2, cw5/2]*5)
    ind_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),CARD),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LINEABOVE",(0,0),(-1,0),2.5, col_cpk),
    ]))
    story.append(ind_tbl)
    story.append(Spacer(1,3*mm))

    # second row
    ind2_cells = []
    for lbl, val, col in [
        ("σ Desvio", f"{r['std']:.4f}", colors.HexColor("#4d9eff")),
        ("R̄ Amplitude", f"{r['r_bar']:.4f}", PURPLE),
        ("UCL", f"{r['UCL_x']:.4f}", RED),
        ("LCL", f"{r['LCL_x']:.4f}", RED),
        ("PPM estimado", str(r.get("ppm_total","—")), AMBER if (r.get("ppm_total") or 0)>0 else GREEN),
    ]:
        ind2_cells += ind_cell(lbl, val, col)

    ind2_tbl = Table([ind2_cells], colWidths=[cw5/2, cw5/2]*5)
    ind2_tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),S2),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    story.append(ind2_tbl)
    story.append(Spacer(1,4*mm))

    # ── Control chart (vector)
    sec("3. Gráfico de controle — Carta X Individual")
    vals = r["vals"]
    vmin_c = min(vals); vmax_c = max(vals)
    all_c = vals + [r["UCL_x"], r["LCL_x"]]
    if lse is not None: all_c.append(lse)
    if lie is not None: all_c.append(lie)
    vmn = min(all_c)*0.9995; vmx = max(all_c)*1.0005
    vr_c = vmx - vmn or 0.001

    DW, DH = cw, 44*mm
    PL2, PR2, PT2, PB2 = 14*mm, 18*mm, 4*mm, 6*mm
    CW2 = DW - PL2 - PR2; CH2 = DH - PT2 - PB2

    def xpc(i): return PL2 + (i/(len(vals)-1 or 1))*CW2
    def ypc(v): return PT2 + CH2 - ((v-vmn)/vr_c)*CH2

    d = Drawing(DW, DH)
    d.add(Rect(0,0,DW,DH,fillColor=S2,strokeColor=colors.HexColor("#1a2540"),strokeWidth=0.4))

    def pdf_hline(val, col, dsh=False):
        yy = ypc(val)
        ln = Line(PL2, yy, PL2+CW2, yy, strokeColor=col, strokeWidth=0.5)
        if dsh: ln.strokeDashArray=[2,2]
        d.add(ln)
        d.add(String(PL2+CW2+0.5*mm, yy-1.5, f"{val:.3f}",
                     fontSize=5.5, fillColor=col, fontName="Helvetica"))

    pdf_hline(r["mean"], BLUE)
    pdf_hline(r["UCL_x"], RED, True)
    pdf_hline(r["LCL_x"], RED, True)
    if lse is not None: pdf_hline(lse, AMBER, True)
    if lie is not None: pdf_hline(lie, AMBER, True)

    for i in range(len(vals)-1):
        d.add(Line(xpc(i), ypc(vals[i]), xpc(i+1), ypc(vals[i+1]),
                   strokeColor=BLUE, strokeWidth=0.8))
    for i, v in enumerate(vals):
        out = (lse is not None and v>lse) or (lie is not None and v<lie) or v>r["UCL_x"] or v<r["LCL_x"]
        fc = RED if out else BLUE
        d.add(Circle(xpc(i), ypc(v), 1.5, fillColor=fc, strokeColor=fc, strokeWidth=0))

    step = max(1, len(vals)//8)
    for i in range(0, len(vals), step):
        d.add(String(xpc(i)-1.5, PB2-1.5, str(i+1), fontSize=5.5, fillColor=MUTED, fontName="Helvetica"))

    story.append(d)
    story.append(Spacer(1,4*mm))

    # ── MR chart
    sec("4. Gráfico de Amplitude Móvel (MR)")
    ranges = r["ranges"]
    r_bar  = r["r_bar"]
    ucl_r  = r["UCL_r"]
    vmx_r  = max(max(ranges), ucl_r)*1.1 or 1

    DH_r = 30*mm
    dr = Drawing(DW, DH_r)
    dr.add(Rect(0,0,DW,DH_r,fillColor=S2,strokeColor=colors.HexColor("#1a2540"),strokeWidth=0.4))

    def xpr(i): return PL2 + (i/(len(ranges)-1 or 1))*CW2
    def ypr(v): return PB2 + (v/vmx_r)*( DH_r-PT2-PB2)

    ucl_yr = DH_r - PT2 - (ucl_r/vmx_r)*(DH_r-PT2-PB2)
    rbar_yr = DH_r - PT2 - (r_bar/vmx_r)*(DH_r-PT2-PB2)

    dr.add(Line(PL2, ucl_yr, PL2+CW2, ucl_yr, strokeColor=RED, strokeWidth=0.5,
                strokeDashArray=[2,2]))
    dr.add(String(PL2+CW2+0.5*mm, ucl_yr-1.5, f"UCL={ucl_r:.3f}",
                  fontSize=5, fillColor=RED, fontName="Helvetica"))
    dr.add(Line(PL2, rbar_yr, PL2+CW2, rbar_yr, strokeColor=BLUE, strokeWidth=0.5,
                strokeDashArray=[2,2]))
    dr.add(String(PL2+CW2+0.5*mm, rbar_yr-1.5, f"R̄={r_bar:.3f}",
                  fontSize=5, fillColor=BLUE, fontName="Helvetica"))

    for i in range(len(ranges)-1):
        y1 = DH_r-PT2-(ranges[i]/vmx_r)*(DH_r-PT2-PB2)
        y2 = DH_r-PT2-(ranges[i+1]/vmx_r)*(DH_r-PT2-PB2)
        dr.add(Line(xpr(i), y1, xpr(i+1), y2, strokeColor=PURPLE, strokeWidth=0.9))
    for i, rv in enumerate(ranges):
        yy = DH_r-PT2-(rv/vmx_r)*(DH_r-PT2-PB2)
        fc = RED if rv > ucl_r else PURPLE
        dr.add(Circle(xpr(i), yy, 1.4, fillColor=fc, strokeColor=fc, strokeWidth=0))

    story.append(dr)
    story.append(Spacer(1,4*mm))

    # ── Diagnostic
    sec("5. Diagnóstico automático")
    ins_list = build_insights(r, lse, lie)
    col_map = {"ok":GREEN,"wn":AMBER,"bad":RED}
    for lvl, txt in ins_list:
        col = col_map.get(lvl, MUTED)
        clean_txt = txt.replace("<strong>","").replace("</strong>","")
        it = Table([[Paragraph(clean_txt, PS("it",fontSize=8,textColor=col,fontName="Helvetica",leading=11))]],
                   colWidths=[cw])
        it.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),CARD),
            ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LINEBEFORE",(0,0),(0,-1),3,col),
        ]))
        story.append(it)
        story.append(Spacer(1,2*mm))

    # ── Samples table
    story.append(Spacer(1,3*mm))
    sec("6. Dados coletados")
    th = PS("th",fontSize=7,textColor=TEXT,fontName="Helvetica-Bold")
    td = PS("td",fontSize=7,textColor=TEXT,fontName="Helvetica")
    per_row = 10
    n_rows = math.ceil(len(vals)/per_row)
    for row_i in range(n_rows):
        seg = vals[row_i*per_row:(row_i+1)*per_row]
        header = [Paragraph(str(row_i*per_row+j+1), th) for j in range(len(seg))]
        data_r = []
        for v in seg:
            out = (lse is not None and v>lse) or (lie is not None and v<lie)
            data_r.append(Paragraph(f"{v:.4f}", PS("dt",fontSize=7,textColor=RED if out else TEXT,fontName="Helvetica-Bold" if out else "Helvetica")))
        ww = cw / per_row
        data_tbl = Table([header, data_r], colWidths=[ww]*len(seg))
        data_tbl.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0d1525")),
            ("BACKGROUND",(0,1),(-1,1),S2),
            ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4),
            ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
            ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#1a2540")),
        ]))
        story.append(data_tbl)
        story.append(Spacer(1,1.5*mm))

    # ── Signature
    story.append(Spacer(1,4*mm))
    sig = Table([[
        Paragraph("Responsável: _________________________________",
                  PS("sg1",fontSize=8,textColor=MUTED,fontName="Helvetica")),
        Paragraph("Data: ___/___/______    Assinatura: _____________",
                  PS("sg2",fontSize=8,textColor=MUTED,fontName="Helvetica",alignment=2)),
    ]], colWidths=[cw*0.5, cw*0.5])
    sig.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),CARD),
        ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),12),
        ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
    ]))
    story.append(sig)

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    buf.seek(0)
    return buf


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

def init():
    if "tab" not in st.session_state:
        st.session_state.tab = "entrada"
    if "samples_raw" not in st.session_state:
        st.session_state.samples_raw = [""] * 25
    if "result" not in st.session_state:
        st.session_state.result = None

init()

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="cep-header">
  <div class="cep-header-icon">📊</div>
  <div>
    <div class="cep-header-title">Indicadores de Capacidade do Processo — CEP</div>
    <div class="cep-header-sub">Cp · Cpk · Cpu · Cpl · X-barra · R-barra · σ · Estabilidade · Repetibilidade</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab_entrada, tab_analise, tab_referencia = st.tabs([
    "📥  Entrada de dados",
    "📊  Análise CEP",
    "📖  Guia de indicadores",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ENTRADA DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════

with tab_entrada:
    st.markdown('<div class="sec-head">Identificação do processo</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: linha = st.text_input("Linha / célula", placeholder="Ex: ABM206", key="id_linha")
    with c2: emb   = st.text_input("Embalagem / produto", placeholder="Ex: 57x206", key="id_emb")
    with c3: op    = st.text_input("OP / lote", placeholder="Ex: 5634857", key="id_op")
    with c4: data_str = st.date_input("Data", value=date.today(), key="id_data").isoformat()

    st.markdown('<div class="sec-head">Parâmetro controlado</div>', unsafe_allow_html=True)
    p1, p2, p3, p4, p5 = st.columns(5)
    with p1: param_name = st.text_input("Nome do parâmetro", placeholder="Ex: Altura total", key="pname")
    with p2: unit        = st.selectbox("Unidade", ["mm","pol","bar","µm","kgf","N","°C","%"], key="punit")
    with p3: lie_str     = st.text_input("LIE — limite inferior", placeholder="Min", key="plie")
    with p4: lse_str     = st.text_input("LSE — limite superior", placeholder="Máx", key="plse")
    with p5: subgroup    = st.selectbox("Tamanho do subgrupo", [1,2,3,4,5], index=0, key="psg",
                                         help="1 = carta de indivíduos (I-MR)")

    lse_v = float(lse_str) if lse_str.strip() not in ("","None") else None
    lie_v = float(lie_str) if lie_str.strip() not in ("","None") else None

    st.markdown('<div class="sec-head">Dados coletados</div>', unsafe_allow_html=True)

    col_opt1, col_opt2 = st.columns([2,3])
    with col_opt1:
        n_samples = st.selectbox("Número de amostras", [10,15,20,25,30,40,50], index=3, key="ns")
    with col_opt2:
        paste_mode = st.checkbox("📋 Colar dados (separados por vírgula, ponto e vírgula ou Enter)", key="paste_mode")

    if paste_mode:
        raw_text = st.text_area("Cole os valores aqui", height=100, key="paste_text",
                                placeholder="14.66, 14.65, 14.63, 14.67, 14.68...")
        if raw_text.strip():
            import re
            parts = re.split(r"[,;\n\t ]+", raw_text.strip())
            vals_paste = []
            for p_ in parts:
                p_ = p_.strip().replace(",",".")
                try:
                    vals_paste.append(float(p_))
                except:
                    pass
            st.session_state.samples_raw = [str(v) for v in vals_paste] + [""]*(max(0, n_samples - len(vals_paste)))
            st.info(f"✅ {len(vals_paste)} valores lidos.")
    else:
        # Adjust list size
        cur = st.session_state.samples_raw
        if len(cur) < n_samples:
            st.session_state.samples_raw = cur + [""]*(n_samples - len(cur))
        else:
            st.session_state.samples_raw = cur[:n_samples]

        st.markdown("**Digite as medições (5 por linha):**")
        COLS = 5
        for row in range(math.ceil(n_samples / COLS)):
            row_cols = st.columns(COLS)
            for ci in range(COLS):
                idx = row * COLS + ci
                if idx >= n_samples: break
                with row_cols[ci]:
                    cur_v = st.session_state.samples_raw[idx]
                    try: cur_num = float(cur_v) if cur_v not in ("","None") else None
                    except: cur_num = None
                    new_v = st.number_input(f"A{idx+1}", value=cur_num, format="%.4f",
                                            label_visibility="visible", key=f"samp_{idx}")
                    st.session_state.samples_raw[idx] = str(new_v) if new_v is not None else ""

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔬 Calcular CEP — Analisar processo", type="primary", use_container_width=True):
        vals_all = parse_vals(st.session_state.samples_raw[:n_samples])
        if len(vals_all) < 5:
            st.error("Informe ao menos 5 amostras válidas para análise.")
        else:
            r = calc_cep(vals_all, lse_v, lie_v, subgroup)
            if r is None:
                st.error("Não foi possível calcular — verifique os dados (desvio padrão zero?).")
            else:
                st.session_state.result = r
                st.session_state.result["lse"] = lse_v
                st.session_state.result["lie"] = lie_v
                st.session_state.result["param_name"] = param_name or "Parâmetro"
                st.session_state.result["unit"] = unit
                st.session_state.result["ident"] = {
                    "linha": linha, "emb": emb, "op": op, "data": data_str
                }
                st.success("✅ Análise concluída! Acesse a aba **Análise CEP**.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANÁLISE CEP
# ═══════════════════════════════════════════════════════════════════════════════

with tab_analise:
    if st.session_state.result is None:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;color:rgba(100,130,200,0.5)">
          <div style="font-size:48px;margin-bottom:16px">📊</div>
          <div style="font-size:16px;font-weight:600;margin-bottom:8px">Nenhuma análise calculada</div>
          <div style="font-size:13px">Insira os dados na aba <strong>Entrada de dados</strong> e clique em Calcular CEP.</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    r   = st.session_state.result
    lse = r.get("lse"); lie = r.get("lie")
    pname = r.get("param_name","Parâmetro")
    unit  = r.get("unit","mm")
    ident = r.get("ident",{})
    vals  = r["vals"]

    # ── Context bar
    ctx = f"**{pname}** &nbsp;·&nbsp; {unit} &nbsp;·&nbsp; {r['n']} amostras"
    if ident.get("linha"): ctx += f" &nbsp;·&nbsp; Linha: **{ident['linha']}**"
    if ident.get("data"):  ctx += f" &nbsp;·&nbsp; {ident['data']}"
    st.markdown(f"<div style='font-size:12px;color:rgba(120,160,255,0.7);margin-bottom:16px'>{ctx}</div>", unsafe_allow_html=True)

    # ── Stability alert
    if r["nelson_violations"] or r["out_ctrl"]:
        st.error(f"⚠️ **Processo instável:** {len(r['out_ctrl'])} ponto(s) fora dos limites de controle, {len(r['nelson_violations'])} violação(ões) de regra detectada(s).")
    else:
        st.success("✅ **Processo estável.** Nenhuma violação das regras de controle.")

    # ── KPI cards
    st.markdown('<div class="sec-head">Indicadores de capacidade</div>', unsafe_allow_html=True)

    def kpi_html(label, value, cls, desc, badge_txt=None, badge_cls=None):
        badge = ""
        if badge_txt:
            badge = f'<div class="scale-badge {badge_cls}">{badge_txt}</div>'
        return f"""
        <div class="ind-card {cls}">
          <div class="ind-label">{label}</div>
          <div class="ind-value">{value}</div>
          <div class="ind-desc">{desc}</div>
          {badge}
        </div>"""

    def fmt(v, n=3): return f"{v:.{n}f}" if v is not None else "—"

    cpk_v = r.get("cpk"); cpk_st = card_cls(cpk_v)
    cp_v  = r.get("cp");  cp_st  = card_cls(cp_v)
    cpu_v = r.get("cpu"); cpu_st = card_cls(cpu_v)
    cpl_v = r.get("cpl"); cpl_st = card_cls(cpl_v)

    html_kpis = '<div class="ind-grid">'
    html_kpis += kpi_html("Cp — Capacidade Potencial", fmt(cp_v), cp_st,
                          "Capacidade sem considerar centralização",
                          cpk_label(cp_v), cpk_status(cp_v))
    html_kpis += kpi_html("Cpk — Capacidade Real", fmt(cpk_v), cpk_st,
                          "Capacidade considerando variação + centralização",
                          cpk_label(cpk_v), cpk_status(cpk_v))
    html_kpis += kpi_html("Cpu — Cap. Superior", fmt(cpu_v), card_cls(cpu_v),
                          "Proximidade da média com o LSE", cpk_label(cpu_v), cpk_status(cpu_v))
    html_kpis += kpi_html("Cpl — Cap. Inferior", fmt(cpl_v), card_cls(cpl_v),
                          "Proximidade da média com o LIE", cpk_label(cpl_v), cpk_status(cpl_v))
    html_kpis += '</div>'

    html_kpis2 = '<div class="ind-grid">'
    html_kpis2 += kpi_html("X̄ — Média", fmt(r["mean"],4), "info", "Centro do processo")
    html_kpis2 += kpi_html("σ — Desvio Padrão", fmt(r["std"],4), "info", "Dispersão do processo")
    html_kpis2 += kpi_html("R̄ — Amplitude Média", fmt(r["r_bar"],4), "info", "Variação dentro das amostras")
    html_kpis2 += kpi_html("UCL / LCL", f"{fmt(r['UCL_x'],3)} / {fmt(r['LCL_x'],3)}", "info",
                            "Limites de controle ±3σ")
    if r.get("ppm_total") is not None:
        ppm_cls = "ok" if r["ppm_total"]==0 else ("wn" if r["ppm_total"]<1000 else "bad")
        html_kpis2 += kpi_html("PPM estimado", str(r["ppm_total"]), ppm_cls,
                               "Estimativa de peças não conformes por milhão")
    html_kpis2 += '</div>'

    st.markdown(html_kpis + html_kpis2, unsafe_allow_html=True)

    # ── Charts
    st.markdown('<div class="sec-head">Gráficos de controle</div>', unsafe_allow_html=True)

    ctab1, ctab2, ctab3, ctab4 = st.tabs([
        "📈 Carta X — Controle Individual",
        "📉 Carta MR — Amplitude Móvel",
        "📊 Histograma + Curva Normal",
        "🔔 Distribuição Normal",
    ])

    with ctab1:
        svg_ctrl = svg_control_chart(vals, r["mean"], r["UCL_x"], r["LCL_x"], lse, lie,
                                     f"Carta X — {pname}")
        st.markdown(svg_ctrl, unsafe_allow_html=True)
        if r["out_ctrl"]:
            out_vals = [(i+1, vals[i]) for i in r["out_ctrl"]]
            st.warning(f"Pontos fora de controle: " + ", ".join(f"Amostra {i} ({v:.4f})" for i,v in out_vals))

    with ctab2:
        if r["ranges"]:
            svg_mr = svg_moving_range(r["ranges"], r["UCL_r"], r["r_bar"])
            st.markdown(svg_mr, unsafe_allow_html=True)
            out_mr = [i+2 for i, rv in enumerate(r["ranges"]) if rv > r["UCL_r"]]
            if out_mr:
                st.warning(f"Amplitudes fora do UCL (D4·R̄={r['UCL_r']:.4f}): amostras {out_mr}")
        else:
            st.info("Carta MR disponível a partir de 2 amostras.")

    with ctab3:
        svg_hist = svg_histogram(vals, r["mean"], r["std"], lse, lie)
        st.markdown(svg_hist, unsafe_allow_html=True)

    with ctab4:
        if r["std"] > 0:
            svg_norm = svg_normal_curve(r["mean"], r["std"], lse, lie)
            st.markdown(f'<div class="normal-wrap">{svg_norm}</div>', unsafe_allow_html=True)
            col_leg1, col_leg2, col_leg3 = st.columns(3)
            with col_leg1: st.markdown('<div style="font-size:11px;color:#ff4455">🟥 Fora da especificação (risco alto)</div>', unsafe_allow_html=True)
            with col_leg2: st.markdown('<div style="font-size:11px;color:#ffb340">🟨 Próximo dos limites (atenção)</div>', unsafe_allow_html=True)
            with col_leg3: st.markdown('<div style="font-size:11px;color:#00e5a0">🟩 Dentro da capacidade (desejável)</div>', unsafe_allow_html=True)

    # ── Nelson violations
    if r["nelson_violations"]:
        st.markdown('<div class="sec-head">Violações das regras de controle (Nelson)</div>', unsafe_allow_html=True)
        for pt, desc in r["nelson_violations"]:
            st.markdown(f'<div class="ins bad"><strong>Amostra {pt}:</strong> {desc}.</div>', unsafe_allow_html=True)

    # ── Insights
    st.markdown('<div class="sec-head">Diagnóstico automático</div>', unsafe_allow_html=True)
    for lvl, txt in build_insights(r, lse, lie):
        css = {"ok":"ok","wn":"wn","bad":"bad"}.get(lvl,"ok")
        st.markdown(f'<div class="ins {css}">{txt}</div>', unsafe_allow_html=True)

    # ── Data summary table
    with st.expander("📋 Tabela de amostras e estatísticas"):
        import pandas as pd
        rows = []
        prev = None
        for i, v in enumerate(vals):
            mr_val = abs(v - prev) if prev is not None else None
            out = (lse is not None and v > lse) or (lie is not None and v < lie)
            out_ctrl_pt = i in r["out_ctrl"]
            rows.append({
                "Amostra": i+1,
                "Valor": round(v, 4),
                "Desvio da média": round(v - r["mean"], 4),
                "MR": round(mr_val, 4) if mr_val is not None else "—",
                "Fora spec": "⚠️ SIM" if out else "OK",
                "Fora controle": "🔴 SIM" if out_ctrl_pt else "OK",
            })
            prev = v
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Summary stats
        st.markdown("**Estatísticas resumidas:**")
        scol1, scol2, scol3, scol4 = st.columns(4)
        with scol1:
            st.metric("Mínimo", f"{min(vals):.4f}")
            st.metric("Máximo", f"{max(vals):.4f}")
        with scol2:
            st.metric("Amplitude total", f"{max(vals)-min(vals):.4f}")
            st.metric("Mediana", f"{sorted(vals)[len(vals)//2]:.4f}")
        with scol3:
            st.metric("Pontos fora spec", sum(1 for v in vals if (lse and v>lse) or (lie and v<lie)))
            st.metric("Pontos fora controle", len(r["out_ctrl"]))
        with scol4:
            st.metric("Violações Nelson", len(r["nelson_violations"]))
            ppm = r.get("ppm_total")
            st.metric("PPM estimado", str(ppm) if ppm is not None else "—")

    # ── PDF Export
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head">Exportar relatório</div>', unsafe_allow_html=True)
    if st.button("📄 Gerar relatório PDF completo", type="primary"):
        with st.spinner("Gerando relatório…"):
            try:
                pdf_buf = generate_pdf_report(ident, r, lse, lie, pname, unit)
                fname = f"cep_{pname.replace(' ','_')}_{ident.get('data',date.today())}.pdf"
                st.download_button(
                    "⬇️ Baixar PDF",
                    data=pdf_buf,
                    file_name=fname,
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REFERENCE GUIDE
# ═══════════════════════════════════════════════════════════════════════════════

with tab_referencia:
    st.markdown('<div class="sec-head">Guia de indicadores CEP</div>', unsafe_allow_html=True)

    guide_html = """
    <div class="ind-grid" style="grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px">

    <div class="ind-card info" style="grid-column:span 1">
      <div class="ind-label">1 · Cp — Capacidade Potencial</div>
      <div class="ind-value" style="font-size:20px">Cp = (LSE−LIE) / 6σ</div>
      <div class="ind-desc">Mede se o processo é capaz de atender às especificações <strong>sem considerar centralização</strong>.<br><br>
        <span style="color:#ff4455">< 1,00 → Ruim</span><br>
        <span style="color:#ffb340">1,00–1,33 → Marginal</span><br>
        <span style="color:#00e5a0">1,33–1,67 → Bom</span><br>
        <span style="color:#00c4ff">≥ 1,67 → Excelente</span>
      </div>
    </div>

    <div class="ind-card ok" style="grid-column:span 1">
      <div class="ind-label">2 · Cpk — Capacidade Real</div>
      <div class="ind-value" style="font-size:20px">Cpk = min(Cpu, Cpl)</div>
      <div class="ind-desc">Mede capacidade considerando <strong>variação + centralização</strong>.<br><br>
        <span style="color:#ff4455">< 1,00 → Incapaz</span><br>
        <span style="color:#ffb340">1,00–1,33 → Aceitável</span><br>
        <span style="color:#00e5a0">1,33–1,67 → Bom</span><br>
        <span style="color:#00c4ff">≥ 1,67 → Excelente</span>
      </div>
    </div>

    <div class="ind-card info">
      <div class="ind-label">3 · Cpu — Capacidade Superior</div>
      <div class="ind-value" style="font-size:20px">Cpu = (LSE−X̄) / 3σ</div>
      <div class="ind-desc">Mede a proximidade da média com o <strong>limite superior (LSE)</strong>.<br>Destaca risco de ultrapassar o limite superior.</div>
    </div>

    <div class="ind-card info">
      <div class="ind-label">4 · Cpl — Capacidade Inferior</div>
      <div class="ind-value" style="font-size:20px">Cpl = (X̄−LIE) / 3σ</div>
      <div class="ind-desc">Mede a proximidade da média com o <strong>limite inferior (LIE)</strong>.<br>Destaca risco de ficar abaixo do limite.</div>
    </div>

    <div class="ind-card info">
      <div class="ind-label">5 · X̄ — X-barra (Média)</div>
      <div class="ind-value" style="font-size:20px">X̄ = Σxi / n</div>
      <div class="ind-desc">Representa o <strong>centro do processo</strong>.<br>Indica deslocamentos ao longo do tempo.</div>
    </div>

    <div class="ind-card info">
      <div class="ind-label">6 · R̄ — Amplitude Média</div>
      <div class="ind-value" style="font-size:20px">R̄ = Σ|xi−xi₋₁| / (n−1)</div>
      <div class="ind-desc">Mede a <strong>variação dentro das amostras</strong>.<br>Indica estabilidade do processo.</div>
    </div>

    <div class="ind-card info">
      <div class="ind-label">7 · σ — Desvio Padrão</div>
      <div class="ind-value" style="font-size:20px">σ = R̄ / d₂</div>
      <div class="ind-desc">Mede a <strong>dispersão dos dados</strong>.<br>
        Alto → processo instável.<br>
        Baixo → processo consistente.
      </div>
    </div>

    </div>

    <br>
    <div class="sec-head">Guia de desempenho</div>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <div class="ind-card bad" style="flex:1;min-width:180px;text-align:center">
        <div style="font-size:28px;margin-bottom:6px">👎</div>
        <div class="ind-label" style="color:#ff4455">RUIM — &lt; 1,00</div>
        <div class="ind-desc">Ação imediata necessária.<br>Processo não atende especificações.</div>
      </div>
      <div class="ind-card wn" style="flex:1;min-width:180px;text-align:center">
        <div style="font-size:28px;margin-bottom:6px">⚠️</div>
        <div class="ind-label" style="color:#ffb340">ATENÇÃO — 1,00 a 1,33</div>
        <div class="ind-desc">Monitore e melhore o processo.<br>Margem de segurança insuficiente.</div>
      </div>
      <div class="ind-card ok" style="flex:1;min-width:180px;text-align:center">
        <div style="font-size:28px;margin-bottom:6px">👍</div>
        <div class="ind-label" style="color:#00e5a0">BOM — 1,33 a 1,67</div>
        <div class="ind-desc">Processo capaz e sob controle.<br>Manter e monitorar.</div>
      </div>
      <div class="ind-card" style="flex:1;min-width:180px;text-align:center;border-color:rgba(0,196,255,0.3);background:rgba(0,196,255,0.05)">
        <div style="font-size:28px;margin-bottom:6px">🏆</div>
        <div class="ind-label" style="color:#00c4ff">EXCELENTE — ≥ 1,67</div>
        <div class="ind-desc">Processo world class.<br>Sigma level elevado.</div>
      </div>
    </div>

    <br>
    <div class="sec-head">Regras de Nelson — Detecção de instabilidade</div>
    <div class="ind-grid">
      <div class="ind-card bad">
        <div class="ind-label">Regra 1</div>
        <div class="ind-desc" style="font-size:12px">1 ponto além de ±3σ dos limites de controle. Indica causa especial.</div>
      </div>
      <div class="ind-card wn">
        <div class="ind-label">Regra 2</div>
        <div class="ind-desc" style="font-size:12px">8 pontos consecutivos no mesmo lado da média. Indica deslocamento.</div>
      </div>
      <div class="ind-card wn">
        <div class="ind-label">Regra 3</div>
        <div class="ind-desc" style="font-size:12px">6 pontos consecutivos em tendência (subindo ou descendo). Indica deriva.</div>
      </div>
    </div>

    <br>
    <div style="background:#0e1423;border:1px solid rgba(30,92,255,0.2);border-radius:12px;padding:16px 20px">
      <div style="font-size:13px;color:rgba(150,180,255,0.8);font-weight:600;margin-bottom:6px">📌 Princípio fundamental</div>
      <div style="font-size:14px;color:#eaf0ff;font-style:italic">
        "Processo bom não é só capaz — é <strong>estável e centralizado</strong>."
      </div>
      <div style="font-size:12px;color:rgba(120,160,255,0.6);margin-top:8px">
        Use Cp para avaliar capacidade potencial, Cpk para capacidade real, e a Carta de Controle para monitorar estabilidade ao longo do tempo.
      </div>
    </div>
    """
    st.markdown(guide_html, unsafe_allow_html=True)
