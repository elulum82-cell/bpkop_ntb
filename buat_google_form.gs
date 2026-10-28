// Membuat "Formulir IDP Prowil NTB" lengkap (semua bagian IDP) dan mencetak konfigurasi untuk aplikasi Streamlit.
// Cara pakai: script.google.com > Proyek baru > tempel file ini > pilih fungsi buatFormIDP > Jalankan > setujui izin > buka Execution log.
const SPEC = [
 {
  "type": "section",
  "t": "Identitas",
  "h": ""
 },
 {
  "k": "tahun",
  "t": "Tahun Rencana Pengembangan (IDP)",
  "type": "list",
  "req": true,
  "o": [
   "2026",
   "2027",
   "2028",
   "2029",
   "2030"
  ]
 },
 {
  "k": "nama",
  "t": "Nama Lengkap (Beserta Gelar)",
  "type": "text",
  "req": true
 },
 {
  "k": "kelas",
  "t": "Kelas",
  "type": "choice",
  "req": true,
  "o": [
   "L3",
   "L4",
   "L5"
  ]
 },
 {
  "k": "pekerjaan",
  "t": "Pekerjaan",
  "type": "list",
  "req": true,
  "o": [
   "ASN",
   "BUMN/BUMD",
   "Lembaga",
   "Swasta",
   "Wirausaha",
   "Pelajar/Mahasiswa",
   "Lainnya"
  ]
 },
 {
  "k": "jabatan",
  "t": "Jabatan",
  "type": "text",
  "req": true
 },
 {
  "k": "pangkat",
  "t": "Pangkat/Golongan",
  "type": "text",
  "req": true,
  "h": "Jika tidak ada ( Non ASN ), cukup isi \"0\""
 },
 {
  "k": "tgl",
  "t": "Tanggal Pengisian (DD-MM-YYYY)",
  "type": "text",
  "req": false
 },
 {
  "k": "email",
  "t": "Email",
  "type": "text",
  "req": true
 },
 {
  "k": "lahir",
  "t": "Tahun Lahir",
  "type": "text",
  "req": true
 },
 {
  "k": "kabkota",
  "t": "Kabupaten/Kota",
  "type": "list",
  "req": false,
  "o": [
   "Kota Mataram",
   "Kab. Lombok Barat",
   "Kab. Lombok Utara",
   "Kab. Lombok Tengah",
   "Kab. Lombok Timur",
   "Kab. Sumbawa Barat",
   "Kab. Sumbawa",
   "Kab. Dompu",
   "Kab. Bima",
   "Kota Bima"
  ]
 },
 {
  "k": "sektor",
  "t": "Sektor Pekerjaan (boleh lebih dari satu)",
  "type": "check",
  "req": true,
  "o": [
   "Public Sector",
   "Public-Private",
   "Private Sector",
   "Private-Third",
   "Third Sector",
   "Public-Third",
   "Independent & Creative Professionals"
  ]
 },
 {
  "k": "kerja",
  "t": "Instansi/Tempat Bekerja",
  "type": "text",
  "req": false
 },
 {
  "type": "section",
  "t": "1. Refleksi Produktivitas Peran",
  "h": "Nilai dampak peran selama 1 tahun terakhir (1-5). Dampak 4 atau 5 wajib disertai deskripsi peran konkret."
 },
 {
  "k": "r_I0",
  "t": "Peran Internal/Organisasi - Pembinaan & Pengembangan Talenta",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak melakukan pembinaan sama sekali",
   "2. Membina sesekali tanpa struktur atau tindak lanjut",
   "3. Membina secara rutin tetapi belum terukur dampaknya",
   "4. Pembinaan terstruktur dan terlihat peningkatan kualitas anggota",
   "5. Melahirkan kader unggul dan sistem pembinaan berkelanjutan"
  ]
 },
 {
  "k": "d_I0",
  "t": "Peran Internal/Organisasi - Pembinaan & Pengembangan Talenta: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_I1",
  "t": "Peran Internal/Organisasi - Dampak Peningkatan Kualitas/Jumlah Anggota",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak ada perubahan",
   "2. Pertumbuhan sangat kecil",
   "3. Ada pertumbuhan moderat",
   "4. Pertumbuhan signifikan & kualitas meningkat",
   "5. Pertumbuhan regeneratif & menciptakan pemimpin baru"
  ]
 },
 {
  "k": "d_I1",
  "t": "Peran Internal/Organisasi - Dampak Peningkatan Kualitas/Jumlah Anggota: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_I2",
  "t": "Peran Internal/Organisasi - Kontribusi pada Daya Dukung Keuangan",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak terlibat",
   "2. Terlibat minimal",
   "3. Mendukung sesuai tugas",
   "4. Menginisiasi penguatan keuangan",
   "5. Menciptakan model pendanaan berkelanjutan"
  ]
 },
 {
  "k": "d_I2",
  "t": "Peran Internal/Organisasi - Kontribusi pada Daya Dukung Keuangan: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_I3",
  "t": "Peran Internal/Organisasi - Stabilitas & Diversifikasi Pendanaan",
  "type": "choice",
  "req": true,
  "o": [
   "1. Bergantung pada satu sumber",
   "2. Upaya awal diversifikasi",
   "3. Ada tambahan sumber dana",
   "4. Sumber dana lebih stabil dan terencana",
   "5. Sistem finansial kokoh dan adaptif"
  ]
 },
 {
  "k": "d_I3",
  "t": "Peran Internal/Organisasi - Stabilitas & Diversifikasi Pendanaan: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_I4",
  "t": "Peran Internal/Organisasi - Optimalisasi Sumberdaya Internal",
  "type": "choice",
  "req": true,
  "o": [
   "1. Banyak sumberdaya tidak termanfaatkan",
   "2. Pemanfaatan sebagian",
   "3. Efisien sesuai kebutuhan",
   "4. Optimal dan meningkatkan produktivitas",
   "5. Menciptakan leverage tinggi & efisiensi sistemik"
  ]
 },
 {
  "k": "d_I4",
  "t": "Peran Internal/Organisasi - Optimalisasi Sumberdaya Internal: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_I5",
  "t": "Peran Internal/Organisasi - Pengembangan Jaringan Strategis",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak membangun jaringan",
   "2. Jaringan pasif",
   "3. Jaringan aktif namun terbatas",
   "4. Jaringan produktif & mendukung organisasi",
   "5. Jaringan strategis lintas sektor berdampak luas"
  ]
 },
 {
  "k": "d_I5",
  "t": "Peran Internal/Organisasi - Pengembangan Jaringan Strategis: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_U0",
  "t": "Peran Keummatan - Mainstreaming Nilai Kebenaran & Kebaikan",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak melakukan",
   "2. Sesekali dalam lingkup kecil",
   "3. Konsisten di lingkungan terbatas",
   "4. Aktif memengaruhi lingkungan lebih luas",
   "5. Menjadi rujukan nilai dan inspirasi publik"
  ]
 },
 {
  "k": "d_U0",
  "t": "Peran Keummatan - Mainstreaming Nilai Kebenaran & Kebaikan: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_U1",
  "t": "Peran Keummatan - Penyebaran Fikrah & Opini Islam",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak ada konten",
   "2. Jarang dan tidak konsisten",
   "3. Rutin tetapi audiens terbatas",
   "4. Konsisten dan memiliki pengaruh nyata",
   "5. Membentuk opini & wacana luas"
  ]
 },
 {
  "k": "d_U1",
  "t": "Peran Keummatan - Penyebaran Fikrah & Opini Islam: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_U2",
  "t": "Peran Keummatan - Kontribusi Pendidikan/Budaya Islami",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak terlibat",
   "2. Terlibat sesekali",
   "3. Rutin mendukung kegiatan",
   "4. Menggerakkan program pendidikan/budaya",
   "5. Membangun sistem/program berkelanjutan"
  ]
 },
 {
  "k": "d_U2",
  "t": "Peran Keummatan - Kontribusi Pendidikan/Budaya Islami: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_U3",
  "t": "Peran Keummatan - Peningkatan Daya Saing Lembaga Umat",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak ada kontribusi",
   "2. Kontribusi kecil",
   "3. Mendukung peningkatan kualitas",
   "4. Mendorong perbaikan manajemen/teknologi",
   "5. Menciptakan model unggulan bagi umat"
  ]
 },
 {
  "k": "d_U3",
  "t": "Peran Keummatan - Peningkatan Daya Saing Lembaga Umat: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_U4",
  "t": "Peran Keummatan - Advokasi Kepentingan Umat",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak pernah melakukan",
   "2. Dukungan normatif",
   "3. Sesekali terlibat advokasi",
   "4. Aktif memperjuangkan kepentingan umat",
   "5. Advokasi strategis dan berdampak kebijakan"
  ]
 },
 {
  "k": "d_U4",
  "t": "Peran Keummatan - Advokasi Kepentingan Umat: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_U5",
  "t": "Peran Keummatan - Membangun Persatuan & Jejaring Umat",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak berperan",
   "2. Terlibat minimal",
   "3. Aktif dalam komunitas",
   "4. Menjadi penghubung lintas kelompok",
   "5. Menjadi simpul strategis persatuan umat"
  ]
 },
 {
  "k": "d_U5",
  "t": "Peran Keummatan - Membangun Persatuan & Jejaring Umat: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_N0",
  "t": "Peran Kenegaraan - Kontribusi pada Kemandirian/Daya Saing Nasional",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak ada kontribusi",
   "2. Dukungan normatif",
   "3. Mendukung sesuai peran formal",
   "4. Inisiatif nyata memperkuat daya saing",
   "5. Kontribusi sistemik terhadap kemandirian nasional"
  ]
 },
 {
  "k": "d_N0",
  "t": "Peran Kenegaraan - Kontribusi pada Kemandirian/Daya Saing Nasional: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_N1",
  "t": "Peran Kenegaraan - Penguatan Ekonomi Nasional",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak terlibat",
   "2. Dukungan kecil",
   "3. Kontribusi sesuai peran",
   "4. Aktif mendorong kewirausahaan/ekonomi",
   "5. Menciptakan dampak ekonomi berkelanjutan"
  ]
 },
 {
  "k": "d_N1",
  "t": "Peran Kenegaraan - Penguatan Ekonomi Nasional: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_N2",
  "t": "Peran Kenegaraan - Perbaikan Tata Kelola & Pelayanan Publik",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak terlibat",
   "2. Mendukung pasif",
   "3. Berkontribusi sesuai tugas",
   "4. Menginisiasi perbaikan nyata",
   "5. Perbaikan struktural & meningkatkan trust publik"
  ]
 },
 {
  "k": "d_N2",
  "t": "Peran Kenegaraan - Perbaikan Tata Kelola & Pelayanan Publik: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_N3",
  "t": "Peran Kenegaraan - Inovasi Pelayanan Publik",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak ada inovasi",
   "2. Mendukung kecil",
   "3. Mengusulkan perbaikan",
   "4. Mengimplementasikan inovasi",
   "5. Inovasi diadopsi luas/menjadi model"
  ]
 },
 {
  "k": "d_N3",
  "t": "Peran Kenegaraan - Inovasi Pelayanan Publik: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_N4",
  "t": "Peran Kenegaraan - Aktivitas Organisasi Profesi/Pusat Keunggulan",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak aktif",
   "2. Terdaftar tanpa kontribusi",
   "3. Aktif sesuai kegiatan rutin",
   "4. Memberi kontribusi nyata",
   "5. Memegang peran strategis & memengaruhi arah organisasi"
  ]
 },
 {
  "k": "d_N4",
  "t": "Peran Kenegaraan - Aktivitas Organisasi Profesi/Pusat Keunggulan: deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "k": "r_N5",
  "t": "Peran Kenegaraan - Advokasi Kepentingan Nasional (Global)",
  "type": "choice",
  "req": true,
  "o": [
   "1. Tidak terlibat",
   "2. Terlibat minimal",
   "3. Mendukung sesuai kapasitas",
   "4. Aktif memperjuangkan kepentingan nasional",
   "5. Berperan strategis dalam memperkuat posisi Indonesia"
  ]
 },
 {
  "k": "d_N5",
  "t": "Peran Kenegaraan - Advokasi Kepentingan Nasional (Global): deskripsi peran konkret yang telah Anda lakukan",
  "type": "para",
  "req": false,
  "h": "Wajib diisi bila dampak yang dipilih 4 atau 5"
 },
 {
  "type": "section",
  "t": "2. Refleksi Kebutuhan Kompetensi (Competency Gap)",
  "h": "Gap kompetensi prioritas (2-5 kompetensi)."
 },
 {
  "k": "g0_t",
  "t": "Gap Kompetensi 1: Judul Kompetensi",
  "type": "text",
  "req": true
 },
 {
  "k": "g0_u",
  "t": "Gap Kompetensi 1: Ukuran Peningkatan",
  "type": "list",
  "req": true,
  "o": [
   "Menguasai skill teknis baru (hardskill)",
   "Menguasai skill manajerial baru (softskill)",
   "Pengetahuan baru (knowledge)",
   "Skor asesmen meningkat",
   "Menyelesaikan penugasan/pencapaian target"
  ]
 },
 {
  "k": "g0_w",
  "t": "Gap Kompetensi 1: Factor Why",
  "type": "para",
  "req": true
 },
 {
  "k": "g1_t",
  "t": "Gap Kompetensi 2: Judul Kompetensi",
  "type": "text",
  "req": true
 },
 {
  "k": "g1_u",
  "t": "Gap Kompetensi 2: Ukuran Peningkatan",
  "type": "list",
  "req": true,
  "o": [
   "Menguasai skill teknis baru (hardskill)",
   "Menguasai skill manajerial baru (softskill)",
   "Pengetahuan baru (knowledge)",
   "Skor asesmen meningkat",
   "Menyelesaikan penugasan/pencapaian target"
  ]
 },
 {
  "k": "g1_w",
  "t": "Gap Kompetensi 2: Factor Why",
  "type": "para",
  "req": true
 },
 {
  "k": "g2_t",
  "t": "Gap Kompetensi 3: Judul Kompetensi",
  "type": "text",
  "req": false
 },
 {
  "k": "g2_u",
  "t": "Gap Kompetensi 3: Ukuran Peningkatan",
  "type": "list",
  "req": false,
  "o": [
   "Menguasai skill teknis baru (hardskill)",
   "Menguasai skill manajerial baru (softskill)",
   "Pengetahuan baru (knowledge)",
   "Skor asesmen meningkat",
   "Menyelesaikan penugasan/pencapaian target"
  ]
 },
 {
  "k": "g2_w",
  "t": "Gap Kompetensi 3: Factor Why",
  "type": "para",
  "req": false
 },
 {
  "k": "g3_t",
  "t": "Gap Kompetensi 4: Judul Kompetensi",
  "type": "text",
  "req": false
 },
 {
  "k": "g3_u",
  "t": "Gap Kompetensi 4: Ukuran Peningkatan",
  "type": "list",
  "req": false,
  "o": [
   "Menguasai skill teknis baru (hardskill)",
   "Menguasai skill manajerial baru (softskill)",
   "Pengetahuan baru (knowledge)",
   "Skor asesmen meningkat",
   "Menyelesaikan penugasan/pencapaian target"
  ]
 },
 {
  "k": "g3_w",
  "t": "Gap Kompetensi 4: Factor Why",
  "type": "para",
  "req": false
 },
 {
  "k": "g4_t",
  "t": "Gap Kompetensi 5: Judul Kompetensi",
  "type": "text",
  "req": false
 },
 {
  "k": "g4_u",
  "t": "Gap Kompetensi 5: Ukuran Peningkatan",
  "type": "list",
  "req": false,
  "o": [
   "Menguasai skill teknis baru (hardskill)",
   "Menguasai skill manajerial baru (softskill)",
   "Pengetahuan baru (knowledge)",
   "Skor asesmen meningkat",
   "Menyelesaikan penugasan/pencapaian target"
  ]
 },
 {
  "k": "g4_w",
  "t": "Gap Kompetensi 5: Factor Why",
  "type": "para",
  "req": false
 },
 {
  "k": "lalu",
  "t": "Kompetensi yang telah dikembangkan 1 tahun ke belakang (maksimal 5)",
  "type": "para",
  "req": true
 },
 {
  "type": "section",
  "t": "3. Rencana Pengembangan Kompetensi",
  "h": "2-5 kompetensi."
 },
 {
  "k": "p0_t",
  "t": "Rencana Pengembangan 1: Judul Kompetensi",
  "type": "text",
  "req": true
 },
 {
  "k": "p0_s",
  "t": "Rencana Pengembangan 1: Sarana Pengembangan",
  "type": "list",
  "req": true,
  "o": [
   "Self development (baca buku, challenge pribadi)",
   "Training/pelatihan (dari kantor maupun biaya sendiri)",
   "Mentor, coach, atau konselor",
   "Penugasan/proyek",
   "Belum tahu"
  ]
 },
 {
  "k": "p0_i",
  "t": "Rencana Pengembangan 1: Indikator Kompetensi",
  "type": "para",
  "req": true
 },
 {
  "k": "p1_t",
  "t": "Rencana Pengembangan 2: Judul Kompetensi",
  "type": "text",
  "req": true
 },
 {
  "k": "p1_s",
  "t": "Rencana Pengembangan 2: Sarana Pengembangan",
  "type": "list",
  "req": true,
  "o": [
   "Self development (baca buku, challenge pribadi)",
   "Training/pelatihan (dari kantor maupun biaya sendiri)",
   "Mentor, coach, atau konselor",
   "Penugasan/proyek",
   "Belum tahu"
  ]
 },
 {
  "k": "p1_i",
  "t": "Rencana Pengembangan 2: Indikator Kompetensi",
  "type": "para",
  "req": true
 },
 {
  "k": "p2_t",
  "t": "Rencana Pengembangan 3: Judul Kompetensi",
  "type": "text",
  "req": false
 },
 {
  "k": "p2_s",
  "t": "Rencana Pengembangan 3: Sarana Pengembangan",
  "type": "list",
  "req": false,
  "o": [
   "Self development (baca buku, challenge pribadi)",
   "Training/pelatihan (dari kantor maupun biaya sendiri)",
   "Mentor, coach, atau konselor",
   "Penugasan/proyek",
   "Belum tahu"
  ]
 },
 {
  "k": "p2_i",
  "t": "Rencana Pengembangan 3: Indikator Kompetensi",
  "type": "para",
  "req": false
 },
 {
  "k": "p3_t",
  "t": "Rencana Pengembangan 4: Judul Kompetensi",
  "type": "text",
  "req": false
 },
 {
  "k": "p3_s",
  "t": "Rencana Pengembangan 4: Sarana Pengembangan",
  "type": "list",
  "req": false,
  "o": [
   "Self development (baca buku, challenge pribadi)",
   "Training/pelatihan (dari kantor maupun biaya sendiri)",
   "Mentor, coach, atau konselor",
   "Penugasan/proyek",
   "Belum tahu"
  ]
 },
 {
  "k": "p3_i",
  "t": "Rencana Pengembangan 4: Indikator Kompetensi",
  "type": "para",
  "req": false
 },
 {
  "k": "p4_t",
  "t": "Rencana Pengembangan 5: Judul Kompetensi",
  "type": "text",
  "req": false
 },
 {
  "k": "p4_s",
  "t": "Rencana Pengembangan 5: Sarana Pengembangan",
  "type": "list",
  "req": false,
  "o": [
   "Self development (baca buku, challenge pribadi)",
   "Training/pelatihan (dari kantor maupun biaya sendiri)",
   "Mentor, coach, atau konselor",
   "Penugasan/proyek",
   "Belum tahu"
  ]
 },
 {
  "k": "p4_i",
  "t": "Rencana Pengembangan 5: Indikator Kompetensi",
  "type": "para",
  "req": false
 },
 {
  "type": "section",
  "t": "4. Rencana Optimalisasi Peran",
  "h": "2-5 rencana untuk 1 tahun ke depan."
 },
 {
  "k": "o0_r",
  "t": "Rencana Optimalisasi 1: Rencana Peran",
  "type": "para",
  "req": true
 },
 {
  "k": "o0_i",
  "t": "Rencana Optimalisasi 1: Indikator Capaian",
  "type": "para",
  "req": true
 },
 {
  "k": "o0_d",
  "t": "Rencana Optimalisasi 1: Target Realisasi (DD-MM-YYYY)",
  "type": "text",
  "req": true
 },
 {
  "k": "o1_r",
  "t": "Rencana Optimalisasi 2: Rencana Peran",
  "type": "para",
  "req": true
 },
 {
  "k": "o1_i",
  "t": "Rencana Optimalisasi 2: Indikator Capaian",
  "type": "para",
  "req": true
 },
 {
  "k": "o1_d",
  "t": "Rencana Optimalisasi 2: Target Realisasi (DD-MM-YYYY)",
  "type": "text",
  "req": true
 },
 {
  "k": "o2_r",
  "t": "Rencana Optimalisasi 3: Rencana Peran",
  "type": "para",
  "req": false
 },
 {
  "k": "o2_i",
  "t": "Rencana Optimalisasi 3: Indikator Capaian",
  "type": "para",
  "req": false
 },
 {
  "k": "o2_d",
  "t": "Rencana Optimalisasi 3: Target Realisasi (DD-MM-YYYY)",
  "type": "text",
  "req": false
 },
 {
  "k": "o3_r",
  "t": "Rencana Optimalisasi 4: Rencana Peran",
  "type": "para",
  "req": false
 },
 {
  "k": "o3_i",
  "t": "Rencana Optimalisasi 4: Indikator Capaian",
  "type": "para",
  "req": false
 },
 {
  "k": "o3_d",
  "t": "Rencana Optimalisasi 4: Target Realisasi (DD-MM-YYYY)",
  "type": "text",
  "req": false
 },
 {
  "k": "o4_r",
  "t": "Rencana Optimalisasi 5: Rencana Peran",
  "type": "para",
  "req": false
 },
 {
  "k": "o4_i",
  "t": "Rencana Optimalisasi 5: Indikator Capaian",
  "type": "para",
  "req": false
 },
 {
  "k": "o4_d",
  "t": "Rencana Optimalisasi 5: Target Realisasi (DD-MM-YYYY)",
  "type": "text",
  "req": false
 },
 {
  "type": "section",
  "t": "5. Tujuan Utama, Rencana Aksi dan Waktu Pelaksanaan",
  "h": ""
 },
 {
  "k": "tujuan",
  "t": "Tujuan/Target Utama",
  "type": "para",
  "req": true,
  "h": "Contoh: menjadi kepala dinas/eselon II; menempati jabatan fungsional; menduduki jabatan direktur; mengelola usaha; kenaikan pangkat ke IV/c"
 },
 {
  "k": "kompet",
  "t": "Kompetensi/Keahlian yang diperlukan",
  "type": "para",
  "req": false,
  "h": "Mis. kompetensi manajerial, sosio kultural, teknis, skill. Boleh lebih dari satu."
 },
 {
  "k": "a0_r",
  "t": "Rencana Aksi 1",
  "type": "para",
  "req": true
 },
 {
  "k": "a0_w",
  "t": "Waktu Pelaksanaan 1",
  "type": "text",
  "req": true
 },
 {
  "k": "a1_r",
  "t": "Rencana Aksi 2",
  "type": "para",
  "req": false
 },
 {
  "k": "a1_w",
  "t": "Waktu Pelaksanaan 2",
  "type": "text",
  "req": false
 },
 {
  "k": "a2_r",
  "t": "Rencana Aksi 3",
  "type": "para",
  "req": false
 },
 {
  "k": "a2_w",
  "t": "Waktu Pelaksanaan 3",
  "type": "text",
  "req": false
 },
 {
  "k": "a3_r",
  "t": "Rencana Aksi 4",
  "type": "para",
  "req": false
 },
 {
  "k": "a3_w",
  "t": "Waktu Pelaksanaan 4",
  "type": "text",
  "req": false
 },
 {
  "k": "komit",
  "t": "Komitmen",
  "type": "check",
  "req": true,
  "o": [
   "Ya, saya berkomitmen menjalankan rencana aksi sesuai linimasa"
  ],
  "h": "Dengan ditandatangani formulir ini: (1) Saya berkomitmen menjalankan rencana aksi sesuai linimasa. (2) Mentor berkomitmen mendampingi, memfasilitasi pelaksanaan aksi, dan melakukan evaluasi secara periodik."
 },
 {
  "k": "mentor",
  "t": "Nama Mentor",
  "type": "text",
  "req": true
 }
];

