import os
import json
import streamlit as st

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="English Listening Lab", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== KONTROL MODE DEVELOPER ====================
# Buka via URL biasa: http://localhost:8501         -> Mode User (Menu Dev Hilang)
# Buka via URL dev:   http://localhost:8501/?dev=true -> Mode Dev (Menu Dev Aktif)
is_dev_mode = st.query_params.get("dev") == "true"

# ==================== KUSTOMISASI CSS & TEMA ====================
is_dark = st.session_state.get("dark_mode", False)

# Palet Konten Utama (Mengikuti Toggle Gelap / Cerah)
if is_dark:
    bg_main = "#111827"        # Latar konten gelap
    bg_header = "#1f2937"      # Header konten gelap
    text_header = "#ffffff"    # Teks header putih
    text_main = "#ffffff"      # Teks konten putih
    text_secondary = "#9ca3af" # Teks keterangan abu terang
    card_bg = "#1f2937"        # Kartu pembahasan gelap
    border_color = "#374151"   # Border gelap
    accent_blue = "#38bdf8"
else:
    bg_main = "#ffffff"        # Latar konten putih
    bg_header = "#ffffff"      # Header konten putih
    text_header = "#111827"    # Teks header hitam
    text_main = "#111827"      # Teks konten hitam
    text_secondary = "#4b5563" # Teks keterangan abu gelap
    card_bg = "#ffffff"        # Kartu pembahasan putih
    border_color = "#e5e7eb"   # Border terang
    accent_blue = "#0284c7"

css_styles = f"""
<style>
    /* Latar Belakang Konten Utama */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {{
        background-color: {bg_main} !important;
        color: {text_main} !important;
    }}
    
    /* Bilah Header Atas Konten */
    header[data-testid="stHeader"] {{
        background-color: {bg_header} !important;
        border-bottom: 1px solid {border_color} !important;
        z-index: 99 !important;
    }}
    header[data-testid="stHeader"] * {{
        color: {text_header} !important;
    }}
    header[data-testid="stHeader"] svg {{
        fill: {text_header} !important;
        stroke: {text_header} !important;
    }}

    /* ======================================================== */
    /*   SIDEBAR & MENU: TOTAL PUTIH / TERANG (TANPA WARNA GELAP) */
    /* ======================================================== */
    section[data-testid="stSidebar"], 
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebarNav"] {{
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
    }}
    
    /* Semua Teks di Sidebar Selalu Hitam Rapi */
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {{
        color: #111827 !important;
    }}

    /* Kotak Pilih Chapter di Sidebar Selalu Putih Bersih */
    section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="select"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] [role="combobox"] {{
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
    }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {{
        color: #111827 !important;
    }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
        fill: #111827 !important;
        stroke: #111827 !important;
    }}

    /* Daftar Pilihan Dropdown Selalu Putih */
    div[data-baseweb="popover"],
    ul[role="listbox"],
    li[role="option"] {{
        background-color: #ffffff !important;
        color: #111827 !important;
    }}
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {{
        background-color: #f3f4f6 !important;
        color: #0284c7 !important;
    }}

    /* Tombol di Sidebar (Reset & Developer Toolbar) */
    section[data-testid="stSidebar"] button {{
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
    }}
    section[data-testid="stSidebar"] button:hover {{
        background-color: #f3f4f6 !important;
        border-color: #9ca3af !important;
        color: #111827 !important;
    }}

    /* Progress Bar di Sidebar Selalu Warna Abu-Abu Terang */
    section[data-testid="stSidebar"] .stProgress > div > div > div > div {{
        background-color: #9ca3af !important;
    }}
    section[data-testid="stSidebar"] .stProgress > div {{
        background-color: #f3f4f6 !important;
    }}

    /* Radio Indicator di Sidebar */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] span {{
        border-color: #0284c7 !important;
    }}

    /* Expander Developer Toolbar di Sidebar */
    section[data-testid="stSidebar"] [data-testid="stExpander"] {{
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 6px !important;
    }}
    section[data-testid="stSidebar"] .streamlit-expanderHeader {{
        background-color: #f9fafb !important;
        color: #111827 !important;
    }}

    /* ======================================================== */
    /*                   KONTEN UTAMA & KOMPONEN                */
    /* ======================================================== */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
        color: {text_main} !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }}
    .stApp p, .stApp span, .stApp label {{
        color: {text_main} !important;
    }}
    .stCaption, small, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {{
        color: {text_secondary} !important;
    }}

    /* Metrik Rekap Nilai */
    [data-testid="stMetric"],
    [data-testid="metric-container"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
    }}
    [data-testid="stMetricValue"], 
    [data-testid="stMetricLabel"] {{
        color: {text_main} !important;
    }}

    /* Expander / Kartu Pembahasan di Konten */
    .block-container [data-testid="stExpander"] {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 6px !important;
    }}
    .block-container .streamlit-expanderHeader {{
        background-color: {card_bg} !important;
        color: {text_main} !important;
    }}
    .block-container .streamlit-expanderContent {{
        background-color: {card_bg} !important;
        border-top: 1px solid {border_color} !important;
    }}

    /* Tombol Utama */
    button[kind="primary"] {{
        background-color: {accent_blue} !important;
        border-color: {accent_blue} !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }}
    button[kind="primary"]:hover {{
        filter: brightness(0.9);
    }}

    /* Tombol Sekunder di Konten */
    .block-container button[kind="secondary"] {{
        background-color: {card_bg} !important;
        color: {text_main} !important;
        border: 1px solid {border_color} !important;
        border-radius: 6px !important;
    }}

    /* Label Toggle Mode Gelap */
    div[data-testid="stToggle"] label p {{
        color: {text_main} !important;
        font-weight: 500 !important;
    }}

    /* Tombol Buka/Tutup Sidebar (Selalu Putih & Ikon Hitam) */
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button,
    button[aria-label="Expand sidebar"],
    button[aria-label="Collapse sidebar"],
    button[data-testid="baseButton-header"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        cursor: pointer !important;
        color: #111827 !important;
        z-index: 10000000 !important;
    }}
    
    [data-testid="stSidebarCollapsedControl"] {{
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        padding: 4px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }}
    
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg {{
        fill: #111827 !important;
        stroke: #111827 !important;
    }}

    .block-container {{
        padding-top: 4.5rem !important;
        padding-bottom: 2.5rem !important;
    }}
"""

