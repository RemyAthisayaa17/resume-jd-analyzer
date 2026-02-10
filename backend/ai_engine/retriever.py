import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def semantic_match(jd_embeddings: np.ndarray, resume_embeddings: np.ndarray) -> list[float]:
    """
    Compute semantic coverage of Job Description requirements by Resume content.

    Direction is IMPORTANT:
    - Each JD embedding is compared against ALL resume embeddings
    - For each JD requirement, we keep the MAX similarity score
      (i.e. best evidence that the resume satisfies that requirement)

    Returns:
        A list of similarity scores aligned 1:1 with JD chunks
    """

    if jd_embeddings.size == 0 or resume_embeddings.size == 0:
        return []

    similarity_matrix = cosine_similarity(jd_embeddings, resume_embeddings)

    # For each JD requirement, take the best resume match
    best_matches = similarity_matrix.max(axis=1)

    return best_matches.tolist()
