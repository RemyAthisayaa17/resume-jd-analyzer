from sentence_transformers import SentenceTransformer
import numpy as np

# -----------------------------
# Load embedding model once
# -----------------------------
# Small, fast, CPU-safe, strong semantic performance
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> np.ndarray:
    """
    Convert a list of texts into L2-normalized semantic embeddings.

    Normalization is critical for cosine similarity to behave correctly.
    """
    if not texts:
        return np.array([])

    embeddings = _model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embeddings
