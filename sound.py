from gtts import gTTS
import os
import platform

try:
    import playsound
except ImportError:
    print("⚠️ 'playsound' modülü yok! Alternatif ses çalma yöntemi kullanılacak.")
    playsound = None
import subprocess

def randevu_sesi_oynat(name, mesaj):
    """
    Kişinin randevu hatırlatmasını sesli olarak okur.
    """
    text = f"{name}, {mesaj}"
    tts = gTTS(text=text, lang="tr")  # Türkçe seslendirme

    # 📌 Ses dosyasını kaydet
    ses_dosyasi = "hatirlatma.mp3"
    tts.save(ses_dosyasi)

    # 📌 Sesi çal
    print(f"🔊 {text}")

    if playsound:
        playsound.playsound(ses_dosyasi)
    else:
        # Alternatif olarak sistemin ses çalma komutunu çalıştır
        if platform.system() == "Windows":
            subprocess.run(["start", ses_dosyasi], shell=True)
        elif platform.system() == "Linux":
            subprocess.run(["mpg321", ses_dosyasi])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["afplay", ses_dosyasi])

    # 📌 Ses dosyasını temizle
    os.remove(ses_dosyasi)
