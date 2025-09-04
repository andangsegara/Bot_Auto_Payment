from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN, ADMINS, PAYMENT_INFO
from database import init_db, get_conn
from utils import rupiah

# ===== Init DB =====
init_db()

# ===== DB helpers =====
def insert_link(creator_id, title, content, price):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO Link (creator_id, tittle, content, price)VALUES(?.?.?)",
        (creator_id, title, content, price)
    )
    lid = c.lastrowid
    conn.commit()
    conn.close()
    return lid

def get_link(link_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM links WHERE id=?", (link_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def create_order(link_id, buyer_id, amount):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO orders (link_id, buyer_id, amount) VALUES (?, ?, ?)",
        (link_id, buyer_id, amount)
    )
    oid = c.lastrowid
    conn.commit()
    conn.close()
    return oid

def get_order(order_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def mark_paid(order_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE orders SET status='paid', paid_at=CURRENT_TIMESTAMP WHERE id=?",
        (order_id,)
    )
    conn.commit()
    conn.close()

# ===== Handlers =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Halo 👋\nGunakan /help untuk melihat perintah.")
        return
    try:
        link_id = int(args[0])
    except:
        await update.message.reply_text("❌ Link tidak valid.")
        return

    link = get_link(link_id)
    if not link:
        await update.message.reply_text("❌ Link tidak ditemukan.")
        return

    order_id = create_order(link_id, update.message.from_user.id, link["price"])
    text = (
        f"🔒 *{link['title']}*\n"
        f"Harga: {rupiah(link['price'])}\n\n"
        f"{PAYMENT_INFO}\n\n"
        f"ID Order: {order_id}\n"
        f"Setelah admin konfirmasi, gunakan /cek {order_id}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def buatlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in ADMINS:
        await update.message.reply_text("❌ Anda bukan admin.")
        return
    if len(context.args) < 2 or "|" not in " ".join(context.args[1:]):
        await update.message.reply_text("Format: /buatlink <harga> <judul>|<konten>")
        return
    price = int(context.args[0])
    title, content = " ".join(context.args[1:]).split("|", 1)
    link_id = insert_link(update.message.from_user.id, title.strip(), content.strip(), price)
    await update.message.reply_text(
        f"✅ Link dibuat!\nJudul: {title}\nHarga: {rupiah(price)}\nID Link: {link_id}"
    )

async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Format: /cek <order_id>")
        return
    order_id = context.args[0]
    order = get_order(order_id)
    if not order:
        await update.message.reply_text("❌ Order tidak ditemukan.")
        return
    link = get_link(order["link_id"])
    if order["status"] == "paid":
        await update.message.reply_text(
            f"🎉 *{link['title']}*\n\n{link['content']}", parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("⚠️ Order masih pending. Tunggu admin konfirmasi.")

async def markpaid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id not in ADMINS:
        await update.message.reply_text("❌ Hanya admin.")
        return
    if not context.args:
        await update.message.reply_text("Format: /markpaid <order_id>")
        return
    order_id = context.args[0]
    if not get_order(order_id):
        await update.message.reply_text("❌ Order tidak ditemukan.")
        return
    mark_paid(order_id)
    await update.message.reply_text(f"✅ Order {order_id} ditandai PAID.")

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/buatlink <harga> <judul>|<konten> (admin)\n"
        "/cek <order_id> — cek status pembayaran\n"
        "/markpaid <order_id> (admin) — konfirmasi pembayaran"
    )

# ===== Run Bot =====
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("buatlink", buatlink))
app.add_handler(CommandHandler("cek", cek))
app.add_handler(CommandHandler("markpaid", markpaid_handler))
app.add_handler(CommandHandler("help", help_handler))
app.run_polling()
