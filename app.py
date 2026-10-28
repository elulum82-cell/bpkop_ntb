"""Form Individual Development Plan (IDP) 2026 - aplikasi Streamlit.

Jalankan:  streamlit run app.py
Kirim email membutuhkan konfigurasi SMTP (lihat README.md).
"""
import csv
import io
import json
import os
import re
import smtplib
from datetime import date, datetime
from email.message import EmailMessage
import urllib.request
from urllib.parse import quote, urlencode

import streamlit as st

DEFAULT_RECIPIENT = "el.ulum82@gmail.com"

PROVINSI = ["Luar Negeri", "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Kepulauan Riau", "Jambi",
    "Sumatera Selatan", "Bangka Belitung", "Bengkulu", "Lampung", "Banten", "DKI Jakarta", "Jawa Barat",
    "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur",
    "Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan", "Kalimantan Timur", "Kalimantan Utara",
    "Sulawesi Utara", "Gorontalo", "Sulawesi Tengah", "Sulawesi Barat", "Sulawesi Selatan", "Sulawesi Tenggara",
    "Maluku", "Maluku Utara", "Papua Barat", "Papua Barat Daya", "Papua", "Papua Tengah", "Papua Pegunungan",
    "Papua Selatan"]

SEKTOR = {
    "Public Sector": "Pekerjaan di instansi pemerintah/negara (ASN, TNI/Polri, lembaga negara).",
    "Public-Private": "Lembaga milik negara berorientasi bisnis (BUMN/BUMD) atau kemitraan pemerintah-swasta.",
    "Private Sector": "Pekerjaan yang berada pada organisasi profit dengan orientasi pasar dan hasil.",
    "Private-Third": "Lembaga yang menggabungkan orientasi bisnis dan misi sosial (social enterprise, yayasan korporasi).",
    "Third Sector": "Lembaga nirlaba/masyarakat sipil (LSM, yayasan, ormas, lembaga sosial-keagamaan).",
    "Public-Third": "Lembaga nirlaba yang dibiayai/dikelola bersama pemerintah (mis. BLU, lembaga pendidikan/kesehatan).",
    "Independent & Creative Professionals": "Freelancer, trainer, konsultan independen, content creator, seniman.",
}

# kode -> (nama dimensi, deskripsi, daftar butir)
PERAN = {
    "I": ("Peran Internal/Organisasi",
          "Peran yang dilakukan dalam lingkup internal organisasi, mendukung pengembangan dan keberlanjutan organisasi.", [
        ("Pembinaan & Pengembangan Talenta", ["Tidak melakukan pembinaan sama sekali", "Membina sesekali tanpa struktur atau tindak lanjut", "Membina secara rutin tetapi belum terukur dampaknya", "Pembinaan terstruktur dan terlihat peningkatan kualitas anggota", "Melahirkan kader unggul dan sistem pembinaan berkelanjutan"]),
        ("Dampak Peningkatan Kualitas/Jumlah Anggota", ["Tidak ada perubahan", "Pertumbuhan sangat kecil", "Ada pertumbuhan moderat", "Pertumbuhan signifikan & kualitas meningkat", "Pertumbuhan regeneratif & menciptakan pemimpin baru"]),
        ("Kontribusi pada Daya Dukung Keuangan", ["Tidak terlibat", "Terlibat minimal", "Mendukung sesuai tugas", "Menginisiasi penguatan keuangan", "Menciptakan model pendanaan berkelanjutan"]),
        ("Stabilitas & Diversifikasi Pendanaan", ["Bergantung pada satu sumber", "Upaya awal diversifikasi", "Ada tambahan sumber dana", "Sumber dana lebih stabil dan terencana", "Sistem finansial kokoh dan adaptif"]),
        ("Optimalisasi Sumberdaya Internal", ["Banyak sumberdaya tidak termanfaatkan", "Pemanfaatan sebagian", "Efisien sesuai kebutuhan", "Optimal dan meningkatkan produktivitas", "Menciptakan leverage tinggi & efisiensi sistemik"]),
        ("Pengembangan Jaringan Strategis", ["Tidak membangun jaringan", "Jaringan pasif", "Jaringan aktif namun terbatas", "Jaringan produktif & mendukung organisasi", "Jaringan strategis lintas sektor berdampak luas"]),
    ]),
    "U": ("Peran Keummatan",
          "Peran yang memberi dampak pada tumbuhnya nilai-nilai kebaikan, syiar Islam dan persatuan umat.", [
        ("Mainstreaming Nilai Kebenaran & Kebaikan", ["Tidak melakukan", "Sesekali dalam lingkup kecil", "Konsisten di lingkungan terbatas", "Aktif memengaruhi lingkungan lebih luas", "Menjadi rujukan nilai dan inspirasi publik"]),
        ("Penyebaran Fikrah & Opini Islam", ["Tidak ada konten", "Jarang dan tidak konsisten", "Rutin tetapi audiens terbatas", "Konsisten dan memiliki pengaruh nyata", "Membentuk opini & wacana luas"]),
        ("Kontribusi Pendidikan/Budaya Islami", ["Tidak terlibat", "Terlibat sesekali", "Rutin mendukung kegiatan", "Menggerakkan program pendidikan/budaya", "Membangun sistem/program berkelanjutan"]),
        ("Peningkatan Daya Saing Lembaga Umat", ["Tidak ada kontribusi", "Kontribusi kecil", "Mendukung peningkatan kualitas", "Mendorong perbaikan manajemen/teknologi", "Menciptakan model unggulan bagi umat"]),
        ("Advokasi Kepentingan Umat", ["Tidak pernah melakukan", "Dukungan normatif", "Sesekali terlibat advokasi", "Aktif memperjuangkan kepentingan umat", "Advokasi strategis dan berdampak kebijakan"]),
        ("Membangun Persatuan & Jejaring Umat", ["Tidak berperan", "Terlibat minimal", "Aktif dalam komunitas", "Menjadi penghubung lintas kelompok", "Menjadi simpul strategis persatuan umat"]),
    ]),
    "N": ("Peran Kenegaraan",
          "Peran yang dilakukan secara inklusif dan memberi dampak pada kepentingan dan pembangunan Indonesia.", [
        ("Kontribusi pada Kemandirian/Daya Saing Nasional", ["Tidak ada kontribusi", "Dukungan normatif", "Mendukung sesuai peran formal", "Inisiatif nyata memperkuat daya saing", "Kontribusi sistemik terhadap kemandirian nasional"]),
        ("Penguatan Ekonomi Nasional", ["Tidak terlibat", "Dukungan kecil", "Kontribusi sesuai peran", "Aktif mendorong kewirausahaan/ekonomi", "Menciptakan dampak ekonomi berkelanjutan"]),
        ("Perbaikan Tata Kelola & Pelayanan Publik", ["Tidak terlibat", "Mendukung pasif", "Berkontribusi sesuai tugas", "Menginisiasi perbaikan nyata", "Perbaikan struktural & meningkatkan trust publik"]),
        ("Inovasi Pelayanan Publik", ["Tidak ada inovasi", "Mendukung kecil", "Mengusulkan perbaikan", "Mengimplementasikan inovasi", "Inovasi diadopsi luas/menjadi model"]),
        ("Aktivitas Organisasi Profesi/Pusat Keunggulan", ["Tidak aktif", "Terdaftar tanpa kontribusi", "Aktif sesuai kegiatan rutin", "Memberi kontribusi nyata", "Memegang peran strategis & memengaruhi arah organisasi"]),
        ("Advokasi Kepentingan Nasional (Global)", ["Tidak terlibat", "Terlibat minimal", "Mendukung sesuai kapasitas", "Aktif memperjuangkan kepentingan nasional", "Berperan strategis dalam memperkuat posisi Indonesia"]),
    ]),
}

