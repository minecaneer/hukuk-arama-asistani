# ⚖️ Hukuk Arama Asistanı

**Hukuk Arama Asistanı**, Türk hukuk terimleri ve yargı kavramları üzerinde **anlam tabanlı (semantik)** arama yapabilen yapay zekâ destekli bir web uygulamasıdır.  
Retrieval Augmented Generation (RAG) mimarisiyle geliştirilmiştir ve kullanıcıların hukukla ilgili terimleri, kavramları veya soruları Türkçe doğal dilde sorgulayarak **doğru ve hızlı yanıtlar** almasını sağlar.  

Uygulama, **Vikisözlük** ve **Kaggle** kaynaklarını bir araya getirerek kullanıcıya çift kaynaktan bilgi sunar.

---

## 🌐 Canlı Demo
🎯 [🔗 Hukuk Arama Asistanı’nı Deneyin](https://hukuk-arama-asistani-2kguurbd6rnc8mgzpwjrhw.streamlit.app/)

> Uygulama Streamlit Cloud üzerinde aktif olarak çalışmaktadır.  
> Herhangi bir kurulum yapmadan doğrudan tarayıcı üzerinden erişebilirsiniz.

---

## 🎬 Tanıtım Videosu
<video src="https://github.com/minecaneer/hukuk-arama-asistani/raw/main/assets/hukuk_asistani.mov" controls width="700"></video>

---

## 🖼️ Arayüz Görseli
![Uygulama Ekran Görüntüsü](assets/hukuk-asistani.png)

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

## ✨ Özellikler ve Kullanım Alanları

- 🔍 **Anlam Tabanlı Arama** – Sadece kelime eşleşmesi değil, anlam benzerliğine göre sonuç döndürür  
- 🧠 **Kısa Yanıt Üretimi** – İlk eşleşmelerden özet çıkarır  
- ⚖️ **Türkçe Veri Desteği** – Tüm veri seti Türkçe kaynaklardan  
- 🌗 **Dark/Light Tema** – Tek tıkla görünüm değiştirilebilir  
- 🧩 **Çift Veri Kaynağı** – Vikisözlük + Kaggle  
- 📱 **Responsive Arayüz** – Masaüstü ve mobil cihazlarla uyumlu  

---

## 🧰 Kullanılan Teknolojiler

| Katman | Teknoloji |
|:--|:--|
| **Model** | SentenceTransformers – `paraphrase-multilingual-MiniLM-L12-v2` |
| **Vektör DB** | FAISS |
| **Framework** | Streamlit |
| **Veri Kaynakları** | Kaggle API, Vikisözlük |
| **Dil** | Python 3.11 |
| **Tasarım** | Özel Light/Dark CSS teması |

---

## ⚙️ Kurulum ve Çalıştırma Adımları

### 1️ **Depoyu klonla**
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


## İletişim

Projeyle ilgili herhangi bir sorunuz varsa lütfen benimle iletişime geçin.

- **E-mail:** [minecaner.1995@gmail.com](mailto:minecaner.1995@gmail.com)
- **GitHub:** [github.com/mminecaneer](https://github.com/minecaneer)
- **LinkedIn:** [linkedin.com/in/minecaner](https://linkedin.com/in/minecaner)


| Kaynak         | Açıklama                | Boyut  |
| :------------- | :---------------------- | :----- |
| **Vikisözlük** | 20+ temel hukuk terimi  | ~15 KB |
| **Kaggle Q&A** | 13.700 satır soru–cevap | ~6 MB  |
| **Toplam**     | ≈13.720 bilgi bloğu     |        |



## Proje Yapısı

```
hukuk-arama-asistani/
├── app.py                  
├── faiss_index.bin         
├── texts.pkl               
├── requirements.txt        
├── runtime.txt             
├── README.md               
└── assets/
    ├── hukuk-asistani.png  
    └── hukuk_asistani.mov
```


