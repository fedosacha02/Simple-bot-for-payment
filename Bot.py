from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor
BOT_TOKEN = 'Token'
PAYMENTS_PROVIDER_TOKEN_NOT_QIWI = 'Token'
PAYMENTS_PROVIDER_TOKEN_VIA_QIWI = 'Token'
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
# Setup prices
prices = [
    types.LabeledPrice(label='Flour', amount=2500)
]


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Hello! Use /buy_not_qiwi to order one flour not through Qiwi or /buy_via_qiwi so that through qiwi")


async def sample(token, currency, message: types.Message):
    await bot.send_invoice(message.chat.id, title='Flour', description="Would you like to buy flour?", provider_token=token, currency=currency, photo_url='https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/flour-in-bowl-bread-flour-vs-all-purpose-flour-1611940896.jpg', photo_height=512, photo_width=512, photo_size=512, need_phone_number=True, prices=prices, payload='Thank you', max_tip_amount=500, need_name=True, need_email=True)


@dp.message_handler(commands=['buy_not_qiwi'])
async def buy_not_qiwi(message: types.Message):
    await sample(PAYMENTS_PROVIDER_TOKEN_NOT_QIWI, "UAH", message)


@dp.message_handler(commands=['buy_via_qiwi'])
async def buy_qiwi(message: types.Message):
    await sample(PAYMENTS_PROVIDER_TOKEN_VIA_QIWI, "RUB", message)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    await bot.send_message(message.chat.id, 'Thanks for payment! We will proceed your order for `{} {}` as fast as possible! \n Use /buy again to get a Time Machine for your friend!'.format(message.successful_payment.total_amount / 100, message.successful_payment.currency), parse_mode='Markdown')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials. Try to pay again in a few minutes, we need a small rest.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
