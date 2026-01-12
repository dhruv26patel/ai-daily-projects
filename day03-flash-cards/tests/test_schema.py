from src.schema import TopicSummaryResult, FlashCard


def test_project3_schema_valid_example():
    """
    Unit test for Project 3 schema.
    This test does NOT call the AI.
    It only verifies schema validation works correctly.
    """

    obj = TopicSummaryResult(
        topics=["Machine Learning Basics"], 
        flash_cards=[ 
            FlashCard(
                question="What is overfitting?",
                answer="When a model learns noise instead of the underlying pattern.",
                difficulty="medium",
            ),
            FlashCard(
                question="What is underfitting?",
                answer="When a model is too simple to capture patterns in data.",
                difficulty="easy",
            ),
            FlashCard(
                question="What is regularization?",
                answer="A technique that reduces overfitting by penalizing complexity.",
                difficulty="medium",
            ),
        ],
    )

    # Basic assertions
    assert isinstance(obj.topics, list)
    assert len(obj.topics) >= 1
    assert all(isinstance(t, str) and t for t in obj.topics)

    assert isinstance(obj.flash_cards, list)
    assert len(obj.flash_cards) >= 1

    # Validate each flash card
    for card in obj.flash_cards:
        assert card.question != ""
        assert card.answer != ""
        assert card.difficulty in ["easy", "medium", "hard"]
