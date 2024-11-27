import requests
import json
import os
from datetime import datetime
import time
from typing import List, Dict

class HotelImageFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Client-ID {api_key}",
            "Accept-Version": "v1"
        }
        
    def fetch_hotel_images(self, count: int = 100) -> List[Dict]:
        """Unsplash'dan otel görsellerini çeker"""
        hotels_data = []
        page = 1
        per_page = 30  # Unsplash API limiti
        
        # Otel ile ilgili arama terimleri
        search_terms = ["hotel", "resort", "luxury hotel", "hotel room", "hotel building"]
        
        while len(hotels_data) < count:
            for term in search_terms:
                try:
                    response = requests.get(
                        f"{self.base_url}/search/photos",
                        headers=self.headers,
                        params={
                            "query": term,
                            "page": page,
                            "per_page": per_page,
                            "orientation": "landscape"
                        }
                    )
                    
                    if response.status_code == 200:
                        results = response.json()["results"]
                        
                        for photo in results:
                            if len(hotels_data) >= count:
                                break
                                
                            hotel_data = {
                                "id": len(hotels_data) + 1,
                                "name": f"Hotel {len(hotels_data) + 1}",
                                "original_image": photo["urls"]["raw"],
                                "large_image": photo["urls"]["regular"],
                                "thumbnail": photo["urls"]["small"],
                                "photographer": photo["user"]["name"],
                                "photographer_url": photo["user"]["links"]["html"],
                                "unsplash_url": photo["links"]["html"],
                                "width": photo["width"],
                                "height": photo["height"],
                                "description": photo["description"] or photo["alt_description"],
                                "fetched_at": datetime.now().isoformat()
                            }
                            
                            hotels_data.append(hotel_data)
                            
                    time.sleep(1)  # API rate limit'e uymak için bekleme
                    
                except Exception as e:
                    print(f"Hata oluştu: {e}")
                    continue
                
            page += 1
            
        return hotels_data[:count]
    
    def save_to_json(self, data: List[Dict], filename: str = "hotel_images.json"):
        """Verileri JSON dosyasına kaydeder"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({"hotels": data}, f, ensure_ascii=False, indent=2)
    
    def download_images(self, data: List[Dict], folder: str = "hotel_images"):
        """Resimleri yerel klasöre indirir"""
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        for hotel in data:
            try:
                # Thumbnail indirme
                thumbnail_response = requests.get(hotel["thumbnail"])
                thumbnail_path = os.path.join(folder, f"hotel_{hotel['id']}_thumb.jpg")
                
                with open(thumbnail_path, 'wb') as f:
                    f.write(thumbnail_response.content)
                
                # Büyük resim indirme
                image_response = requests.get(hotel["large_image"])
                image_path = os.path.join(folder, f"hotel_{hotel['id']}_large.jpg")
                
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                    
                # Yerel dosya yollarını data'ya ekleme
                hotel["local_thumbnail"] = thumbnail_path
                hotel["local_image"] = image_path
                
                time.sleep(1)  # İndirme işlemleri arasında bekleme
                
            except Exception as e:
                print(f"Resim indirme hatası (Hotel {hotel['id']}): {e}")

def main():
    # Unsplash API key'inizi buraya girin
    UNSPLASH_API_KEY = "hvdUvwavZQIjNfG4Gb82Bb3W7g88hH3TRVyc522LCps"
    
    fetcher = HotelImageFetcher(UNSPLASH_API_KEY)
    
    # 100 otel resmi çek
    print("Otel resimleri çekiliyor...")
    hotels_data = fetcher.fetch_hotel_images(100)
    
    # JSON olarak kaydet
    print("Veriler JSON dosyasına kaydediliyor...")
    fetcher.save_to_json(hotels_data)
    
    # Resimleri indir
    print("Resimler indiriliyor...")
    fetcher.download_images(hotels_data)
    
    print(f"İşlem tamamlandı. {len(hotels_data)} otel verisi işlendi.")

if __name__ == "__main__":
    main()