UKURAN = ["Menguasai skill teknis baru (hardskill)", "Menguasai skill manajerial baru (softskill)",
          "Pengetahuan baru (knowledge)", "Skor asesmen meningkat", "Menyelesaikan penugasan/pencapaian target"]
SARANA = ["Self development (baca buku, challenge pribadi)", "Training/pelatihan (dari kantor maupun biaya sendiri)",
          "Mentor, coach, atau konselor", "Penugasan/proyek", "Belum tahu"]
N_ROWS = 5
MIN_ROWS = 2

TAHUN = [2026, 2027, 2028, 2029, 2030]
KELAS = ["L3", "L4", "L5"]
PEKERJAAN = ["ASN", "BUMN/BUMD", "Lembaga", "Swasta", "Wirausaha", "Pelajar/Mahasiswa", "Lainnya"]
KABKOTA = ["Kota Mataram", "Kab. Lombok Barat", "Kab. Lombok Utara", "Kab. Lombok Tengah", "Kab. Lombok Timur",
           "Kab. Sumbawa Barat", "Kab. Sumbawa", "Kab. Dompu", "Kab. Bima", "Kota Bima"]
N_AKSI = 4
CONTOH_AKSI = [
    ("Mengikuti pelatihan kepemimpinan (sebut jenisnya, mis. PKN Tingkat III)", "Maret - Mei 2026"),
    ("Mengikuti seleksi terbuka jabatan pimpinan tinggi pratama", "Agustus 2026"),
    ("Membentuk jejaring dengan komunitas dan lembaga mitra", "Sepanjang 2026, 1x per bulan"),
    ("Menyiapkan dokumen/portofolio untuk kenaikan pangkat", "Oktober - Desember 2026"),
]
CONTOH_PERAN = {
    "I0": "Membina 5 calon pengurus lewat mentoring bulanan; 2 di antaranya kini menjadi ketua divisi.",
    "I1": "Jumlah anggota naik dari 30 menjadi 55 orang; 10 anggota baru sudah mengikuti pelatihan dasar.",
    "I2": "Menyusun proposal dukungan dana ke 3 mitra dan membuka unit layanan berbayar untuk lembaga.",
    "I3": "Menambah sumber dana dari donasi rutin, kerja sama program, dan jasa pelatihan.",
    "I4": "Memetakan aset dan SDM yang belum terpakai, lalu memanfaatkan ruang kantor untuk kelas pelatihan.",
    "I5": "Menjalin kerja sama dengan 2 kampus dan 1 dinas untuk program magang bersama.",
    "U0": "Mengisi kajian mingguan di lingkungan RT/kampus tentang akhlak dan kejujuran dalam bekerja.",
    "U1": "Menulis 2 artikel per bulan di Instagram/blog komunitas dengan jangkauan sekitar 1.500 pembaca.",
    "U2": "Menjadi panitia pesantren kilat dan mengajar kelas literasi Al-Qur'an untuk 20 anak.",
    "U3": "Membantu masjid/lembaga zakat membuat sistem pendataan donasi digital.",
    "U4": "Menyusun surat dukungan warga untuk perbaikan fasilitas ibadah di tingkat kelurahan.",
    "U5": "Menginisiasi forum silaturahmi antar komunitas pemuda masjid satu kecamatan.",
    "N0": "Ikut menyusun standar pelatihan SDM lokal untuk mendukung industri daerah.",
    "N1": "Mendampingi 15 pelaku UMKM menyusun pembukuan sederhana dan memasarkan produk secara online.",
    "N2": "Terlibat menyusun SOP layanan satu pintu dan survei kepuasan masyarakat.",
    "N3": "Mengusulkan aplikasi antrean online untuk layanan puskesmas/kantor desa.",
    "N4": "Aktif hadir di rapat bulanan asosiasi profesi dan menjadi panitia seminar tahunan.",
    "N5": "Menyampaikan masukan kebijakan dalam forum konsultasi publik tingkat provinsi.",
}
CONTOH_GAP = [
    ("Manajemen SDM", "agar bisa meningkatkan kapasitas tim dan menyiapkan suksesi pengurus"),
    ("Pengolahan data dengan Tableau", "agar bisa mengembangkan kapasitas data analysis lembaga"),
    ("Public Speaking", "agar tidak gugup saat bicara di panggung dan memperbanyak portofolio sebagai narasumber"),
    ("Penulisan proposal dan laporan program", "agar mampu menyusun proposal pendanaan secara mandiri"),
    ("Manajemen keuangan dan legal lembaga", "agar lembaga patuh regulasi dan siap diaudit"),
]
CONTOH_RENCANA = [
    ("Manajemen SDM", "Suksesi 2 posisi strategis berjalan tanpa hambatan"),
    ("Pengolahan data dengan Tableau", "Dashboard data feedback dan demografi peserta pelatihan selesai dan dipakai rutin"),
    ("Public Speaking", "2 kali menjadi narasumber dengan audiens >100 orang tanpa grogi"),
    ("Penulisan proposal dan laporan program", "2 proposal terkirim ke mitra pendanaan, minimal 1 disetujui"),
    ("Manajemen keuangan dan legal lembaga", "Legalitas lembaga lengkap dan laporan keuangan tahunan diaudit"),
]
CONTOH_OPT = [
    ("Menumbuhkan ekselensi di berbagai instansi di Indonesia",
     "1. Membantu 2 lembaga mengembangkan tim kerja\n2. Kolaborasi program dengan setiap lembaga mitra yang dibentuk"),
    ("Mengembangkan tim yang tersertifikasi untuk kebutuhan konsultasi",
     "1. Tim memiliki 4 jenis sertifikasi\n2. Ada 2 mitra kolaborasi baru dengan kebutuhan ekspert tersertifikasi"),
    ("Membangun komunitas pengembangan pemuda di kota/kabupaten saya",
     "1. Ada akun media sosial komunitas\n2. Anggota lebih dari 100 orang\n3. Kegiatan 1x per bulan"),
    ("Menjadi pembicara rutin sesuai bidang keahlian saya",
     "1. 6 kali menjadi narasumber\n2. 1 modul pelatihan terpublikasi"),
    ("Menerbitkan karya tulis/riset dari pengalaman program",
     "1. 2 artikel terbit di media atau jurnal\n2. 1 buku saku panduan"),
]


