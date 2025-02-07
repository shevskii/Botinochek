from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile, Update
from aiogram.fsm.context import FSMContext
from g4f.client import Client

from random import choice

from keyboards.inline.for_answer import for_answer

import asyncio
from gtts import gTTS
import io

import json


router = Router()

start_message = {"role": "system", "content": "Привет! Ты мой ДРУГ и помощник. Ты девочка, тебя зовут Мэй. Общение исключительно дружелюбное, пока не попрошу иного. отвечай в маркдаун разметке, только так, как поддерживает телеграмм (ты телеграмм бот), то есть без решеток и таблиц. Очень хорошо будет если будешь вставлять уместные шутки и добавлять смайлы из скобок и просто скобки, например пожайлуста))"}
messages=[start_message]
messagess = [
    'ща', 
    "сек", 
    "думаю...", 
    "ща решим", 
    "минутку",
    "мозг загружается...",
    "подожди, щас придумаю",
    "секунду, дружище!",
    "ща-ща, не уходи!",
    "дай мне пару секунд 🤔",
    "копаюсь в мыслях...",
    "ща расчехлю свои знания!",
    "думаю, но это не точно...",
    "секундочку, загружаюсь...",
    "обрабатываю... почти готово!",
    "дай мне время, я же не робот! А, стоп...",
    "ща поколдую над ответом 🧙‍♂️",
    "вспоминаю умные мысли...",
    "я уже близок к ответу!",
    "техническая пауза... и вот!",
    "ща будет, не переключайся!",
    "думать трудно, но я справлюсь!",
]

@router.message(F.text == 'Очистить сессию')
async def question_handler(message: Message, state: FSMContext):
    global messages
    messages = [start_message]  # Оставляем только системное сообщение

    await message.answer("Сессия очищена! Можно начинать заново 😊")

@router.message(F.text)
async def question_handler(message: Message, state: FSMContext):
    client = Client()

    messages.append({"role": "user", "content": {message.text}})

    temp_msg = await message.answer(choice(messagess))

    response = await asyncio.to_thread(client.chat.completions.create,
        model="gpt-4o-mini",
        messages=messages,
        web_search=False
    )

    await message.bot.delete_message(chat_id=message.chat.id, message_id=temp_msg.message_id)
    messages.append({"role": "assistant", "content": response.choices[-1].message.content})
    await message.answer(f'{response.choices[-1].message.content}', reply_markup=await for_answer())

@router.callback_query(F.data == 'clear_session')
async def clear_session(call_data: CallbackQuery, state: FSMContext):
    global messages
    messages = [start_message]  # Оставляем только системное сообщение

    await call_data.message.edit_reply_markup(reply_markup=None)  # Убираем кнопки
    await call_data.answer("Сессия очищена! Можно начинать заново 😊")
    await call_data.answer()

# # Укажи ID чата, куда будет отправляться история
# HISTORY_CHAT_ID = -1002361090126  # Заменить на реальный ID

# @router.callback_query(F.data == "clear_session")
# async def clear_session(call: CallbackQuery):
#     global messages

#     try:
#         history_text = "\n\n".join(
#             [
#                 f"{msg.get('username', 'User')}: {parse_user_message(msg['content'])}"
#                 if msg["role"] == "user"
#                 else f"Мэй: {msg['content']}"
#                 for msg in messages
#                 if msg["role"] != "system"
#             ]
#         )

#         await call.bot.send_message(chat_id=HISTORY_CHAT_ID, text=f"📜 История сессии:\n\n{history_text}")

#     except Exception as e:
#         await call.message.answer(f"Ошибка при отправке истории: {e}")

#     messages = [start_message]
#     await call.message.answer("Сессия очищена! Можно начинать заново 😊")
#     await call.answer()

# def parse_user_message(content):
#     """Функция для корректного отображения сообщений пользователя"""
#     if isinstance(content, (set, list, tuple)):
#         return " ".join(map(str, content))
#     elif isinstance(content, dict):
#         return " ".join(f"{k}: {v}" for k, v in content.items())
#     return str(content)


@router.callback_query(F.data == "not_undestand")
async def explain_answer(call: CallbackQuery):
    # Берем последний ответ
    last_response = next((msg["content"] for msg in reversed(messages) if msg["role"] == "assistant"), None)
    
    if not last_response:
        await call.message.answer("Ошибка: Нет последнего ответа для пояснения.")
        return

    # Отправляем запрос в нейронку, чтобы объяснила ответ проще
    client = Client()
    
    explanation_prompt = f"Поясни, пожалуйста, свой ответ простыми словами: {last_response}"

    response = await asyncio.to_thread(client.chat.completions.create,
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": explanation_prompt}],
        web_search=False
    )

    explanation = response.choices[-1].message.content

    # Отправляем пояснение пользователю
    await call.message.answer(explanation, reply_markup=await for_answer())

@router.callback_query(F.data == "to_voice")
async def send_voice(call: CallbackQuery):
    # Берем последний ответ
    last_response = next((msg["content"] for msg in reversed(messages) if msg["role"] == "assistant"), None)
    
    if not last_response:
        await call.message.answer("Ошибка: Нет последнего ответа для преобразования в голосовое.")
        return

    # Конвертируем текст в речь
    tts = gTTS(text=last_response, lang="ru", slow=False)  # Женский голос по умолчанию
    voice_io = io.BytesIO()
    tts.write_to_fp(voice_io)
    voice_io.seek(0)

    # Отправляем голосовое сообщение
    await call.message.answer_voice(BufferedInputFile(voice_io.getvalue(), filename="voice.ogg"))


@router.errors()
async def error_handler(update: Update, exception: Exception):
    await update.message.answer("Произошла ошибка, попробуй ещё раз 😕")