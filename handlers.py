import keyboard

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()
router.message.filter(F.chat.type == "private")


class Question(StatesGroup):
    consent_to_publication = State()
    consent_to_publicity = State()
    ask_question = State()


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(text=f"Здравствуйте, {hbold(message.from_user.full_name)}! Рад, что Вы нашли время на то,"
                              f" чтобы разобраться в себе. Если желаете продолжить - нажимайте на /new."
                         )


@router.message(Command("new"))
async def consent_to_publication(message: Message, state: FSMContext) -> None:
    await state.set_state(Question.consent_to_publication)
    await message.answer(text="Перед тем, как Вы зададите мне вопрос, мне нужно Ваше согласие на публикацию вопроса"
                              " в наш канал после разбора (можно анонимно 🔒).",
                         reply_markup=keyboard.inline_menu_approval
                         )


@router.callback_query(Question.consent_to_publication,
                       F.data == "disagree")
async def disagree_message(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text="Извините 😢, но без Вашего согласия я не могу принять вопрос,"
                                       " так как ответ на него может быть опубликован только в нашем канале."
                                       " Если Вы всё-таки согласны на публикацию вашего вопроса (можно анонимно 🔒)"
                                       " - нажимайте на /new"
                                  )


@router.callback_query(Question.consent_to_publication,
                       F.data == "agree")
async def consent_to_publicity(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Question.consent_to_publicity)
    await callback.message.delete()
    await callback.message.answer(text="И последнее: хотели бы вы остаться анонимным или согласны на публичность?",
                                  reply_markup=keyboard.inline_menu_publicity
                                  )


@router.callback_query(Question.consent_to_publicity,
                       F.data.in_({"publicly", "anonymous"})
                       )
async def ask_question(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Question.ask_question)
    await state.update_data(id=callback.from_user.id, status=callback.data)
    await callback.message.delete()
    await callback.message.answer(text="Отлично! Пожалуйста, задавайте <b>Ваш вопрос</b>. "
                                       "Как только мы на него ответим, Вы получите сюда <b>ссылку</b> на публикацию"
                                       " с разбором Вашего вопроса.",
                                  )


@router.message(Question.ask_question,
                F.text,
                F.text.len() <= 2000,
                F.text.len() >= 20
                )
async def farewell_message(message: Message, state: FSMContext) -> None:
    await state.update_data(question=message.text)
    user_data = await state.get_data()
    await state.clear()
    await message.answer(text="Благодарю за Ваш вопрос, наш <b>специалист</b> в скором времени получит уведомление"
                              " и разберёт Ваш случай. Обычно это занимает до <b>24 часов</b>.\n\n"
                              " Берегите себя и своих близких. Ваша Сова ❤️"
                         )


@router.message(Question.ask_question)
async def question_not_text_message(message: Message) -> None:
    await message.answer("Пожалуйста, введите только текстовый вопрос длинной от 20 до 2000 символов!")


@router.message(F.text)
async def no_command_handler(message: Message) -> None:
    await message.answer(text="Если Вы хотите задать вопрос, используйте команду /new")
