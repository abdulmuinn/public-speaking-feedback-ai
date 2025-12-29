🎤 AI Public Speaking Feedback App

Aplikasi pelatih public speaking berbasis AI untuk analisis suara, kecepatan bicara, filler words, grammar, dan emosi secara otomatis.

🚀 Tentang Proyek

Aplikasi ini dirancang untuk membantu pengguna meningkatkan kemampuan public speaking dengan memberikan feedback otomatis berbasis AI.
User tinggal rekam / upload audio → klik analisis → dapat skor & saran perbaikan.

Aplikasi ini menggunakan:

Whisper (OpenAI) untuk Speech-to-Text

Transformers (Hugging Face) untuk analisis emosi / sentiment

Python + Gradio untuk UI interaktif

Pydub & Scipy untuk pemrosesan audio

Matplotlib untuk visualisasi radar chart

🎯 Fitur Utama
Fitur	Deskripsi
🎙 Speech-to-Text (STT)	Mengubah rekaman suara menjadi teks otomatis
🧠 Analisis Tempo Bicara	Menghitung kecepatan bicara (WPM)
⏸ Deteksi Jeda / Pause	Mengukur jumlah jeda dan ritme berbicara
🤐 Filler Words Detection	Deteksi kata “emm, eee, anu, uh, gitu”
📝 Grammar Issue Count	Pengecekan kesalahan struktur kalimat sederhana
😄 Emotion Recognition	Deteksi emosi suara (positive/neutral/negative)
🏆 Penilaian & Leveling	Beginner / Intermediate / Professional
📊 Radar Chart	Visualisasi kekuatan & kelemahan
📈 Progress Tracking	Simpan histori skor ke CSV otomatis
📱 Responsive UI	Nyaman digunakan di HP / Laptop
🏆 Level Penilaian
Skor	Level
0 – 60	🔰 Beginner
61 – 85	⚡ Intermediate
86 – 100	🏆 Professional
🖥️ Cara Menggunakan

Buka aplikasi Hugging Face Space:
👉  https://huggingface.co/spaces/abdulmuinnn/public-speaking-feedback-ai

Upload / rekam suara (format .wav / .mp3)

Pilih bahasa output: 🇮🇩 Bahasa Indonesia / 🇺🇸 English

Klik 🚀 Analisis Sekarang

Lihat hasil, grafik, dan skor tingkat public speaking kamu!

🔧 Teknologi yang Digunakan
Python
Gradio
OpenAI Whisper
HuggingFace Transformers
Matplotlib
Pydub
Scipy

📂 Struktur Proyek
📦 ai-public-speaking
├── app.py                # Main aplikasi
├── requirements.txt      # Dependencies
├── apt.txt               # Instalasi ffmpeg
├── score_history.csv     # Data skor tersimpan otomatis
└── README.md             # Dokumentasi proyek


🙋 Tentang Pengembang

Nama: Abdul Muin
Role: AI Enthusiast
Project: Solusi AI End-to-End Public Speaking Trainer

⭐ Kontribusi & Saran

Jika kamu ingin menambahkan fitur lain seperti:

Real-time microphone analysis

Speaker diarization (siapa yang bicara)

Auto coaching / tips berbasis AI

Voice emotion scoring detail

Silakan buka issue atau hubungi saya!
