#!/bin/bash
# Python kurulumu kontrol ediliyor ve gerekirse kurulum yapılıyor (Debian/Ubuntu örneği)
if command -v python3 &>/dev/null; then
    echo "Python zaten kurulu."
else
    echo "Python bulunamadı. Kurulum başlatılıyor..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
fi 