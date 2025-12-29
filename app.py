import gradio as gr
from pydub import AudioSegment
import pandas as pd
import matplotlib.pyplot as plt
import os, numpy as np
import whisper
from scipy.io import wavfile
from transformers import pipeline

theme = gr.themes.Soft(
    primary_hue="orange",
    neutral_hue="slate",
    font="Inter",
)

# === LOAD MODEL ===
model = whisper.load_model("tiny")
sentiment = pipeline("sentiment-analysis")

# === SPEECH TO TEXT ===
def speech_to_text(wav_path):
    result = model.transcribe(wav_path)
    return result["text"]

# === HITUNG TEMPO (WPM) ===
def analyze_tempo(text, duration):
    words = len(text.split())
    if duration == 0:
        return 0
    return words / (duration / 60)

# === HITUNG PAUSE JEDA ===
def analyze_pauses(wav_path):
    sr, wav = wavfile.read(wav_path)
    silence = np.sum(np.abs(wav) < 500)
    pauses = silence // (sr*0.3)
    return int(pauses)

# === HITUNG FILLER WORDS ===
def analyze_filler(text):
    filler_words = ["emm","em","eee","anu","uh","umm","kayak","gitu"]
    t = text.lower()
    return sum(t.count(w) for w in filler_words)

# === SIMPLE GRAMMAR CHECK (tanpa Java) ===
def grammar_score(text):
    sentences = text.split(".")
    errors = 0
    for s in sentences:
        if len(s.split()) > 20:
            errors += 1
        if s.strip() != "" and s[0].islower():
            errors += 1
    return errors

# === EMOTION / SENTIMENT ===
def emotion(text):
    return sentiment(text)[0]["label"]

# === SCORING SYSTEM ===
def scoring(wpm, pauses, filler, grammar):
    score = 100
    if wpm > 150: score -= 10
    if filler > 5: score -= 10
    if grammar > 5: score -= 10
    if pauses < 3: score -= 5
    return max(score, 0)

# === STORAGE SCORE ===
score_history = []


def level_category(score):
    if score <= 60:
        return "🔰 Beginner"
    elif score <= 85:
        return "⚡ Intermediate"
    else:
        return "🏆 Professional"


# === PIPELINE UTAMA ===
def full_pipeline(audio, lang):
    wav_path = "temp.wav"
    AudioSegment.from_file(audio).export(wav_path, format="wav")

    duration = AudioSegment.from_file(wav_path).duration_seconds
    text = speech_to_text(wav_path)
    wpm = analyze_tempo(text, duration)
    pauses = analyze_pauses(wav_path)
    filler = analyze_filler(text)
    grammar = grammar_score(text)
    emo = emotion(text)
    score = scoring(wpm, pauses, filler, grammar)
    
    level = level_category(score)  # <-- LEVEL dimasukkan sini

    score_history.append(score)
    save_score_to_csv(score)

    radar = plot_radar(wpm, pauses, filler, grammar, emo)

    # === OUTPUT BERDASARKAN BAHASA ===
    if lang == "🇮🇩 Bahasa Indonesia":
        feedback_output = f"""
======================
🇮🇩 LAPORAN FEEDBACK
======================
🎯 Level : {level}
📊 Skor  : {score}/100
🗣️ Transkripsi : {text}
🧠 Detail Analisis:
- Tempo bicara     : {wpm:.1f} kata/menit
- Jumlah jeda      : {pauses} kali
- Kata filler      : {filler}
- Grammar (ringkas): {grammar} kesalahan
- Emosi suara      : {emo}
"""
    else:
        feedback_output = f"""
======================
🇺🇸 FEEDBACK REPORT
======================
🎯 Level : {level}
📊 Score : {score}/100
🗣️ Transcription : {text}
🧠 Analysis Details:
- Speaking rate    : {wpm:.1f} WPM
- Pause count      : {pauses}
- Filler words     : {filler}
- Grammar issues   : {grammar}
- Detected emotion : {emo}
"""

    return feedback_output, radar




# === SIMPAN CSV ===
def save_score_to_csv(score):
    file_name = "score_history.csv"
    new_row = {"latihan_ke": len(score_history), "score": score}
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df.to_csv(file_name, index=False)

