# 🤖 JARVIS - Sesli ve İnsansı Yapay Zeka Asistanı

Bu proje, Windows işletim sistemini tamamen sesli komutlarla kontrol etmenizi sağlayan, arkasında **Google Gemini 2.5 Flash** modelini barındıran ve kullanıcıyla tamamen insansı bir tonlamayla Türkçe konuşan gelişmiş bir kişisel asistan projesidir.

Klasik asistanların aksine, sabit `if-else` komut bloklarına bağımlı değildir. Gelişmiş entegrasyonu sayesinde bilgisayarınızda yüklü olan herhangi bir uygulamayı Windows arama algoritmasını simüle ederek akıllıca başlatabilir.

---

## ✨ Özellikler

* 🎙️ **Gelişmiş Ses Tanıma:** Google Speech Recognition altyapısı ile Türkçe ses komutlarını yüksek doğrulukla metne çevirir.
* 🧠 **Gemini Çekirdeği:** Sadece komut çalıştırmaz; sorduğunuz sorulara zeki, cool ve esprili Türkçe yanıtlar verir.
* 🗣️ **İnsansı Ses Motoru:** Robotik sesler yerine, Microsoft Edge TTS (Ahmet Canlı Ses Modeli) kullanarak doğal vurgularla konuşur.
* ⌨️ **Typewriter Efekti:** JARVIS konuşurken, terminal ekranında harfler sinematik bir şekilde akarak yazılır.
* 👁️ **Evrensel Uygulama Başlatıcı:** İçine kod yazmanıza gerek kalmadan; "Visual Studio Code aç", "Spotify aç", "Steam başlat" gibi komutlarla her uygulamayı Windows üzerinden bulur ve çalıştırır.
* 🔒 **Wake Word (Uyanma Kelimesi):** "Jarvis" kelimesini duymadığı sürece arka planda sessizce bekler, kotanızı ve bilgisayarınızı yormaz.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Gereksinimler
Sisteminizde Python 3.x sürümünün kurulu olduğundan emin olun. Ardından gerekli kütüphaneleri terminal üzerinden yükleyin:

```bash
pip install google-genai speech_recognition pyttsx3 pyautogui edge-tts pygame
