# helper_audio.py (yt_dlp sürümü)

import os
import uuid
import whisper
import yt_dlp

def download_audio_temp_from_youtube(url: str, output_dir="temp_audio") -> str:
    """
    YouTube videosunun sesini MP3 olarak indirir (yt_dlp ile).
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(output_dir, f"{unique_id}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': True,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            mp3_filename = f"{unique_id}.mp3"
            mp3_path = os.path.join(output_dir, mp3_filename)

            if not os.path.exists(mp3_path):
                return "HATA: MP3 dosyası oluşturulamadı."

            return mp3_path

    except Exception as e:
        return f"HATA: yt_dlp ses indirme hatası - {e}"


def transcribe_audio_whisper(path: str, lang: str = "tr") -> str:
    """
    Whisper modeli ile ses dosyasından transkript çıkarır.
    """
    try:
        model = whisper.load_model("base")  # İsteğe bağlı: "tiny", "medium", "large"
        result = model.transcribe(path, language=lang)
        return result["text"]
    except Exception as e:
        return f"HATA: Whisper transkripsiyon hatası - {e}"
