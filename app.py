import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss, re, os, pickle

# ---- Sayfa ayarları
st.set_page_config(page_title="⚖️ Hukuk Arama Asistanı", page_icon="⚖️", layout="centered")

# ---- Tema Durumu
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

def toggle_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

# ---- CSS Temalar
LIGHT_THEME = """
<style>
body { background-color:#f7f9fc; color:#1e293b; font-family:'Segoe UI', Roboto, sans-serif; }
.main-title { text-align:center; font-size:2.2em; font-weight:800; color:#0f172a; margin:0.2em 0 0.15em; }
.sub-title { text-align:center; color:#475569; font-size:1.05em; margin-bottom:1.2em; }
.header-row { display:flex; justify-content:center; align-items:center; gap:10px; margin-bottom:12px; }
.badge { display:inline-flex; align-items:center; gap:6px; padding:8px 12px; border-radius:999px;
         background:#ffffff; color:#0f172a; border:1px solid #e2e8f0; text-decoration:none; font-size:0.9em; }
.badge:hover { background:#f1f5f9; }
.result-card { background-color:#ffffff; border-radius:16px; padding:1.1em 1.3em;
               box-shadow:0 4px 10px rgba(0,0,0,0.05); margin-bottom:1.2em; }
.short-answer { background-color:#f0fdf4; border-left:6px solid #22c55e; padding:1em;
                border-radius:10px; margin-top:12px; }
.toggle-btn { position: fixed; top: 18px; right: 18px; background-color:#334155;
              color:white; border:none; padding:8px 14px; border-radius:10px; cursor:pointer; font-size:0.9em; }
.toggle-btn:hover { background-color:#475569; }
hr{ border:none; height:1px; background:#e2e8f0; margin:18px 0; }
</style>
"""

DARK_THEME = """
<style>
body { background-color:#0f172a; color:#e2e8f0; font-family:'Segoe UI', Roboto, sans-serif; }
.main-title { text-align:center; font-size:2.2em; font-weight:800; color:#e2e8f0; margin:0.2em 0 0.15em; }
.sub-title { text-align:center; color:#94a3b8; font-size:1.05em; margin-bottom:1.2em; }
.header-row { display:flex; justify-content:center; align-items:center; gap:10px; margin-bottom:12px; }
.badge { display:inline-flex; align-items:center; gap:6px; padding:8px 12px; border-radius:999px;
         background:#1f2937; color:#e5e7eb; border:1px solid #334155; text-decoration:none; font-size:0.9em; }
.badge:hover { background:#111827; }
.result-card { background-color:#1e293b; border-radius:16px; padding:1.1em 1.3em;
               box-shadow:0 4px 14px rgba(0,0,0,0.45); margin-bottom:1.2em; }
.short-answer { background-color:#0f766e; border-left:6px solid #14b8a6; color:#ecfeff;
                padding:1em; border-radius:10px; margin-top:12px; }
.toggle-btn { position: fixed; top: 18px; right: 18px; background-color:#e2e8f0;
              color:#0f172a; border:none; padding:8px 14px; border-radius:10px; cursor:pointer; font-size:0.9em; }
.toggle-btn:hover { background-color:#cbd5e1; }
hr{ border:none; height:1px; background:#334155; margin:18px 0; }
</style>
"""

# ---- Tema uygula
if st.session_state["theme"] == "dark":
    st.markdown(DARK_THEME, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_THEME, unsafe_allow_html=True)

# ---- Tema butonu
btn_text = "🌙 Dark Mode" if st.session_state["theme"] == "light" else "☀️ Light Mode"
col_toggle = st.columns([1,1,1])[2]
with col_toggle:
    if st.button(btn_text, key="theme_btn"):
        toggle_theme()
        st.rerun()
st.markdown(f"<button class='toggle-btn'>{btn_text}</button>", unsafe_allow_html=True)

# ---- Başlık ve Sosyal Bağlantılar (ikonlu rozetler)
st.markdown("<div class='main-title'>⚖️ Hukuk Arama Asistanı</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Vikisözlük + Kaggle verileriyle Türkçe hukuk arama ve hızlı yanıtlar</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='header-row'>
      <a class='badge' href='https://github.com/minecaneer/hukuk-arama-asistani' target='_blank'>🧩 GitHub</a>
      <a class='badge' href='https://www.linkedin.com/in/minecaneer' target='_blank'>💼 LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True
)

