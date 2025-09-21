import os,sys
import google.generativeai as genai
from sentence_transformers import SentenceTransformer, util
import torch
import numpy as np
import re
import traceback

SubjectTitles ='''
Başlarken
adekoCAM Nedir ?
adekoCAM ile CNC Kesim
Kesim Planı ve Su Yönü
Prosedürlerle Çalışma
Parça ve Kapak Arayüzleri
Kapak Türetme & Kapak Model Parametreleri
Kapak Modeli Programlama
Kapak Model Parametrelerinin Kullanıcıya Açılması
Ürün Arayüzü
Ürün Modeli Oluşturma
Patron Arayüzü
Keyfi Parça Şekli
Operasyonlar ve Takım Atamaları
Kapak ve Modül Programlama Komutları
Yönetici-Operatör Modu Eşgüdümü - Tracking
Etiket Şablonu Düzenleme
Malzeme Birleştirme(içe aktarım sırasında)
Çift Yüzeyinde İşlem Olan Panelleri Çevirme İşlemi
Karşılıklı Deliklerin Boydan Boya Delinme Ayarının Yapılışı
Makineye Parça Bağlama
AES Sirius Gibi Makinelere Parça Bağlama (Z ekseni yere bakan)
adekoCAM Güncelleyici'yi Ayarlama
adekoCAM Verilerinin Yedeklenmesi ve Yönetilmesi
Kenar bandı makinesinde açılması istenilen kanallar için kural tanımlama.
Parça ölçülerine göre parça listesi csv'si oluşturma
CNC Routerlarda orijin ofsetleme
Makineye özel keyfi parametre tanımlama
adekoCAM'in Açılmaması Problemi ve Çözümleri
'''
# Gemini API anahtarınızı ortam değişkeni olarak ayarladığınızdan emin olun.