# === RADAR SCORE NORMALIZATION ===
def radar_scores(wpm, pauses, filler, grammar, emo):
    tempo_score   = max(0, min(100, (150 - abs(130 - wpm))))
    pause_score   = max(0, min(100, pauses * 10))
    filler_score  = max(0, min(100, 100 - filler * 10))
    grammar_score = max(0, min(100, 100 - grammar * 8))
    emotion_score = 80 if emo == "POSITIVE" else 60 if emo == "NEUTRAL" else 40
    return [tempo_score, pause_score, filler_score, grammar_score, emotion_score]

# === RADAR CHART ===
def plot_radar(wpm, pauses, filler, grammar, emo):
    labels = ['Tempo','Pause','Filler','Grammar','Emotion']
    scores = radar_scores(wpm, pauses, filler, grammar, emo)

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    scores += scores[:1]; angles += angles[:1]

    plt.figure(figsize=(8,8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, scores); ax.fill(angles, scores, alpha=0.25)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels)
    plt.title("Radar Chart - Public Speaking Skill Overview")
    plt.tight_layout()
    return plt

# === GRAFIK SKOR HISTORY ===
def plot_scores():
    if len(score_history) == 0:
        return "Belum ada data."
    plt.figure(figsize=(6,4))
    plt.plot(score_history, marker='o')
    return plt

# === DOWNLOAD CSV ===
def download_csv():
    return "score_history.csv" if os.path.exists("score_history.csv") else "Belum ada data."

# === UI DESIGN (FIXED & MOBILE FRIENDLY) ===
with gr.Blocks() as analysis_tab:
    gr.Markdown("""
    # 🎤 **AI Public Speaking Feedback**
    Latih kemampuan public speaking kamu dengan analisis otomatis berbasis AI 🔥
    """)

    with gr.Group():
        audio_input = gr.Audio(type="filepath", format="wav", label="🎤 Upload / Rekam Suara")
        language_choice = gr.Radio(
            ["🇮🇩 Bahasa Indonesia", "🇺🇸 English"],
            value="🇮🇩 Bahasa Indonesia",
            label="🌐 Pilih Bahasa Output"
        )
        analyze_btn = gr.Button("🚀 Analisis Sekarang", variant="primary")

    # === RESPONSIVE LAYOUT ===
    with gr.Column():  # <--- ini tadi salah indent nya
        feedback_output = gr.Textbox(
            label="📄 Feedback",
            lines=22,
            placeholder="Hasil analisis akan muncul di sini..."
        )
        radar_output = gr.Plot(label="📊 Radar Chart")

    analyze_btn.click(
        fn=full_pipeline,
        inputs=[audio_input, language_choice],
        outputs=[feedback_output, radar_output],
        show_progress=True
    )


# === TAB GRAFIK & CSV ===
with gr.Blocks() as graph_tab:
    gr.Markdown("## 📈 Grafik Skor Latihan & Download CSV")

    with gr.Row():
        score_plot_btn = gr.Button("📊 Tampilkan Grafik")
        download_btn   = gr.Button("📁 Download CSV")

    with gr.Column():  # <-- column supaya responsif
        score_plot = gr.Plot()
        csv_file   = gr.File(label="Download CSV")

    score_plot_btn.click(plot_scores, None, score_plot)
    download_btn.click(download_csv, None, csv_file)


# === RESPONSIVE MOBILE CSS ===
gr.HTML("""
<style>
.gradio-container {max-width: 900px !important; margin:auto; padding:20px;}
@media (max-width: 768px) {
    .gr-row {flex-direction: column !important;}
    textarea, input, button, .gradio-plot {width:100% !important;}
    .gradio-plot {height:300px !important;}
}
button {transition: .25s; font-weight:bold;}
button:hover {transform: scale(1.05);}
</style>
""")


# === TABBED INTERFACE + THEME ===
demo = gr.TabbedInterface(
    [analysis_tab, graph_tab],
    ["🎙️ Analisis Suara", "📈 Grafik Skor & CSV"]
)

demo.launch(theme=theme)