# ---- Model ve index yükleme
@st.cache_resource
def load_model():
    m = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    m.max_seq_length = 256
    return m

@st.cache_resource
def load_faiss_data():
    if not os.path.exists("faiss_index.bin") or not os.path.exists("texts.pkl"):
        st.error("❌ FAISS index veya texts.pkl bulunamadı. Lütfen önce index'i oluşturup bu klasöre koyun.")
        st.stop()
    index = faiss.read_index("faiss_index.bin")
    with open("texts.pkl", "rb") as f:
        texts = pickle.load(f)
    return index, texts

model = load_model()
index, texts = load_faiss_data()

# ---- Yardımcı fonksiyonlar
def normalize_definition(s: str) -> str:
    s = re.sub(r'^\(\s*hukuk\s*\)\s*', 'Hukukta ', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip(' .')
    if s and not s[0].isupper():
        s = s[0].upper() + s[1:]
    return s

def parse_block(block: str):
    if block.startswith("SOURCE: WIKI"):
        term = re.search(r"TERİM:\s*(.+)", block)
        meanings = re.findall(r"^\-\s*(.+)$", block, flags=re.MULTILINE)
        return {"source":"WIKI","term":term.group(1).strip() if term else "","meanings":[m.strip() for m in meanings]}
    if block.startswith("SOURCE: KAGGLE"):
        q = re.search(r"SORU:\s*(.+)", block)
        a = re.search(r"CEVAP:\s*(.+)", block, flags=re.DOTALL)
        return {"source":"KAGGLE","question":(q.group(1).strip() if q else ""),"answer":(a.group(1).strip() if a else "")}
    return {"source":"UNKNOWN"}

def choose_short_answer(blocks):
    for blk in blocks:
        p = parse_block(blk)
        if p["source"]=="WIKI" and p.get("meanings"):
            title = p.get("term","Terim")
            return f"**{title}**: {normalize_definition(p['meanings'][0])}", "Vikisözlük"
    for blk in blocks:
        p = parse_block(blk)
        if p["source"]=="KAGGLE" and p.get("answer"):
            a = p["answer"]
            return f"**Kısa yanıt:** {a[:400]}{'…' if len(a)>400 else ''}", "Kaggle Q&A"
    return "", ""

def search_query(query, k=5):
    q_emb = model.encode([query], convert_to_numpy=True)
    q_emb = q_emb / np.clip(np.linalg.norm(q_emb, axis=1, keepdims=True), 1e-12, None)
    D, I = index.search(q_emb.astype("float32"), k)
    results = [texts[int(i)] for i in I[0]]
    return results, D[0]

# ---- Ana içerik
query = st.text_input("🔍 Aramak istediğiniz terim veya soru:", placeholder="örn: mülkiyet nedir? / miras paylaşımı nasıl olur?")

if st.button("Ara") or query:
    with st.spinner("Sorgulanıyor..."):
        blocks, scores = search_query(query, k=5)

    short, source_name = choose_short_answer(blocks)
    if short:
        st.markdown(f"<div class='short-answer'>{short}<br><small>📚 Kaynak: {source_name}</small></div>", unsafe_allow_html=True)
    else:
        st.info("Kısa cevap bulunamadı, en yakın sonuçlar aşağıda listelendi.")

    st.subheader("🔎 En İlgili 5 Sonuç")
    for i, (blk, sc) in enumerate(zip(blocks, scores), 1):
        p = parse_block(blk)
        source_label = "Vikisözlük" if p["source"] == "WIKI" else ("Kaggle Q&A" if p["source"] == "KAGGLE" else "Bilinmeyen")
        st.markdown(f"<div class='result-card'><b>#{i}</b> • <i>{source_label}</i> • <small>benzerlik: {sc:.3f}</small><br>", unsafe_allow_html=True)
        if p["source"] == "WIKI":
            st.markdown(f"<b>{p.get('term','(terim)')}</b><br>", unsafe_allow_html=True)
            for m in (p.get("meanings") or [])[:5]:
                st.markdown(f"- {m}")
        elif p["source"] == "KAGGLE":
            st.markdown(f"<b>Soru:</b> {p.get('question','')}<br>", unsafe_allow_html=True)
            a = p.get("answer","")
            st.markdown(f"<b>Cevap:</b> {a[:800]}{'…' if len(a)>800 else ''}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.caption("💡 Veri Kaynakları: Vikisözlük + Kaggle • Model: paraphrase-multilingual-MiniLM-L12-v2")
