"""
CineMatch — Premium Streamlit UI for the Movie Recommender API
==============================================================
A cinematic, dark-themed front-end. Pure-HTML poster cards (clickable,
hover-zoom), glassmorphism surfaces, scroll-snap carousels and skeleton
loaders. Talks to the same FastAPI endpoints as before.
"""

from __future__ import annotations

import html
import os
from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st

# =============================================================================
# CONFIG
# =============================================================================
API_BASE = os.getenv("API_BASE", "https://movie-rec-466x.onrender.com").rstrip("/")
TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_IMG_LG = "https://image.tmdb.org/t/p/w1280"

CATEGORIES: List[Tuple[str, str, str]] = [
    ("trending", "Trending", "Rising right now"),
    ("popular", "Popular", "What everyone's watching"),
    ("top_rated", "Top Rated", "The all-time greats"),
    ("now_playing", "In Theatres", "Playing this week"),
    ("upcoming", "Upcoming", "Coming soon"),
]
CATEGORY_LOOKUP = {c[0]: c for c in CATEGORIES}

st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# THEME
# =============================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

:root{
--bg:#08090D;
--bg-2:#0C0E14;
--surface:rgba(255,255,255,.045);
--surface-2:rgba(255,255,255,.07);
--stroke:rgba(255,255,255,.09);
--stroke-2:rgba(255,255,255,.16);
--ink:#EDEEF2;
--ink-2:#A2A6B4;
--ink-3:#6E7385;
--gold:#F5B544;
--gold-2:#FF8A3D;
--grad:linear-gradient(135deg,#F5B544 0%,#FF8A3D 55%,#FF6B6B 100%);
--r-sm:10px; --r-md:16px; --r-lg:22px; --r-xl:28px;
--ease:cubic-bezier(.22,.61,.36,1);
--shadow:0 18px 50px -12px rgba(0,0,0,.85);
}

/* ---------- base ---------- */
html,body,[class*="css"]{ -webkit-font-smoothing:antialiased; }
.stApp{
background:
radial-gradient(1100px 620px at 12% -12%, rgba(245,181,68,.13), transparent 62%),
radial-gradient(950px 560px at 92% 4%, rgba(255,107,107,.10), transparent 58%),
radial-gradient(800px 800px at 50% 120%, rgba(96,120,255,.09), transparent 60%),
var(--bg);
background-attachment:fixed;
color:var(--ink);
font-family:'Inter',system-ui,sans-serif;
}
.stApp::before{
content:''; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.5;
background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.045'/%3E%3C/svg%3E");
}
.block-container{ padding:1.1rem 2.4rem 5rem !important; max-width:1620px; position:relative; z-index:1; }

/* hide streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"]{ display:none !important; }
[data-testid="stDecoration"]{ display:none !important; }
[data-testid="stToolbar"]{ right:.5rem; top:.4rem; }
.stApp a{ text-decoration:none !important; }

h1,h2,h3,h4,h5{ font-family:'Outfit',sans-serif !important; letter-spacing:-.022em; color:var(--ink); }

::-webkit-scrollbar{ width:9px; height:9px; }
::-webkit-scrollbar-track{ background:transparent; }
::-webkit-scrollbar-thumb{ background:rgba(255,255,255,.13); border-radius:99px; }
::-webkit-scrollbar-thumb:hover{ background:rgba(245,181,68,.5); }

@keyframes rise{ from{opacity:0; transform:translateY(16px);} to{opacity:1; transform:none;} }
@keyframes fade{ from{opacity:0;} to{opacity:1;} }
@keyframes shimmer{ 0%{background-position:-500px 0;} 100%{background-position:500px 0;} }
@keyframes float{ 0%,100%{transform:translateY(0);} 50%{transform:translateY(-7px);} }
@keyframes spin{ to{ transform:rotate(360deg); } }
.rise{ animation:rise .6s var(--ease) both; }

/* ---------- brand / hero ---------- */
.brand{ display:flex; align-items:center; gap:15px; margin:.2rem 0 .1rem; animation:rise .7s var(--ease) both; }
.brand-mark{
width:50px; height:50px; border-radius:15px; background:var(--grad); display:grid; place-items:center;
font-size:25px; box-shadow:0 12px 34px -8px rgba(245,181,68,.6); animation:float 5s ease-in-out infinite;
}
.brand-name{ font-family:'Outfit',sans-serif; font-size:2.05rem; font-weight:800; letter-spacing:-.04em; line-height:1;
background:linear-gradient(100deg,#fff 8%,#FFD79A 48%,#FF9A62 88%); -webkit-background-clip:text; background-clip:text; color:transparent; }
.brand-sub{ color:var(--ink-3); font-size:.83rem; margin-top:5px; letter-spacing:.05em; text-transform:uppercase; font-weight:500; }

/* ---------- section head ---------- */
.sec{ display:flex; align-items:flex-end; justify-content:space-between; gap:18px; margin:2.3rem 0 1.05rem; animation:rise .6s var(--ease) both; }
.sec-l{ display:flex; align-items:center; gap:13px; }
.sec-bar{ width:4px; height:31px; border-radius:99px; background:var(--grad); box-shadow:0 0 18px rgba(245,181,68,.55); }
.sec-t{ font-family:'Outfit',sans-serif; font-size:1.44rem; font-weight:700; letter-spacing:-.03em; }
.sec-s{ color:var(--ink-3); font-size:.85rem; margin-top:2px; }
.sec-count{ font-size:.72rem; color:var(--ink-2); border:1px solid var(--stroke); background:var(--surface);
padding:5px 12px; border-radius:99px; letter-spacing:.07em; text-transform:uppercase; font-weight:600; white-space:nowrap; }

/* ---------- poster grid + rail ---------- */
.grid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(178px,1fr)); gap:22px 19px; }
.rail{ display:flex; gap:19px; overflow-x:auto; padding:4px 4px 20px; scroll-snap-type:x proximity; scroll-behavior:smooth; }
.rail::-webkit-scrollbar{ height:7px; }
.rail > .card{ flex:0 0 178px; scroll-snap-align:start; }

.card{ display:block; animation:rise .55s var(--ease) both; }
.card .shot{
position:relative; border-radius:var(--r-md); overflow:hidden; aspect-ratio:2/3;
background:linear-gradient(145deg,#15171F,#0D0F15); border:1px solid var(--stroke);
box-shadow:0 10px 26px -14px rgba(0,0,0,.9);
transition:transform .48s var(--ease), box-shadow .48s var(--ease), border-color .48s var(--ease);
will-change:transform;
}
/* film-strip glyph sits behind the poster, so a dead TMDB URL degrades gracefully */
.card .shot::before{ content:'🎞️'; position:absolute; inset:0; display:grid; place-items:center;
font-size:2rem; opacity:.2; z-index:0; }
.card img{ position:relative; z-index:1; width:100%; height:100%; object-fit:cover; display:block;
transition:transform .7s var(--ease), filter .45s var(--ease); }
.card img[src=""], .card img:not([src]){ display:none; }
.card .noimg{ width:100%; height:100%; display:grid; place-items:center; font-size:2rem; opacity:.22; }
.card .veil{
position:absolute; inset:0; opacity:0; transition:opacity .42s var(--ease);
background:linear-gradient(to top,rgba(6,7,10,.94) 0%,rgba(6,7,10,.5) 38%,rgba(6,7,10,0) 70%);
}
.card .play{
position:absolute; left:50%; top:50%; width:50px; height:50px; margin:-25px 0 0 -25px; border-radius:50%;
background:rgba(245,181,68,.95); color:#12140f; display:grid; place-items:center; font-size:16px;
opacity:0; transform:scale(.55); transition:all .42s var(--ease); box-shadow:0 10px 30px rgba(245,181,68,.5);
}
.card:hover .shot{ transform:translateY(-9px) scale(1.026); border-color:rgba(245,181,68,.5);
box-shadow:0 26px 54px -16px rgba(0,0,0,.95), 0 0 0 1px rgba(245,181,68,.16), 0 0 44px -14px rgba(245,181,68,.5); }
.card:hover img{ transform:scale(1.09); filter:saturate(1.14) contrast(1.03); }
.card:hover .veil{ opacity:1; }
.card:hover .play{ opacity:1; transform:scale(1); }

.badge{
position:absolute; top:9px; right:9px; z-index:2; font-size:.7rem; font-weight:700; letter-spacing:.02em;
padding:4px 9px; border-radius:99px; color:#0B0C10; background:linear-gradient(135deg,#FFD98A,#F5B544);
box-shadow:0 5px 16px rgba(0,0,0,.55); font-family:'Outfit',sans-serif;
}
.badge.dim{ background:rgba(16,18,24,.86); color:var(--ink-2); border:1px solid var(--stroke-2); backdrop-filter:blur(8px); }
.badge.sim{ background:linear-gradient(135deg,#8FD6FF,#5AA9FF); }
.rank{
position:absolute; left:-4px; bottom:6px; z-index:2; font-family:'Outfit',sans-serif; font-weight:800;
font-size:3.1rem; line-height:.8; color:rgba(255,255,255,.94); opacity:.92;
text-shadow:0 3px 18px rgba(0,0,0,.95); -webkit-text-stroke:1.5px rgba(0,0,0,.45);
}
.meta{ padding:11px 3px 0; }
.meta .t{ font-size:.855rem; font-weight:600; color:var(--ink); line-height:1.28; letter-spacing:-.008em;
display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; min-height:2.2em;
transition:color .3s var(--ease); }
.card:hover .meta .t{ color:var(--gold); }
.meta .y{ font-size:.72rem; color:var(--ink-3); margin-top:3px; letter-spacing:.04em; }

/* ---------- skeleton ---------- */
.sk{ border-radius:var(--r-md); aspect-ratio:2/3; border:1px solid var(--stroke);
background:linear-gradient(100deg,#101219 8%,#191C26 20%,#101219 33%); background-size:900px 100%;
animation:shimmer 1.5s linear infinite; }
.sk-t{ height:11px; border-radius:99px; margin-top:12px; width:82%;
background:linear-gradient(100deg,#101219 8%,#191C26 20%,#101219 33%); background-size:900px 100%; animation:shimmer 1.5s linear infinite; }

/* ---------- detail hero ---------- */
.hero{ position:relative; border-radius:var(--r-xl); overflow:hidden; margin:.5rem 0 0; border:1px solid var(--stroke);
box-shadow:var(--shadow); animation:fade .8s var(--ease) both; }
.hero-bg{ position:absolute; inset:0; background-size:cover; background-position:center 22%; transform:scale(1.06); filter:saturate(1.05); }
.hero-scrim{ position:absolute; inset:0;
background:linear-gradient(90deg,rgba(8,9,13,.94) 0%,rgba(8,9,13,.82) 38%,rgba(8,9,13,.34) 72%,rgba(8,9,13,.58) 100%),
linear-gradient(to top,rgba(8,9,13,.99) 1%,rgba(8,9,13,.06) 66%); }
.hero-in{ position:relative; display:flex; gap:36px; padding:44px 46px; align-items:flex-end; min-height:430px; }
.hero-poster{ flex:0 0 232px; border-radius:var(--r-lg); overflow:hidden; border:1px solid rgba(255,255,255,.2);
box-shadow:0 30px 70px -18px rgba(0,0,0,.95); animation:rise .8s var(--ease) both; }
.hero-poster img{ width:100%; display:block; }
.hero-body{ flex:1 1 auto; min-width:0; animation:rise .8s .08s var(--ease) both; }
.hero-kicker{ font-size:.71rem; letter-spacing:.22em; text-transform:uppercase; color:var(--gold); font-weight:700; margin-bottom:11px; }
.hero-title{ font-family:'Outfit',sans-serif; font-size:3.1rem; font-weight:800; letter-spacing:-.045em; line-height:1.03; margin:0 0 6px;
text-shadow:0 4px 34px rgba(0,0,0,.75); }
.hero-tag{ color:var(--ink-2); font-style:italic; font-size:1rem; margin-bottom:16px; }
.facts{ display:flex; flex-wrap:wrap; align-items:center; gap:9px; margin-bottom:18px; }
.fact{ font-size:.79rem; color:var(--ink-2); background:var(--surface); border:1px solid var(--stroke);
padding:6px 13px; border-radius:99px; backdrop-filter:blur(10px); font-weight:500; }
.fact.hot{ color:#0B0C10; background:linear-gradient(135deg,#FFD98A,#F5B544); border-color:transparent; font-weight:700; }
.pill{ font-size:.77rem; color:#FFD79A; border:1px solid rgba(245,181,68,.32); background:rgba(245,181,68,.09);
padding:6px 14px; border-radius:99px; font-weight:600; transition:all .3s var(--ease); }
.pill:hover{ background:rgba(245,181,68,.2); transform:translateY(-1px); }
.overview{ color:#C6C9D4; font-size:.965rem; line-height:1.78; max-width:70ch; }
.ov-h{ font-size:.71rem; letter-spacing:.2em; text-transform:uppercase; color:var(--ink-3); font-weight:700; margin-bottom:9px; }

/* score ring */
.ring{ position:relative; width:70px; height:70px; flex:0 0 70px; display:grid; place-items:center; }
.ring svg{ position:absolute; inset:0; transform:rotate(-90deg); }
.ring .num{ font-family:'Outfit',sans-serif; font-weight:800; font-size:1.14rem; }
.ring .num small{ font-size:.6rem; opacity:.65; }

/* ---------- misc ---------- */
.note{ border:1px solid var(--stroke); background:var(--surface); border-radius:var(--r-md); padding:17px 20px;
color:var(--ink-2); font-size:.9rem; backdrop-filter:blur(12px); }
.note b{ color:var(--ink); }
.empty{ text-align:center; padding:66px 20px; color:var(--ink-3); border:1px dashed var(--stroke-2); border-radius:var(--r-lg); background:var(--surface); }
.empty .ico{ font-size:2.6rem; opacity:.35; margin-bottom:12px; }
.empty .h{ font-family:'Outfit',sans-serif; font-size:1.12rem; color:var(--ink); font-weight:600; margin-bottom:5px; }
.loader{ display:flex; align-items:center; gap:12px; color:var(--ink-2); font-size:.9rem; padding:6px 0 14px; }
.loader .sp{ width:17px; height:17px; border-radius:50%; border:2px solid rgba(245,181,68,.22); border-top-color:var(--gold); animation:spin .8s linear infinite; }
.divider{ height:1px; background:linear-gradient(90deg,transparent,var(--stroke),transparent); margin:2.4rem 0 .4rem; }

/* ---------- streamlit widgets ---------- */
[data-testid="stSidebar"]{ background:linear-gradient(180deg,#0B0D12,#08090D); border-right:1px solid var(--stroke); }
[data-testid="stSidebar"] .block-container{ padding-top:1.6rem !important; }
[data-testid="stSidebarCollapseButton"] button{ color:var(--ink-2) !important; }

.stTextInput input{
background:var(--surface) !important; border:1px solid var(--stroke) !important; border-radius:14px !important;
color:var(--ink) !important; height:52px; padding:0 18px !important; font-size:.98rem !important;
transition:all .3s var(--ease) !important; backdrop-filter:blur(12px);
}
.stTextInput input::placeholder{ color:var(--ink-3) !important; }
.stTextInput input:focus{ border-color:rgba(245,181,68,.55) !important;
box-shadow:0 0 0 3px rgba(245,181,68,.12), 0 8px 30px -12px rgba(245,181,68,.45) !important; background:rgba(255,255,255,.07) !important; }

[data-baseweb="select"] > div{ background:var(--surface) !important; border:1px solid var(--stroke) !important;
border-radius:12px !important; color:var(--ink) !important; transition:all .3s var(--ease); }
[data-baseweb="select"] > div:hover{ border-color:var(--stroke-2) !important; }
[data-baseweb="popover"] [role="listbox"]{ background:#101219 !important; border:1px solid var(--stroke) !important; border-radius:12px !important; }
[data-baseweb="popover"] li:hover{ background:rgba(245,181,68,.12) !important; }

.stButton button{
background:var(--surface) !important; border:1px solid var(--stroke) !important; color:var(--ink) !important;
border-radius:12px !important; font-weight:600 !important; font-size:.86rem !important; padding:.5rem 1.05rem !important;
transition:all .32s var(--ease) !important; width:100%;
}
.stButton button:hover{ border-color:rgba(245,181,68,.55) !important; color:var(--gold) !important;
transform:translateY(-2px); box-shadow:0 10px 26px -12px rgba(245,181,68,.6) !important; background:rgba(245,181,68,.08) !important; }
.stButton button:focus{ box-shadow:none !important; }

[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"]{ background:var(--gold) !important; box-shadow:0 0 0 4px rgba(245,181,68,.18) !important; }
[data-testid="stRadio"] label{ color:var(--ink-2) !important; font-size:.88rem !important; }
.stSpinner > div{ border-top-color:var(--gold) !important; }
[data-testid="stAlert"]{ background:var(--surface) !important; border:1px solid var(--stroke) !important;
border-radius:var(--r-md) !important; color:var(--ink-2) !important; backdrop-filter:blur(12px); }

/* sidebar nav labels */
.sb-h{ font-size:.68rem; letter-spacing:.2em; text-transform:uppercase; color:var(--ink-3); font-weight:700; margin:1.5rem 0 .6rem; }
.sb-brand{ display:flex; align-items:center; gap:11px; margin-bottom:.4rem; }
.sb-brand .m{ width:34px; height:34px; border-radius:11px; background:var(--grad); display:grid; place-items:center; font-size:17px; }
.sb-brand .n{ font-family:'Outfit',sans-serif; font-weight:800; font-size:1.12rem; letter-spacing:-.03em; color:var(--ink); }
.sb-stat{ display:flex; justify-content:space-between; font-size:.78rem; color:var(--ink-3); padding:7px 0; border-bottom:1px solid rgba(255,255,255,.05); }
.sb-stat b{ color:var(--ink-2); font-weight:600; }
.dot{ display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:7px; }
.dot.on{ background:#4ADE80; box-shadow:0 0 9px #4ADE80; }
.dot.off{ background:#F87171; box-shadow:0 0 9px #F87171; }

@media (max-width:1000px){
.block-container{ padding:1rem 1.1rem 4rem !important; }
.hero-in{ flex-direction:column; align-items:flex-start; padding:28px 24px; gap:22px; }
.hero-poster{ flex:0 0 auto; width:150px; }
.hero-title{ font-size:2.05rem; }
.grid{ grid-template-columns:repeat(auto-fill,minmax(132px,1fr)); gap:16px 13px; }
.rail > .card{ flex:0 0 138px; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =============================================================================
# ROUTING
# =============================================================================
st.session_state.setdefault("view", "home")
st.session_state.setdefault("movie_id", None)
st.session_state.setdefault("category", "trending")

_qp = st.query_params
if _qp.get("view") in ("home", "details"):
    st.session_state.view = _qp["view"]
if _qp.get("cat") in CATEGORY_LOOKUP:
    st.session_state.category = _qp["cat"]
if _qp.get("id"):
    try:
        st.session_state.movie_id = int(_qp["id"])
        st.session_state.view = "details"
    except (TypeError, ValueError):
        pass


def goto_home() -> None:
    st.session_state.view = "home"
    st.session_state.movie_id = None
    st.query_params.clear()
    st.query_params["view"] = "home"
    st.query_params["cat"] = st.session_state.category
    st.rerun()


# =============================================================================
# API
# =============================================================================
@st.cache_data(ttl=600, show_spinner=False)
def api(path: str, params: Optional[dict] = None, timeout: int = 30):
    """GET the backend. Returns (payload, error_string)."""
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=timeout)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code} — {r.text[:180]}"
        return r.json(), None
    except requests.exceptions.Timeout:
        return None, "timeout"
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


@st.cache_data(ttl=120, show_spinner=False)
def api_alive() -> bool:
    try:
        return requests.get(f"{API_BASE}/health", timeout=8).status_code == 200
    except Exception:  # noqa: BLE001
        return False


# =============================================================================
# CARD MODEL + RENDERERS
# =============================================================================
def esc(v: Any) -> str:
    return html.escape(str(v or ""), quote=True)


def normalize(raw: Any) -> List[Dict[str, Any]]:
    """Coerce any of the API's card shapes into one flat dict list."""
    out: List[Dict[str, Any]] = []
    if not raw:
        return out
    items = raw.get("results", []) if isinstance(raw, dict) else raw
    for m in items or []:
        if not isinstance(m, dict):
            continue
        # TF-IDF bundle item -> unwrap, keep the similarity score
        score = m.get("score")
        if "tmdb" in m:
            inner = m.get("tmdb") or {}
            if not inner:
                continue
            m = {**inner, "score": score}
        mid = m.get("tmdb_id") or m.get("id")
        title = (m.get("title") or m.get("name") or "").strip()
        if not mid or not title:
            continue
        poster = m.get("poster_url")
        if not poster and m.get("poster_path"):
            poster = f"{TMDB_IMG}{m['poster_path']}"
        out.append(
            {
                "id": int(mid),
                "title": title,
                "poster": poster,
                "date": m.get("release_date") or "",
                "vote": m.get("vote_average"),
                "score": m.get("score"),
            }
        )
    return out


def card_html(m: Dict[str, Any], i: int = 0, rank: Optional[int] = None) -> str:
    title, year = esc(m["title"]), esc((m.get("date") or "")[:4])
    href = f"?view=details&amp;id={int(m['id'])}"
    delay = f"{min(i, 22) * 0.035:.3f}s"

    if m.get("score") is not None:
        badge = f"<span class='badge sim'>{float(m['score']) * 100:.0f}%</span>"
    elif m.get("vote"):
        v = float(m["vote"])
        cls = "badge" if v >= 6.5 else "badge dim"
        badge = f"<span class='{cls}'>★ {v:.1f}</span>"
    else:
        badge = ""

    # alt is intentionally empty: a failed TMDB fetch then falls back to the
    # CSS film-strip glyph instead of painting broken alt text over the card.
    art = (
        f"<img src='{esc(m['poster'])}' alt='' loading='lazy'>"
        if m.get("poster")
        else "<div class='noimg'>🎞️</div>"
    )
    rk = f"<span class='rank'>{rank}</span>" if rank else ""

    return (
        f"<a class='card' href='{href}' target='_self' style='animation-delay:{delay}'>"
        f"<div class='shot'>{badge}{art}{rk}<div class='veil'></div><div class='play'>▶</div></div>"
        f"<div class='meta'><div class='t'>{title}</div>"
        f"<div class='y'>{year or '—'}</div></div></a>"
    )


def render(cards: List[Dict[str, Any]], mode: str = "grid", ranked: bool = False) -> None:
    if not cards:
        st.markdown(
            "<div class='empty'><div class='ico'>🍿</div>"
            "<div class='h'>Nothing here yet</div>"
            "<div>Try another title or switch categories in the sidebar.</div></div>",
            unsafe_allow_html=True,
        )
        return
    body = "".join(
        card_html(m, i, rank=(i + 1) if ranked else None) for i, m in enumerate(cards)
    )
    st.markdown(f"<div class='{mode}'>{body}</div>", unsafe_allow_html=True)


def skeletons(n: int = 12, mode: str = "grid") -> str:
    cell = "<div class='card'><div class='sk'></div><div class='sk-t'></div></div>"
    return f"<div class='{mode}'>{cell * n}</div>"


def section(title: str, sub: str = "", count: Optional[int] = None) -> None:
    tail = f"<span class='sec-count'>{count} titles</span>" if count else ""
    subline = f"<div class='sec-s'>{esc(sub)}</div>" if sub else ""
    st.markdown(
        f"<div class='sec'><div class='sec-l'><div class='sec-bar'></div>"
        f"<div><div class='sec-t'>{esc(title)}</div>{subline}</div></div>{tail}</div>",
        unsafe_allow_html=True,
    )


def ring(value: float) -> str:
    pct = max(0.0, min(1.0, value / 10.0))
    circ = 2 * 3.14159 * 30
    color = "#4ADE80" if value >= 7 else ("#F5B544" if value >= 5.5 else "#F87171")
    return (
        "<div class='ring'>"
        "<svg width='70' height='70'>"
        "<circle cx='35' cy='35' r='30' fill='rgba(0,0,0,.45)' stroke='rgba(255,255,255,.1)' stroke-width='4'/>"
        f"<circle cx='35' cy='35' r='30' fill='none' stroke='{color}' stroke-width='4' stroke-linecap='round' "
        f"stroke-dasharray='{circ:.1f}' stroke-dashoffset='{circ * (1 - pct):.1f}'/></svg>"
        f"<div class='num' style='color:{color}'>{value:.1f}<small>/10</small></div></div>"
    )


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown(
        "<div class='sb-brand'><div class='m'>🎬</div><div class='n'>CineMatch</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='color:var(--ink-3);font-size:.78rem;margin-bottom:1.2rem'>"
        "TF-IDF + genre recommendations</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='sb-h'>Browse</div>", unsafe_allow_html=True)
    labels = [c[1] for c in CATEGORIES]
    keys = [c[0] for c in CATEGORIES]
    picked = st.radio(
        "Category",
        options=labels,
        index=keys.index(st.session_state.category),
        label_visibility="collapsed",
    )
    new_cat = keys[labels.index(picked)]
    if new_cat != st.session_state.category:
        st.session_state.category = new_cat
        st.session_state.view = "home"
        st.query_params.clear()
        st.query_params["view"] = "home"
        st.query_params["cat"] = new_cat
        st.rerun()

    st.markdown("<div class='sb-h'>Feed size</div>", unsafe_allow_html=True)
    feed_limit = st.slider("Titles", 12, 40, 24, step=4, label_visibility="collapsed")

    st.markdown("<div class='sb-h'>Navigate</div>", unsafe_allow_html=True)
    if st.button("← Back to home", use_container_width=True):
        goto_home()

    online = api_alive()
    st.markdown("<div class='sb-h'>Status</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='sb-stat'><span><span class='dot {'on' if online else 'off'}'></span>API</span>"
        f"<b>{'Online' if online else 'Waking…'}</b></div>"
        "<div class='sb-stat'><span>Engine</span><b>TF-IDF cosine</b></div>"
        "<div class='sb-stat'><span>Data</span><b>TMDB</b></div>",
        unsafe_allow_html=True,
    )

# =============================================================================
# HEADER
# =============================================================================
st.markdown(
    "<div class='brand'><div class='brand-mark'>🎬</div><div>"
    "<div class='brand-name'>CineMatch</div>"
    "<div class='brand-sub'>Find your next favourite film</div>"
    "</div></div>",
    unsafe_allow_html=True,
)

# =============================================================================
# VIEW: HOME
# =============================================================================
if st.session_state.view == "home":
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    query = st.text_input(
        "Search",
        placeholder="🔍   Search any movie —  inception, batman, spirited away…",
        label_visibility="collapsed",
    ).strip()

    if query:
        if len(query) < 2:
            st.markdown(
                "<div class='note'>Keep typing — <b>2 characters minimum</b> to search.</div>",
                unsafe_allow_html=True,
            )
            st.stop()

        section("Search results", f'Matching “{query}”')
        slot = st.empty()
        slot.markdown(skeletons(12), unsafe_allow_html=True)

        data, err = api("/tmdb/search", {"query": query})
        slot.empty()

        if err:
            st.markdown(
                f"<div class='note'>⚠️ <b>Search unavailable.</b> {esc(err)}<br>"
                "<span style='color:var(--ink-3)'>The API may be spinning up on Render — retry in ~30s.</span></div>",
                unsafe_allow_html=True,
            )
            st.stop()

        found = normalize(data)
        low = query.lower()
        exact = [m for m in found if low in m["title"].lower()]
        results = exact or found
        results.sort(key=lambda m: (m.get("vote") or 0), reverse=True)
        render(results[:30])
        st.stop()

    label, name, tagline = CATEGORY_LOOKUP[st.session_state.category]
    section(name, tagline)

    slot = st.empty()
    slot.markdown(skeletons(feed_limit), unsafe_allow_html=True)
    feed, err = api("/home", {"category": label, "limit": feed_limit}, timeout=60)
    slot.empty()

    if err:
        st.markdown(
            f"<div class='note'>⚠️ <b>Couldn't reach the recommender API.</b> {esc(err)}<br>"
            f"<span style='color:var(--ink-3)'>Free Render instances sleep after inactivity — "
            "the first request can take up to a minute. Refresh shortly.</span></div>",
            unsafe_allow_html=True,
        )
        st.stop()

    cards = normalize(feed)
    render(cards, ranked=(label in ("trending", "top_rated")))

# =============================================================================
# VIEW: DETAILS
# =============================================================================
else:
    mid = st.session_state.movie_id
    if not mid:
        st.markdown(
            "<div class='empty'><div class='ico'>🎬</div><div class='h'>No movie selected</div>"
            "<div>Head back home and pick a poster.</div></div>",
            unsafe_allow_html=True,
        )
        st.stop()

    with st.spinner(""):
        detail, err = api(f"/movie/id/{mid}", timeout=45)

    if err or not detail:
        st.markdown(
            f"<div class='note'>⚠️ <b>Couldn't load this title.</b> {esc(err or 'Unknown error')}</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    title = detail.get("title") or "Untitled"
    date = detail.get("release_date") or ""
    year = date[:4] if date else ""
    genres = [g.get("name", "") for g in (detail.get("genres") or []) if g.get("name")]
    poster = detail.get("poster_url")
    backdrop = detail.get("backdrop_url") or poster
    overview = detail.get("overview") or "No synopsis available for this title."

    # Optional enrichment — present only if the API exposes these fields.
    vote = detail.get("vote_average")
    runtime = detail.get("runtime")
    tagline = (detail.get("tagline") or "").strip()

    facts = []
    if year:
        facts.append(f"<span class='fact hot'>{esc(year)}</span>")
    if runtime:
        facts.append(f"<span class='fact'>⏱ {int(runtime) // 60}h {int(runtime) % 60}m</span>")
    if date:
        facts.append(f"<span class='fact'>📅 {esc(date)}</span>")
    facts.append(f"<span class='fact'>TMDB #{int(mid)}</span>")
    chips = "".join(f"<span class='pill'>{esc(g)}</span>" for g in genres)
    tag_html = f"<div class='hero-tag'>“{esc(tagline)}”</div>" if tagline else ""
    score_html = ring(float(vote)) if vote else ""

    hero_bg = (
        f"<div class='hero-bg' style=\"background-image:url('{esc(backdrop)}')\"></div>"
        if backdrop
        else "<div class='hero-bg' style='background:linear-gradient(135deg,#15171F,#0B0D12)'></div>"
    )
    hero_poster = (
        f"<div class='hero-poster'><img src='{esc(poster)}' alt='{esc(title)}'></div>"
        if poster
        else ""
    )

    st.markdown(
        f"<div class='hero'>{hero_bg}<div class='hero-scrim'></div>"
        f"<div class='hero-in'>{hero_poster}"
        f"<div class='hero-body'>"
        f"<div class='hero-kicker'>Now viewing</div>"
        f"<h1 class='hero-title'>{esc(title)}</h1>"
        f"{tag_html}"
        f"<div class='facts'>{score_html}{''.join(facts)}</div>"
        f"<div class='facts'>{chips}</div>"
        f"<div class='ov-h'>Synopsis</div>"
        f"<div class='overview'>{esc(overview)}</div>"
        f"</div></div></div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ---- recommendations ----
    section("Because you're watching this", "Content similarity — TF-IDF over plot, cast & keywords")
    slot = st.empty()
    slot.markdown(skeletons(8, mode="rail"), unsafe_allow_html=True)

    bundle, berr = api(
        "/movie/search",
        {"query": title, "tfidf_top_n": 14, "genre_limit": 16},
        timeout=90,
    )
    slot.empty()

    got_tfidf = False
    if not berr and bundle:
        sims = normalize(bundle.get("tfidf_recommendations"))
        if sims:
            got_tfidf = True
            render(sims, mode="rail")
        else:
            st.markdown(
                "<div class='note'>This title isn't in the local TF-IDF corpus — "
                "showing genre matches instead.</div>",
                unsafe_allow_html=True,
            )

        genre_cards = normalize(bundle.get("genre_recommendations"))
        if genre_cards:
            head = genres[0] if genres else "genre"
            section("More like this", f"Popular in {head}")
            render(genre_cards, mode="rail")
    else:
        st.markdown(
            "<div class='note'>Similarity engine is warming up — falling back to genre matches.</div>",
            unsafe_allow_html=True,
        )

    if not got_tfidf:
        fallback, ferr = api("/recommend/genre", {"tmdb_id": mid, "limit": 18}, timeout=60)
        if not ferr and fallback:
            section("You might also like", "Genre-based discovery")
            render(normalize(fallback))

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    if st.button("←  Back to browsing"):
        goto_home()
