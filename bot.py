import os
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Token yahan se lega - Render pe hum isko set karenge
TOKEN = os.environ.get("BOT_TOKEN", "APNA_TOKEN_YAHAN_DALO")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam Ijaz Bhai! ✅ Bot ON hai!\nKoi stock ka naam bhejo jaise: AAPL, TSLA, BTC-USD")

async def stock_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.strip().upper()
    if symbol.startswith("/"):
        return
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if data.empty:
            await update.message.reply_text(f"{symbol} nahi mila. Sahi symbol bhejo!")
            return
        price = data['Close'].iloc[-1]
        await update.message.reply_text(f"📈 {symbol} ka price: ${price:.2f}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stock_price))
print("Bot starting...")
app.run_polling()