# ---------------------------------------------------------------- util
def cfg(key, default=None):
    """Baca konfigurasi dari st.secrets, lalu environment variable."""
    val = None
    try:
        if key in st.secrets:
            val = st.secrets[key]
    except Exception:
        pass
    if val in (None, ""):
        val = os.environ.get(key)
    if isinstance(val, str):
        val = val.strip()
        if not val or val.lower().startswith(("isi", "xxxx", "alamat-pengirim", "your")):
            val = None  # masih placeholder
    return default if val in (None, "") else val


KOMIT_TEXT = "Ya, saya berkomitmen menjalankan rencana aksi sesuai linimasa"


def gform_entries():
    ent = cfg("GFORM_ENTRIES") or {}
    if isinstance(ent, str):
        try:
            ent = json.loads(ent)
        except ValueError:
            ent = {}
    try:
        return {k: v for k, v in dict(ent).items() if v}
    except (TypeError, ValueError):
        return {}


def gform_ready():
    return bool(cfg("GFORM_URL") and gform_entries())


def smtp_ready():
    return bool(cfg("SMTP_USER") and cfg("SMTP_PASSWORD"))


def S(key, default=""):
    v = st.session_state.get(key, default)
    return v.strip() if isinstance(v, str) else v


def fmt_date(d):
    return d.strftime("%d-%m-%Y") if isinstance(d, (date, datetime)) else "-"


def scale_widget(code, i, title, opts, contoh):
    st.markdown(f"**{i + 1}. {title}**")
    st.radio("Dampak peran", [1, 2, 3, 4, 5], index=None, key=f"{code}{i}",
             format_func=lambda v: f"{v}. {opts[v - 1]}", label_visibility="collapsed")
    st.text_area("Deskripsikan peran konkret yang telah Anda lakukan", key=f"{code}{i}_d", height=80,
                 placeholder=f"Contoh: {contoh}", help="Wajib diisi bila dampak yang dipilih 4 atau 5.")
    st.divider()


# ---------------------------------------------------------------- validasi
def validate():
    err = []
    if not re.match(r"^\S+@\S+\.\S+$", S("email")):
        err.append("Email peserta belum valid.")
    ly = S("lahir", 0)
    if not (1930 < int(ly or 0) < 2015):
        err.append("Tahun lahir belum valid.")
    if not st.session_state.get("sektor"):
        err.append("Sektor pekerjaan belum dipilih.")
    for code, (nama, _, items) in PERAN.items():
        for i, (title, _) in enumerate(items):
            v = st.session_state.get(f"{code}{i}")
            if v is None:
                err.append(f"{nama}: '{title}' belum dinilai.")
            elif v >= 4 and not S(f"{code}{i}_d"):
                err.append(f"{nama}: '{title}' berdampak {v}, deskripsi peran wajib diisi.")
    for i in range(MIN_ROWS):
        if not (S(f"g{i}_t") and S(f"g{i}_u") and S(f"g{i}_w")):
            err.append(f"Gap kompetensi baris {i + 1} belum lengkap.")
        if not (S(f"p{i}_t") and S(f"p{i}_s") and S(f"p{i}_i")):
            err.append(f"Rencana pengembangan kompetensi baris {i + 1} belum lengkap.")
        if not (S(f"o{i}_r") and S(f"o{i}_i") and st.session_state.get(f"o{i}_d")):
            err.append(f"Rencana optimalisasi peran No {i + 1} belum lengkap.")
    if not S("lalu"):
        err.append("Kompetensi yang dikembangkan 1 tahun ke belakang belum diisi.")
    for k, label in [("nama", "Nama lengkap (beserta gelar)"), ("kelas", "Kelas"), ("pekerjaan", "Pekerjaan"), ("jabatan", "Jabatan"),
                     ("pangkat", "Pangkat/Golongan (isi 0 jika non-ASN)"), ("tujuan", "Tujuan/Target utama"),
                     ("a0_r", "Rencana Aksi 1"), ("a0_w", "Waktu Pelaksanaan 1"), ("mentor", "Nama mentor")]:
        if not S(k):
            err.append(f"{label} belum diisi.")
    if not st.session_state.get("komit"):
        err.append("Pernyataan komitmen (tab 5) belum dicentang.")
    return err


# ---------------------------------------------------------------- ringkasan
def build_summary():
    L = ["INDIVIDUAL DEVELOPMENT PLAN 2026", f"Tanggal pengisian: {fmt_date(st.session_state.get('tgl'))}",
         f"Tahun IDP: {S('tahun')}", f"Nama lengkap: {S('nama') or '-'}", f"Kelas: {S('kelas')}",
         f"Pekerjaan: {S('pekerjaan')}", f"Jabatan: {S('jabatan')}", f"Pangkat/Golongan: {S('pangkat')}", f"Email: {S('email')}", f"Tahun lahir: {S('lahir')}",
         f"Kabupaten/Kota: {S('kabkota') or '-'}",
         f"Sektor: {'; '.join(st.session_state.get('sektor', []))}", f"Instansi/tempat bekerja: {S('kerja') or '-'}"]
    for code, (nama, _, items) in PERAN.items():
        L.append(f"\n== 1. REFLEKSI PERAN: {nama.upper()} ==")
        for i, (title, opts) in enumerate(items):
            v = st.session_state.get(f"{code}{i}")
            L.append(f"- {title}: {v}. {opts[v - 1]}")
            if S(f"{code}{i}_d"):
                L.append(f"    Peran konkret: {S(f'{code}{i}_d')}")
    L.append("\n== 2. GAP KOMPETENSI PRIORITAS ==")
    for i in range(N_ROWS):
        if S(f"g{i}_t"):
            L.append(f"{i + 1}. {S(f'g{i}_t')} | {S(f'g{i}_u') or '-'} | Factor Why: {S(f'g{i}_w') or '-'}")
    L.append(f"Kompetensi yang dikembangkan 1 tahun lalu: {S('lalu')}")
    L.append("\n== 3. RENCANA PENGEMBANGAN KOMPETENSI ==")
    for i in range(N_ROWS):
        if S(f"p{i}_t"):
            L.append(f"{i + 1}. {S(f'p{i}_t')} | {S(f'p{i}_s') or '-'} | Indikator: {S(f'p{i}_i') or '-'}")
    L.append("\n== 4. RENCANA OPTIMALISASI PERAN ==")
    for i in range(N_ROWS):
        if S(f"o{i}_r"):
            L += [f"No {i + 1}", f"  Rencana peran : {S(f'o{i}_r')}", f"  Indikator     : {S(f'o{i}_i') or '-'}",
                  f"  Target        : {fmt_date(st.session_state.get(f'o{i}_d'))}"]
    L += ["\n== 5. TUJUAN UTAMA & RENCANA AKSI ==", f"Tujuan/Target utama: {S('tujuan')}",
          f"Kompetensi/keahlian yang diperlukan: {S('kompet') or '-'}"]
    for i in range(N_AKSI):
        if S(f"a{i}_r"):
            L.append(f"Aksi {i + 1}: {S(f'a{i}_r')} | Waktu: {S(f'a{i}_w') or '-'}")
    L += ["Komitmen: peserta berkomitmen menjalankan rencana aksi sesuai linimasa.",
          f"Nama mentor: {S('mentor')}"]
    return "\n".join(L)