if is_dev_mode:
    css_styles += """
    #MainMenu, [data-testid="stMainMenu"] {
        display: block !important;
        visibility: visible !important;
    }
    div[data-testid="stSettingsModal"] div[data-testid="stSelectbox"],
    div[data-testid="stSettingsModal"] div:has(> label[data-testid="stWidgetLabel"]) {
        display: none !important;
    }
    .stDeployButton, [data-testid="stDeployButton"], [data-testid="stAppDeployButton"], [data-testid="manage-app-button"] {
        display: none !important;
    }
    """
else:
    css_styles += """
    #MainMenu, [data-testid="stMainMenu"], [data-testid="stToolbarActions"] {
        display: none !important;
    }
    footer { display: none !important; }
    .stDeployButton, [data-testid="stDeployButton"], [data-testid="stAppDeployButton"], [data-testid="manage-app-button"] {
        display: none !important;
    }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    """

css_styles += "</style>"
st.markdown(css_styles, unsafe_allow_html=True)

# Path dasar direktori file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data_soal.json")

# ==================== LOAD DATA ====================
@st.cache_data
def load_bank():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_bank()

# ==================== SESSION STATE ====================
if "user_choices" not in st.session_state:
    st.session_state.user_choices = {}
if "sub_status" not in st.session_state:
    st.session_state.sub_status = {}
if "ch_select" not in st.session_state:
    st.session_state.ch_select = data[0]["chapter_title"]
if "sub_select" not in st.session_state:
    st.session_state.sub_select = data[0]["subchapters"][0]["sub_id"]

# ==================== CALLBACKS ====================
def on_chapter_change():
    selected_ch = next(c for c in data if c["chapter_title"] == st.session_state.ch_select)
    st.session_state.sub_select = selected_ch["subchapters"][0]["sub_id"]

def submit_answers(current_sub_id, questions):
    for q in questions:
        q_id = q["id"]
        val = st.session_state.get(f"widget_{q_id}")
        st.session_state.user_choices[q_id] = val
    st.session_state.sub_status[current_sub_id] = True

