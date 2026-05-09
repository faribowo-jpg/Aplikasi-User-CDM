import streamlit as st
import pandas as pd
import os
import base64
import io
from datetime import datetime

import base64

def make_download_link(filename):
    if pd.isna(filename) or filename == "":
        return ""

    path = os.path.join("uploads", filename)

    if not os.path.exists(path):
        return ""

    with open(path, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode()

    return f"data:application/pdf;base64,{b64}"
def set_bg(image_file):
    import base64

    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Aplikasi CDM", layout="wide")
st.markdown(
    """
<style>

/* FORCE HEADER COLOR (WORK ALL VERSION) */
div[data-testid="stDataFrame"] div[role="table"] div[role="columnheader"] {
    background: linear-gradient(90deg, #4facfe, #00c6ff) !important;
    color: white !important;
    font-weight: 700 !important;
    text-align: center !important;
}

/* DATA EDITOR */
div[data-testid="stDataEditor"] div[role="columnheader"] {
    background: linear-gradient(90deg, #4facfe, #00c6ff) !important;
    color: white !important;
    font-weight: 700 !important;
}

/* ROW */
div[data-testid="stDataFrame"] div[role="row"]:nth-child(even) {
    background-color: #f8fafc !important;
}

/* HOVER */
div[data-testid="stDataFrame"] div[role="row"]:hover {
    background-color: #e0f2fe !important;
}

/* TEXT CENTER */
div[data-testid="stDataFrame"] div[role="cell"] {
    text-align: center;
}

</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    """
<style>
/* Card */
.card {
background: white;
padding: 20px;
border-radius: 15px;
box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
margin-bottom: 20px;
}

/* Header */
h3 {
margin-bottom: 15px;
}

/* Table */
</style>
""",
    unsafe_allow_html=True,
)
# ==============================
# BACKGROUND DINAMIS
# ==============================
if "login" not in st.session_state:
    st.session_state.login = False

if st.session_state.login:
    set_bg("background_app.jpg")  # setelah login
else:
    set_bg("background_login.jpg")  # sebelum login
# ==============================
# CSS ALFAMART STYLE
# ==============================
st.markdown("""
<style>

/* Semua tombol */
.stButton > button {
    background-color: #ED1C24;
    color: white;
    border-radius: 10px;
    border: none;
    height: 36px;
    padding: 0 15px;
    font-size: 14px;
}

/* DOWNLOAD BUTTON (WAJIB INI) */
.stDownloadButton > button {
    background-color: #ED1C24 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    height: 36px !important;
    padding: 0 15px !important;
    font-size: 14px !important;
}

</style>
""", unsafe_allow_html=True)
st.markdown(
    """
<style>

/* Background */
.main {
    background-color: #f5f7fa;
}

/* Header */
.header {
    background: linear-gradient(90deg, #0057A8, #ED1C24);
    padding: 20px;
    border-radius: 15px;
    color: white;
    margin-bottom: 20px;
}

/* Card */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Sidebar profile */
.profile-box {
    background: linear-gradient(90deg, #0057A8, #ED1C24);
    padding: 15px;
    border-radius: 12px;
    color: white;
    margin-bottom: 15px;
}

/* Button */
.stButton>button {
    background-color: #ED1C24;
    color: white;
    border-radius: 10px;
    border: none;
    height: 40px;
}

/* Input */
.stTextInput>div>div>input {
    border-radius: 8px;
}

textarea {
    border-radius: 8px !important;
}

</style>
""",
    unsafe_allow_html=True,
)
st.markdown("""
<style>

/* SELECTBOX NAVBAR */
div[data-baseweb="select"] > div {
    background-color: #ED1C24 !important;
    border-radius: 10px !important;
    min-height: 45px !important;
    border: none !important;
}

/* TEXT VALUE */
div[data-baseweb="select"] div {
    color: white !important;
    font-weight: 600 !important;
}

/* PLACEHOLDER / SELECTED TEXT */
div[data-baseweb="select"] span {
    color: white !important;
    font-weight: 600 !important;
}

/* INPUT TEXT */
div[data-baseweb="select"] input {
    color: white !important;
}

/* DROPDOWN ICON */
div[data-baseweb="select"] svg {
    fill: white !important;
}

/* HOVER */
div[data-baseweb="select"]:hover > div {
    background-color: #c81018 !important;
}

</style>
""", unsafe_allow_html=True)


# ==============================
# TABLE RENDER (FULL FITUR)
# ==============================
def render_table(df, page=1, page_size=10):

    total_data = len(df)
    total_page = max(
        1, (total_data // page_size) + (1 if total_data % page_size else 0)
    )

    start = (page - 1) * page_size
    end = start + page_size
    df_page = df.iloc[start:end]

    html = """
    <style>
    .custom-table {
        border-collapse: collapse;
        width: 100%;
        font-size: 14px;
        border-radius: 12px;
        overflow: hidden;
    }

    .custom-table th {
        background: linear-gradient(90deg, #4facfe, #00c6ff);
        color: white;
        padding: 10px;
        text-align: center;
    }

    .custom-table td {
        padding: 8px;
        text-align: center;
        border-bottom: 1px solid #eee;
    }

    .custom-table tr:nth-child(even) {
        background-color: #f9fafb;
    }

    .custom-table tr:hover {
        background-color: #e0f2fe;
    }

    .status-pengajuan {background:#dbeafe;color:#1e40af;font-weight:bold;}
    .status-diproses {background:#fef3c7;color:#92400e;font-weight:bold;}
    .status-done {background:#d1fae5;color:#065f46;font-weight:bold;}
    .status-Batal {background:#fee2e2;color:#991b1b;font-weight:bold;}
    </style>

    <table class="custom-table">
        <thead><tr>
    """

    for col in df.columns:
        html += f"<th>{col}</th>"

        html += "</tr></thead><tbody>"

    for _, row in df_page.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            if col == "status":
                cls = f"status-{str(val).lower()}"
                html += f"<td class='{cls}'>{val}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"

        html += "</tbody></table>"
        st.markdown(html, unsafe_allow_html=True)
        return total_page


# ==============================
# SAFE
# ==============================
def safe(x):
    return "" if pd.isna(x) else str(x)


def highlight_status(val):
    if val == "done":
        return "background-color: #d1fae5; color:#065f46; font-weight:600;"
    elif val == "diproses":
        return "background-color: #fef3c7; color:#92400e; font-weight:600;"
    elif val == "Batal":
        return "background-color: #fee2e2; color:#991b1b; font-weight:600;"
    elif val == "Pengajuan":
        return "background-color: #dbeafe; color:#1e40af; font-weight:600;"
    return ""



    for col in df.columns:
        html += "<th>" + str(col) + "</th>"

    html += "</tr></thead><tbody>"

    for i in range(len(df)):
        html += "<tr>"
        for col in df.columns:
            html += "<td>" + str(df.iloc[i][col]) + "</td>"
        html += "</tr>"

    html += "</tbody></table>"

    st.markdown(html, unsafe_allow_html=True)


# ==============================
# LOAD MASTER
# ==============================
@st.cache_data
def load_master():
    cabang = pd.read_excel("master_data.xlsx", sheet_name="cabang")
    toko = pd.read_excel("master_data.xlsx", sheet_name="toko")
    ms = pd.read_excel("master_data.xlsx", sheet_name="ms")
    rekening = pd.read_excel("master_data.xlsx", sheet_name="rekening")
    user = pd.read_excel("master_data.xlsx", sheet_name="user")

    user["nik"] = user["nik"].astype(str).str.strip().str.lstrip("0")
    return cabang, toko, ms, rekening, user


cabang, toko, ms, rekening, user = load_master()


# ==============================
# LOOKUP
# ==============================
def get_cabang(k):
    if not k:
        return None

    k = str(k).strip().upper()

    df = cabang.copy()
    df["kode_cabang"] = df["kode_cabang"].astype(str).str.strip().str.upper()

    d = df[df["kode_cabang"] == k]

    return d.iloc[0] if not d.empty else None


def get_toko(k):
    d = toko[toko["kode_toko"] == k]
    return d.iloc[0] if not d.empty else None


def get_ms(k):
    d = ms[ms["kode_ms"] == k]
    return d.iloc[0] if not d.empty else None


def get_rek(k):
    d = rekening[rekening["kode_toko"] == k]
    return d.iloc[0] if not d.empty else None


# ==============================
# BACKGROUND (TARUH DI SINI)
# ==============================
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()


def set_bg(image_file):
    import base64

    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# ==============================
# LOGIN
# ==============================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    # ======================
    # LAYOUT LOGIN (HARUS DI DALAM IF)
    # ======================
    col1, col2 = st.columns([1, 1])

    with col1:

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.image("logo_alfamart.png", width=180)

        st.markdown(
            "<h2 style='color:#0057A8;'>Login Aplikasi CDM</h2>", unsafe_allow_html=True
        )

        nik = st.text_input("NIK")
        pw = st.text_input("Password", type="password")

        if st.button("Login"):
            nik = safe(nik).lstrip("0")
            cek = user[(user["nik"] == nik) & (user["password"] == pw)]

            if not cek.empty:
                st.session_state.login = True
                st.session_state.nik = nik
                st.session_state.role = cek.iloc[0]["role"]
                st.session_state.kode_cabang = cek.iloc[0]["kode_cabang"]
                st.session_state.nama = cek.iloc[0]["nama_user"]
                st.session_state.vendor = cek.iloc[0]["vendor"]
                st.session_state.jabatan = cek.iloc[0]["jabatan"]
                st.session_state.login = True
                st.session_state.menu = "HOME"  # ⬅️ TAMBAHKAN INI
                st.rerun()

            else:
                st.error("Login gagal")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.empty()

    # STOP HARUS DI DALAM IF
    st.stop()

# ==============================
# MENU: HOME
# ==============================
# ======================
# INIT MENU
# ======================
if "menu" not in st.session_state:
    st.session_state.menu = "HOME"

menu = st.session_state.menu
role = st.session_state.get("role", "user")  


    
     

# ==============================
# NOTIF BADGE
# ==============================
def get_notif_per_menu(df_all, user_df):
    if df_all.empty:
        return {
            "QR Toko GO": 0,
            "CS Pindah MS": 0,
            "Relokasi Mesin": 0,
            "Penambahan Mesin": 0,
        }

    nik_login = str(st.session_state.nik)
    role = st.session_state.role

    df_all["user"] = df_all["user"].astype(str)
    df_all["status"] = df_all["status"].astype(str)

    # ======================
    # FILTER ROLE
    # ======================
    if role == "admin":
        df_notif = df_all

    elif role == "regional":
        user_df["nik"] = user_df["nik"].astype(str)
        user_df["nik_regional"] = user_df["nik_regional"].astype(str)

        user_regional = user_df[user_df["nik_regional"] == nik_login]
        nik_list = user_regional["nik"].tolist()
        nik_list.append(nik_login)

        df_notif = df_all[df_all["user"].isin(nik_list)]

    else:
        df_notif = df_all[df_all["user"] == nik_login]

    # ======================
    # FILTER BELUM DONE
    # ======================
    df_notif = df_notif[
        df_notif["status"].isin(["Pengajuan", "diproses"])
    ]

    # ======================
    # HITUNG PER JENIS
    # ======================
    result = {
        "QR Toko GO": 0,
        "CS Pindah MS": 0,
        "Relokasi Mesin": 0,
        "Penambahan Mesin": 0,
    }

    counts = df_notif["jenis_pengajuan"].value_counts()

    for k in result.keys():
        result[k] = int(counts.get(k, 0))

    return result
# ==============================
# TOP NAVIGATION
# ==============================

# Load data untuk badge
if os.path.exists("data.xlsx"):
    df_all = pd.read_excel("data.xlsx")
else:
    df_all = pd.DataFrame()

notif = get_notif_per_menu(df_all, user)

if not df_all.empty and "status" in df_all.columns:
    pending = df_all[
        ~df_all["status"].isin(["done", "Batal"])
    ]
    badge_count = len(pending)
else:
    badge_count = 0



# ======================
# MENU STYLE
# ======================
st.markdown("""
<style>

.top-menu button {
    width: 100%;
    height: 45px;
    border-radius: 10px;
    border: none;
    background-color: #0057A8;
    color: white;
    font-weight: 600;
}

.top-menu button:hover {
    background-color: #ED1C24;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ======================
# MENU BUTTON FUNCTION
# ======================
def set_menu(menu_name):
    st.session_state.menu = menu_name

# ==============================
# TOP NAVIGATION
# ==============================

# Load data badge
if os.path.exists("data.xlsx"):
    df_all = pd.read_excel("data.xlsx")
else:
    df_all = pd.DataFrame()

notif = get_notif_per_menu(df_all, user)

if not df_all.empty and "status" in df_all.columns:
    pending = df_all[
        ~df_all["status"].isin(["done", "Batal"])
    ]
    badge_count = len(pending)
else:
    badge_count = 0

# ======================
# INIT MENU
# ======================
if "menu" not in st.session_state:
    st.session_state.menu = "HOME"

# ======================
# INIT MENU PENGAJUAN
# ======================
menu_options = [
    "📋 Menu Pengajuan",
    "QR Toko GO",
    "CS Pindah MS",
    "Relokasi Mesin",
    "Penambahan Mesin"
]

# reset jika value lama tidak valid
if (
    "menu_pengajuan" not in st.session_state
    or st.session_state.menu_pengajuan not in menu_options
):
    st.session_state.menu_pengajuan = "📋 Menu Pengajuan"


# ======================
# TOP MENU
# ======================
col1, col2, col3, col4 = st.columns([1,2,1,1])

with col1:
    if st.button("🏠 HOME", use_container_width=True):
        st.session_state.menu = "HOME"

with col2:

    pilihan = [
        "Pilih Menu",
        "QR Toko GO",
        "CS Pindah MS",
        "Relokasi Mesin",
        "Penambahan Mesin"
    ]

    selected = st.selectbox(
    "",
    menu_options,
    key="menu_pengajuan",
    label_visibility="collapsed"
)


    if selected != "📋 Menu Pengajuan":
        st.session_state.menu = selected

with col3:
    if st.button(f"📊 Monitoring ({badge_count})", use_container_width=True):
        st.session_state.menu = "Monitoring"

with col4:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("---")

# ======================
# PROFILE
# ======================
st.markdown(
f"""
<div class="profile-box">
<h4>👤 {st.session_state.nama}</h4>
<p>
Cabang: {st.session_state.kode_cabang} |
Jabatan: {st.session_state.get("jabatan","-")} |
Role: <b>{st.session_state.role.upper()}</b>
</p>
</div>
""",
unsafe_allow_html=True,
)

menu = st.session_state.menu

if menu == "HOME":

    st.markdown(
    f"""
<h2>👋 Selamat Datang, {st.session_state.get("nama", "-")}</h2>
""",
    unsafe_allow_html=True,
)
    

    col1, col2, col3 = st.columns([1, 3, 1])

# ==============================
# HEADER
# ==============================
col1, col2 = st.columns([1, 6])

with col1:
    st.image("logo_alfamart.png", width=140)

with col2:
    st.markdown(
        """
        <h1 style='margin-top:20px; color:#2d3748;'>
        Aplikasi Pengajuan User CDM
        </h1>
        """,
        unsafe_allow_html=True,
    )


def load_data():

    if os.path.exists("data.xlsx"):
        df = pd.read_excel("data.xlsx")
    else:
        df = pd.DataFrame()

    # ======================
    # HANDLE EMPTY
    # ======================
    if df.empty:
        return df

    # ======================
    # REQUIRED COLUMN
    # ======================
    required_cols = [
        "user",
        "status",
        "jenis_pengajuan"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # ======================
    # NORMALISASI
    # ======================
    df["user"] = (
        df["user"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["status"] = (
        df["status"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    return df
def filter_by_role(df, user_df, nik_login, role):

    # ======================
    # EMPTY DF
    # ======================
    if df is None or df.empty:
        return pd.DataFrame()

    # ======================
    # COPY
    # ======================
    df = df.copy()
    user_df = user_df.copy()

    # ======================
    # REQUIRED COLUMN
    # ======================
    required_cols = [
        "user",
        "status",
        "jenis_pengajuan"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # ======================
    # NORMALISASI DF
    # ======================
    df["user"] = (
        df["user"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["status"] = (
        df["status"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ======================
    # NORMALISASI USER MASTER
    # ======================
    if "nik" not in user_df.columns:
        user_df["nik"] = ""

    if "nik_regional" not in user_df.columns:
        user_df["nik_regional"] = ""

    if "regional" not in user_df.columns:
        user_df["regional"] = ""

    user_df["nik"] = (
        user_df["nik"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    user_df["nik_regional"] = (
        user_df["nik_regional"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    user_df["regional"] = (
        user_df["regional"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ======================
    # NORMALISASI LOGIN
    # ======================
    nik_login = str(nik_login).strip()
    role = str(role).strip().lower()

    # ======================
    # ADMIN
    # ======================
    if role == "admin":
        return df

    # ======================
    # RFM
    # ======================
    elif role == "rfm":

        rfm_data = user_df[
            user_df["nik"] == nik_login
        ]

        if rfm_data.empty:
            return pd.DataFrame()

        regional_rfm = (
            str(rfm_data.iloc[0]["regional"])
            .strip()
            .upper()
        )

        user_regional = user_df[
            user_df["regional"] == regional_rfm
        ]

        nik_list = (
            user_regional["nik"]
            .astype(str)
            .str.strip()
            .tolist()
        )

        nik_list.append(nik_login)

        return df[
            df["user"].isin(nik_list)
        ]

    # ======================
    # REGIONAL
    # ======================
    elif role == "regional":

        user_regional = user_df[
            user_df["nik_regional"] == nik_login
        ]

        nik_list = (
            user_regional["nik"]
            .astype(str)
            .str.strip()
            .tolist()
        )

        nik_list.append(nik_login)

        return df[
            df["user"].isin(nik_list)
        ]

    # ======================
    # USER
    # ======================
    else:

        return df[
            df["user"] == nik_login
        ]
# ==============================
# SAVE
# ==============================
def save(data):
    
    file = "data.xlsx"
    if os.path.exists(file):
        df = pd.read_excel(file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_excel(file, index=False)


# ==============================
# MENU 1: QR
# ==============================
if menu == "QR Toko GO":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📌 QR Toko GO")

    col1, col2 = st.columns(2)

    with col1:
        kode_cabang = st.text_input("Kode Cabang")

        kode_toko = st.text_input("Kode Toko")
        nama_toko = st.text_input("Nama Toko")
        tipe = st.selectbox("Tipe", ["R", "F"])

    with col2:
        
        kode_ms = st.text_input("Kode MS").upper()
        ms_d = get_ms(kode_ms)
        nama_ms = ms_d["nama_ms"] if ms_d is not None else ""
        st.text_input("Nama MS", value=nama_ms, disabled=True)
        id_mesin = ms_d["id_mesin"] if ms_d is not None else ""
        st.text_input("ID Mesin", value=id_mesin, disabled=True)
        tanggal_go = st.date_input("Tanggal GO", value=datetime.today())

    alamat = st.text_area("Alamat")
    
   
    

    rek_d = get_rek(kode_toko)
    rekening_no = rek_d["no_rekening"] if rek_d is not None else ""
    bank = rek_d["bank"] if rek_d is not None else ""
    
    cabang_data = get_cabang(kode_cabang)
    vendor = cabang_data["vendor"] if cabang_data is not None else ""

    
    st.text_input("Bank", value=bank, disabled=True)
    st.text_input("Rekening", value=rekening_no, disabled=True)
    st.text_input("Vendor", value=vendor, disabled=True)


    
    # ======================
    # SUBMIT
    # ======================
    if st.button("💾 Submit QR"):

        if not kode_toko or not kode_ms:
            st.error("Kode Toko & Kode MS wajib diisi")
            st.stop()

        if ms_d is None:
            st.error("Kode MS tidak ditemukan")
            st.stop()

        save(
            {
                "jenis_pengajuan": "QR Toko GO",
                "vendor": st.session_state.vendor,
                "kode_cabang": kode_cabang,
                "kode_toko": kode_toko,
                "nama_toko": nama_toko,
                "tipe": tipe,
                "alamat": alamat,
                "kode_ms": kode_ms,
                "nama_ms": nama_ms,
                "id_mesin": id_mesin,
                "bank": bank,
                "rekening": rekening_no,
                "tanggal_go": tanggal_go.strftime("%d-%m-%Y"),
                "status": "diproses",
                "tanggal_submit": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "tanggal_update_status": "",
                "status": "Pengajuan",
                "user": st.session_state.nik,
            }
        )

        st.success("Berhasil disimpan")
        st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# MENU 2: CS
# ==============================
elif menu == "CS Pindah MS":

    st.subheader("CS Pindah MS")
    kode_cabang = st.session_state.kode_cabang
    kode_cabang = st.text_input("Kode Cabang", key="cs_kode_cabang").upper()
    cabang_data = get_cabang(kode_cabang)
    vendor = cabang_data["vendor"] if cabang_data is not None else ""
    st.text_input("Vendor", value=vendor, disabled=True)
    
    kode_toko = st.text_input("Kode Toko", key="cs_kode_toko").strip().upper()

# ======================
# INIT
# ======================
    data = pd.DataFrame()
    toko_d = None

# ======================
# LOOKUP
# ======================
    if kode_toko:
     data = toko[toko["kode_toko"] == kode_toko]

    if not data.empty:
        toko_d = data.iloc[0]

# ======================
# AUTO FIELD
# ======================
    nama_toko = toko_d["nama_toko"] if toko_d is not None else ""
    alamat = toko_d["alamat"] if toko_d is not None else ""
    tipe = toko_d["tipe"] if toko_d is not None else ""

# ======================
# TAMPILKAN
# ======================
    st.text_input("Nama Toko", value=nama_toko, disabled=True)
    st.text_input("Alamat", value=alamat, disabled=True)
    st.text_input("Tipe", value=tipe, disabled=True)

    ms_awal = st.text_input("Kode MS Lama").upper()
    ms_tujuan = st.text_input("Kode MS Baru").upper()

    ms_lama = get_ms(ms_awal)
    ms_baru = get_ms(ms_tujuan)

    nama_ms_lama = ms_lama["nama_ms"] if ms_lama is not None else ""
    id_mesin_lama = ms_lama["id_mesin"] if ms_lama is not None else ""

    nama_ms_baru = ms_baru["nama_ms"] if ms_baru is not None else ""
    id_mesin_baru = ms_baru["id_mesin"] if ms_baru is not None else ""

    rek_d = get_rek(kode_toko)
    rekening_no = rek_d["no_rekening"] if rek_d is not None else ""
    bank = rek_d["bank"] if rek_d is not None else ""

    st.text_input("Nama MS Lama", value=nama_ms_lama, disabled=True)
    st.text_input("ID Mesin Lama", value=id_mesin_lama, disabled=True)
    st.text_input("Nama MS Baru", value=nama_ms_baru, disabled=True)
    st.text_input("ID Mesin Baru", value=id_mesin_baru, disabled=True)

    if st.button("Submit CS"):
        save(
            {
                "jenis_pengajuan": "CS Pindah MS",
                "vendor": vendor,
                "kode_cabang": kode_cabang,
                "kode_toko": kode_toko,
                "nama_toko": nama_toko,
                "tipe": tipe,
                "alamat": alamat,
                "kode_ms_lama": ms_awal,
                "nama_ms_lama": nama_ms_lama,
                "id_mesin_lama": id_mesin_lama,
                "kode_ms_baru": ms_tujuan,
                "nama_ms_baru": nama_ms_baru,
                "id_mesin_baru": id_mesin_baru,
                "bank": bank,
                "rekening": rekening_no,
                "status": "diproses",
                "tanggal_submit": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "tanggal_update_status": "",
                "status": "Pengajuan",
                "user": st.session_state.nik,
            }
        )
        st.success("Saved")
# ====================
# MENU: RELOKASI MESIN
# ====================
elif menu == "Relokasi Mesin":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚚 Relokasi Mesin CDM")

    
    if "submitted_ids" not in st.session_state:
     st.session_state.submitted_ids = []

    # ======================
    # INPUT
    # ======================
    col1, col2 = st.columns(2)

    with col1:
     kode_cabang = st.text_input("Kode Cabang").upper()
     id_mesin = st.text_input("ID Mesin")

     kode_ms_lama = st.text_input("Kode MS Lama").upper()

     toko_lama = get_toko(kode_ms_lama)  # ✅ GANTI KE TOKO

     nama_ms_lama = toko_lama["nama_toko"] if toko_lama is not None else ""

     st.text_input("Nama MS Lama", value=nama_ms_lama, disabled=True)

    with col2:
     kode_ms_baru = st.text_input("Kode MS Baru").upper()  # ✅ PINDAH KE SINI

     nama_ms_baru = st.text_input("Nama MS Baru")
     cabang_ms_baru = st.text_input("Kode Cabang MS Baru")

    # ======================
    # LOOKUP CABANG → VENDOR
    # ======================
     cabang_data = get_cabang(cabang_ms_baru)
     vendor = cabang_data["vendor"] if cabang_data is not None else ""

     st.text_input("Vendor", value=vendor, disabled=True)

    # ======================
    # TAMBAHAN BARU (ALAMAT)
    # ======================
    alamat_ms_baru = st.text_area("Alamat MS Baru")
    koordinat = st.text_input("Koordinat Lat,Lon", key="add_koordinat")

    # ======================
    # SUBMIT
    # ======================
    if st.button(
        "💾 Submit Relokasi",
        disabled=id_mesin in st.session_state.submitted_ids,
        use_container_width=True
    ):

        if not id_mesin or not kode_ms_lama or not kode_ms_baru:
            st.error("Field wajib belum lengkap")
            st.stop()

        save({
            "jenis_pengajuan": "Relokasi Mesin",
            "kode_cabang": kode_cabang,
            "id_mesin": id_mesin,
            "kode_ms_lama": kode_ms_lama,
            "nama_ms_lama": nama_ms_lama,  
            "kode_ms_baru": kode_ms_baru,
            "nama_ms_baru": nama_ms_baru,
            "cabang_ms_baru": cabang_ms_baru,
            "alamat_ms_baru": alamat_ms_baru,
            "koordinat": koordinat,  
            "vendor": vendor,
            "status": "Pengajuan",
            "tanggal_submit": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "user": st.session_state.nik
        })

        st.success("✅ Relokasi berhasil disimpan")

        st.session_state.submitted_ids.append(id_mesin)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
# ==============================
# MENU: PENAMBAHAN MESIN CDM
# ==============================
elif menu == "Penambahan Mesin":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ Penambahan Mesin CDM")

    role = st.session_state.get("role", "user")

    # ======================
    # RESET FORM (kalau kamu pakai reset_form)
    # ======================
    if st.session_state.get("reset_form", False):
        for key in [
            "add_kode_cabang",
            "add_kode_toko",
            "add_nama_toko",
            "add_tipe",
            "add_alamat",
            "add_koordinat",
            "add_vendor"
        ]:
            st.session_state[key] = ""
        st.session_state.reset_form = False

    col1, col2 = st.columns(2)

    # ======================
    # KOLOM KIRI
    # ======================
    with col1:

        if role in ["admin", "regional"]:
            kode_cabang = st.text_input("Kode Cabang", key="add_kode_cabang")
            kode_cabang = kode_cabang.strip().upper()
            
        else:
            kode_cabang = st.text_input("Kode Cabang", key="add_kode_cabang").upper()
            kode_cabang = kode_cabang.strip().upper()

        kode_toko = st.text_input("Kode Toko", key="add_kode_toko").upper()
        nama_toko = st.text_input("Nama Toko", key="add_nama_toko")

    # ======================
    # KOLOM KANAN
    # ======================
    with col2:
        tipe = st.selectbox("Tipe Toko", ["R", "F"], key="add_tipe")
        koordinat = st.text_input("Koordinat Lat,Lon", key="add_koordinat")
        cabang_data = get_cabang(kode_cabang)
        vendor = cabang_data["vendor"] if cabang_data is not None else ""
        st.text_input("Vendor", value=vendor, disabled=True)

    # ======================
    # BAWAH
    # ======================
    alamat = st.text_area("Alamat", key="add_alamat")

    # ======================
    # UPLOAD FILE (WAJIB)
    # ======================
    file = st.file_uploader(
        "Upload ADS Bap Pengajuan Mesin Baru (PDF)",
        type=["pdf"]
    )

    # ======================
    # SUBMIT
    # ======================
    if st.button("💾 Submit Penambahan", use_container_width=True):

        # VALIDASI FIELD
        if not all([kode_cabang, kode_toko, nama_toko, tipe, alamat, koordinat]):
            st.error("Semua field wajib diisi")
            st.stop()

        # VALIDASI FILE
        if file is None:
            st.error("File PDF wajib diupload")
            st.stop()

        if not file.name.lower().endswith(".pdf"):
            st.error("File harus PDF")
            st.stop()

        

        # SIMPAN FILE
        folder = "uploads"
        os.makedirs(folder, exist_ok=True)

        file_path = os.path.join(folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        # SAVE DATA
        save({
            "jenis_pengajuan": "Penambahan Mesin",
            "kode_cabang": kode_cabang,
            "kode_toko": kode_toko,
            "nama_toko": nama_toko,
            "tipe": tipe,
            "alamat": alamat,
            "koordinat": koordinat,
            "vendor": vendor,
            "file": file.name,
            "status": "Pengajuan",
            "tanggal_submit": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "user": st.session_state.nik
        })

        st.success("✅ Pengajuan Penambahan Mesin berhasil disimpan")

        st.session_state.reset_form = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================
# MENU 3: MONITORING (UI UPGRADE)
# ==============================
elif menu == "Monitoring":

    # ======================
    # INIT
    # ======================
    nik_login = str(st.session_state.nik)
    role = str(st.session_state.role).strip().lower()

    df = load_data()
    df_view = filter_by_role(df, user, nik_login, role)

    if df_view.empty:
        st.info("📭 Belum ada pengajuan")
        st.stop()

    # ======================
    # KPI
    # ======================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total", len(df_view))
    col2.metric("Pengajuan", len(df_view[df_view["status"] == "Pengajuan"]))
    col3.metric("Diproses", len(df_view[df_view["status"] == "diproses"]))
    col4.metric("Done", len(df_view[df_view["status"] == "done"]))
    col5.metric("Batal", len(df_view[df_view["status"] == "Batal"]))

    st.markdown("---")

    # ======================
    # FILTER UI
    # ======================
    col1, col2 = st.columns(2)

    with col1:
        filter_status = st.selectbox(
            "Filter Status", ["Semua", "Pengajuan", "diproses", "done", "Batal"]
        )

    with col2:
        search = st.text_input("🔍 Cari Kode Toko")

    df_filtered = df_view.copy()

    # ======================
    # FILTER LOGIC
    # ======================
    if filter_status != "Semua":
        df_filtered = df_filtered[df_filtered["status"] == filter_status]

    if search:
        df_filtered = df_filtered[
            df_filtered["kode_toko"].astype(str).str.contains(search, case=False, na=False)
        ]

    column_order = {

    "CS Pindah MS": [
        "tanggal_submit","jenis_pengajuan","vendor","kode_cabang",
        "kode_toko","nama_toko","tipe","alamat",
        "kode_ms_lama","nama_ms_lama","id_mesin_lama",
        "kode_ms_baru","nama_ms_baru","id_mesin_baru",
        "bank","rekening","user","status"
    ],

    "Penambahan Mesin": [
        "tanggal_submit","jenis_pengajuan","vendor","kode_cabang",
        "kode_toko","nama_toko","tipe",
        "alamat","koordinat","file","user","status"
    ],

    "QR Toko GO": [
        "tanggal_submit","jenis_pengajuan","vendor","kode_cabang",
        "kode_toko","nama_toko","tipe",
        "alamat","kode_ms","nama_ms","id_mesin",
        "bank","rekening","tanggal_go","user","status"
    ],

    "Relokasi Mesin": [
        "tanggal_submit","jenis_pengajuan","vendor","id_mesin",
        "kode_cabang","kode_ms_lama","nama_ms_lama",
        "cabang_ms_baru","kode_ms_baru","nama_ms_baru",
        "alamat_ms_baru","koordinat","user","status"
    ]
}
    # ======================
    # EXPORT
    # ======================
    import io

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        workbook = writer.book

        header_format = workbook.add_format({
            "bold": True,
            "align": "center",
            "border": 1,
            "bg_color": "#4F81BD",
            "color": "white"
        })

        cell_format = workbook.add_format({"border": 1})
        zebra_format = workbook.add_format({"bg_color": "#F2F2F2", "border": 1})

        df_export = df_view.copy()

        if df_export.empty:
            df_export.to_excel(writer, sheet_name="Data", index=False)

        else:
            grouped = df_export.groupby("jenis_pengajuan")

            for jenis, data in grouped:

                data = data.copy()

            # hapus kolom kosong
                data = data.dropna(axis=1, how="all")
                data = data.loc[:, (data != "").any()]
                if jenis in column_order:
                    ordered_cols = [col for col in column_order[jenis] if col in data.columns]
                    remaining_cols = [col for col in data.columns if col not in ordered_cols]
                    data = data[ordered_cols + remaining_cols]

                sheet_name = str(jenis)[:31]

            # TULIS DATA NORMAL DULU
                data.to_excel(writer, sheet_name=sheet_name, index=False)

                worksheet = writer.sheets[sheet_name]

            # HEADER STYLE
                for col_num, col_name in enumerate(data.columns):
                    worksheet.write(0, col_num, col_name, header_format)

            # AUTO WIDTH
                for col_num, col in enumerate(data.columns):
                    max_len = max(
                        data[col].astype(str).map(len).max(),
                        len(col)
                    ) + 2
                    worksheet.set_column(col_num, col_num, max_len)

            # ZEBRA ROW
                for row in range(1, len(data) + 1):
                    fmt = zebra_format if row % 2 == 0 else cell_format
                    worksheet.set_row(row, cell_format=fmt)

                worksheet.freeze_panes(1, 0)
                worksheet.autofilter(0, 0, len(data), len(data.columns)-1)

    output.seek(0)
    # ======================
    # ADMIN EDIT
    # ======================
    if role == "admin":

        edited_df = st.data_editor(
            df_filtered,
            use_container_width=True,
            column_config={
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pengajuan", "diproses", "done", "Batal"],
                    required=True
                ),
                "Download": st.column_config.LinkColumn(
                    "Download",
                    display_text="📥 Download"
                )
            },
            disabled=[col for col in df_filtered.columns if col != "status"]
        )

        col_btn1, col_btn2, col_spacer = st.columns([2, 2, 6])

        with col_btn1:
            if st.button("💾 Simpan Perubahan"):
                edited_df.to_excel("data.xlsx", index=False)
                st.success("Berhasil")
                st.rerun()

        with col_btn2:
            st.download_button(
                "📥 Export Excel",
                data=output.getvalue(),
                file_name="EXPORT_CDM.xlsx",
                use_container_width=True,
            )

    else:
        st.dataframe(df_filtered, use_container_width=True)

        st.download_button(
        "📥 Export Excel",
        data=output.getvalue(),
        file_name="EXPORT_CDM.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
    st.markdown("</div>", unsafe_allow_html=True)