def build_csv():
    row = {"waktu_kirim": datetime.now().isoformat(timespec="seconds"), "nama": S("nama"), "email": S("email"),
           "tahun_lahir": S("lahir"),
           "sektor": "; ".join(st.session_state.get("sektor", [])), "instansi": S("kerja"),
           "tahun_idp": S("tahun"), "kelas": S("kelas"), "pekerjaan": S("pekerjaan"), "jabatan": S("jabatan"),
           "pangkat_golongan": S("pangkat"), "tujuan_utama": S("tujuan"), "kompetensi_diperlukan": S("kompet"),
           "kabupaten_kota": S("kabkota"), "nama_mentor": S("mentor"), "komitmen": "ya" if st.session_state.get("komit") else "tidak"}
    for i in range(N_AKSI):
        row[f"aksi{i + 1}_rencana"] = S(f"a{i}_r")
        row[f"aksi{i + 1}_waktu"] = S(f"a{i}_w")
    for code, (nama, _, items) in PERAN.items():
        for i, (title, _) in enumerate(items):
            row[f"{code}{i + 1}_{title}"] = st.session_state.get(f"{code}{i}")
            row[f"{code}{i + 1}_deskripsi"] = S(f"{code}{i}_d")
    for i in range(N_ROWS):
        row.update({f"gap{i + 1}_judul": S(f"g{i}_t"), f"gap{i + 1}_ukuran": S(f"g{i}_u"), f"gap{i + 1}_why": S(f"g{i}_w"),
                    f"rencana{i + 1}_judul": S(f"p{i}_t"), f"rencana{i + 1}_sarana": S(f"p{i}_s"),
                    f"rencana{i + 1}_indikator": S(f"p{i}_i"), f"optimalisasi{i + 1}_rencana": S(f"o{i}_r"),
                    f"optimalisasi{i + 1}_indikator": S(f"o{i}_i"), f"optimalisasi{i + 1}_target": fmt_date(st.session_state.get(f"o{i}_d"))})
    row["kompetensi_tahun_lalu"] = S("lalu")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(row))
    w.writeheader()
    w.writerow(row)
    return "\ufeff" + buf.getvalue()


# ---------------------------------------------------------------- Google Form
def gform_payload():
    """Semua isian -> dict {kunci: nilai}; kunci sama dengan yang dibuat skrip Apps Script."""
    ss, out = st.session_state, {}

    def put(k, v):
        if v not in (None, "", [], "-"):
            out[k] = v

    put("tgl", fmt_date(ss.get("tgl")))
    put("tahun", str(S("tahun")))
    for k in ("nama", "kelas", "pekerjaan", "jabatan", "pangkat", "email", "kabkota", "kerja", "tujuan", "kompet",
              "lalu", "mentor"):
        put(k, S(k))
    put("lahir", str(int(S("lahir"))) if S("lahir") else "")
    put("sektor", list(ss.get("sektor", [])))
    for code, (_, _, items) in PERAN.items():
        for i, (_, opts) in enumerate(items):
            v = ss.get(f"{code}{i}")
            if v:
                put(f"r_{code}{i}", f"{v}. {opts[v - 1]}")
            put(f"d_{code}{i}", S(f"{code}{i}_d"))
    for i in range(N_ROWS):
        for k in ("g%d_t", "g%d_u", "g%d_w", "p%d_t", "p%d_s", "p%d_i", "o%d_r", "o%d_i"):
            put(k % i, S(k % i))
        put(f"o{i}_d", fmt_date(ss.get(f"o{i}_d")))
    for i in range(N_AKSI):
        put(f"a{i}_r", S(f"a{i}_r"))
        put(f"a{i}_w", S(f"a{i}_w"))
    if ss.get("komit"):
        put("komit", [KOMIT_TEXT])
    return out


def submit_gform(payload):
    """Kirim jawaban ke Google Form lewat endpoint formResponse."""
    url, entries = cfg("GFORM_URL"), gform_entries()
    pairs = []
    for k, v in payload.items():
        if k in entries:
            for item in (v if isinstance(v, list) else [v]):
                pairs.append((entries[k], item))
    pairs += [("fvv", "1"), ("pageHistory", "0")]
    req = urllib.request.Request(url, data=urlencode(pairs).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status != 200:
            raise RuntimeError(f"Google Form menjawab status {r.status}")
    return len(pairs) - 2


# ---------------------------------------------------------------- email
def send_email(summary, csv_text, cc_participant):
    host = cfg("SMTP_HOST", "smtp.gmail.com")
    port = int(cfg("SMTP_PORT", 465))
    user = cfg("SMTP_USER")
    pwd = (cfg("SMTP_PASSWORD") or "").replace(" ", "")
    to = cfg("EMAIL_TO", DEFAULT_RECIPIENT)
    if not user or not pwd:
        raise RuntimeError("Pengiriman email otomatis belum diaktifkan oleh penyelenggara.")
    msg = EmailMessage()
    msg["Subject"] = f"[IDP 2026] {S('nama') or S('email')}"
    msg["From"] = user
    msg["To"] = to
    if cc_participant:
        msg["Cc"] = S("email")
    msg["Reply-To"] = S("email")
    msg.set_content(summary)
    nm = re.sub(r"[^A-Za-z0-9_-]+", "_", S("nama") or "peserta")
    msg.add_attachment(summary.encode("utf-8"), maintype="text", subtype="plain", filename=f"IDP2026_{nm}.txt")
    msg.add_attachment(csv_text.encode("utf-8"), maintype="text", subtype="csv", filename=f"IDP2026_{nm}.csv")
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=30) as s:
            s.login(user, pwd)
            s.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=30) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)


