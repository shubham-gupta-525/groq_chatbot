

import requests
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()
# =========================
# GROQ API KEY
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# =========================
# Conversation History
# =========================
conversation_history = [
    {
        "role": "system",
        "content": "You are a smart and helpful AI assistant."
    }
]

# =========================
# Chat Function
# =========================
def chat_with_groq(message, model="llama-3.3-70b-versatile"):

    global conversation_history

    conversation_history.append(
        {
            "role": "user",
            "content": message
        }
    )

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": conversation_history,
        "temperature": 0.7
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code == 200:

        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        conversation_history.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        return reply

    else:
        return f"❌ Error {response.status_code}\n{response.text}"


# =========================
# Chat Response Function
# =========================
def respond(message, chat_history):

    reply = chat_with_groq(message)

    chat_history.append(
        {
            "role": "user",
            "content": message
        }
    )

    chat_history.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    return "", chat_history


# =========================
# Clear Chat Function
# =========================
def clear_chat():

    global conversation_history

    conversation_history = [
        {
            "role": "system",
            "content": "You are a smart and helpful AI assistant."
        }
    ]

    return "", []


# =========================
# Custom CSS
# =========================
custom_css = """
body {
    background-color: #0f172a;
}

.gradio-container {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

#chatbot {
    height: 550px;
    border-radius: 15px;
}

footer {
    visibility: hidden;
}

h1 {
    text-align: center;
    font-size: 40px;
    color: white;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 20px;
}
"""

# =========================
# UI
# =========================
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        """
        # 🤖 AI Assistant
        
        <div class="subtitle">
        Powered by Groq + Gradio 🚀
        </div>
        """
    )

    chatbot = gr.Chatbot(
        type="messages",
        elem_id="chatbot",
        bubble_full_width=False
    )

    with gr.Row():

        msg = gr.Textbox(
            placeholder="Type your message here...",
            show_label=False,
            scale=8
        )

        send = gr.Button("Send 🚀", scale=1)

    with gr.Row():

        clear = gr.Button("🗑️ Clear Chat")

    send.click(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )

    msg.submit(
        respond,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    )

    clear.click(
        clear_chat,
        outputs=[msg, chatbot]
    )

# =========================
# Launch App
# =========================
demo.launch()