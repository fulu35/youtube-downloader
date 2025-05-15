#!/usr/bin/env python3
import sys
import yt_dlp
import re

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

def check_url_source(url):
    """URL'nin kaynağını kontrol eder"""
    youtube_pattern = r'(youtube\.com|youtu\.be)'
    instagram_pattern = r'(instagram\.com|instagr\.am)'
    
    if re.search(youtube_pattern, url):
        return 'youtube'
    elif re.search(instagram_pattern, url):
        return 'instagram'
    else:
        raise ValueError("Desteklenmeyen platform!")

def download_instagram_video(url):
    """Instagram videosunu indirir"""
    ydl_opts = {
        'format': '(bestvideo+bestaudio/best)[height<=720]',
        'outtmpl': '%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt',
        'extractor_args': {
            'instagram': {
                'use_api': ['no'],
                'allow_downloads': ['yes'],
                'force_direct': ['yes']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
        }
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    url = input("Lütfen video URL'sini girin (YouTube/Instagram): ").strip()
    
    try:
        platform = check_url_source(url)
    except ValueError as e:
        print(str(e))
        sys.exit(1)
        
    try:
        if platform == 'youtube':
            # Mevcut YouTube işlemleri
            info = get_audio_info(url)
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
            
        elif platform == 'instagram':
            print("Instagram videosu tespit edildi.")
            confirmation = input("İndirmeyi başlatmak için 'e' tuşlayın: ")
            if confirmation.lower() != 'e':
                print("İndirme iptal edildi.")
                sys.exit(0)
                
            download_instagram_video(url)
            print("\nİşlem tamamlandı.")
            return
            
    except Exception as e:
        print(f"{platform.capitalize()} videosu işlenirken hata oluştu:", str(e))
        sys.exit(1)

if __name__ == '__main__':
    main() 