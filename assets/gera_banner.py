"""Gera o banner animado do perfil (hero-dark.svg e hero-light.svg).

    python3 assets/gera_banner.py

Depois de regerar, suba o ?v=N das URLs do banner no README: o GitHub guarda a
imagem em cache pela URL e, sem trocar a URL, continua mostrando a versão antiga.
"""

import os
from html import escape

SAIDA = os.path.dirname(os.path.abspath(__file__))

TEMAS = {
    "dark": {
        "bg1": "#0c0910", "bg2": "#160b19", "grid": "#ffffff", "grid_op": "0.035",
        "texto": "#f6f1f8", "sub": "#cdc2d4", "mudo": "#8b7f95",
        "chip_bg": "#1c1420", "chip_borda": "#3a2b40", "linha": "#4a3552",
        "term_bg": "#120d16", "term_barra": "#1d1522", "glow_op": "0.55", "glow_meio": "0.30",
    },
    "light": {
        "bg1": "#fdf9fd", "bg2": "#f6eef7", "grid": "#5b2a55", "grid_op": "0.05",
        "texto": "#1d1220", "sub": "#4a3d52", "mudo": "#7b6e85",
        "chip_bg": "#ffffff", "chip_borda": "#e7d6e8", "linha": "#d9c3db",
        "term_bg": "#1a1220", "term_barra": "#251a2c", "glow_op": "0.28", "glow_meio": "0.15",
    },
}

# (prompt?, texto, cor) — cada linha "digita" depois da anterior
LINHAS = [
    (True, "whoami", "#f6f1f8"),
    (False, "head of data engineering @ cienty", "#cdc2d4"),
    (True, "terraform apply -auto-approve", "#f6f1f8"),
    (False, "✓ bronze → silver → gold", "#3ee08f"),
    (True, 'claude "gold table: avg price by EAN"', "#f6f1f8"),
    (False, "✓ SQL + Terraform + PR opened", "#3ee08f"),
    (True, "", "#f6f1f8"),
]


def terminal():
    x0, y0, passo, larg_char = 712, 132, 28, 7.9
    linhas, t = "", 0.8
    for i, (prompt, texto, cor) in enumerate(LINHAS):
        y = y0 + i * passo
        pre = '<tspan fill="#ff5ce1">❯ </tspan>' if prompt else ""
        largura = (len(texto) + (2 if prompt else 0)) * larg_char + 12
        dur = max(0.25, len(texto) * 0.035) if prompt else 0.15
        linhas += (
            f'<clipPath id="c{i}"><rect x="{x0}" y="{y - 16}" height="22" width="0">'
            f'<animate attributeName="width" from="0" to="{largura:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>'
            f"</rect></clipPath>"
            f'<text x="{x0}" y="{y}" class="mono term" fill="{cor}" clip-path="url(#c{i})">{pre}{escape(texto)}</text>'
        )
        t += dur + (0.35 if prompt else 0.5)
    ultimo_y = y0 + (len(LINHAS) - 1) * passo
    linhas += (
        f'<rect x="{x0 + 2 * larg_char + 2}" y="{ultimo_y - 14}" width="9" height="18" fill="#ff5ce1" opacity="0">'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.01;.5;.51" dur="1s" begin="{t - 0.5:.2f}s" repeatCount="indefinite"/>'
        f"</rect>"
    )
    return linhas


