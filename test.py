import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "7846152188:AAGuff2EKF88CYgxdkacPXiDnUP7TsAhVbE"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Класс состояний
class MultiChoice(StatesGroup):
    step = State()  # Текущий шаг
    answers = State()  # Храним ответы пользователя

# Тексты вопросов
questions = [
    "Вопрос 1", "Вопрос 2", "Вопрос 3", "Вопрос 4",
    "Вопрос 5", "Вопрос 6", "Вопрос 7", "Вопрос 8",
    "Вопрос 9", "Вопрос 10"
]

# Генерируем кнопки A, B, C, D
def get_choice_buttons():
    builder = InlineKeyboardBuilder()
    for option in ["A", "B", "C", "D"]:
        builder.button(text=option, callback_data=f"answer_{option}")
    return builder.as_markup()

# Старт: отправляем первый вопрос
@router.message(Command("start"))
async def start_quiz(message: Message, state: FSMContext):
    await state.set_state(MultiChoice.step)
    await state.update_data(step=0, answers=[])  # Обнуляем шаг и список ответов
    await message.answer(questions[0], reply_markup=get_choice_buttons())

# Обработка ответов (A, B, C, D)
@router.callback_query(F.data.startswith("answer_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    step = data.get("step", 0)  # Текущий вопрос
    answers = data.get("answers", [])  # Ответы пользователя

    answer = callback.data.split("_")[1]  # A, B, C или D
    answers.append(f"{step + 1}: {answer}")  # Запоминаем ответ
    await state.update_data(step=step + 1, answers=answers)

    if step + 1 < len(questions):  # Если вопросы еще есть
        await callback.message.answer(questions[step + 1], reply_markup=get_choice_buttons())
    else:  # Если это был последний вопрос
        results = "\n".join(answers)
        await callback.message.answer(f"Тест завершен! Вот твои ответы:\n\n{results}")
        await state.clear()  # Очищаем состояние

# Запуск бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
