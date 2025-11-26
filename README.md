# 🏨 Hotel Reservation System

Modern, kullanıcı dostu bir arayüz ile **otel arama**, **rezervasyon**, **ödeme**, **misafir yönetimi** ve **yorum ekleme** gibi işlemleri yapabileceğiniz **Python & SQLite tabanlı bir Otel Rezervasyon Sistemi**.

Tkinter ile modern GUI, SQLite ile güçlü veri yönetimi ve Pandas & SQLAlchemy ile dinamik veri işleme desteği sağlar.

---

## 🗂 İçindekiler
- [✨ Özellikler](#-özellikler)
- [🛠️ Kullanılan-Teknolojiler](#-kullanılan-teknolojiler)
- [📂 Proje-Yapısı](#-proje-yapısı)
- [⚙️ Kurulum](#️-kurulum)
- [🚀 Nasıl-Çalışır](#-nasıl-çalışır)
- [🧭 Kullanıcı-Akışı](#-kullanıcı-akışı)
- [📸 Ekran-Görüntüleri](#-ekran-görüntüleri)
- [🤝 Katkıda-Bulunma](#-katkıda-bulunma)
- [📄 Lisans](#-lisans)
- [📌 Geliştirme-Önerileri](#-geliştirme-önerileri)
- [⭐ Destek-Ol](#-destek-ol)

---

## ✨ Özellikler

✔ Modern Tkinter GUI (Airbnb stil tasarım)  
✔ Tarih, şehir, otel türü, fiyat filtreleme  
✔ Otel ve oda fotoğraf görüntüleme  
✔ Rezervasyon yapma ve misafir bilgisi girme  
✔ Çoklu dependent (eş, çocuk, arkadaş vb.) ekleme  
✔ Dinamik fiyat hesaplama (gece sayısı × kişi sayısı)  
✔ SQLite veritabanı ve CSV veri entegrasyonu  
✔ Rezervasyon sorgulama ve iptal etme  
✔ Kullanıcı doğrulamalı yorum & puanlama sistemi  
✔ JSON tabanlı otel fotoğraf yönetimi  

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| Python | Ana yazılım dili |
| Tkinter & ttk | GUI arayüz |
| SQLite | Veritabanı |
| SQLAlchemy & Pandas | Veri aktarımı ve tablo yönetimi |
| Pillow (PIL) | Görsel işlemleri |
| tkcalendar | Takvim / tarih seçici |
| JSON | Fotoğraf & yorum yönetimi |

---

## 📂 Proje Yapısı

```plaintext
📦 HotelReservationSystem
 ┣ 📂 data
 ┃ ┗ 📂 csv
 ┃ ┃ ┣ amenities.csv
 ┃ ┃ ┣ guests.csv
 ┃ ┃ ┣ reservations.csv
 ┃ ┃ ┗ ...
 ┣ 📂 images
 ┃ ┣ 📂 hotel_1
 ┃ ┣ 📂 hotel_2
 ┃ ┗ ...
 ┣ db_control_sql.py
 ┣ fix_tables.py
 ┣ GUI.py
 ┣ hotel_images.json
 ┣ HotelManagement.db
 ┗ README.md
```

---

## ⚙️ Kurulum

### 1️⃣ Bağımlılıkları yükleyin
```bash
pip install pandas sqlalchemy pillow tkcalendar
```

### 2️⃣ Veritabanı tablolarını oluşturun
```bash
python fix_tables.py
```

### 3️⃣ Uygulamayı başlatın
python GUI.py


## 🚀 Nasıl Çalışır?

| İşlem | Açıklama |
|-------|----------|
| Otel Arama | Tarih, otel türü, şehir, fiyat filtresi ile arama |
| Rezervasyon Yapma | Misafir & dependent bilgisi girilir |
| Ödeme Hesaplama | Gün × kişi sayısı formülüyle otomatik |
| Yorum Ekleme | TC & rezervasyon ID doğrulamasıyla |
| Rezervasyon İptal | Reservation ID & TC ile iptal |



## 🧭 Kullanıcı Akışı

flowchart TD
A[Otel Arama] --> B[Otel Seçimi]
B --> C[Misafir Bilgileri]
C --> D[Dependent Ekle]
D --> E[Ödeme ve Tamamlama]
E --> F{Rezervasyon Tamamlandı}
F --> G[Yorum Yap]
F --> H[Rezervasyon Sorgula]
F --> I[Rezervasyon İptal]


