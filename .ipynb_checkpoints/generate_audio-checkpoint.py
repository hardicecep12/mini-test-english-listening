import os
import re
import json
import asyncio
import edge_tts

print("=== GENERATOR AUDIO (CLEAN OVERWRITE) ===")
os.makedirs("audio", exist_ok=True)
os.makedirs("temp_chunks", exist_ok=True)

# Pemetaan suara per tokoh
VOICE_MAPPING = {
    "manager": "en-US-ChristopherNeural",
    "david": "en-US-GuyNeural",
    "sarah": "en-US-JennyNeural",
    "passenger": "en-US-JennyNeural",
    "ticket clerk": "en-US-GuyNeural",
    "customer": "en-US-JennyNeural",
    "waiter": "en-US-GuyNeural",
    "professor": "en-US-EricNeural"
}

DEFAULT_VOICE = "en-US-GuyNeural"

def get_voice(speaker_name):
    name = speaker_name.lower().strip()
    for key, voice in VOICE_MAPPING.items():
        if key in name:
            return voice
    return DEFAULT_VOICE

async def generate_chunk(text, voice, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

dialogue_pattern = r'([A-Za-z\s]+?):\s*(.+?)(?=(?:[A-Za-z\s]+?:|$))'

async def main():
    with open("data_soal.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for chapter in data:
        for sub in chapter["subchapters"]:
            file_path = sub["audio_path"].replace(".wav", ".mp3")
            sub["audio_path"] = file_path
            script_text = sub.get("script", "")

            if not script_text:
                continue

            print(f"\nMemproses: {sub['sub_title']}")

            # Hapus file target lama jika sudah ada agar benar-benar fresh
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

            matches = re.findall(dialogue_pattern, script_text, flags=re.DOTALL)
            chunks = []

            if matches:
                for idx, (speaker, dialogue) in enumerate(matches):
                    voice = get_voice(speaker)
                    chunk_file = f"temp_chunks/chunk_{idx}.mp3"
                    
                    # Hapus chunk sementara jika ada sisa proses sebelumnya
                    if os.path.exists(chunk_file):
                        os.remove(chunk_file)

                    await generate_chunk(dialogue.strip(), voice, chunk_file)
                    chunks.append(chunk_file)
            else:
                chunk_file = "temp_chunks/chunk_0.mp3"
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
                await generate_chunk(script_text.strip(), DEFAULT_VOICE, chunk_file)
                chunks.append(chunk_file)

            # Tulis file audio baru (mode 'wb' menimpa total)
            with open(file_path, "wb") as outfile:
                for c in chunks:
                    if os.path.exists(c):
                        with open(c, "rb") as infile:
                            outfile.write(infile.read())
                        os.remove(c)

            print(f"  -> File berhasil ditimpa/dibuat: {file_path}")

    # Bersihkan folder sementara
    if os.path.exists("temp_chunks"):
        try:
            os.rmdir("temp_chunks")
        except Exception:
            pass

    with open("data_soal.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("\n=== SEMUA FILE AUDIO BERHASIL DIPERBARUI & DITIMPA ===")

asyncio.run(main())
