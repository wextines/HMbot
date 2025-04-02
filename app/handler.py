from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import asyncio
from database import CREATE_INSERT, DELETE_TABLE, init_db, close_db
import time
from app.answers import fetch_keys
import app.keyboards as kb
from config import adminDB

router = Router()

checker = kb.teachBtn

class Student(StatesGroup):
    fullname = State()
    step = State() 
    answers = State()
    right_answers = State()

class Teacher(StatesGroup):
    adding = State()
    deleting = State()

# Асинхронное получение ключей и их подсчёт
async def get_count_keys():
    keys = await fetch_keys()  # Получаем все ключи асинхронно
    return len(keys)



# for teacher 
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if message.from_user.id == adminDB:
        await message.reply('Здравствуйте устоз!\nВыберите действие записями 👇', reply_markup=checker)
    else:
        await message.reply('Привет, нажми на /check чтобы проверить дз!  🚀')
    await state.clear()
@router.callback_query(F.data == 'addData')
async def addData(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Teacher.adding)
    await callback.message.edit_text('Пришлите новый ключ для записи.. ✍️', reply_markup=kb.addMessage)

@router.callback_query(F.data == 'viewDB')
async def addData(callback: CallbackQuery):
    countKeys = await get_count_keys()
    if countKeys == 0:
        await callback.message.answer(text='Ключи отсутствуют', reply_markup=kb.onlyAdd)
    else:
        allKeys = await fetch_keys()
        formatted_keys = [f"{i + 1}. {key}" for i, key in enumerate(allKeys)]
        keys_text = '\n'.join(formatted_keys)
        await callback.message.answer(text=f'🔑 Ключи в Базе данных: \n\n{keys_text}', reply_markup=checker)
    callback.answer()


@router.message(Teacher.adding)
async def finishAdding(message: Message, state: FSMContext):
    await state.update_data(adding=(message.text).upper())
    await init_db()
    await CREATE_INSERT((message.text).upper()) 
    await message.answer('Записи добавлены! ✅\nМожете проверить нажав /check', reply_markup=checker)
    await close_db()
    await state.clear()


@router.callback_query(F.data == 'deleteData')
async def deleteData(callback: CallbackQuery):
    await callback.message.edit_text('Вы действительно хотите удалить ключи? ⚠️', reply_markup=kb.deleteMessage)

@router.callback_query(F.data == 'backData')
async def backData(callback: CallbackQuery, state: FSMContext):
    countKeys = await fetch_keys()  # Получение количество ключей асинхронно
    if countKeys == 0:
        checker = kb.onlyAdd
    else:
        checker = kb.teachBtn
    await callback.message.edit_text('Выберите действие 👇', reply_markup=checker)
    await state.clear()


@router.callback_query(F.data == 'confirmData')
async def backData(callback: CallbackQuery, state: FSMContext):
    await init_db()
    await DELETE_TABLE()
    await callback.message.answer('Записи удалены! ✅', reply_markup=kb.onlyAdd)
    callback.answer()
    await close_db()
    await state.clear()
    

# for students

@router.message(Command('check'))
async def checkStart(message: Message, state: FSMContext):
    countKeys = await get_count_keys()  # Получаем количество ключей асинхронно
    if countKeys == 0:
        await message.answer('На данный момент тестов нету!')
    else:
        await state.set_state(Student.fullname)
        await message.answer('Напиши свое ФИО  💬:')


@router.message(Student.fullname)
async def start_quiz(message: Message, state: FSMContext):
    await state.update_data(fullname=(message.text).title())
    await state.set_state(Student.step)
    unique_id = str(int(time.time() * 1000))  # Уникальный ID на основе времени
    await state.update_data(unique_id=unique_id, right_answers=0)  # Сохраняем уникальный ID
    await message.answer(
        text='Ответьте на вопрос <b>1</b> ❓',
        reply_markup=kb.testKeyboard(unique_id),  # Передаем уникальный ID в клавиатуру
        parse_mode='html'
    )


@router.callback_query(F.data.startswith("answer_"), Student.step)
async def process_key(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    step = data.get("step", 0)
    answers = data.get("answers", [])
    fullname = data.get('fullname')
    unique_id = data.get('unique_id')
    right_answers = data.get("right_answers", 0)

    stiker = '✅'
    answer = callback.data.split("_")[1]
    callback_parts = callback.data.split("_")
    callback_unique_id = callback_parts[2]  # Уникальный ID из callback_data
    answer = callback_parts[1]  # Ответ пользователя (A, B, C, D)

    # Обрабатываем только если уникальный ID совпадает
    if callback_unique_id != unique_id:
        await callback.answer("Это старый вопрос, он больше не актуален!", show_alert=True)
        return

    countKeys = await get_count_keys()  # Получаем количество ключей асинхронно

    # Получаем правильный ответ на текущий вопрос
    keys = await fetch_keys()
    correct_answer = keys[step] if step < countKeys else None

    if correct_answer and answer == correct_answer:
        right_answers += 1
        answers.append(f"{step + 1}: {answer} — ✅")  # Совпадает с правильным ответом
        stiker = '✅'
    else:
        answers.append(f"{step + 1}: {answer} — ❌")
        stiker = '❌'

    step += 1
    await state.update_data(step=step, answers=answers, right_answers=right_answers)

    await callback.answer()

    if step + 1 < countKeys + 1:
        new_unique_id = str(int(time.time() * 1000))  # Новый уникальный ID для следующего вопроса
        await state.update_data(unique_id=new_unique_id)  # Обновляем уникальный ID
        await callback.message.edit_text(text=f'Вопрос <b>{step}</b>\nВаш ответ: {answer} — {stiker}', parse_mode='html')
        await callback.message.answer(
            f'Ответьте на вопрос <b>{step + 1}</b> ❓',
            reply_markup=kb.testKeyboard(new_unique_id),  # Передаем новый уникальный ID
            parse_mode='html')
    else:
        await callback.message.edit_text(text=f'Вопрос <b>{step}</b>\nВаш ответ: {answer} — {stiker}', parse_mode='html')
        results = "\n".join(answers)
        await callback.message.answer(f"Тест завершен!\nРезультаты <i>{fullname}</i>:\n\n{results}\n\n{right_answers}/{countKeys}", parse_mode='html')
        await state.clear()
