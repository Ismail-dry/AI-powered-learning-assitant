from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-MiniLM-L6-v2")  # ✅ Uyumlu model
model.save("sbert_model")


