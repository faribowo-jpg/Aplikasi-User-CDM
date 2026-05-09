import streamlit as st
import pandas as pd
import os
import base64
import io
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Aplikasi Pengajuan User CDM",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

/* GLOBAL */
.main {
    background-color: #f5f7fa;
}

/* BUTTON */
.stButton > button {
    background-color: #ED1C24;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    height: 38px;
}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
    background-color: #ED1C24 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
}

/* CARD */
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* PROFILE */
.profile-box {
    background: linear-gradient(90deg, #0057A8, #ED1C24);
    padding: 15px;
    border-radius: 12px;
    color: white;
    margin-bottom: 15px;
}

/* TABLE HEADER */
div[data-testid="stDataFrame"] div[role="columnheader"] {
    background: linear-gradient(90deg, #4facfe, #00c6ff) !important;
    color: white !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# BACKGROUND
# =========================================================
def set_bg(image_file):

    if not os.path.exists(image_file):
        return

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
        unsafe_allow_html=True
    )

# =========================================================
# SAFE
# =========================================================
def safe(x):
    return "" if pd.isna(x) else str(x)

# =========================================================
# DOWNLOAD LINK
# =========================================================
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

# =========================================================
# SESSION INIT
# =========================================================
if "login" not in st.session_state:
    st.session_state.login = False

if "menu" not in st.session_state:
    st.session_state.menu = "HOME"

# =========================================================
# BACKGROUND SWITCH
# =========================================================
if st.session_state.login:
    set_bg("background_app.jpg")
else:
    set_bg("background_login.jpg")

# =========================================================
# LOAD MASTER
# =========================================================
@st.cache_data
def load_master():

    cabang = pd.read_excel(
        "master_data.xlsx",
        sheet_name="cabang"
    )

    toko = pd.read_excel(
        "master_data.xlsx",
        sheet_name="toko"
    )

    ms = pd.read_excel(
        "master_data.xlsx",
        sheet_name="ms"
    )

    rekening = pd.read_excel(
        "master_data.xlsx",
        sheet_name="rekening"
    )

    user = pd.read_excel(
        "master_data.xlsx",
        sheet_name="user"
    )

    user["nik"] = (
        user["nik"]
        .astype(str)
        .str.strip()
        .str.lstrip("0")
    )

    return cabang, toko, ms, rekening, user

cabang, toko, ms, rekening, user = load_master()

# =========================================================
# LOOKUP
# =========================================================
def get_cabang(k):

    if not k:
        return None

    k = str(k).strip().upper()

    df = cabang.copy()

    df["kode_cabang"] = (
        df["kode_cabang"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    d = df[df["kode_cabang"] == k]

    return d.iloc[0] if not d.empty else None

def get_toko(k):

    d = toko[
        toko["kode_toko"]
        .astype(str)
        .str.upper() == str(k).upper()
    ]

    return d.iloc[0] if not d.empty else None

def get_ms(k):

    d = ms[
        ms["kode_ms"]
        .astype(str)
        .str.upper() == str(k).upper()
    ]

    return d.iloc[0] if not d.empty else None

def get_rek(k):

    d = rekening[
        rekening["kode_toko"]
        .astype(str)
        .str.upper() == str(k).upper()
    ]

    return d.iloc[0] if not d.empty else None

# =========================================================
# LOAD DATA
# =========================================================
def load_data():

    file = "data.xlsx"

    if os.path.exists(file):
        df = pd.read_excel(file)
    else:
        df = pd.DataFrame()

    if df.empty:
        return df

    required_cols = [
        "jenis_pengajuan",
        "status",
        "user"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    df["user"] = (
        df["user"]
        .fillna("")
        .astype(str)
    )

    return df

# =========================================================
# FILTER ROLE
# =========================================================
def filter_by_role(df, user_df, nik_login, role):

    # ======================
    # HANDLE EMPTY
    # ======================
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    user_df = user_df.copy()

    # ======================
    # VALIDASI USER COLUMN
    # ======================
    if "user" not in df.columns:
        df["user"] = ""

    df["user"] = (
        df["user"]
        .fillna("")
        .astype(str)
    )

    # ======================
    # NORMALIZE USER MASTER
    # ======================
    if "nik" in user_df.columns:
        user_df["nik"] = (
            user_df["nik"]
            .fillna("")
            .astype(str)
        )

    if "nik_regional" in user_df.columns:
        user_df["nik_regional"] = (
            user_df["nik_regional"]
            .fillna("")
            .astype(str)
        )

    if "regional" in user_df.columns:
        user_df["regional"] = (
            user_df["regional"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
        )

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
            user_df["nik"] == str(nik_login)
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
            .tolist()
        )

        return df[df["user"].isin(nik_list)]

    # ======================
    # REGIONAL
    # ======================
    elif role == "regional":

        user_regional = user_df[
            user_df["nik_regional"] == str(nik_login)
        ]

        nik_list = (
            user_regional["nik"]
            .astype(str)
            .tolist()
        )

        nik_list.append(str(nik_login))

        return df[df["user"].isin(nik_list)]

    # ======================
    # USER
    # ======================
    else:

        return df[
            df["user"] == str(nik_login)
        ]

# =========================================================
# SAVE DATA
# =========================================================
def save(data):

    file = "data.xlsx"

    if os.path.exists(file):

        old = pd.read_excel(file)

        new = pd.concat(
            [old, pd.DataFrame([data])],
            ignore_index=True
        )

    else:

        new = pd.DataFrame([data])

    new.to_excel(file, index=False)

# =========================================================
# LOGIN
# =========================================================
if not st.session_state.login:

    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.image("logo_alfamart.png", width=180)

        st.markdown(
            "<h2 style='color:#0057A8;'>Login Aplikasi CDM</h2>",
            unsafe_allow_html=True
        )

        nik = st.text_input("NIK")
        pw = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            nik = safe(nik).lstrip("0")

            cek = user[
                (user["nik"] == nik) &
                (user["password"] == pw)
            ]

            if not cek.empty:

                st.session_state.login = True
                st.session_state.nik = nik
                st.session_state.role = cek.iloc[0]["role"]
                st.session_state.kode_cabang = cek.iloc[0]["kode_cabang"]
                st.session_state.nama = cek.iloc[0]["nama_user"]
                st.session_state.vendor = cek.iloc[0]["vendor"]
                st.session_state.jabatan = cek.iloc[0]["jabatan"]
                st.session_state.menu = "HOME"

                st.rerun()

            else:
                st.error("Login gagal")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# =========================================================
# HEADER
# =========================================================
col1, col2 = st.columns([1,6])

with col1:
    st.image("logo_alfamart.png", width=140)

with col2:
    st.markdown(
        """
        <h1>Aplikasi Pengajuan User CDM</h1>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown(
        f"""
        <div class="profile-box">
            <h4>👤 {st.session_state.nama}</h4>
            <p>Cabang : {st.session_state.kode_cabang}</p>
            <p>Role : {st.session_state.role}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🏠 HOME", use_container_width=True):
        st.session_state.menu = "HOME"
        st.rerun()

    if st.button("📊 Monitoring", use_container_width=True):
        st.session_state.menu = "Monitoring"
        st.rerun()

    st.markdown("---")

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# =========================================================
# MENU
# =========================================================
menu = st.session_state.menu

# =========================================================
# HOME
# =========================================================
if menu == "HOME":

    st.markdown(
        f"""
        <div class="card">
            <h2>👋 Selamat Datang, {st.session_state.nama}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# MONITORING
# =========================================================
elif menu == "Monitoring":

    nik_login = str(st.session_state.nik)

    role = (
        str(st.session_state.role)
        .strip()
        .lower()
    )

    df = load_data()

    df_view = filter_by_role(
        df,
        user,
        nik_login,
        role
    )

    if df_view.empty:
        st.info("Belum ada data")
        st.stop()

    # KPI
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", len(df_view))

    col2.metric(
        "Pengajuan",
        len(
            df_view[
                df_view["status"] == "Pengajuan"
            ]
        )
    )

    col3.metric(
        "Done",
        len(
            df_view[
                df_view["status"] == "done"
            ]
        )
    )

    col4.metric(
        "Batal",
        len(
            df_view[
                df_view["status"] == "Batal"
            ]
        )
    )

    st.markdown("---")

    # FILTER
    filter_status = st.selectbox(
        "Filter Status",
        [
            "Semua",
            "Pengajuan",
            "diproses",
            "done",
            "Batal"
        ]
    )

    search = st.text_input(
        "Cari Kode Toko"
    )

    df_filtered = df_view.copy()

    if filter_status != "Semua":

        df_filtered = df_filtered[
            df_filtered["status"] == filter_status
        ]

    if search and "kode_toko" in df_filtered.columns:

        df_filtered = df_filtered[
            df_filtered["kode_toko"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # DOWNLOAD LINK
    if "file" in df_filtered.columns:

        df_filtered["Download"] = (
            df_filtered["file"]
            .apply(make_download_link)
        )

    # ADMIN EDIT
    if role == "admin":

        edited_df = st.data_editor(
            df_filtered,
            use_container_width=True,
            column_config={
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    options=[
                        "Pengajuan",
                        "diproses",
                        "done",
                        "Batal"
                    ]
                )
            },
            disabled=[
                col for col in df_filtered.columns
                if col != "status"
            ]
        )

        if st.button("💾 Simpan"):

            edited_df.to_excel(
                "data.xlsx",
                index=False
            )

            st.success("Berhasil disimpan")
            st.rerun()

    else:

        st.dataframe(
            df_filtered,
            use_container_width=True
        )

    # EXPORT
    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        df_filtered.to_excel(
            writer,
            index=False,
            sheet_name="Monitoring"
        )

    output.seek(0)

    st.download_button(
        "📥 Export Excel",
        data=output.getvalue(),
        file_name="EXPORT_CDM.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )