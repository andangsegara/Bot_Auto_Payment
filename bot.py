from telegram import Update, LabeledPrice
from telegram.ext import Application, CommandHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters

TOKEN = "ISI_TOKEN_BOTMU"
PROVIDER_TOKEN = "ISI_PROVIDER_TOKEN"  # dari BotFather (Payments)

# Link berbayar (hanya diberikan setelah pembayaran sukses)
PAID_LINK = "https://t.me/your_channel_or_file"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Selamat datang!\n"
        "Ketik /buy untuk membeli akses link berbayar."
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    title = "Akses Premium"
    description = "Beli untuk mendapatkan akses link khusus."
    payload = "custom-payload"
    currency = "USD"
    price = 1  # harga dalam USD
    prices = [LabeledPrice("Akses Premium", price * 100)]  # *100 karena dalam cents

    await context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        PROVIDER_TOKEN,
        currency,
        prices
    )

async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload != "custom-payload":
        await query.answer(ok=False, error_message="Terjadi kesalahan.")
    else:
        await query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"✅ Pembayaran berhasil!\n\nInilah link aksesmu:\n{PAID_LINK}"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    print("Bot berjalan...")
    app.run_polling()

if name == "main":
    main()
