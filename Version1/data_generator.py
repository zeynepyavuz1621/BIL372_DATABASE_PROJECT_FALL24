from faker import Faker
import random
from datetime import datetime, date, time, timedelta
import csv
import os
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

# Türkçe fake data üreteci
fake = Faker('tr_TR')

class HotelDataGenerator:
    def __init__(self, num_hotels=100, num_guests=500):
        self.photos = []
        self.male_names = [
            "Ahmet", "Mehmet", "Ali", "Mustafa", "Can", "Cem", "Efe", 
            "Yusuf", "İbrahim", "Murat", "Hasan", "Hüseyin", "Ömer", "Özcan",
            "Burak", "Emre", "Kaan", "Kerem", "Tolga", "Tuncay", "Serkan", 
            "Selim", "Sinan", "Semih", "Arda", "Alp", "Baran", "Onur", "Orhan",
            "Ozan", "Eren", "Emir", "Furkan", "Berkay", "Barış", "Yasin",
            "Mert", "Erdem", "Volkan", "Gökhan", "Oğuz", "Umut", "Koray",
            "Alper", "Uğur", "Özgür", "Cihan", "Serdar", "Ercan", "Fatih",
            "Tarık", "Taner", "Kaya", "Polat", "Çağlar", "Cenk", "Erhan",
            "Taylan", "Görkem", "İlker", "Mesut", "Oğuzhan", "Oktay", "Olcay",
            "Rıza", "Samet", "Sarp", "Serhat", "Soner", "Teoman", "Turgay",
            "Ufuk", "Yağız", "Yiğit", "Zafer", "Poyraz", "Çınar", "Toprak",
            "Utku", "Berke", "Doruk", "Göktürk", "Kutay", "Atakan", "Batuhan",
            "Kuzey", "Yalın", "Aras", "Çağan", "Dağhan", "Eymen", "Güney",
            "Kaan", "Kerem", "Meriç", "Özay", "Rüzgar", "Sarp", "Şahin",
            "Tuna", "Yaman", "Ateş", "Demir", "Güneş", "Koral", "Onat",
            "Berk", "Derin", "Ediz", "Ferit", "Harun", "İnanç", "Kartal",
            "Mert", "Nedim", "Özgün", "Polat", "Rüzgar", "Sedat", "Şener",
            "Ahmet", "Mehmet", "Ali", "Mustafa", "Can", "Cem", "Deniz", "Efe", 
            "Yusuf", "İbrahim", "Murat", "Hasan", "Hüseyin", "Ömer", "Özcan",
            "Burak", "Emre", "Kaan", "Kerem", "Tolga", "Tuncay", "Serkan", 
            "Selim", "Sinan", "Semih", "Arda", "Alp", "Baran", "Onur", "Orhan",
            "Ozan", "Eren", "Emir", "Furkan", "Berkay", "Barış", "Yasin",
            "Mert", "Erdem", "Volkan", "Gökhan", "Oğuz", "Umut", "Koray",
            "Alper", "Uğur", "Özgür", "Cihan", "Serdar", "Ercan", "Fatih",
            "Tarık", "Taner", "Kaya", "Polat", "Çağlar", "Cenk", "Erhan",
            "Taylan", "Görkem", "İlker", "Mesut", "Oğuzhan", "Oktay", "Olcay",
            "Rıza", "Samet", "Sarp", "Serhat", "Soner", "Teoman", "Turgay",
            "Ufuk", "Yağız", "Yiğit", "Zafer", "Poyraz", "Çınar", "Toprak",
            "Utku", "Berke", "Doruk", "Göktürk", "Kutay", "Atakan", "Batuhan",
            "Deniz","Ege", "Çağlar", "Doruk", "Kaya",
            "Yücel",  "Erdem", "Aydın", "Barış", "Evren",
            "Fırat", "Harun", "İlkay", "Okan", "Özgün", "Poyraz", "Rüzgar"
            
        ]
            
        self.female_names = [
            "Ayşe", "Fatma", "Emine", "Hatice", "Zeynep", "Elif", "Defne",
            "Merve", "Selin", "Özge", "Ebru", "Büşra", "Esra", "Zehra", 
            "Derya", "Sevgi", "Yağmur", "İrem", "Aslı", "Özlem", "Yasemin",
            "Seda", "Şeyma", "Melis", "Dilan", "Eylül", "Ela", "Azra", "Ecrin",
            "Nil", "Naz", "Damla", "Dilara", "Sude", "Berfin", "Beyza", "Buse",
            "Ceren", "Deren", "Ece", "Ekin", "Elvan", "Fulya", "Gamze", "Gizem",
            "Gözde", "Gül", "Hande", "Hazal", "Hilal", "Ipek", "Kübra", "Melisa",
            "Melike", "Meltem", "Nihan", "Nur", "Pelin", "Pınar", "Selin", "Simge",
            "Şimal", "Tuba", "Tuğba", "Tuğçe", "Yaren", "Yasmin", "Zara", "Mina",
            "Ada", "Asya", "Duru", "Lina", "Maya", "Mira", "Nehir", "Su", "Lara",
            "İdil", "Irmak", "Nisa", "Aylin", "Cansu", "Cemre", "Çağla", "Duygu",
            "Aslı", "Başak", "Canan", "Deniz", "Eda", "Figen", "Gülşen", "Hale",
            "İlayda", "Jale", "Kader", "Leyla", "Mine", "Nalan", "Oya", "Perihan",
            "Rüya", "Selma", "Şule", "Tülin", "Ülkü", "Vildan", "Yıldız", "Zeliha",
            "Acelya", "Begüm", "Ceyda", "Didem", "Ecesu", "Feyza", "Gökçe", "Helin",
            "Ayşe", "Fatma", "Emine", "Hatice", "Zeynep", "Elif", "Defne",
            "Merve", "Selin", "Özge", "Ebru", "Büşra", "Esra", "Zehra", 
            "Derya", "Sevgi", "Yağmur", "İrem", "Aslı", "Özlem", "Yasemin",
            "Seda", "Şeyma", "Melis", "Dilan", "Eylül", "Ela", "Azra", "Ecrin",
            "Nil", "Naz", "Damla", "Dilara", "Sude", "Berfin", "Beyza", "Buse",
            "Ceren", "Deren", "Ece", "Ekin", "Elvan", "Fulya", "Gamze", "Gizem",
            "Gözde", "Gül", "Hande", "Hazal", "Hilal", "Ipek", "Kübra", "Melisa",
            "Melike", "Meltem", "Nihan", "Nur", "Pelin", "Pınar", "Selin", "Simge",
            "Şimal", "Tuba", "Tuğba", "Tuğçe", "Yaren", "Yasmin", "Zara", "Mina",
            "Ada", "Asya", "Duru", "Lina", "Maya", "Mira", "Nehir", "Su", "Lara",
            "İdil", "Irmak", "Nisa", "Aylin", "Cansu", "Cemre", "Çağla", "Duygu",
            "Deniz", "Özge", "Ege", "Çağlar", "Bilge", "Doruk", "Güneş", 
            "Arzu", "İlke", "Derya", "Evren","Mercan", "Özgün"
        ]
            
            
        self.last_names = [
            # Genel soyadları
            "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım",
            "Öztürk", "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç", "Aslan",
            "Çetin", "Eren", "Güneş", "Kurt", "Özkan", "Koç", "Karahan", "Acar",
            "Tekin", "Alkan", "Bulut", "Gül", "Taş", "Aksoy", "Aydoğan", "Ateş",
            "Akbaş", "Akgül", "Akman", "Aksu", "Aktaş", "Akyüz", "Alkan", "Alp",
            "Alparslan", "Altın", "Altınbaş", "Arı", "Aslan", "Atalay", "Avan",
            "Avcı", "Ayhan", "Bağcı", "Bakır", "Bal", "Balcı", "Baran", "Başaran",
            "Bayrak", "Bayram", "Berber", "Bezci", "Bilgin", "Bilen", "Bilir",
            "Bodur", "Bozdemir", "Bozkurt", "Budak", "Bulut", "Candan", "Caner",
            "Cankar", "Cansever", "Cansız", "Cantürk", "Cesur", "Ceylan", "Çakır",
            "Çakmak", "Çalışkan", "Çam", "Çatal", "Çeken", "Çelik", "Çetin",
            "Çetiner", "Çınar", "Çiçek", "Çiftçi", "Çoban", "Dağ", "Dağlı",
            "Damar", "Davut", "Dede", "Demir", "Demirbaş", "Demirci", "Demirel",
            "Demirtaş", "Deniz", "Derin", "Dinç", "Dinçer", "Doğan", "Doğru",
            "Duran", "Durmuş", "Dursun", "Durmaz", "Ege", "Eker", "Ekici", "Ekin",
            "Ekinci", "Elmas", "Emre", "Erdem", "Erdoğan", "Eren", "Ergün", "Erkan",
            "Eroğlu", "Ersoy", "Ertekin", "Ertürk", "Eyüboğlu", "Ezgi", "Filiz",
            "Gedik", "Gezer", "Gök", "Göker", "Gökmen", "Göksu", "Göktan", "Göktaş",
            "Göktepe", "Gül", "Güler", "Güleç", "Gültekin", "Gümüş", "Gün", "Günay",
            "Gündoğdu", "Gündüz", "Güner", "Güneş", "Güney", "Günhan", "Gürkan",
            "Gürsoy", "Güven", "Güzel", "Işık", "İlhan", "İnan", "İnce", "Kahraman",
            "Kalaycı", "Kandemir", "Kara", "Karabaş", "Karabıyık", "Karaca",
            "Karadağ", "Karadeniz", "Karaduman", "Karakaş", "Karaman", "Karatay",
            "Karlı", "Kaya", "Kayaalp", "Kayabaşı", "Kayhan", "Kaynak", "Kazan",
            "Keskin", "Kılıç", "Kılınç", "Kınay", "Kıran", "Kırat", "Kırca",
            "Kırdar", "Kırıcı", "Kırlı", "Kırman", "Koç", "Korkmaz", "Korkut",
            "Koyuncu", "Köse", "Köylü", "Kulaç", "Kulaksız", "Kurt", "Kurtuluş",
            "Kurucu", "Kutlu", "Kutlu", "Kuzu", "Maden", "Maraşlı", "Memiş",
            "Mert", "Metin", "Murat", "Mutlu", "Müjde", "Namlı", "Nazlı", "Ocak",
            "Odabaşı", "Oğuz", "Okay", "Okur", "Olgun", "Onur", "Orhan", "Orhon",
            "Öcal", "Öğüt", "Önder", "Öner", "Öz", "Özak", "Özal", "Özay",
            "Özcan", "Özçelik", "Özdemir", "Özen", "Özer", "Özgür", "Özkan",
            "Özmen", "Öztürk", "Özyurt", "Pala", "Parlak", "Pekcan", "Peker",
            "Pekkan", "Polat", "Sağlam", "Şahin", "Şahiner", "Şanlı", "Şeker",
            "Şen", "Şener", "Şengül", "Şenol", "Şentürk", "Şimşek", "Taner",
            "Tanrıverdi", "Tarhan", "Taş", "Taşçı", "Taşkın", "Teker", "Tekin",
            "Temel", "Temiz", "Terzi", "Tilki", "Timur", "Toker", "Tokgöz",
            "Tolan", "Topak", "Topal", "Topaloğlu", "Topçu", "Toprak", "Tuna",
            "Tunalı", "Tuncer", "Turan", "Turhan", "Tüfekçi", "Türk", "Türker",
            "Türkmen", "Türkoğlu", "Uçar", "Uğur", "Uğurlu", "Ulu", "Ulucan",
            "Uluer", "Ulusoy", "Umut", "Uyar", "Uysal", "Uzun", "Ünal", "Ünlü",
            "Ünsal", "Ünver", "Üstün", "Varol", "Vural", "Yalçın", "Yaldız",
            "Yalın", "Yaman", "Yanık", "Yavuz", "Yazıcı", "Yener", "Yeniçeri",
            "Yeşil", "Yeşilbaş", "Yıldırım", "Yıldız", "Yılmaz", "Yiğit",
            "Yiğiter", "Yolcu", "Yörük", "Yüce", "Yücel", "Yüksel", "Yurt",
            "Yurtsever", "Zafer", "Zengin"
        ]
        self.num_hotels = num_hotels
        self.num_guests = num_guests
        self.hotels = []
        self.amenities = []
        self.photos = []
        self.guests = []
        self.dependents = []
        self.rooms = []
        self.payments = []
        self.reservations = []
        self.comments = []
        self.used_tc_numbers = set()
        
        # Tutarlı kullanıcı profilleri için cache
        self.guest_profiles = {}
        
        # Özellik bazlı yorum şablonları
        self.feature_based_comments = {
            'has_wifi': {
                'pos': [
                    "Wi-Fi hızlı ve kesintisiz çalışıyor.",
                    "İnternet bağlantısı tüm alanlarda güçlü.",
                    "Ücretsiz Wi-Fi tüm odalarda mevcut.",
                    "Online işlemlerim için internet hızı yeterliydi.",
                    "Wi-Fi kapsama alanı çok iyi."
                ],
                'neg': [
                    "Wi-Fi bağlantısı çok yavaş.",
                    "İnternet sürekli kesiliyor.",
                    "Odalarda Wi-Fi çekmiyor.",
                    "İnternet hızı yetersiz.",
                    "Wi-Fi şifresi sürekli değişiyor ve almak zor."
                ]
            },
            'has_pool': {
                'pos': [
                    "Havuz geniş ve temiz.",
                    "Havuz başı servisi mükemmel.",
                    "Çocuk havuzu çok kullanışlı.",
                    "Havuz alanı bakımlı ve ferah.",
                    "Havuzun sıcaklığı ideal seviyedeydi.",
                    "Kapalı havuz çok konforlu.",
                    "Havuz başındaki şezlonglar rahat."
                ],
                'neg': [
                    "Havuz çok kalabalık.",
                    "Havuz suyu yeterince temiz değil.",
                    "Havuz başında yeterli şezlong yok.",
                    "Havuz bakımı yetersiz.",
                    "Havuz suyu çok soğuktu.",
                    "Havuz alanı küçük.",
                    "Havuz hijyeni şüpheli."
                ]
            },
            'has_restaurant': {
                'pos': [
                    "Restoran menüsü çok zengin.",
                    "Yemekler lezzetli ve taze.",
                    "Restoran personeli çok ilgili.",
                    "A'la carte restoran seçenekleri güzel.",
                    "Kahvaltı büfesi çok çeşitli.",
                    "Akşam yemekleri mükemmel.",
                    "Dünya mutfağından lezzetler var.",
                    "Çocuk menüsü seçenekleri çok iyi."
                ],
                'neg': [
                    "Restoran menüsü sınırlı.",
                    "Yemekler vasatın altında.",
                    "Restoran servisi çok yavaş.",
                    "Yemek kalitesi düşük.",
                    "Kahvaltı çeşitleri yetersiz.",
                    "Akşam yemekleri soğuk servis ediliyor.",
                    "Restoran çok gürültülü.",
                    "Çocuklar için uygun menü yok."
                ]
            },
            'has_parking': {
                'pos': [
                    "Otopark geniş ve güvenli.",
                    "Vale hizmeti çok iyi.",
                    "Araç park etmek çok kolay.",
                    "Kapalı otopark çok kullanışlı.",
                    "Otopark ücretsiz.",
                    "7/24 güvenlik var."
                ],
                'neg': [
                    "Otopark çok dar.",
                    "Park yeri bulmak zor.",
                    "Otopark ücretleri yüksek.",
                    "Vale hizmeti yetersiz.",
                    "Otopark güvenliği yetersiz.",
                    "Kapalı otopark yok."
                ]
            },
            'has_air_conditioning': {
                'pos': [
                    "Klima sistemi çok iyi çalışıyor.",
                    "Odalar ideal sıcaklıkta.",
                    "Klimalar sessiz ve verimli.",
                    "İklimlendirme gayet başarılı.",
                    "Her odada ayrı klima kontrolü var."
                ],
                'neg': [
                    "Klima yetersiz kalıyor.",
                    "Klimalar çok gürültülü.",
                    "Odalar çok sıcak.",
                    "İklimlendirme sistemi sorunlu.",
                    "Klima bakımsız ve eski."
                ]
            },
            'has_room_service': {
                'pos': [
                    "Oda servisi çok hızlı.",
                    "24 saat oda servisi mükemmel.",
                    "Oda servisi menüsü zengin.",
                    "Oda servisi personeli çok ilgili.",
                    "Oda servisi fiyatları makul.",
                    "Geç saatte bile hızlı servis."
                ],
                'neg': [
                    "Oda servisi çok yavaş.",
                    "Oda servisi menüsü sınırlı.",
                    "Oda servisi pahalı.",
                    "Gece oda servisi hizmeti yetersiz.",
                    "Sipariş sürekli yanlış geliyor.",
                    "Oda servisi kalitesi düşük."
                ]
            },
            'has_breakfast': {
                'pos': [
                    "Kahvaltı çeşitleri zengin.",
                    "Kahvaltıda yerel lezzetler muhteşem.",
                    "Kahvaltı salonu ferah ve temiz.",
                    "Kahvaltıda taze ürünler sunuluyor.",
                    "Kahvaltı servisi çok düzenli.",
                    "Kahvaltı saatleri esnek.",
                    "Kahvaltıda ev yapımı ürünler var."
                ],
                'neg': [
                    "Kahvaltı çeşitleri yetersiz.",
                    "Kahvaltı kalitesi düşük.",
                    "Kahvaltı saatleri çok kısıtlı.",
                    "Kahvaltıda ürünler taze değil.",
                    "Kahvaltı salonu çok küçük.",
                    "Kahvaltıda servis yavaş.",
                    "Kahvaltı menüsü her gün aynı."
                ]
            }
        }
        
        # Genel değerlendirmeler
        self.genel_izlenim_pos = [
            "Harika bir tatil deneyimiydi.",
            "Muhteşem bir konaklama geçirdik.",
            "Beklentilerimizin üzerinde bir deneyimdi.",
            "Olağanüstü bir tatildi.",
            "Çok memnun kaldık.",
            "Kusursuz bir konaklama.",
            "Her şey mükemmeldi.",
            "Tatilimiz harikaydı.",
            "Çok keyifli bir deneyimdi.",
            "Unutulmaz bir tatil geçirdik."
        ]

        self.genel_izlenim_neg = [
            "Hayal kırıklığına uğradık.",
            "Beklentilerimizin çok altındaydı.",
            "Kötü bir deneyimdi.",
            "Maalesef memnun kalmadık.",
            "Sorunlu bir konaklama oldu.",
            "Tatilimiz berbattı.",
            "Pişman olduğumuz bir seçimdi.",
            "Keşke başka bir otel seçseydik.",
            "Parasının karşılığını vermedi.",
            "Ciddi sıkıntılar yaşadık."
        ]

        # Tavsiye cümleleri
        self.recommendation_pos = [
            "Kesinlikle tavsiye ediyorum.",
            "Mutlaka tekrar geleceğim.",
            "Herkese gönül rahatlığıyla önerebilirim.",
            "Ailenizle rahatlıkla tercih edebilirsiniz.",
            "Pişman olmayacağınız bir seçim.",
            "Tereddüt etmeden rezervasyon yapabilirsiniz."
        ]

        self.recommendation_neg = [
            "Kesinlikle tavsiye etmiyorum.",
            "Bir daha asla tercih etmem.",
            "Paranızı boşa harcamayın.",
            "Başka otellere bakmanızı öneririm.",
            "Bu fiyata çok daha iyisini bulabilirsiniz.",
            "Pişman olacağınız bir seçim olabilir."
        ]

    


    
    def generate_tc(self):
            """
            TC Kimlik numarası algoritmasına uygun ve tekrarsız numara üretir
            """
            while True:
                # 11 haneli TC numarası algoritması
                digits = []
                
                # İlk 9 haneyi oluştur
                for _ in range(9):
                    if not digits:  # İlk rakam 0 olamaz
                        digits.append(random.randint(1, 9))
                    else:
                        digits.append(random.randint(0, 9))
                
                # 10. haneyi hesapla
                # ((10 - ((d1+d3+d5+d7+d9)*7 + (d2+d4+d6+d8)) % 10)) % 10
                tenth = (10 - (((digits[0] + digits[2] + digits[4] + digits[6] + digits[8]) * 7 +
                            (digits[1] + digits[3] + digits[5] + digits[7])) % 10)) % 10
                digits.append(tenth)
                
                # 11. haneyi hesapla
                # (d1+d2+d3+d4+d5+d6+d7+d8+d9+d10) % 10
                eleventh = sum(digits) % 10
                digits.append(eleventh)
                
                # Listeyi stringe çevir
                tc = ''.join(map(str, digits))
                
                # Eğer bu TC daha önce kullanılmamışsa
                if tc not in self.used_tc_numbers:
                    self.used_tc_numbers.add(tc)
                    return tc

    def generate_name_with_gender(self):
        """İsim üretir ve cinsiyetle birlikte döner"""
        gender = random.choice(['M', 'F'])
        
        if gender == 'M':
            names_list = self.male_names
        else:
            names_list = self.female_names
        
        # %30 ihtimalle iki isim
        if random.random() < 0.3:
            first_name = f"{random.choice(names_list)} {random.choice(names_list)}"
        else:
            first_name = random.choice(names_list)
            
        last_name = random.choice(self.last_names)
        return f"{first_name} {last_name}", gender
    
    def generate_dependent_name(self, guest_gender, is_family, guest_surname=None):
        """
        Dependent için isim oluşturur.
        Args:
            guest_gender: Ana misafirin cinsiyeti ('M' veya 'F')
            is_family: Aile üyesi mi (True/False)
            guest_surname: Ana misafirin soyadı
        """
        gender = random.choice(['M', 'F'])
        
        if gender == 'M':
            names_list = self.male_names
        else:
            names_list = self.female_names
            
        # %30 ihtimalle iki isim
        if random.random() < 0.3:
            first_name = f"{random.choice(names_list)} {random.choice(names_list)}"
        else:
            first_name = random.choice(names_list)
        
        # Aile üyesi ise ve ana misafir erkekse aynı soyadı
        if is_family and guest_gender == 'M':
            last_name = guest_surname
        else:
            last_name = random.choice(self.last_names)
            
        return f"{first_name} {last_name}", gender
    
    def generate_guests(self):
        print(f"Generating {self.num_guests} guests...")
        
        for i in range(self.num_guests):
            # İsim ve cinsiyet üret
            full_name, gender = self.generate_name_with_gender()
            name_parts = full_name.split()
            surname = name_parts[-1]
            
            # Doğum tarihi üret
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
            
            # Email oluştur
            first_name = name_parts[0].lower()
            email = f"{first_name}.{surname.lower()}@{fake.free_email_domain()}"
            email = email.replace('ı', 'i').replace('ö', 'o').replace('ü', 'u').replace('ş', 's').replace('ğ', 'g').replace('ç', 'c')
            
            guest = {
                'guest_id': i + 1,
                'g_name': full_name,
                'g_email': email,
                'phone_number': fake.phone_number(),
                'g_birth_date': birth_date,
                'is_new_guest': random.choice([True, False]),
                'guest_tc': self.generate_tc(),
                'gender': gender,
                'surname': surname  # Soyadını dependents için saklayalım
            }
            
            # Guest profilini cache'e kaydet
            self.guest_profiles[i + 1] = guest
            self.guests.append(guest)
            
            if (i + 1) % 100 == 0:
                print(f"Generated {i + 1} guests")

        print(f"Completed generating {self.num_guests} guests")



    def generate_hotel_name(self, city, used_names):
        luxury_prefixes = {
            "The Ritz", "Palace", "Grand", "Royal", "Imperial", 
            "Waldorf", "Four Seasons", "St. Regis"
        }
        location_features = {
            "Beachfront", "Oceanview", "Bay", "Seaside", "Marina", 
            "Resort & Spa", "Hotel & Suites", "Beach Resort"
        }
        
        while True:
            name_patterns = [
                f"{random.choice(list(luxury_prefixes))} {city}",
                f"{city} {random.choice(list(luxury_prefixes))}",
                f"{random.choice(list(luxury_prefixes))} {random.choice(list(location_features))}"
            ]
            hotel_name = f"{random.choice(name_patterns)} {random.choice(['Otel', 'Hotel', 'Resort', 'Suites'])}"
            
            if hotel_name not in used_names:
                used_names.add(hotel_name)
                return hotel_name

    def generate_address(self, city):
        street_types = {
            "Dubai": ["Sheikh Zayed Road", "Jumeirah Beach Road", "Al Wasl Road", "Dubai Marina"],
            "Miami": ["Ocean Drive", "Collins Avenue", "Brickell Avenue", "Palm Boulevard"],
            "Cancun": ["Kukulcan Boulevard", "Tulum Avenue", "Costa Mujeres", "Zona Hotelera"],
            "Bali": ["Sunset Road", "Kuta Beach Road", "Nusa Dua Beach", "Seminyak Beach"],
            "Phuket": ["Thalang Road", "Beach Road", "Paradise Beach", "Rawai Beach"],
            "Barcelona": ["Las Ramblas", "Passeig de Gracia", "Barceloneta Beach", "Marina Bay"],
            "Maldives": ["Ocean Front", "Coral Road", "Paradise Island", "Palm Beach"],
            "Hawaii": ["Kalakaua Avenue", "Waikiki Beach", "Sunset Beach", "Palm Drive"],
            "Nice": ["Promenade des Anglais", "Boulevard Victor Hugo", "Rue de France", "Avenue Jean Médecin"],
            "Gold Coast": ["Surfers Paradise", "Main Beach Parade", "Marine Parade", "The Esplanade"]
        }
        
        
    def generate_address(self, city,used_addresses):
        street_types = {
            "Dubai": ["Sheikh Zayed Road", "Jumeirah Beach Road", "Al Wasl Road", "Dubai Marina"],
            "Miami": ["Ocean Drive", "Collins Avenue", "Brickell Avenue", "Palm Boulevard"],
            "Cancun": ["Kukulcan Boulevard", "Tulum Avenue", "Costa Mujeres", "Zona Hotelera"],
            "Bali": ["Sunset Road", "Kuta Beach Road", "Nusa Dua Beach", "Seminyak Beach"],
            "Phuket": ["Thalang Road", "Beach Road", "Paradise Beach", "Rawai Beach"],
            "Barcelona": ["Las Ramblas", "Passeig de Gracia", "Barceloneta Beach", "Marina Bay"],
            "Maldives": ["Ocean Front", "Coral Road", "Paradise Island", "Palm Beach"],
            "Hawaii": ["Kalakaua Avenue", "Waikiki Beach", "Sunset Beach", "Palm Drive"],
            "Nice": ["Promenade des Anglais", "Boulevard Victor Hugo", "Rue de France", "Avenue Jean Médecin"],
            "Gold Coast": ["Surfers Paradise", "Main Beach Parade", "Marine Parade", "The Esplanade"]
        }
        
        while True:
            street = random.choice(street_types[city])
            number = random.randint(1, 999)
            address = f"{number} {street}, {city}"
            
            if address not in used_addresses:
                used_addresses.add(address)
                return address


    def generate_hotels(self):
        print(f"Generating {self.num_hotels} hotels...")
        hotel_types = ['Lüks', 'İş', 'Resort', 'Butik', 'Ekonomik']
        cities = ["Dubai", "Miami", "Cancun", "Bali", "Phuket", 
                    "Barcelona", "Maldives", "Hawaii", "Nice", "Gold Coast"]
        used_names = set()
        used_addresses=set()

        for i in range(self.num_hotels):
            city = random.choice(cities)
            hotel = {
                'hotel_id': i + 1,
                'hotel_name': self.generate_hotel_name(city, used_names),
                'room_num': random.randint(20, 200),
                'location': self.generate_address(city,used_addresses),
                'city': city,
                'type': random.choice(hotel_types),
                'opening_date': fake.date_between(
                    start_date=datetime.now().date() - timedelta(days=365*20),
                    end_date=datetime.now().date() - timedelta(days=180)
                ),
                'h_capacity': random.randint(40, 400),
                'rate': round(random.uniform(200.0, 2000.0), 2)
            }
            self.hotels.append(hotel)

    def generate_amenities(self):
        print("Generating amenities...")
        for hotel in self.hotels:
            # Otel tipine göre olasılıkları ayarla
            if hotel['type'] == 'Lüks':
                prob_multiplier = 0.9
            elif hotel['type'] == 'İş':
                prob_multiplier = 0.7
            elif hotel['type'] == 'Resort':
                prob_multiplier = 0.8
            elif hotel['type'] == 'Butik':
                prob_multiplier = 0.6
            else:  # Ekonomik
                prob_multiplier = 0.4

            amenity = {
                'amenities_id': hotel['hotel_id'],
                'has_wifi': random.random() < (0.95 * prob_multiplier),  # Wi-Fi çoğu otelde var
                'has_pool': random.random() < (0.7 * prob_multiplier),
                'has_restaurant': random.random() < (0.8 * prob_multiplier),
                'has_parking': random.random() < (0.9 * prob_multiplier),
                'has_air_conditioning': random.random() < (0.95 * prob_multiplier),
                'has_room_service': random.random() < (0.6 * prob_multiplier),
                'has_breakfast': random.random() < (0.9 * prob_multiplier),
                'hotel_id': hotel['hotel_id']
            }
            self.amenities.append(amenity)


    def generate_rooms(self):
        print("Generating rooms...")
        room_id = 1
        room_types = ['Standart', 'Deluxe', 'Suit', 'Aile Odası', 'Business']
        current_date = datetime.now().date()

        for hotel in self.hotels:
            # Otel büyüklüğüne göre oda sayısını belirle
            if hotel['type'] == 'Lüks':
                num_rooms = random.randint(50, 100)
            elif hotel['type'] == 'Resort':
                num_rooms = random.randint(100, 200)
            else:
                num_rooms = random.randint(20, 50)
            
            hotel['room_num'] = num_rooms  # Otel kaydını güncelle
            
            for room_num in range(num_rooms):
                room_type = random.choice(room_types)
                # Oda tipine göre fiyat çarpanı
                price_multiplier = {
                    'Standart': 1.0,
                    'Deluxe': 1.5,
                    'Suit': 2.0,
                    'Aile Odası': 1.8,
                    'Business': 1.3
                }[room_type]

                room = {
                    'room_id': room_id,
                    'room_number': f"{random.randint(1,8)}{random.randint(0,9)}{random.randint(0,9)}",
                    'type': room_type,
                    'has_balcony': random.choice([True, False]),
                    'has_sea_view': random.choice([True, False]),
                    'r_capacity': {
                        'Standart': random.choice([1, 2]),
                        'Deluxe': random.choice([2, 3]),
                        'Suit': random.choice([2, 4]),
                        'Aile Odası': random.choice([4, 6]),
                        'Business': random.choice([1, 2])
                    }[room_type],
                    'price_per_night': round(hotel['rate'] * price_multiplier * random.uniform(0.9, 1.1), 2),
                    'floor': room_num // 30 + 1,  # Her katta 30 oda
                    'hotel_id': hotel['hotel_id'],
                    'is_available': True  # Başlangıçta tüm odalar müsait
                }
                self.rooms.append(room)
                room_id += 1


    def update_room_availability(self):
        """Odaların müsaitlik durumunu mevcut rezervasyonlara göre günceller"""
        print("Updating room availability...")
        current_date = datetime.now().date()
        
        # Önce tüm odaları müsait yap
        for room in self.rooms:
            room['is_available'] = True
        
        # Aktif rezervasyonları kontrol et
        for reservation in self.reservations:
            # İptal edilmiş rezervasyonları atla
            if reservation['is_canceled']:
                continue
                
            # Rezervasyon tarihleri mevcut tarihi kapsıyorsa
            if (reservation['arrival_date'] <= current_date <= reservation['departure_date']):
                # İlgili odayı dolu olarak işaretle
                room = next(r for r in self.rooms if r['room_id'] == reservation['room_id'])
                room['is_available'] = False
                
        # İstatistikleri göster
        available_rooms = sum(1 for room in self.rooms if room['is_available'])
        total_rooms = len(self.rooms)
        print(f"Room availability updated. {available_rooms} of {total_rooms} rooms are currently available.")


    def generate_payments(self):
        print("Generating payments...")
        payment_methods = ['Kredi Kartı', 'Nakit', 'Banka Transferi', 'Online Ödeme']
        payment_id = 1
        self.payments = []  # Önceki ödemeleri temizle

        for reservation in self.reservations:
            room = next(r for r in self.rooms if r['room_id'] == reservation['room_id'])
            
            # Konaklama süresini hesapla
            stay_duration = (reservation['departure_date'] - reservation['arrival_date']).days
            total_amount = round(room['price_per_night'] * stay_duration,2)

            if reservation['is_canceled']:
                # İptal edilen rezervasyonlar için iptal bedeli (%20)
                amount = round(total_amount * 0.2, 2)
                status = 'Canceled'
            else:
                # Normal rezervasyonlar için tam ödeme
                amount = total_amount
                status = 'Completed'

            # Gelecek rezervasyonları için ön ödeme
            if reservation['arrival_date'] > datetime.now().date():
                payment = {
                    'PaymentID': payment_id,
                    'PaymentMethod': random.choice(payment_methods),
                    'Amount': round(total_amount * 0.3, 2),  # %30 ön ödeme
                    'PaymentDate': datetime.now().date() - timedelta(days=random.randint(1, 10)),
                    'Status': 'PrePayment',
                    'room_id': room['room_id'],
                    'reservation_id': reservation['reservation_id']
                }
                self.payments.append(payment)
                payment_id += 1
            else:
                # Geçmiş rezervasyonlar için tam ödeme
                payment = {
                    'PaymentID': payment_id,
                    'PaymentMethod': random.choice(payment_methods),
                    'Amount': amount,
                    'PaymentDate': reservation['arrival_date'],
                    'Status': status,
                    'room_id': room['room_id'],
                    'reservation_id': reservation['reservation_id']
                }
                self.payments.append(payment)
                payment_id += 1

            if len(self.payments) % 100 == 0:
                print(f"Generated {len(self.payments)} payments")

        print(f"Completed generating {len(self.payments)} payments")

    def generate_reservations(self):
        print("Generating reservations...")
        reservation_id = 1
        self.reservations = []  # Önceki rezervasyonları temizle
        current_date = datetime.now().date()
        
        # Geçmiş rezervasyonlar için tarih aralığı (5 yıl öncesinden bugüne)
        past_start_date = current_date - timedelta(days=1825)
        # Gelecek rezervasyonlar için tarih aralığı (bugünden 3 ay sonrasına)
        future_end_date = current_date + timedelta(days=90)

        for guest in self.guests:
            # Her misafirin 1-3 arası rezervasyonu olsun
            num_reservations = random.randint(1, 3)
            
            for _ in range(num_reservations):
                hotel = random.choice(self.hotels)
                available_rooms = [r for r in self.rooms if r['hotel_id'] == hotel['hotel_id']]
                if not available_rooms:
                    continue
                    
                room = random.choice(available_rooms)
                
                # %70 geçmiş, %30 gelecek rezervasyon
                is_past = random.random() < 0.7
                
                if is_past:
                    check_in_date = fake.date_between(
                        start_date=past_start_date,
                        end_date=current_date - timedelta(days=1)
                    )
                else:
                    check_in_date = fake.date_between(
                        start_date=current_date,
                        end_date=future_end_date
                    )
                
                stay_duration = random.randint(1, 7)  # 1-7 gün arası konaklama
                check_out_date = check_in_date + timedelta(days=stay_duration)
                
                reservation = {
                    'reservation_id': reservation_id,
                    'arrival_date': check_in_date,
                    'departure_date': check_out_date,
                    'arrival_time': time(hour=random.randint(14, 20), minute=random.randint(0, 59)),
                    'exit_time': time(hour=random.randint(8, 12), minute=random.randint(0, 59)),
                    'num_guests': random.randint(1, room['r_capacity']),
                    'is_canceled': random.random() < 0.05,  # %5 iptal şansı
                    'guest_id': guest['guest_id'],
                    'room_id': room['room_id']
                }
                
                self.reservations.append(reservation)
                reservation_id += 1

            if len(self.reservations) % 100 == 0:
                print(f"Generated {len(self.reservations)} reservations")

        print(f"Completed generating {len(self.reservations)} reservations")

    def generate_amenity_based_comment(self, hotel_id, stars):
        hotel_amenities = next(a for a in self.amenities if a['hotel_id'] == hotel_id)
        comment_parts = []
        available_features = []
        
        # Otelin özelliklerini kontrol et
        for feature, has_feature in hotel_amenities.items():
            if feature.startswith('has_') and has_feature:
                available_features.append(feature)
        
        # Rastgele 2-4 özellik seç
        selected_features = random.sample(
            available_features,
            min(random.randint(2, 4), len(available_features))
        )
        
        if stars >= 4:
            comment_parts.append(random.choice(self.genel_izlenim_pos))
            # Seçilen özellikler için pozitif yorumlar
            for feature in selected_features:
                comment_parts.append(random.choice(self.feature_based_comments[feature]['pos']))
            comment_parts.append(random.choice(self.recommendation_pos))
        elif stars < 3:
            comment_parts.append(random.choice(self.genel_izlenim_neg))
            # Seçilen özellikler için negatif yorumlar
            for feature in selected_features:
                comment_parts.append(random.choice(self.feature_based_comments[feature]['neg']))
            comment_parts.append(random.choice(self.recommendation_neg))
        else:  # 3 yıldız için tek cümle
            comment_parts.append("Ortalama bir konaklama deneyimiydi.")
        
        return ' '.join(comment_parts)

    def generate_comments(self):
        print("Generating comments...")
        comment_id = 1
        current_date = datetime.now().date()
        
        for guest in self.guests:
            # Her misafirin yaptığı rezervasyonları bul
            guest_reservations = [r for r in self.reservations if r['guest_id'] == guest['guest_id']]
            
            for reservation in guest_reservations:
                # Sadece geçmiş ve tamamlanmış rezervasyonlar için yorum yapılabilir
                if (reservation['departure_date'] < current_date and 
                    not reservation['is_canceled'] and 
                    random.random() < 0.4):  # 40% yorum yapma şansı
                    
                    room = next(r for r in self.rooms if r['room_id'] == reservation['room_id'])
                    hotel_id = room['hotel_id']
                    
                    # Yorum tarihi rezervasyon çıkış tarihinden sonra, en fazla 30 gün içinde
                    latest_comment_date = min(
                        reservation['departure_date'] + timedelta(days=30),
                        current_date
                    )
                    
                    comment_date = fake.date_between(
                        start_date=reservation['departure_date'],
                        end_date=latest_comment_date
                    )
                    
                    # Yıldızları belirle (otel tipine göre ağırlıklı)
                    hotel = next(h for h in self.hotels if h['hotel_id'] == hotel_id)
                    if hotel['type'] in ['Lüks', 'Resort']:
                        stars = random.choices([1,2,3,4,5], weights=[5,10,15,35,35])[0]
                    else:
                        stars = random.choices([1,2,3,4,5], weights=[10,15,40,25,10])[0]
                        
                    comment = {
                        'comment_id': comment_id,
                        'date': comment_date,
                        'content': self.generate_amenity_based_comment(hotel_id, stars),
                        'num_stars': stars,
                        'guest_id': guest['guest_id'],
                        'hotel_id': hotel_id
                    }
                    self.comments.append(comment)
                    comment_id += 1


    def generate_dependents(self):
        print("Generating dependents...")
        dependent_id = 1
        
        for guest in self.guests:
            # Her misafir için dependent sayısını belirle (0-3 arası)
            num_dependents = random.randint(0, 3)
            
            for _ in range(num_dependents):
                # İlişki türünü belirle (family veya friend)
                relation_type = random.choice(['family', 'friend'])
                
                # Guest'in yaşına göre dependent yaş aralığını belirle
                guest_age = (datetime.now().date() - guest['g_birth_date']).days // 365
                
                if relation_type == 'family':
                    # Aile üyesi için yaş aralığı
                    # Eğer guest 50 yaşından küçükse dependent çocuk olabilir
                    if guest_age < 50:
                        min_age = 1
                        max_age = max(1, guest_age - 18)  # En az 18 yaş farkı olsun
                    else:
                        # Yaşlı guest için dependent yetişkin olabilir
                        min_age = 18
                        max_age = guest_age - 18
                else:
                    # Arkadaş için yakın yaş aralığı (±10 yaş)
                    min_age = max(18, guest_age - 10)
                    max_age = min(90, guest_age + 10)
                
                # Yaş aralığını kontrol et
                if min_age >= max_age:
                    min_age = 18
                    max_age = 90
                
                # Dependent doğum tarihi
                birth_date = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
                
                # İsim üret
                full_name, gender = self.generate_dependent_name(
                    guest_gender=guest['gender'],
                    is_family=relation_type == 'family',
                    guest_surname=guest['surname']
                )
                
                dependent = {
                    'dependent_id': dependent_id,
                    'TC_No': self.generate_tc(),
                    'birth_date': birth_date,
                    'name': full_name,
                    'gender': gender,
                    'relation_type': relation_type,
                    'guest_id': guest['guest_id'],
                    'primary_guest_id': guest['guest_id']
                }
                
                # Yaş ilişkisi kontrolü
                dependent_age = (datetime.now().date() - birth_date).days // 365
                guest_age = (datetime.now().date() - guest['g_birth_date']).days // 365
                
                # Eğer mantıklı bir yaş ilişkisi yoksa dependent'ı ekleme
                if (relation_type == 'family' and 
                    (dependent_age >= guest_age or 
                    (guest_age - dependent_age < 18 and guest['gender'] == 'M'))):
                    continue
                    
                self.dependents.append(dependent)
                dependent_id += 1
                
                # İstatistik için
                if len(self.dependents) % 100 == 0:
                    print(f"Generated {len(self.dependents)} dependents...")

        print(f"Completed generating {len(self.dependents)} dependents.")

    def add_family_stats(self):
        """Aile ve arkadaş istatistiklerini hesapla ve yazdır"""
        family_count = sum(1 for d in self.dependents if d['relation_type'] == 'family')
        friend_count = sum(1 for d in self.dependents if d['relation_type'] == 'friend')
        
        guests_with_deps = len(set(d['guest_id'] for d in self.dependents))
        
        print("\nDependent Statistics:")
        print(f"Total Dependents: {len(self.dependents)}")
        print(f"Family Members: {family_count}")
        print(f"Friends: {friend_count}")
        print(f"Guests with Dependents: {guests_with_deps}")
        print(f"Average Dependents per Guest: {len(self.dependents)/self.num_guests:.2f}")


    def save_to_csv(self, data, filename):
            """Verileri CSV dosyasına kaydeder"""
            if not data:
                return
                
            print(f"Saving {len(data)} records to {filename}...")
            
            # CSV dosyasının bulunacağı klasörü oluştur
            os.makedirs('data/csv', exist_ok=True)
            filepath = os.path.join('data/csv', filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            print(f"Finished saving {filename}")

    def save_all_data(self):
            """Tüm verileri CSV dosyalarına kaydeder"""
            self.save_to_csv(self.hotels, 'hotels.csv')
            self.save_to_csv(self.amenities, 'amenities.csv')
            self.save_to_csv(self.photos, 'photos.csv')
            self.save_to_csv(self.guests, 'guests.csv')
            self.save_to_csv(self.dependents, 'dependents.csv')
            self.save_to_csv(self.rooms, 'rooms.csv')
            self.save_to_csv(self.payments, 'payments.csv')
            self.save_to_csv(self.reservations, 'reservations.csv')
            self.save_to_csv(self.comments, 'comments.csv')


    def create_sample_hotel_photos(self, num_hotels):
        base_dir = "hotel_photos"

        # Ana klasörü oluştur
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)  # Bu satır if bloğunun dışında olmalı

        # Her otel için klasör oluştur...
        for hotel_id in range(1, num_hotels + 1):
            hotel_dir = os.path.join(base_dir, f"hotel_{hotel_id}")
            os.makedirs(hotel_dir)

            # Otel tiplerine göre foto sayısını belirle
            is_luxury = random.random() < 0.3  # %30 lüks otel
            num_photos = random.randint(8, 15) if is_luxury else random.randint(3, 8)

            # Her otel için foto kategorileri
            categories = {
                'exterior': ['Dış Görünüm', 'Giriş', 'Bahçe'],
                'lobby': ['Lobi', 'Resepsiyon', 'Bekleme Alanı'],
                'room': ['Standart Oda', 'Deluxe Oda', 'Suit Oda', 'Banyo'],
                'amenities': ['Havuz', 'Restoran', 'Spa', 'Fitness'],
                'view': ['Manzara', 'Balkon Görünümü', 'Teras']
            }

            photo_count = 1
            for category, subcats in categories.items():
                # Her kategoriden en az 1 foto
                n_photos = random.randint(1, 3)
                for _ in range(n_photos):
                    if photo_count > num_photos:
                        break

                    # Örnek foto oluştur
                    img = Image.new('RGB', (800, 600), color='white')
                    d = ImageDraw.Draw(img)

                    # Gradyan arka plan
                    for y in range(600):
                        r = int(200 * (1 - y / 600))
                        g = int(150 * (1 - y / 600))
                        b = int(100 * (1 - y / 600))
                        d.line([(0, y), (800, y)], fill=(r, g, b))

                    # Metin oluştur ve ortala
                    font = ImageFont.load_default()
                    text = f"Hotel {hotel_id}\n{random.choice(subcats)}"
                    
                    # Metin boyutlarını hesapla
                    text_bbox = d.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    
                    # Metni ortala
                    text_x = (800 - text_width) // 2
                    text_y = (600 - text_height) // 2

                    # Gölge ve metni ekle
                    shadow_offset = 2
                    d.text((text_x + shadow_offset, text_y + shadow_offset), text, font=font, fill='black')  # Gölge
                    d.text((text_x, text_y), text, font=font, fill='white')  # Asıl metin

                    # Kaydet
                    img_path = os.path.join(hotel_dir, f"photo_{photo_count}.jpg")
                    img.save(img_path, 'JPEG', quality=85)

                    photo_count += 1

        print(f"Created photo directories for {num_hotels} hotels")
        return base_dir




    def generate_all(self):
        self.generate_hotels()
        self.generate_amenities()
        self.generate_rooms()
        self.generate_guests()
        self.generate_dependents()
        self.generate_reservations()
        self.generate_payments()
        self.generate_comments()
        self.update_room_availability()  # Oda müsaitlik durumlarını güncelle
        
        self.save_all_data()
                
        print("\nData generation completed successfully!")
        print(f"Generated:")
        print(f"- {len(self.hotels)} hotels")
        print(f"- {len(self.amenities)} amenities records")
        print(f"- {len(self.photos)} photos")
        print(f"- {len(self.guests)} guests")
        print(f"- {len(self.dependents)} dependents")
        print(f"- {len(self.rooms)} rooms")
        print(f"- {len(self.payments)} payments")
        print(f"- {len(self.reservations)} reservations")
        print(f"- {len(self.comments)} comments")
        
        # Müsaitlik istatistiklerini göster
        available_rooms = sum(1 for room in self.rooms if room['is_available'])
        print(f"- Currently available rooms: {available_rooms}")
        print("\nFiles have been saved in the 'data/csv' directory.")


    
if __name__ == "__main__":
    # Daha dengeli sayılar için
    # Daha dengeli sayılar için
    generator = HotelDataGenerator(num_hotels=10, num_guests=1000)
    generator.create_sample_hotel_photos(10)  # Önce fotoları oluştur
    generator.generate_all()