def reset_answers(current_sub_id, questions):
    st.session_state.sub_status[current_sub_id] = False
    for q in questions:
        q_id = q["id"]
        st.session_state.user_choices.pop(q_id, None)
        if f"widget_{q_id}" in st.session_state:
            del st.session_state[f"widget_{q_id}"]

def go_to_next_sub(next_sub_id):
    st.session_state.sub_select = next_sub_id

def go_to_next_chapter(next_ch_title, first_sub_id):
    st.session_state.ch_select = next_ch_title
    st.session_state.sub_select = first_sub_id

def reset_all_data():
    current_dark_state = st.session_state.get("dark_mode", False)
    st.session_state.clear()
    st.session_state.dark_mode = current_dark_state

# ==================== SIDEBAR (SERBA PUTIH & TERANG) ====================
if is_dev_mode:
    st.sidebar.warning("Developer Toolbar")
    col_d1, col_d2 = st.sidebar.columns(2)
    with col_d1:
        if st.button("Rerun", use_container_width=True):
            st.rerun()
    with col_d2:
        if st.button("Cache", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with st.sidebar.expander("Session State Inspector"):
        st.json(dict(st.session_state))
    st.sidebar.divider()

total_all_subs = sum(len(ch["subchapters"]) for ch in data)
completed_subs = sum(1 for status in st.session_state.sub_status.values() if status)

st.sidebar.title("Menu Latihan")
menu = st.sidebar.radio("Pilih Halaman:", ["Kerjakan Soal", "Rekap Nilai"])

st.sidebar.divider()
st.sidebar.write(f"Progres Keseluruhan: {completed_subs}/{total_all_subs} Materi")
st.sidebar.progress(completed_subs / total_all_subs if total_all_subs > 0 else 0.0)

if st.sidebar.button("Reset Semua Latihan", use_container_width=True):
    reset_all_data()
    st.rerun()

# ==================== HEADER ATAS HALAMAN ====================
top_col1, top_col2 = st.columns([5, 1.2])

# ==================== HALAMAN: KERJAKAN SOAL ====================
if menu == "Kerjakan Soal":
    ch_titles = [ch["chapter_title"] for ch in data]
    
    selected_ch_title = st.sidebar.selectbox(
        "Pilih Chapter:", 
        ch_titles, 
        key="ch_select",
        on_change=on_chapter_change
    )
    selected_chapter = next(ch for ch in data if ch["chapter_title"] == selected_ch_title)

    sub_list = selected_chapter["subchapters"]
    sub_ids = [s["sub_id"] for s in sub_list]
    sub_dict = {s["sub_id"]: s for s in sub_list}

    def format_sub_label(sub_id):
        is_done = st.session_state.sub_status.get(sub_id, False)
        status_text = "[Selesai]" if is_done else "[Belum]"
        return f"{status_text} {sub_dict[sub_id]['sub_title']}"

    if st.session_state.sub_select not in sub_ids:
        st.session_state.sub_select = sub_ids[0]

    selected_sub_id = st.sidebar.radio(
        "Pilih Materi:", 
        sub_ids, 
        format_func=format_sub_label,
        key="sub_select"
    )
    
    current_sub = sub_dict[selected_sub_id]
    sub_id = current_sub["sub_id"]

    st.sidebar.divider()
    st.sidebar.caption("Mode: Offline Practice")

    # Header Halaman & Toggle Mode Gelap
    with top_col1:
        st.title(selected_chapter["chapter_title"])
    with top_col2:
        st.write("")
        st.toggle("Mode Gelap", key="dark_mode")

    st.subheader(current_sub["sub_title"])
    st.caption("Dengarkan rekaman audio di bawah, lalu pilih jawaban yang paling tepat.")

    # Audio Player
    st.markdown("#### Audio Rekaman")
    audio_path = os.path.join(BASE_DIR, current_sub["audio_path"]) if not os.path.isabs(current_sub["audio_path"]) else current_sub["audio_path"]
    
    if os.path.exists(audio_path):
        st.audio(audio_path, format="audio/mp3")
    else:
        st.warning(f"File audio belum ada di lokasi: `{audio_path}`.")

    st.divider()

    # Form Soal
    st.markdown("#### Soal Latihan")
    is_submitted = st.session_state.sub_status.get(sub_id, False)

    for idx, q in enumerate(current_sub["questions"], start=1):
        q_id = q["id"]
        saved_val = st.session_state.user_choices.get(q_id, None)
        
        st.markdown(f"**{idx}. {q['question']}**")
        
        selected_option = st.radio(
            label=f"Opsi_{q_id}",
            options=q["options"],
            index=q["options"].index(saved_val) if saved_val in q["options"] else None,
            key=f"widget_{q_id}",
            disabled=is_submitted,
            label_visibility="collapsed"
        )
        st.write("")

    # Tombol Aksi
    col1, col2, _ = st.columns([1.5, 2, 3])
    with col1:
        if not is_submitted:
            st.button(
                "Kirim Jawaban", 
                type="primary", 
                on_click=submit_answers, 
                args=(sub_id, current_sub["questions"])
            )
        else:
            st.button(
                "Kerjakan Ulang", 
                on_click=reset_answers, 
                args=(sub_id, current_sub["questions"])
            )

    with col2:
        if is_submitted:
            current_sub_idx = sub_ids.index(sub_id)
            current_ch_idx = ch_titles.index(selected_ch_title)

            if current_sub_idx < len(sub_list) - 1:
                next_sub_id = sub_ids[current_sub_idx + 1]
                st.button(
                    "Materi Berikutnya", 
                    type="primary", 
                    on_click=go_to_next_sub, 
                    args=(next_sub_id,)
                )
            elif current_ch_idx < len(data) - 1:
                next_ch = data[current_ch_idx + 1]
                st.button(
                    "Lanjut ke Chapter Berikutnya", 
                    type="primary", 
                    on_click=go_to_next_chapter, 
                    args=(next_ch["chapter_title"], next_ch["subchapters"][0]["sub_id"])
                )

    # Pembahasan Jawaban & Nilai
    if is_submitted:
        st.divider()
        correct_count = 0
        st.markdown("#### Pembahasan Jawaban")

        for q in current_sub["questions"]:
            user_ans = st.session_state.user_choices.get(q["id"])
            is_correct = user_ans == q["answer"]
            if is_correct:
                correct_count += 1

            status_tag = "[Benar]" if is_correct else "[Salah]"
            with st.expander(f"{status_tag} Soal: {q['question']}"):
                st.write(f"**Jawaban kamu:** {user_ans if user_ans is not None else 'Tidak dijawab'}")
                st.write(f"**Kunci jawaban:** {q['answer']}")
                st.info(f"Catatan: {q['explanation']}")

        total_q = len(current_sub["questions"])
        score = int((correct_count / total_q) * 100)
        st.metric(label="Skor Sub-chapter Ini", value=f"{score}%", delta=f"{correct_count} dari {total_q} soal benar")

# ==================== HALAMAN: REKAP NILAI ====================
else:
    with top_col1:
        st.title("Rekap Nilai Keseluruhan")
    with top_col2:
        st.write("")
        st.toggle("Mode Gelap", key="dark_mode")
        
    st.caption("Ringkasan hasil nilai dari seluruh chapter yang sudah dikerjakan.")
    st.divider()

    total_all_q = 0
    total_all_correct = 0

    for ch in data:
        st.markdown(f"### {ch['chapter_title']}")
        sub_cols = st.columns(len(ch["subchapters"]))

        for idx, sub in enumerate(ch["subchapters"]):
            s_id = sub["sub_id"]
            num_q = len(sub["questions"])
            total_all_q += num_q
            is_done = st.session_state.sub_status.get(s_id, False)

            with sub_cols[idx]:
                if is_done:
                    correct = sum(1 for q in sub["questions"] if st.session_state.user_choices.get(q["id"]) == q["answer"])
                    total_all_correct += correct
                    sub_score = int((correct / num_q) * 100)
                    st.metric(label=f"[Selesai] {sub['sub_title']}", value=f"{sub_score}%", delta=f"{correct}/{num_q} Benar")
                else:
                    st.metric(label=f"[Belum] {sub['sub_title']}", value="Belum Dikerjakan", delta_color="off")
        st.write("")

    st.divider()
    overall_score = int((total_all_correct / total_all_q) * 100) if total_all_q > 0 else 0
    st.metric(label="Akumulasi Nilai Semua Chapter", value=f"{overall_score}%", delta=f"{total_all_correct} dari {total_all_q} Soal Benar")
