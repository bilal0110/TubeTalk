import re
import requests
import gradio as gr


API_URL = "http://127.0.0.1:8000"


def extract_video_id(url):
    patterns = [
        r"(?:youtube\.com/watch\?v=)([^&]+)",
        r"(?:youtu\.be/)([^?&]+)",
        r"(?:youtube\.com/shorts/)([^?&]+)",
        r"(?:youtube\.com/embed/)([^?&]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


def process_video(url):
    if not url or not url.strip():
        return (
            "❌ Please enter a YouTube URL.",
            "",
            gr.update(visible=False),
            None,
        )

    url = url.strip()

    video_id = extract_video_id(url)

    if not video_id:
        return (
            "❌ Invalid YouTube URL.",
            "",
            gr.update(visible=False),
            None,
        )

    try:
        response = requests.post(
            f"{API_URL}/yourube_url",
            json={"url": url},
            timeout=600,
        )

        data = response.json()

        if response.status_code != 200:
            return (
                f"❌ API Error: {data}",
                "",
                gr.update(visible=False),
                None,
            )

        if "message" in data:
            message = data["message"]

            if "error" in message.lower():
                return (
                    f"❌ {message}",
                    "",
                    gr.update(visible=False),
                    None,
                )

        video_id = data.get("video_id", video_id)

        return (
            "✅ Video processed successfully!",
            video_id,
            gr.update(
                value=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                visible=True,
            ),
            video_id,
        )

    except requests.exceptions.ConnectionError:
        return (
            "❌ Cannot connect to FastAPI. Make sure port 8000 is running.",
            "",
            gr.update(visible=False),
            None,
        )

    except Exception as e:
        return (
            f"❌ {str(e)}",
            "",
            gr.update(visible=False),
            None,
        )


def ask_question(message, history, video_id):
    if not video_id:
        return (
            history,
            "",
            "⚠️ Please process a YouTube video first.",
        )

    if not message or not message.strip():
        return (
            history,
            "",
            "Please enter a question.",
        )

    message = message.strip()

    try:
        response = requests.post(
            f"{API_URL}/query",
            json={
                "query": message,
                "video_id": video_id,
            },
            timeout=600,
        )

        data = response.json()

        if response.status_code != 200:
            answer = f"❌ API Error: {data}"
        else:
            answer = data.get(
                "message",
                "❌ No answer received from the AI.",
            )

        history = history + [
            {
                "role": "user",
                "content": message,
            },
            {
                "role": "assistant",
                "content": answer,
            },]

        return (
            history,
            "",
            "🟢 Ready",
        )

    except requests.exceptions.ConnectionError:
        return (
            history,
            "",
            "❌ FastAPI is not running on port 8000.",
        )

    except Exception as e:
        return (
            history,
            "",
            f"❌ {str(e)}",
        )


def clear_chat():
    return [], "", "🟢 Ready"


css = """
body {
    background: #0b0d12 !important;
}

.gradio-container {
    max-width: 1100px !important;
    margin: auto !important;
}

#title {
    text-align: center;
    margin-top: 20px;
}

#title h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

#subtitle {
    text-align: center;
    color: #8b93a3;
    margin-bottom: 25px;
}

.panel {
    border-radius: 18px !important;
}

.status {
    border-radius: 12px !important;
}

.process-btn {
    min-width: 150px !important;
}

.chatbot {
    min-height: 450px !important;
}

footer {
    display: none !important;
}
"""


with gr.Blocks(
    title="TubeTalk",
) as demo:

    video_id_state = gr.State(None)

    gr.Markdown(
        """
        # 🎬 TubeTalk
        """,
        elem_id="title",
    )

    gr.Markdown(
        """
        ### Watch less. Ask more.
        Upload a YouTube video and chat with its content using RAG + ChromaDB + Llama 3.2.
        """,
        elem_id="subtitle",
    )

    with gr.Group(elem_classes="panel"):

        gr.Markdown("### 🎥 YouTube Video")

        with gr.Row():

            youtube_url = gr.Textbox(
                label="YouTube URL",
                placeholder="https://www.youtube.com/watch?v=...",
                scale=5,
            )

            process_button = gr.Button(
                "🚀 Process Video",
                variant="primary",
                scale=1,
                elem_classes="process-btn",
            )

        process_status = gr.Markdown(
            "Paste a YouTube URL and click **Process Video**.",
            elem_classes="status",
        )

        video_id_display = gr.Textbox(
            label="Video ID",
            interactive=False,
            visible=False,
        )

        thumbnail = gr.Image(
            label="Video Preview",
            visible=False,
            height=220)

    gr.Markdown("## 💬 Chat with your video")

    with gr.Group(elem_classes="panel"):

        chatbot = gr.Chatbot(
            label="Tube AI",
            height=450,
        )

        with gr.Row():

            question = gr.Textbox(
                placeholder="Ask something about the video...",
                show_label=False,
                scale=6,
            )

            send_button = gr.Button(
                "➤",
                variant="primary",
                scale=1,
            )

        with gr.Row():

            chat_status = gr.Markdown(
                "⚪ Process a video first."
            )

            clear_button = gr.Button(
                "🗑️ Clear Chat",
                scale=0,
            )

    process_button.click(
        fn=process_video,
        inputs=youtube_url,
        outputs=[
            process_status,
            video_id_display,
            thumbnail,
            video_id_state,
        ],
    )

    send_button.click(
        fn=ask_question,
        inputs=[
            question,
            chatbot,
            video_id_state,
        ],
        outputs=[
            chatbot,
            question,
            chat_status,
        ],
    )

    question.submit(
        fn=ask_question,
        inputs=[
            question,
            chatbot,
            video_id_state,
        ],
        outputs=[
            chatbot,
            question,
            chat_status,
        ],
    )

    clear_button.click(
        fn=clear_chat,
        outputs=[
            chatbot,
            question,
            chat_status,
        ],
    )


if __name__ == "__main__":
    demo.launch(
    server_name="0.0.0.0",
    server_port=7861,
    show_error=True,
    css=css,
    theme=gr.themes.Soft(
        primary_hue="red",
        neutral_hue="slate",
    ),
)