os.environ["GEMINI_API_KEY"] = "AIzaSyC0wq0jpRhXjBBp9hpQDky9R__ZA4MBvVQ"
class AICore:
    """
    Google Gemini API ile GPT tabanlı özetleme ve anlamsal arama işlemlerini yöneten çekirdek sınıf.
    """

    def __init__(self):
        print("AI Core başlatılıyor...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Kullanılacak cihaz: {self.device}")

        # Gemini API
        try:
            # Ortam değişkeninden Gemini API anahtarını alıyoruz.
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise EnvironmentError("GEMINI_API_KEY ortam değişkeni tanımlı değil.")
            
            # Gemini API'sini yapılandır
            genai.configure(api_key=self.api_key)
            
           
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("Google Gemini modeli başarıyla yüklendi.")

        except Exception as e:
            print(f"Hata: Gemini modeli başlatılamadı. Detay: {e}")
            self.model = None

       # Anlamsal arama modeli
        try:
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_path, "sbert_model")

            print(f"[DEBUG] Model klasörü yolu: {model_path}")
            self.search_model = SentenceTransformer(model_path, device=self.device)

            print(f"[DEBUG] Bu klasördeki dosyalar: {os.listdir(model_path)}")


            print("✅ Anlamsal arama modeli yüklendi.")
        except Exception as e:
            print("❌ Anlamsal arama modeli yüklenemedi.")
            print("[TRACEBACK HATASI]")
            print(traceback.format_exc())
            self.search_model = None

            print("AI Core hazır.") 

    def summarize_with_gemini(self, text: str, user_prompt: str = None) -> str:
        """
        Google Gemini API ile metni özetler.
        """
        if not self.model:
            return "❌ Gemini modeli yüklenemedi."

        try:
            # Gemini için prompt'u hazırlıyoruz.
            # Sistem ve kullanıcı rollerini tek bir prompt içinde birleştirmek genellikle daha iyi çalışır.
            system_instruction = system_instruction = """Sen öğretici uzman bir yardımcı asistansın.
Kullanıcı sana bir işlem sorduğunda (örneğin nasıl düzenlenir, nasıl yapılır, nasıl eklenir, nasıl silinir, nasıl değiştirilir gibi),
sadece tanım değil, adım adım işlem sırasını açıkla.
Her adımı sırasıyla numaralandır. Gerekiyorsa kod örnekleri, buton isimleri, menü yolları, ayarlar veya ilgili kavramları da ekle.
Cevabın sade, net, kısa cümleli ve anlaşılır olsun. Gereksiz açıklamalar yapma.
Eğer içerikte adım adım bölümler, 'Nasıl yapılır', 'Prosedür', 'Adımlar' gibi başlıklar varsa, özellikle onları ön plana çıkar ve kullanıcının amacına yönelik en faydalı cevabı oluştur.
"""

            
            # Eğer özel bir kullanıcı prompt'u varsa, onu da ekleyelim.
            if user_prompt:
                if user_prompt:
                    prompt = f"{system_instruction}\n\nKullanıcının sorusu: '{user_prompt}'\n\nLütfen aşağıdaki açıklamayı bu soruya göre cevapla ve eğer işlem adımları varsa sıralı bir şekilde detaylandır:\n\n---\n{text}\n---"
                else:
                    prompt = f"{system_instruction}\n\nVideonun durduğu andaki ifadeyi açıkla:\n\n---\n{text}\n---"

            else:
                prompt = f"{system_instruction}\n\n Videonun durduğu andaki ifadeyi açıkla:\n\n---\n{text}\n---"

            # Gemini API'ye istek gönder
            response = self.model.generate_content(prompt)
            
            return response.text.strip()
        except Exception as e:
            return f"Gemini özetleme hatası: {e}"

    def find_and_summarize(self, query: str, context_text: str, min_chunk_size: int = 20) -> str:
        """
        Web'den alınan içerikte sorguya en uygun kısmı bulur ve Gemini ile özetler.
        """
        if not self.search_model:
            return "❌ Anlamsal arama modeli yüklenemedi."

        if not context_text or not context_text.strip():
            return "⚠️ Analiz edilecek bir metin bulunamadı."

        print(f"'{query}' sorgusu için anlamsal arama yapılıyor...")

        text_chunks = [chunk.strip() for chunk in re.split(r'\n{1,2}', context_text) if len(chunk.strip()) >= min_chunk_size]
        if not text_chunks:
            return f"⚠️ Yeterli uzunlukta analiz edilecek bölüm bulunamadı."

        query_embedding = self.search_model.encode(query, convert_to_tensor=True, device=self.device)
        context_embeddings = self.search_model.encode(text_chunks, convert_to_tensor=True, device=self.device)
        search_results = util.semantic_search(query_embedding, context_embeddings, top_k=1)

        if not search_results or not search_results[0]:
            return "🔍 İlgili bir bölüm bulunamadı."

        best_match_index = search_results[0][0]["corpus_id"]
        best_match_score = search_results[0][0]["score"]
        relevant_text = text_chunks[best_match_index]

        print(f"✔️ En alakalı bölüm bulundu. Benzerlik skoru: {best_match_score:.4f}")
        print(f"[DEBUG] Özetlenecek içerik:\n{relevant_text[:300]}...\n")

        if "session info" in relevant_text.lower() or "chrome=" in relevant_text.lower():
            return "⚠️ Geçersiz içerik alındı. Sayfa doğru şekilde yüklenmemiş olabilir."
        
        print("🤖 Gemini ile özetleme başlatılıyor...")
        # Özetleme fonksiyonunu `summarize_with_gemini` olarak güncelliyoruz.
        # `query`'yi de `user_prompt` olarak göndererek daha odaklı bir özet almasını sağlıyoruz.
        summary = self.summarize_with_gemini(relevant_text, user_prompt=query)
        return summary
    
    def find_subject_title_with_gemini(self, UserInput: str) -> str:
        """
        Google Gemini API ile metni özetler.
        """
        if not self.model:
            return "❌ Gemini modeli yüklenemedi."

        try:
            # Gemini için prompt'u hazırlıyoruz.
            # Sistem ve kullanıcı rollerini tek bir prompt içinde birleştirmek genellikle daha iyi çalışır.
                system_instruction = f"Sen sadece başlık söyleme uzmanısın. {SubjectTitles}elimizdeki konu başlıkları bunlar, bu başlıkları öğren. Sen sadece buradan {UserInput} gelen cümleyle ilgili başlıkların isimlerini söyleyeceksin. Başka bir şey yazmayacaksın"
            
            # Eğer özel bir kullanıcı prompt'u varsa, onu da ekleyelim.
                prompt = f"{system_instruction}"
            
            # Gemini API'ye istek gönder
                response = self.model.generate_content(prompt)
                return response.text.strip()
        except Exception as e:
            return f"Gemini özetleme hatası: {e}"