def compose_links(summary):
    """Tautan penulisan email berisi ringkasan: Gmail web, Outlook web, dan aplikasi email bawaan (mailto)."""
    to = cfg("EMAIL_TO", DEFAULT_RECIPIENT)
    subj = f"[IDP 2026] {S('nama') or S('email')}"
    note = "\n\n(Mohon lampirkan file IDP2026.txt dan IDP2026.csv yang diunduh dari aplikasi.)"

    def body(limit):
        t = summary if len(summary) <= limit else summary[:limit] + "\n\n[... dipotong, lihat lampiran .txt ...]"
        return t + note

    web, short = quote(body(2800)), quote(body(1200))
    return {
        "to": to, "subject": subj,
        "gmail": f"https://mail.google.com/mail/?view=cm&fs=1&to={quote(to)}&su={quote(subj)}&body={web}",
        "outlook": f"https://outlook.live.com/mail/0/deeplink/compose?to={quote(to)}&subject={quote(subj)}&body={web}",
        "mailto": f"mailto:{to}?subject={quote(subj)}&body={short}",
    }


SETUP_HELP = """
**Untuk penyelenggara (sekali saja)**

*A. Kirim ke Google Form*
1. Buka https://script.google.com, buat proyek baru, tempel isi file `buat_google_form.gs`, lalu jalankan fungsi `buatFormIDP`
   (setujui izin akses).
2. Buka **Execution log**: salin blok `GFORM_URL` dan `[GFORM_ENTRIES]` ke `.streamlit/secrets.toml`.
3. Jalankan ulang aplikasi. Di Streamlit Cloud: **Settings > Secrets**.

*B. Kirim ke email (opsional)*
1. Aktifkan **Verifikasi 2 langkah** di Gmail pengirim, buat **App Password** di https://myaccount.google.com/apppasswords.
2. Isi `SMTP_USER` dan `SMTP_PASSWORD` di `secrets.toml`.
"""


# ---------------------------------------------------------------- UI
st.set_page_config(page_title="BPKOP NTB | IDP 2026", page_icon="📝", layout="centered")
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800;900&display=swap');
html, body, .stApp, .stMarkdown, label, p, li, input, textarea, button, [data-baseweb="tab"],
[data-baseweb="select"] div, [data-testid="stWidgetLabel"] { font-family: 'Poppins', system-ui, sans-serif; }
/* ikon Streamlit harus tetap memakai font ikonnya (mencegah teks "arrow_right" menumpuk) */
[data-testid="stIconMaterial"], .material-icons, .material-symbols-rounded, .material-symbols-outlined {
  font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important; }
/* sembunyikan tombol Deploy dan menu toolbar */
.stAppDeployButton, [data-testid="stAppDeployButton"], [data-testid="stToolbar"], [data-testid="stDecoration"],
#MainMenu, footer { display: none !important; visibility: hidden; }
.block-container { max-width: 880px; padding-top: 1.2rem; }
header[data-testid="stHeader"] { background: transparent; }

