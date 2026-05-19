import uuid
from pathlib import Path

import chainlit as cl

from bracelet_api.database import async_session_factory
from bracelet_api.models import ChatConversation, ChatMessage
from agents.coordinator import Coordinator

coordinator = Coordinator()


@cl.on_chat_start
async def start():
    conversation_id = str(uuid.uuid4())
    cl.user_session.set("conversation_id", conversation_id)

    async with async_session_factory() as session:
        session.add(ChatConversation(id=conversation_id))
        await session.commit()

    await cl.Message(
        content=(
            "Bun venit! Sunt asistentul IoT pentru brățări de monitorizare. "
            "Îmi poți cere informații despre:\n"
            "- **Locații GPS** ale dispozitivelor\n"
            "- **Starea de sănătate** (puls, SpO2)\n"
            "- Trimiterea de **alerte** pe Discord\n\n"
            "Cu ce te pot ajuta?"
        )
    ).send()


@cl.on_message
async def main(message: cl.Message):
    conversation_id = cl.user_session.get("conversation_id")

    data = await cl.make_async(coordinator.route)(message.content)
    answer = await cl.make_async(coordinator.generate)(message.content, data)

    async with async_session_factory() as session:
        session.add_all([
            ChatMessage(
                conversation_id=conversation_id,
                role="user",
                content=message.content,
            ),
            ChatMessage(
                conversation_id=conversation_id,
                role="assistant",
                content=answer,
            ),
        ])
        await session.commit()

    await cl.Message(content=answer).send()


def main():
    import subprocess
    import sys
    subprocess.run(
        [sys.executable, "-m", "chainlit", "run", "src/agents/chainlit_app.py"],
        cwd=Path(__file__).resolve().parents[2],
    )
