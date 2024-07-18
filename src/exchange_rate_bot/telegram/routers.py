from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters.command import CommandStart, Command, CommandObject
from aiogram.types.message import Message
from dishka.integrations.aiogram import inject, FromDishka

from exchange_rate_bot.usecases.get_all_rates import GetAllRates, GetAllRatesError
from exchange_rate_bot.usecases.convert_currency import ConvertCurrency, ConvertCurrencyError, CurrencyNotFoundError
from exchange_rate_bot.usecases.update_rates import KickUpdateRates, UpdateRatesError

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('Привет. Я знаю актуальные курсы валют от ЦБ РФ и даже умею их конвертировать.')


@router.message(Command(commands=['rates']))
@inject
async def rates_handler(
    message: Message,
    *,
    get_all_rates: FromDishka[GetAllRates],
):
    rates = await get_all_rates()
    text = ''
    for currency in rates:
        text += f' • <code>{currency.char_code}</code> ({currency.name}): <code>{currency.value}</code> (за {currency.nominal})\n'
    await message.answer(text, parse_mode=ParseMode.HTML)


@router.message(Command(commands=['exchange']))
@inject
async def exchange_handler(
    message: Message,
    command: CommandObject,
    *,
    convert_currency: FromDishka[ConvertCurrency],
):
    args = command.args.split(' ')
    if len(args) == 0:
        return await message.answer(
            'Формат аргументов: CUR [CUR [AMOUNT]]\n'
            'Например, USD или USD EUR или USD RUB 10'
        )
    if len(args) == 1:
        from_currency = args[0]
        to_currency = 'RUB'
        amount = 1
    elif len(args) == 2:
        from_currency = args[0]
        to_currency = args[1]
        amount = 1
    elif len(args) == 3:
        from_currency = args[0]
        to_currency = args[1]
        try:
            amount = float(args[2])
        except ValueError:
            return await message.answer(
                'Некорректный формат\n'
                'Формат аргументов: CUR [CUR [AMOUNT]]\n'
                'Например, USD или USD EUR или USD RUB 10'
            )
    else:
        return await message.answer(
            'Некорректный формат\n'
            'Формат аргументов: CUR [CUR [AMOUNT]]\n'
            'Например, USD или USD EUR или USD RUB 10'
        )
    try:
        result = await convert_currency(from_currency, to_currency, amount)
    except CurrencyNotFoundError:
        return await message.answer('Неправильный код валюты. Узнать допустимые коды можно командой /rates')
    return await message.answer(
        text=f'{amount} <code>{from_currency}</code> ≈ {result:.2f} <code>{to_currency}</code>',
        parse_mode=ParseMode.HTML,
    )


@router.message(Command(commands=['update']))
@inject
async def exchange_handler(
    message: Message,
    *,
    kick_update_rates: FromDishka[KickUpdateRates],
):
    try:
        await kick_update_rates(requested_by=message.from_user.id)
    except UpdateRatesError:
        return await message.answer('Что-то пошло не так')
    return await message.answer('Команда на обновление курсов валют отправлена')