/* ---------- HERO ---------- */
.hero { position: relative; overflow: hidden; border-radius: 24px; padding: 44px 18px 34px; text-align: center; color: #fff;
  background: linear-gradient(135deg, #062f2d, #0f6b68, #2f8f94, #0f6b68, #062f2d); background-size: 300% 300%;
  animation: bgmove 14s ease infinite; box-shadow: 0 14px 40px rgba(6, 47, 45, .35); margin-bottom: 18px; }
.hero::after { content: ""; position: absolute; top: 0; left: -60%; width: 40%; height: 100%;
  background: linear-gradient(100deg, transparent, rgba(255,255,255,.22), transparent); transform: skewX(-20deg);
  animation: sweep 5s ease-in-out 1.6s infinite; }
.orb { position: absolute; border-radius: 50%; filter: blur(2px); opacity: .35; animation: floaty 9s ease-in-out infinite; }
.o1 { width: 140px; height: 140px; background: #7fd6d2; top: -40px; left: -30px; }
.o2 { width: 90px; height: 90px; background: #f2c14e; bottom: -25px; right: 12%; animation-delay: -3s; }
.o3 { width: 60px; height: 60px; background: #ffffff; top: 20%; right: -15px; animation-delay: -6s; }
.kicker { position: relative; z-index: 2; font-size: .8rem; letter-spacing: .35em; text-transform: uppercase; opacity: 0;
  animation: fadein 1s ease .2s forwards; }
.title { position: relative; z-index: 2; display: flex; flex-wrap: wrap; justify-content: center; gap: 0 .35em; margin: 10px 0 6px;
  font-weight: 900; line-height: 1.05; font-size: clamp(2.8rem, 12vw, 5.6rem); letter-spacing: .04em; }
.title .w { display: inline-flex; }
.title .ch { display: inline-block; opacity: 0; transform: translateY(46px) scale(.5) rotate(-8deg);
  animation: pop .8s cubic-bezier(.2, 1.5, .4, 1) forwards, glow 2.8s ease-in-out infinite alternate;
  animation-delay: calc(var(--i) * .1s + .3s), calc(var(--i) * .12s + 1.6s);
  background: linear-gradient(180deg, #ffffff 30%, #bff3ee 100%); -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; }
.rule { position: relative; z-index: 2; height: 4px; width: 0; margin: 12px auto 14px; border-radius: 9px;
  background: linear-gradient(90deg, #f2c14e, #fff, #f2c14e); animation: grow 1.2s ease 1.3s forwards; }
.subtitle { position: relative; z-index: 2; font-size: clamp(1.05rem, 3.6vw, 1.5rem); font-weight: 600; opacity: 0;
  animation: fadein 1s ease 1.6s forwards; }
.tag { position: relative; z-index: 2; margin-top: 6px; font-size: .92rem; opacity: 0; animation: fadein 1s ease 2s forwards; }
@keyframes pop { to { opacity: 1; transform: none; } }
@keyframes glow { from { filter: drop-shadow(0 0 2px rgba(255,255,255,.2)); } to { filter: drop-shadow(0 0 14px rgba(150,255,240,.85)); } }
@keyframes bgmove { 0%,100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
@keyframes sweep { 0% { left: -60%; } 55%,100% { left: 130%; } }
@keyframes floaty { 0%,100% { transform: translateY(0) translateX(0); } 50% { transform: translateY(-22px) translateX(14px); } }
@keyframes fadein { to { opacity: .95; } }
@keyframes grow { to { width: min(260px, 60%); } }
@media (prefers-reduced-motion: reduce) { .hero, .hero *, .hero::after { animation: none !important; opacity: 1 !important; transform: none !important; }
  .rule { width: 200px; } }

/* ---------- KOMPONEN ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 10px; padding: 10px 8px 14px; position: sticky; top: 3.4rem; z-index: 50;
  background: linear-gradient(180deg, rgba(244,250,249,.97) 70%, rgba(244,250,249,0)); overflow-x: auto;
  scroll-snap-type: x proximity; scrollbar-width: thin; scrollbar-color: #58a6ad transparent; }
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { height: 5px; }
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb { background: #58a6ad; border-radius: 9px; }
.stTabs [data-baseweb="tab"] { height: auto; padding: 10px 18px; border-radius: 14px; background: #fff;
  border: 1.5px solid rgba(15,107,104,.18); box-shadow: 0 2px 8px rgba(15,107,104,.08); font-weight: 600; font-size: .92rem;
  white-space: nowrap; scroll-snap-align: center; transition: transform .2s, box-shadow .2s, background .2s, border-color .2s; }
.stTabs [data-baseweb="tab"] p { font-size: .92rem; font-weight: 600; margin: 0; }
.stTabs [data-baseweb="tab"]:hover { transform: translateY(-3px); border-color: #2f8f94; box-shadow: 0 8px 18px rgba(15,107,104,.22); }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #0f6b68, #2f8f94) !important; color: #fff !important;
  border-color: transparent; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(15,107,104,.45); }
.stTabs [aria-selected="true"] p { color: #fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] { animation: fadein .5s ease; padding-top: 10px; }
h2, h3 { color: #0f6b68; font-weight: 800 !important; }
.stButton > button, .stDownloadButton > button { border-radius: 14px; font-weight: 700; padding: .6rem 1.4rem;
  transition: transform .15s, box-shadow .15s; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #0f6b68, #2f8f94); border: 0; color: #fff;
  box-shadow: 0 6px 18px rgba(15,107,104,.4); }
.stButton > button:hover, .stDownloadButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(15,107,104,.35); }
div[data-testid="stAlert"], div[data-testid="stExpander"] { border-radius: 14px; }
div[data-testid="stRadio"] label { border-radius: 10px; }
div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="textarea"] { border-radius: 10px !important; }
div[data-testid="stProgress"] > div > div > div > div { background: linear-gradient(90deg, #0f6b68, #f2c14e); }
</style>
"""


def hero_html():
    def word(text, start):
        chars = "".join(f'<span class="ch" style="--i:{start + i}">{c}</span>' for i, c in enumerate(text))
        return f'<span class="w">{chars}</span>'

    return (CSS + '<div class="hero"><div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>'
            '<div class="kicker">Formulir IDP Prowil NTB</div>'
            f'<div class="title">{word("BPKOP", 0)}{word("NTB", 5)}</div><div class="rule"></div>'
            '<div class="subtitle">Individual Development Plan 2026</div>'
            '<div class="tag">Rencanakan pengembangan kompetensi dan optimalkan peran Anda dalam 1 tahun ke depan</div></div>')


def completeness():
    """Proporsi isian wajib yang sudah terisi (untuk progress bar)."""
    ss = st.session_state
    checks = [bool(re.match(r"^\S+@\S+\.\S+$", S("email"))), bool(ss.get("lahir")), bool(ss.get("sektor")),
              bool(S("lalu"))]
    for code, (_, _, items) in PERAN.items():
        for i in range(len(items)):
            v = ss.get(f"{code}{i}")
            checks.append(v is not None and (v < 4 or bool(S(f"{code}{i}_d"))))
    for i in range(MIN_ROWS):
        checks += [bool(S(f"g{i}_t") and S(f"g{i}_u") and S(f"g{i}_w")), bool(S(f"p{i}_t") and S(f"p{i}_s") and S(f"p{i}_i")),
                   bool(S(f"o{i}_r") and S(f"o{i}_i") and ss.get(f"o{i}_d"))]
    checks += [bool(S(k)) for k in ("nama", "kelas", "pekerjaan", "jabatan", "pangkat", "tujuan", "a0_r", "a0_w", "mentor")]
    checks.append(bool(ss.get("komit")))
    return sum(checks) / len(checks)


st.markdown(hero_html(), unsafe_allow_html=True)
_pct = completeness()
st.progress(_pct, text=f"Kelengkapan isian wajib: {int(_pct * 100)}%")

tabs = st.tabs(["🏠 Identitas", "🏢 1A Internal", "🕌 1B Keummatan", "🏛️ 1C Kenegaraan",
                "🎯 2 Gap Kompetensi", "📚 3 Pengembangan", "🚀 4 Optimalisasi", "🧭 5 Tujuan & Aksi", "✉️ Kirim"])

with tabs[0]:
    st.subheader("Pengantar")
    st.write("Individual Development Plan (IDP) adalah rencana yang disusun oleh seorang anggota organisasi untuk "
             "mengidentifikasi dan merencanakan tujuan pengembangan pribadi dan profesional dalam satu tahun ke depan. "
             "Bagi organisasi, IDP membantu anggotanya menetapkan tujuan yang jelas, spesifik dan terukur yang mendukung "
             "visi dan misi organisasi.")
    st.info("**Disclaimer:** format IDP ini tidak baku, disesuaikan dengan pandangan kami mengenai peran profesional "
            "muslim di Indonesia. Anda dapat mengembangkan format sendiri atau mengadaptasi format ini sesuai kebutuhan, "
            "atau memakai format IDP lain dari kantor/komunitas.")
    st.date_input("Tanggal pengisian", value=date.today(), key="tgl", format="DD/MM/YYYY")
    st.selectbox("Tahun rencana pengembangan (IDP) *", TAHUN, index=0, key="tahun")
    st.text_input("Nama lengkap (beserta gelar) *", key="nama", placeholder="Contoh: Ahmad Fauzi, S.T., M.Si.")
    st.selectbox("Kelas *", KELAS, index=None, placeholder="Pilih kelas (L3/L4/L5)", key="kelas")
    st.selectbox("Pekerjaan *", PEKERJAAN, index=None, placeholder="-- Pilih pekerjaan --", key="pekerjaan")
    st.text_input("Jabatan *", key="jabatan", placeholder="Contoh: Kepala Seksi Perencanaan / Staf Program / Pemilik Usaha")
    st.text_input("Pangkat/Golongan *", key="pangkat", placeholder='Contoh: Penata Muda Tk. I (III/b), atau "0" jika non-ASN',
                  help='Jika tidak ada (Non ASN), cukup isi "0".')
    st.text_input("Email *", key="email", placeholder="Contoh: ahmad.fauzi@gmail.com")
    st.number_input("Tahun lahir *", min_value=1931, max_value=2014, value=None, step=1, key="lahir", format="%d", help="Contoh: 1995")
    st.selectbox("Kabupaten/Kota (Nusa Tenggara Barat)", KABKOTA, index=None, placeholder="--Pilih Kabupaten/Kota--", key="kabkota")
    st.multiselect("Sektor pekerjaan * (boleh lebih dari satu)", list(SEKTOR), key="sektor",
                   help="Sektor dibagi 6: public; public-private; private; private-third; third; public-third.")
    with st.expander("Penjelasan tiap sektor"):
        for k, v in SEKTOR.items():
            st.markdown(f"- **{k}**: {v}")
    st.text_input("Instansi/tempat bekerja", key="kerja", placeholder="Contoh: Staf Program, Yayasan Rumah Energi")
    st.markdown("""
**Cara kerja format IDP ini.** Format dirancang untuk rencana pengembangan diri **1 tahun**. Sebaiknya Anda sudah memiliki
hasil evaluasi kompetensi. Monitoring IDP juga memerlukan *support system* (mentor, atasan, circle komunitas, atau rekan
kerja yang kompeten) untuk memberi masukan, feedback dan motivasi.

1. **Refleksi Produktivitas Peran** melalui self-assessment
2. **Refleksi Kebutuhan Kompetensi** berdasarkan masukan pihak ketiga
3. **Rencana Pengembangan Kompetensi** berdasarkan bagian 1 dan 2
4. **Rencana Optimalisasi Peran** berdasarkan bagian 1 dan 3
""")

for tab, code in zip(tabs[1:4], PERAN):
    nama, desc, items = PERAN[code]
    with tab:
        st.subheader(f"1. Refleksi Produktivitas Peran ({nama})")
        st.write(desc)
        st.info("**Petunjuk:** nilai dampak peran Anda (1-5) selama **1 tahun terakhir**. Jika memilih **4 atau 5** "
                "(dampak signifikan), tuliskan peran konkret yang telah dilakukan. Aktivitas di luar pekerjaan yang "
                "berkaitan dengan 3 dimensi peran boleh dimasukkan.")
        for i, (title, opts) in enumerate(items):
            scale_widget(code, i, title, opts, CONTOH_PERAN[f"{code}{i}"])

with tabs[4]:
    st.subheader("2. Refleksi Kebutuhan Kompetensi (Competency Gap)")
    st.write("Gap kompetensi adalah kompetensi yang perlu Anda tingkatkan berdasarkan: (1) hasil asesmen; "
             "(2) masukan atasan; (3) penugasan yang belum selesai; (4) feedback dari user/customer.")
    st.info("**Petunjuk:** pilih 2-5 gap prioritas. **Judul Kompetensi**: kompetensi yang perlu ditingkatkan. "
            "**Ukuran Peningkatan**: hardskill/softskill/knowledge baru, skor asesmen, penyelesaian tugas atau "
            "pencapaian target. **Factor Why**: mengapa ini prioritas dan apa yang ingin dicapai?")
    st.caption("Contoh: Public Speaking | menguasai skill teknis baru | agar tidak gugup saat bicara di panggung dan "
               "memperbanyak portfolio sebagai narasumber.")
    for i in range(N_ROWS):
        st.markdown(f"**Gap {i + 1}** {'(wajib)' if i < MIN_ROWS else '(opsional)'}")
        st.text_input("Judul kompetensi", key=f"g{i}_t", placeholder=f"Contoh: {CONTOH_GAP[i][0]}")
        st.selectbox("Ukuran peningkatan", UKURAN, index=None, key=f"g{i}_u", placeholder="Pilih ukuran keberhasilan")
        st.text_area("Factor Why", key=f"g{i}_w", height=70, placeholder=f"Contoh: {CONTOH_GAP[i][1]}")
        st.divider()
    st.text_area("Kompetensi yang telah Anda kembangkan 1 tahun ke belakang (maksimal 5) *", key="lalu",
                 placeholder="Contoh:\n1. Manajemen proyek\n2. Analisis data dengan Excel\n3. Penulisan laporan program",
                 help="Tulis satu per baris.")

with tabs[5]:
    st.subheader("3. Rencana Pengembangan Kompetensi")
    st.info("**Petunjuk:** pilih kompetensi dari gap prioritas (bagian 2) atau tambahkan dari rencana peran (bagian 1). "
            "Tentukan **Sarana Pengembangan** dan **Indikator Kompetensi** yang ingin dicapai dalam 1 tahun. "
            "Fokus pada **2-5 kompetensi**.")
    st.caption("Contoh: Public Speaking | mencari mentor atau coach | 2 kali menjadi narasumber dengan audiens >100 "
               "orang tanpa grogi.")
    for i in range(N_ROWS):
        st.markdown(f"**Kompetensi {i + 1}** {'(wajib)' if i < MIN_ROWS else '(opsional)'}")
        st.text_input("Judul kompetensi", key=f"p{i}_t", placeholder=f"Contoh: {CONTOH_RENCANA[i][0]}")
        st.selectbox("Sarana pengembangan", SARANA, index=None, key=f"p{i}_s", placeholder="Pilih sarana")
        st.text_area("Indikator kompetensi (target 1 tahun)", key=f"p{i}_i", height=70,
                     placeholder=f"Contoh: {CONTOH_RENCANA[i][1]}")
        st.divider()

with tabs[6]:
    st.subheader("4. Rencana Optimalisasi Peran")
    st.write("Bertujuan meningkatkan produktivitas dan dampak aktivitas pada 3 dimensi peran, untuk membentuk "
             "portofolio profesional muslim yang transformatif dan berdampak signifikan.")
    st.info("**Petunjuk:** Anda tidak harus mengisi semua poin tiap dimensi. Pilih fokus utama sesuai minat dan peluang, "
            "lalu isi **2-5 rencana** untuk 1 tahun ke depan. **Rencana Peran**: gambaran peran yang ingin "
            "dikembangkan (spesifik). **Indikator Capaian**: target terukur/kuantitatif. **Target Realisasi**: "
            "batas waktu tercapainya indikator.")
    st.caption("Contoh: membangun komunitas pengembangan pemuda di Kota Jember | 1) ada akun medsos, 2) anggota >100 "
               "orang, 3) kegiatan 1x per bulan | 23-10-2026.")
    for i in range(N_ROWS):
        st.markdown(f"**Rencana No {i + 1}** {'(wajib)' if i < MIN_ROWS else '(opsional)'}")
        st.text_area("Rencana peran", key=f"o{i}_r", height=70, placeholder=f"Contoh: {CONTOH_OPT[i][0]}")
        st.text_area("Indikator capaian (bernomor, terukur)", key=f"o{i}_i", height=110,
                     placeholder=f"Contoh:\n{CONTOH_OPT[i][1]}")
        st.date_input("Target realisasi", value=None, key=f"o{i}_d", format="DD/MM/YYYY",
                      help="Pilih tanggal batas indikator tercapai, mis. 31-12-2026.")
        st.divider()

with tabs[7]:
    st.subheader("5. Tujuan Utama & Rencana Aksi")
    st.write("Bagian ini merangkum tujuan karier/pengembangan Anda dan langkah aksi beserta waktunya.")
    st.info("**Contoh tujuan/target utama:**\n"
            "- Menjadi kepala dinas/eselon II\n"
            "- Menempati jabatan fungsional utama/madya/muda/pertama\n"
            "- Menduduki jabatan direktur\n"
            "- Memiliki/mengelola usaha wiraswasta\n"
            "- Kenaikan pangkat ke IV/c, dll.")
    st.text_area("Tujuan/Target utama *", key="tujuan", height=90, placeholder="Contoh: Menjadi kepala dinas/eselon II pada tahun 2030")
    st.text_area("Kompetensi/keahlian yang diperlukan", key="kompet", height=90,
                 placeholder="Contoh: Kompetensi manajerial, sosio kultural, teknis (analisis kebijakan), public speaking",
                 help="Isikan kompetensi/keahlian yang diperlukan untuk mencapai tujuan. Boleh lebih dari satu.")
    st.markdown("#### Rencana aksi dan waktu pelaksanaan")
    st.info("**Contoh rencana aksi:** mengikuti pelatihan (sebut jenisnya); mengikuti seleksi terbuka; mencari ide bisnis; "
            "riset pasar; menyiapkan lokasi bisnis; merekrut karyawan; membentuk jejaring; membuat yayasan, koperasi, dll.")
    for i in range(N_AKSI):
        st.markdown(f"**Rencana aksi {i + 1}** {'(wajib)' if i == 0 else '(opsional)'}")
        st.text_area(f"Rencana aksi {i + 1}" + (" *" if i == 0 else ""), key=f"a{i}_r", height=70,
                     placeholder=f"Contoh: {CONTOH_AKSI[i][0]}")
        st.text_input(f"Waktu pelaksanaan {i + 1}" + (" *" if i == 0 else ""), key=f"a{i}_w",
                      placeholder=f"Contoh: {CONTOH_AKSI[i][1]}")
        st.divider()
    st.markdown("#### Komitmen & pendampingan")
    st.markdown("Dengan menandatangani formulir ini:\n1. Saya berkomitmen untuk menjalankan rencana aksi sesuai dengan linimasa.\n"
                "2. Mentor berkomitmen mendampingi dan memfasilitasi pelaksanaan aksi serta melakukan evaluasi secara periodik.")
    st.checkbox(KOMIT_TEXT + " *", key="komit")
    st.text_input("Nama mentor *", key="mentor", placeholder="Contoh: Dr. Nama Mentor, M.Si.")

with tabs[8]:
    st.subheader("Kirim IDP")
    to_email = cfg("EMAIL_TO", DEFAULT_RECIPIENT)
    dests = (["Google Form"] if gform_ready() else []) + ([f"email {to_email}"] if smtp_ready() else [])
    if dests:
        st.write("Jawaban akan dikirim ke: **" + " dan ".join(dests) + "**.")
    cc = st.checkbox("Kirim salinan ke email saya", value=True, disabled=not smtp_ready())
    if not (gform_ready() or smtp_ready()):
        st.warning("Pengiriman otomatis belum diaktifkan. Anda tetap bisa mengirim lewat aplikasi email "
                   "atau mengunduh hasilnya setelah menekan tombol di bawah.")
    if not (gform_ready() and smtp_ready()):
        with st.expander("Untuk penyelenggara: cara mengaktifkan"):
            st.markdown(SETUP_HELP)
    if st.button("Periksa & kirim", type="primary"):
        errors = validate()
        if errors:
            st.session_state.pop("_last", None)
            st.error("Mohon lengkapi dulu:")
            for e in errors:
                st.write(f"- {e}")
        else:
            summary, csv_text = build_summary(), build_csv()
            st.session_state["_last"] = (summary, csv_text)
            ok = False
            if gform_ready():
                try:
                    with st.spinner("Mengirim ke Google Form..."):
                        n = submit_gform(gform_payload())
                    st.success(f"Jawaban masuk ke Google Form ({n} isian terkirim).")
                    ok = True
                except Exception as ex:
                    st.error(f"Gagal mengirim ke Google Form: {ex}")
            if smtp_ready():
                try:
                    with st.spinner("Mengirim email..."):
                        send_email(summary, csv_text, cc)
                    st.success("IDP juga terkirim lewat email.")
                    ok = True
                except smtplib.SMTPAuthenticationError:
                    st.error("Login email pengirim ditolak. Pastikan memakai App Password Gmail (bukan password "
                             "biasa) dan verifikasi 2 langkah aktif.")
                except Exception as ex:
                    st.error(f"Email gagal terkirim: {ex}")
            if not ok:
                st.warning("Belum ada pengiriman yang berhasil. Gunakan tombol di bawah untuk mengirim manual.")
    if "_last" in st.session_state:
        summary, csv_text = st.session_state["_last"]
        L = compose_links(summary)
        st.markdown("**Kirim manual lewat email** (isi email terisi otomatis, tinggal tekan Kirim):")
        e1, e2, e3 = st.columns(3)
        e1.link_button("Gmail (browser)", L["gmail"], use_container_width=True)
        e2.link_button("Outlook (browser)", L["outlook"], use_container_width=True)
        e3.link_button("Aplikasi email", L["mailto"], use_container_width=True,
                       help="Hanya berfungsi jika komputer punya aplikasi email bawaan (Outlook/Mail).")
        st.caption(f"Tujuan: {L['to']} | Subjek: {L['subject']}. Lampirkan file .txt/.csv dari tombol unduh di bawah.")
        c1, c2 = st.columns(2)
        c1.download_button("Unduh ringkasan (.txt)", summary, file_name="IDP2026.txt", mime="text/plain")
        c2.download_button("Unduh data (.csv)", csv_text, file_name="IDP2026.csv", mime="text/csv")
        with st.expander("Lihat ringkasan"):
            st.text(summary)
