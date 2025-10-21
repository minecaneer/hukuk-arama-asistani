# ⚖️ Hukuk Arama Asistanı

**Hukuk Arama Asistanı**, Türk hukuk terimleri ve yargı kavramları üzerinde **anlam tabanlı (semantik)** arama yapabilen yapay zekâ destekli bir web uygulamasıdır.  
Retrieval Augmented Generation (RAG) mimarisiyle geliştirilmiştir ve kullanıcıların hukukla ilgili terimleri, kavramları veya soruları Türkçe doğal dilde sorgulayarak **doğru ve hızlı yanıtlar** almasını sağlar.  

Uygulama, **Vikisözlük** ve **Kaggle** kaynaklarını bir araya getirerek, kullanıcıya çift kaynaktan bilgi sunar.

---

## 🧠 RAG Pipeline Yapısı

**Hukuk Arama Asistanı**, tam bir RAG (Retrieval Augmented Generation) pipeline’ı uygular:

1. **Veri Toplama ve Hazırlama**  
   - Kaggle’dan: [Turkish Law Dataset for LLM Finetuning](https://www.kaggle.com/datasets/batuhankalem/turkish-law-dataset-for-llm-finetuning)  
   - Vikisözlük’ten: Temel hukuk terimleri (örnek: *mülkiyet, nafaka, delil, tazminat...*)

2. **Metin Birleştirme**  
   - Soru–cevap blokları ve terim tanımları etiketlenip birleştirilir

3. **Vektörleştirme (Embedding)**  
   - `paraphrase-multilingual-MiniLM-L12-v2` modeliyle metinler embedding’e dönüştürülür  

4. **Vektör Veritabanı (FAISS)**  
   - Tüm veriler FAISS index’e eklenir, benzerlik aramaları yapılır  

5. **Sorgu Eşleştirme ve Yanıt Oluşturma**  
   - Kullanıcının yazdığı terim embedding’e dönüştürülür  
   - En ilgili 5 sonuç listelenir, kısa bir yanıt çıkarılır  

---

## 🌐 Canlı Demo

➡️ [**Hukuk Arama Asistanı (Ngrok Demo)**](https://noncensored-synonymously-joni.ngrok-free.dev)  

---

## 🗂️ Veri Seti

- **Vikisözlük:** 20’ye yakın temel hukuk terimi  
- **Kaggle Soru-Cevap:** ~13.700 satır soru–cevap verisi  
- Her biri tek bir “bilgi bloğu” olarak embedding’e dönüştürülür  
- **Toplam:** ≈13.700 Q&A + 19 terim tanımı  

---

## ✨ Özellikler ve Kullanım Alanları

- 🔍 **Anlam Tabanlı Arama** – Sadece kelime eşleşmesi değil, anlam benzerliğine göre sonuç döndürür  
- 🧠 **Kısa Yanıt Üretimi** – İlk eşleşmelerden özet çıkarır  
- ⚖️ **Türkçe Veri Desteği** – Tüm veri seti Türkçe kaynaklardan  
- 🌗 **Dark/Light Tema** – Tek tıkla görünüm değiştirilebilir  
- 🧩 **Çift Veri Kaynağı** – Vikisözlük + Kaggle  
- 📱 **Responsive Arayüz** – Masaüstü ve mobil cihazlarla uyumlu  

### 🎓 Kullanım Senaryoları
- Hukuk öğrencileri için terim açıklamaları ve örnek soru–cevap aracı  
- Avukat ve akademisyenler için hızlı referans kaynağı  
- Hukuk alanında dil modeli tabanlı arama projelerine örnek uygulama  

---

## 🧰 Kullanılan Teknolojiler

| Katman | Teknoloji |
|:--|:--|
| **Model** | SentenceTransformers – `paraphrase-multilingual-MiniLM-L12-v2` |
| **Vektör DB** | FAISS |
| **Framework** | Streamlit |
| **Veri Kaynakları** | Kaggle API, Vikisözlük API |
| **Dil** | Python 3.10 (Google Colab) |
| **Tasarım** | Özel Light/Dark CSS teması |

---

## ⚙️ Kurulum ve Çalıştırma Adımları

### 1  **Depoyu klonla**
```bash
git clone https://github.com/minecaneer/hukuk-arama-asistani.git
cd hukuk-arama-asistani
```

### 2️  **Sanal ortam oluştur**
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```


### 3 **Gerekli kütüphaneleri yükle**
```bash
pip install -r requirements.txt
```

### 4️ **FAISS verisini oluştur (ilk kullanımda)**
```bash
Bu adım Colab üzerinde zaten gerçekleştirilmiştir.  
Eğer FAISS dosyaları (`faiss_index.bin` ve `texts.pkl`) bulunmuyorsa,  
Colab’deki "veri hazırlama" kodunu yeniden çalıştırarak oluşturabilirsiniz.
```
