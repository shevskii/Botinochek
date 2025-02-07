from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.session_state import Session_State

router = Router()

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer('Привет, спрашивай - помогу :)')
    # data = await state.get_data()

    # if data:
    #     await message.answer('У вас уже есть чат с ботом, вы можете продолжить его или очистить сессию и начать сначала', reply_markup=clear_session())

    # else:
    #     await message.answer('У вас нет открытой сессии с ботом, задайте вопрос!')
    #     await state.set_state(Session_State.session)