"""
Customer Rating & Review Analysis (CRRA) - UI Component Library (BUILD-06)
Tailwind CSS Injection via st.components.v1.html & Tailwind CDN
Author: Alisha Khan (Roll No. 2503201450012)
"""

try:
    import streamlit as st
    import streamlit.components.v1 as components
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

def render_tailwind_header(title: str, subtitle: str, badge_text: str = "Enterprise Analytics"):
    """
    Renders a responsive, modern executive header using Tailwind CSS.
    Returns the generated HTML string and calls components.html if in a Streamlit context.
    """
    html_code = f"""
    {TAILWIND_CDN}
    <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 p-6 rounded-2xl shadow-md border border-slate-800 text-white font-sans mb-4">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
            <div>
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-400/30 mb-2">
                    <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
                    {badge_text}
                </div>
                <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white">{title}</h1>
                <p class="text-slate-400 text-sm mt-1">{subtitle}</p>
            </div>
            <div class="text-right text-xs text-slate-400 border-t md:border-t-0 md:border-l border-slate-800 pt-2 md:pt-0 md:pl-5">
                <span class="block font-semibold text-slate-300">NexCart Retail Solutions</span>
                <span>Alisha Khan | Roll: 2503201450012</span>
            </div>
        </div>
    </div>
    """
    if HAS_STREAMLIT:
        try:
            components.html(html_code, height=135, scrolling=False)
        except Exception:
            pass
    return html_code

def render_kpi_card(title: str, value: str, delta: str, delta_type: str = "positive", icon: str = "📊"):
    """
    Generates a single Tailwind CSS KPI card HTML.
    """
    if delta_type == "positive":
        badge = "bg-emerald-100 text-emerald-800 border-emerald-300"
        accent = "border-emerald-500/40 bg-emerald-50/30"
    elif delta_type == "warning":
        badge = "bg-amber-100 text-amber-800 border-amber-300"
        accent = "border-amber-500/40 bg-amber-50/30"
    elif delta_type == "critical":
        badge = "bg-rose-100 text-rose-800 border-rose-300"
        accent = "border-rose-500/40 bg-rose-50/30"
    else:
        badge = "bg-slate-100 text-slate-700 border-slate-200"
        accent = "border-slate-200 bg-white"

    card_html = f"""
    {TAILWIND_CDN}
    <div class="bg-white p-5 rounded-2xl shadow-sm border {accent} font-sans">
        <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">{title}</span>
            <span class="text-xs font-bold px-2 py-0.5 rounded-full border {badge}">{delta}</span>
        </div>
        <div class="flex items-baseline gap-2 mb-1">
            <span class="text-xl">{icon}</span>
            <span class="text-3xl font-black text-slate-900 tracking-tight">{value}</span>
        </div>
    </div>
    """
    return card_html

def render_kpi_cards(kpi_list: list):
    """
    Renders a 4-column responsive grid of executive KPI cards.
    """
    cards_html = ""
    for card in kpi_list:
        status = card.get("status", "neutral")
        if status == "positive":
            accent = "border-emerald-500/40 bg-emerald-50/50"
            badge = "bg-emerald-100 text-emerald-800 border-emerald-300"
        elif status == "warning":
            accent = "border-amber-500/40 bg-amber-50/50"
            badge = "bg-amber-100 text-amber-800 border-amber-300"
        elif status == "critical":
            accent = "border-rose-500/40 bg-rose-50/50"
            badge = "bg-rose-100 text-rose-800 border-rose-300"
        else:
            accent = "border-slate-200 bg-white"
            badge = "bg-slate-100 text-slate-700 border-slate-200"

        icon = card.get("icon", "⭐")
        cards_html += f"""
        <div class="bg-white p-5 rounded-2xl shadow-sm border {accent} transition duration-200 hover:shadow-md">
            <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">{card.get('label', '')}</span>
                <span class="text-xs font-bold px-2 py-0.5 rounded-full border {badge}">{card.get('trend', '')}</span>
            </div>
            <div class="flex items-baseline gap-2 mb-1">
                <span class="text-xl">{icon}</span>
                <span class="text-3xl font-black text-slate-900 tracking-tight">{card.get('value', '')}</span>
            </div>
            <div class="text-xs text-slate-500">{card.get('sub', '')}</div>
        </div>
        """

    html_code = f"""
    {TAILWIND_CDN}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-sans mb-4">
        {cards_html}
    </div>
    """
    if HAS_STREAMLIT:
        try:
            components.html(html_code, height=130, scrolling=False)
        except Exception:
            pass
    return html_code

def render_insight_box(title: str, text: str, box_type: str = "info"):
    """
    Renders an executive analytical callout box.
    """
    if box_type == "warning":
        box_style = "border-amber-400 bg-amber-50/70 text-amber-900"
        tag = "CRITICAL DIAGNOSTIC"
        tag_style = "bg-amber-200 text-amber-900"
    elif box_type == "success":
        box_style = "border-emerald-400 bg-emerald-50/70 text-emerald-900"
        tag = "COMMERCIAL WIN"
        tag_style = "bg-emerald-200 text-emerald-900"
    else:
        box_style = "border-blue-400 bg-blue-50/70 text-blue-900"
        tag = "ANALYST INSIGHT"
        tag_style = "bg-blue-200 text-blue-900"

    html_code = f"""
    {TAILWIND_CDN}
    <div class="p-4 rounded-xl border {box_style} font-sans my-3">
        <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-bold px-2 py-0.5 rounded {tag_style} tracking-wide">{tag}</span>
            <span class="text-sm font-bold">{title}</span>
        </div>
        <p class="text-xs leading-relaxed mt-1">{text}</p>
    </div>
    """
    if HAS_STREAMLIT:
        try:
            components.html(html_code, height=95, scrolling=False)
        except Exception:
            pass
    return html_code

def apply_plotly_theme(fig):
    """
    Applies the NexCart corporate theme styling to a Plotly figure.
    """
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Calibri, sans-serif", size=12, color="#0F172A"),
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

if __name__ == "__main__":
    h = render_tailwind_header("Test Header", "Subtitle")
    print(f"Header generated: {len(h)} chars")
    k = render_kpi_card("Mean Rating", "4.2", "+0.3", "positive", "⭐")
    print(f"KPI card generated: {len(k)} chars")
