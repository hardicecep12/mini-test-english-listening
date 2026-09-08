# Mini English Listening — Streamlit

Platform latihan *listening* bahasa Inggris interaktif berbasis web lokal dengan sistem audio multi-suara dan penilaian otomatis.

---

## Fitur Utama

* **Operasional Mandiri (Offline)**: Pengerjaan soal dan pemutaran audio berjalan di komputer lokal tanpa memerlukan koneksi internet saat tes berlangsung.
* **Audio Multi-Penutur**: Karakter suara berganti secara otomatis (pria dan wanita) sesuai peran dialog pada naskah.
* **Bank Data Terpisah**: Naskah percakapan, butir pertanyaan, kunci jawaban, dan pembahasan tersimpan rapi dalam file JSON.
* **Koreksi & Pembahasan**: Penilaian jawaban instan per sub-bab yang dilengkapi pembahasan serta rekap skor akhir.

---

## Komponen Utama

* **Streamlit**: Antarmuka web interaktif untuk memutar audio, memilih jawaban, dan menampilkan rekap nilai.
* **Edge-TTS**: Generator sintesis suara (*Text-to-Speech*) untuk membuat audio percakapan MP3 dari naskah dialog.
* **JSON (`data_soal.json`)**: Tempat penyimpanan terpusat untuk bank soal dan materi pembahasan.

---

## Cara Menjalankan

* Pasang dependensi `streamlit` dan `edge-tts` melalui Anaconda Prompt atau terminal.
* Jalankan `generate_audio.py` sekali untuk membuat seluruh file audio percakapan.
* Jalankan `streamlit run app.py` untuk membuka antarmuka latihan di browser.

```bash
pip install streamlit edge-tts
python generate_audio.py
streamlit run app.py