function buatFormIDP() {
  const form = FormApp.create('Formulir IDP Prowil NTB');
  form.setDescription('INDIVIDUAL DEVELOPMENT PLAN');
  form.setConfirmationMessage('Terima kasih, IDP Anda sudah tercatat.');
  form.setCollectEmail(false);
  try { form.setPublished(true); } catch (e) {}
  try { form.setAcceptingResponses(true); } catch (e) {}

  const made = [];
  SPEC.forEach(q => {
    if (q.type === 'section') {
      const s = form.addSectionHeaderItem().setTitle(q.t);
      if (q.h) s.setHelpText(q.h);
      return;
    }
    let it;
    switch (q.type) {
      case 'text':   it = form.addTextItem(); break;
      case 'para':   it = form.addParagraphTextItem(); break;
      case 'choice': it = form.addMultipleChoiceItem().setChoiceValues(q.o); break;
      case 'list':   it = form.addListItem().setChoiceValues(q.o); break;
      case 'check':  it = form.addCheckboxItem().setChoiceValues(q.o); break;
    }
    it.setTitle(q.t);
    if (q.h) it.setHelpText(q.h);
    it.setRequired(!!q.req);
    made.push({ k: q.k, type: q.type, o: q.o, item: it });
  });

  // Cari ID entry tiap pertanyaan lewat tautan prefilled.
  const entries = {};
  made.forEach(m => {
    let ir;
    // m.item sudah bertipe spesifik (TextItem, ListItem, dst), jadi langsung createResponse (tanpa asXxxItem()).
    if (m.type === 'text' || m.type === 'para') ir = m.item.createResponse('x');
    else if (m.type === 'check') ir = m.item.createResponse([m.o[0]]);
    else ir = m.item.createResponse(m.o[0]);   // choice, list
    const url = form.createResponse().withItemResponse(ir).toPrefilledUrl();
    const mt = url.match(/entry\.(\d+)=/);
    entries[m.k] = mt ? 'entry.' + mt[1] : '';
  });

  const lines = ['GFORM_URL = "' + form.getPublishedUrl().replace('/viewform', '/formResponse') + '"', '', '[GFORM_ENTRIES]'];
  Object.keys(entries).forEach(k => lines.push(k + ' = "' + entries[k] + '"'));
  Logger.log('=== SALIN BLOK DI BAWAH KE .streamlit/secrets.toml ===\n' + lines.join('\n'));
  Logger.log('Tautan isi form : ' + form.getPublishedUrl());
  Logger.log('Tautan edit form: ' + form.getEditUrl());
}
