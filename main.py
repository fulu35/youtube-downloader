#!/usr/bin/env python3
import sys
import yt_dlp

# İndirme sırasında ilerlemeyi göstermek için progress hook fonksiyonu
def my_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total:
            percentage = downloaded / total * 100
            # İndirilen miktar ve toplam boyut MB cinsinden hesaplanıyor
            print(f"\rİndirme: {percentage:.2f}% ({downloaded // (1024*1024)} MB / {total // (1024*1024)} MB)", end="")
    elif d['status'] == 'finished':
        print("\nİndirme tamamlandı. Dönüştürülüyor...")

# Belirtilen URL'den video bilgilerini çekiyoruz (download=False)
def get_audio_info(url):
    ydl_opts = {}  # quiet seçeneğini kaldırdık
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(info)  # Çıktıyı incelemek için
        return info

# Videonun mp3 olarak indirilip dönüştürülmesini sağlıyor
def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [my_hook],
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    url = input("Lütfen YouTube video URL'sini girin: ").strip()
    try:
        info = get_audio_info(url)
    except Exception as e:
        print("Video bilgilerini çekerken hata oluştu:", str(e))
        sys.exit(1)
        
    # Yaklaşık dosya boyutunu bulmak için, video formatları içinde yalnızca ses formatı olanı seçiyoruz.
    size = None
    bestaudio = None
    for f in info.get('formats', []):
        # Ses formatı olup video bileşeni olmayan formatı seçiyoruz
        if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
            bestaudio = f
            break
    if bestaudio:
        size = bestaudio.get('filesize') or bestaudio.get('filesize_approx')
        
    if size:
        size_mb = size / (1024 * 1024)
        print(f"Yaklaşık dosya boyutu: {size_mb:.2f} MB")
    else:
        print("Dosya boyutu bilgisi mevcut değil.")
    
    confirmation = input("İndirmeyi başlatmak için 'e' tuşlayın, iptal için herhangi bir tuşa basın: ")
    if confirmation.lower() != 'e':
        print("İndirme iptal edildi.")
        sys.exit(0)
    
    download_audio(url)
    print("\nİşlem tamamlandı.")

if __name__ == '__main__':
    main() 