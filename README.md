# ⚖️ Hukuk Arama Asistanı

Türkçe hukuk terimleri ve Kaggle hukuk Soru-Cevap verisi üzerinde **semantik arama** yapan bir Streamlit uygulaması.

## 🎯 Amaç
- Hukuk terimlerinin kısa anlamlarına hızlı erişim
- İlgili soru-cevap içeriklerini tek yerden keşfetme

## 🧠 Veri Seti
- **Vikisözlük:** seçilmiş hukuk terimleri (manuel liste)
- **Kaggle:** Turkish Law Dataset for LLM Finetuning  
  Bağlantı: https://www.kaggle.com/datasets/batuhankalem/turkish-law-dataset-for-llm-finetuning

## 🧩 Yöntem / Mimarî
- Embedding: `paraphrase-multilingual-MiniLM-L12-v2` (hızlı)  
- Vektör DB: **FAISS**  
- Arayüz: **Streamlit**  
- Adımlar: Veri Toplama → Embed → FAISS Index → Sorgu & Benzerlik → Kısa Cevap

## 🚀 Çalıştırma
```bash
pip install -r requirements.txt
streamlit run app.py