def svg(t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400" role="img" aria-labelledby="titulo desc">
<title id="titulo">Weslei Camargo</title>
<desc id="desc">Weslei Camargo, Head of Data Engineering at Cienty.</desc>
<defs>
  <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg1"]}"/><stop offset="1" stop-color="{t["bg2"]}"/></linearGradient>
  <linearGradient id="mag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff5ce1"/><stop offset=".55" stop-color="#dc36c0"/><stop offset="1" stop-color="#8b3dff"/></linearGradient>
  <radialGradient id="glow1"><stop offset="0" stop-color="#dc36c0"/><stop offset="1" stop-color="#dc36c0" stop-opacity="0"/></radialGradient>
  <radialGradient id="glow2"><stop offset="0" stop-color="#7b3dff"/><stop offset="1" stop-color="#7b3dff" stop-opacity="0"/></radialGradient>
  <pattern id="grade" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_op"]}"/></pattern>
  <filter id="sombra" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000" flood-opacity=".4"/></filter>
  <clipPath id="moldura"><rect width="1200" height="400" rx="18"/></clipPath>
</defs>
<style>
  text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Open Sans", Helvetica, Arial, sans-serif; }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  .nome {{ font-size: 66px; font-weight: 800; letter-spacing: -2.5px; fill: {t["texto"]}; }}
  .cargo {{ font-size: 26px; font-weight: 700; fill: url(#mag); }}
  .sub {{ font-size: 18px; fill: {t["sub"]}; }}
  .meta {{ font-size: 13.5px; fill: {t["mudo"]}; }}
  .pill-t {{ font-size: 12px; font-weight: 700; letter-spacing: 2.4px; fill: {t["sub"]}; }}
  .chip {{ fill: {t["chip_bg"]}; stroke: {t["chip_borda"]}; }}
  .term {{ font-size: 13.5px; }}
  .fade {{ opacity: 0; animation: entra .9s cubic-bezier(.2,.7,.2,1) forwards; }}
  .pulsa {{ animation: pulsa 7s ease-in-out infinite; }}
  .pisca {{ animation: pisca 1.8s ease-in-out infinite; }}
  @keyframes entra {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes pulsa {{ 0%,100% {{ opacity: {t["glow_op"]}; }} 50% {{ opacity: {t["glow_meio"]}; }} }}
  @keyframes pisca {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .fade {{ opacity: 1; }} }}
</style>
<g clip-path="url(#moldura)">
  <rect width="1200" height="400" fill="url(#fundo)"/>
  <rect width="1200" height="400" fill="url(#grade)"/>
  <circle cx="160" cy="30" r="360" fill="url(#glow1)" class="pulsa" opacity="{t["glow_op"]}"/>
  <circle cx="1120" cy="400" r="340" fill="url(#glow2)" class="pulsa" style="animation-delay:-3.5s" opacity="{t["glow_op"]}"/>
  <rect x="0" y="0" width="1200" height="3" fill="url(#mag)"/>

  <g class="fade">
    <rect x="64" y="70" width="232" height="30" rx="15" class="chip"/>
    <circle cx="82" cy="85" r="4.5" fill="#3ee08f" class="pisca"/>
    <text x="96" y="89.5" class="pill-t">BUILDING @ CIENTY</text>
  </g>
  <g class="fade" style="animation-delay:.1s"><text x="60" y="178" class="nome">Weslei Camargo</text></g>
  <g class="fade" style="animation-delay:.22s"><text x="64" y="222" class="cargo">Head of Data Engineering</text></g>
  <g class="fade" style="animation-delay:.34s">
    <text x="64" y="268" class="sub">Turning raw data into decisions.</text>
  </g>
  <g class="fade" style="animation-delay:.46s">
    <text x="64" y="318" class="meta mono">BigQuery · Terraform · Python · SQL · Azure · Claude Code</text>
  </g>

  <g class="fade" style="animation-delay:.3s">
    <rect x="690" y="66" width="450" height="270" rx="12" fill="{t["term_bg"]}" stroke="#3a2b40" filter="url(#sombra)"/>
    <path d="M702 66 H1128 A12 12 0 0 1 1140 78 V98 H690 V78 A12 12 0 0 1 702 66 Z" fill="{t["term_barra"]}"/>
    <circle cx="712" cy="82" r="5.5" fill="#ff5f57"/><circle cx="730" cy="82" r="5.5" fill="#febc2e"/><circle cx="748" cy="82" r="5.5" fill="#28c840"/>
    <text x="915" y="86.5" class="mono" style="font-size:12px;fill:#8b7f95;text-anchor:middle">~/cienty-data</text>
  </g>
  {terminal()}
</g>
<rect x=".5" y=".5" width="1199" height="399" rx="18" fill="none" stroke="{t["chip_borda"]}"/>
</svg>
'''


if __name__ == "__main__":
    for nome, tema in TEMAS.items():
        with open(f"{SAIDA}/hero-{nome}.svg", "w") as f:
            f.write(svg(tema))
        print(f"hero-{nome}.svg")
