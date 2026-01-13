from src.search import cosine_similarity, top_k


def test_cosine_similarity_identical_vectors():
    a = [1.0, 0.0, 0.0]
    b = [1.0, 0.0, 0.0]
    assert cosine_similarity(a, b) == 1.0


def test_cosine_similarity_orthogonal_vectors():
    a = [1.0, 0.0]
    b = [0.0, 1.0]
    assert abs(cosine_similarity(a, b)) < 1e-6


def test_top_k_orders_by_score_desc():
    query = [1.0, 0.0]

    items = [
        {"file_path": "a.txt", "text": "A", "embedding": [0.9, 0.1]},
        {"file_path": "b.txt", "text": "B", "embedding": [1.0, 0.0]},
        {"file_path": "c.txt", "text": "C", "embedding": [0.0, 1.0]},
    ]

    results = top_k(query, items, k=2)
    assert results[0][1]["file_path"] == "b.txt"  # best match
    assert results[1][1]["file_path"] == "a.txt"  # second best
