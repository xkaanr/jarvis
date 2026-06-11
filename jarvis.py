import speech_recognition as sr
import os
import sys
import pyautogui
import time
import webbrowser
import asyncio
import pygame
from google import genai
from google.genai import types

# 1. API ve Yapay Zeka Kurulumu
API_KEY = "BURAYA_ALDIĞIN_API_KEYI_YAZ"
client = genai.Client(api_key=API_KEY)

sistem_talimati = (
    "Sen JARVIS'sin. Kullanıcının Windows işletim sistemini yöneten dahi, çok cool ve tamamen insansı bir asistansın.\n"
    "Kullanıcı bir web sitesi açmak istediğinde cevabına MUTLAKA şu etiketi ekle: [WEB: url_adresi]\n"
    "Kullanıcı bilgisayardan bir uygulama, program veya oyun açmak istediğinde cevabına MUTLAKA şu etiketi ekle: [UYGULAMA: uygulama_adi]\n"
    "Cevapların kısa, havalı ve zekice olsun. Cümlelerinin sonunda 'efendim' kelimesini kullan."
)

# 2. Ses ve Pygame Kurulumu
pygame.mixer.init()

def insanca_konus_ve_yaz(metin):
    temiz_metin = metin
    if "[WEB:" in temiz_metin:
        temiz_metin = temiz_metin.split("]")[-1]
    if "[UYGULAMA:" in temiz_metin:
        temiz_metin = temiz_metin.split("]")[-1]
    temiz_metin = temiz_metin.strip()

    if not temiz_metin:
        return

    VOICE = "tr-TR-AhmetNeural"
    OUTPUT_FILE = "jarvis_ses.mp3"
    
    async def generate_speech():
        import edge_tts
        communicate = edge_tts.Communicate(temiz_metin, VOICE)
        await communicate.save(OUTPUT_FILE)

    try:
        asyncio.run(generate_speech())
        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"\n[SES HATASI] Oynatılamadı: {e}")

    print("\nJARVIS: ", end="", flush=True)
    for harf in temiz_metin:
        print(harf, end="", flush=True)
        time.sleep(0.04)
    print()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.music.unload()
    try:
        os.remove(OUTPUT_FILE)
    except:
        pass

def uygulama_ac(uygulama_adi):
    print(f"[SİSTEM] {uygulama_adi} aranıyor ve başlatılıyor...")
    pyautogui.press('win')
    time.sleep(0.4)
    pyautogui.write(uygulama_adi, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def komut_al(mod="normal"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if mod == "uyanma":
            print("[JARVIS Uyku Modunda... Dinleniyor...]", end="\r", flush=True)
        else:
            print("\n[Dinleniyor...] Buyrun efendim, sizi dinliyorum...")
            
        r.pause_threshold = 0.7
        r.adjust_for_ambient_noise(source, duration=0.6)
        audio = r.listen(source)
    try:
        sorgu = r.recognize_google(audio, language='tr-TR')
        return sorgu
    except Exception:
        return "none"

# --- SİSTEMİ BAŞLAT ---
insanca_konus_ve_yaz("Gelişmiş yapay zeka çekirdeği aktif edildi. Arka plan kota koruma modülleri devrede efendim.")

while True:
    # Önce sessizce uyanma kelimesini bekliyoruz
    uyandirma_isteği = komut_al(mod="uyanma")
    
    if uyandirma_isteği == "none" or uyandirma_isteği.strip() == "":
        continue
        
    # Eğer sesin içinde "jarvis" kelimesi geçerse sistem tetikleniyor
    if "jarvis" in uyandirma_isteği.lower():
        
        # Kullanıcı uyanma kelimesiyle birlikte direkt komut vermiş olabilir (Örn: "Jarvis Spotify aç")
        istek = uyandirma_isteği.lower().replace("jarvis", "").strip()
        
        # Eğer sadece "Jarvis" dediyse, ne istediğini sorması için bir sonraki cümleyi bekleyelim
        if not istek:
            insanca_konus_ve_yaz("Efendim?")
            istek = komut_al(mod="normal")
            if istek == "none" or istek.strip() == "":
                insanca_konus_ve_yaz("Sizi duyamadım efendim, uyku moduna geçiyorum.")
                continue
        
        print(f"Siz: {istek}")

        if "sistemi kapat" in istek.lower() or "çıkış" in istek.lower() or "kapat" in istek.lower():
            insanca_konus_ve_yaz("Sistemler güvenli modda kapatılıyor. İyi günler efendim.")
            break

        # ==== YAPAY ZEKA MODÜLÜ ====
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=istek,
                config=types.GenerateContentConfig(
                    system_instruction=sistem_talimati,
                    max_output_tokens=150
                )
            )
            
            cevap = response.text
            insanca_konus_ve_yaz(cevap)
            
            # ==== AKILLI ETİKET KONTROLLERİ ====
            if "[WEB:" in cevap:
                url = cevap.split("[WEB:")[1].split("]")[0].strip()
                webbrowser.get().open_new_tab(url)
                
            elif "[UYGULAMA:" in cevap:
                uyg_adi = cevap.split("[UYGULAMA:")[1].split("]")[0].strip()
                uygulama_ac(uyg_adi)

        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                insanca_konus_ve_yaz("Sorgu limit sınırına ulaştık efendim. Güvenlik protokolü gereği beni birkaç saniye dinlendirir misiniz?")
                time.sleep(5)
            elif "503" in str(e) or "UNAVAILABLE" in str(e):
                insanca_konus_ve_yaz("Sunucu yoğunluğu var efendim, lütfen tekrar deneyin.")
            else:
                print(f"Hata: {e}")
                insanca_konus_ve_yaz("İsteğinizi işlerken merkez çekirdekte bir hata oluştu efendim.")
