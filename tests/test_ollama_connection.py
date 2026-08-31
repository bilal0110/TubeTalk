from unittest.mock import MagicMock, patch

from services.ollama_connection import detect_language, llama3_model


def test_detect_english():
    question = "What is this video about?"

    assert detect_language(question) == "English"


def test_detect_hindi():
    question = "यह वीडियो किस बारे में है?"

    assert detect_language(question) == "Hindi"


def test_llama3_model_uses_english_instruction():
    fake_response = MagicMock()
    fake_response.choices[0].message.content = (
        "This video is about polarized light."
    )

    with patch(
        "services.ollama_connection.client.chat.completions.create",
        return_value=fake_response,
    ) as mock_create:

        result = llama3_model(
            "What is this video about?",
            ["The video explains polarized light."]
        )

    assert result == "This video is about polarized light."

    messages = mock_create.call_args.kwargs["messages"]
    system_prompt = messages[0]["content"]

    assert "The user's question is in English." in system_prompt
    assert "You MUST answer entirely in English." in system_prompt