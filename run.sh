#!/bin/bash

# Sanal ortamı oluştur
python3 -m venv venv

# Sanal ortamı aktifleştir
source venv/bin/activate

# Gerekli paketleri yükle
pip install --upgrade pip
pip install -r requirements.txt

# Programı çalıştır
python3 main.py 

# Adımlar:
# 1. Sanal ortamı oluşturmak için: python3 -m venv venv
# 2. Sanal ortamı aktifleştirmek için: source venv/bin/activate
# 3. Gerekli paketleri yüklemek için: pip install --upgrade pip ve pip install -r requirements.txt
# 4. Programı çalıştırmak için: python3 main.py 