import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# កំណត់ Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ទាញយក BOT_TOKEN ពី Environment
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """មុខងារសម្រាប់បញ្ជា /start"""
    keyboard = [
        [InlineKeyboardButton("⭐ កញ្ចប់សេវាកម្ម (Subscriptions)", callback_data="menu_subscription")],
        [InlineKeyboardButton("💵 ឧបត្ថម្ភ / Tip Us", callback_data="menu_tips")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 **សូមស្វាគមន៍!**\n\nសូមជ្រើសរើសជម្រើសខាងក្រោម ដើម្បីមើលកញ្ចប់សេវាកម្ម ឬឧបត្ថម្ភដល់យើងខ្ញុំ៖",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """មុខងារសម្រាប់ចុចប៊ូតុង Inline Keyboard"""
    query = update.callback_query
    await query.answer()

    data = query.data

    # --- ម៉ឺនុយមេ ---
    if data == "menu_subscription":
        keyboard = [
            [InlineKeyboardButton("🥉 ប្រចាំខែ - $5/ខែ", callback_data="sub_monthly")],
            [InlineKeyboardButton("🥇 ប្រចាំឆ្នាំ - $50/ឆ្នាំ (ចំណេញ 17%)", callback_data="sub_yearly")],
            [InlineKeyboardButton("🔙 ម៉ឺនុយដើម", callback_data="menu_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "⭐ **សូមជ្រើសរើសកញ្ចប់សេវាកម្ម (Subscription):**\n\nដើម្បីទទួលបានសិទ្ធិប្រើប្រាស់ពេញលេញ និងមុខងារពិសេសៗ។",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    elif data == "menu_tips":
        keyboard = [
            [InlineKeyboardButton("☕ Tip $1", callback_data="tip_1")],
            [InlineKeyboardButton("🍕 Tip $5", callback_data="tip_5")],
            [InlineKeyboardButton("🚀 Tip $10", callback_data="tip_10")],
            [InlineKeyboardButton("🔙 ម៉ឺនុយដើម", callback_data="menu_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "💵 **សូមជ្រើសរើសទំហំទឹកប្រាក់ឧបត្ថម្ភ (Tip):**\n\nសូមអរគុណសម្រាប់ការគាំទ្រដល់ការអភិវឌ្ឍន៍របស់យើងខ្ញុំ!",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    # --- ឆ្លើយតបពេលជ្រើសរើស SUB ---
    elif data in ["sub_monthly", "sub_yearly"]:
        plan = "ប្រចាំខែ ($5)" if data == "sub_monthly" else "ប្រចាំឆ្នាំ ($50)"
        keyboard = [[InlineKeyboardButton("🔙 ត្រឡប់ទៅកញ្ចប់សេវាកម្ម", callback_data="menu_subscription")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"✅ **អ្នកបានជ្រើសរើស៖** {plan}\n\n"
            f"💳 *ដើម្បីបន្តការទូទាត់ប្រាក់ សូមទាក់ទងផ្នែកគាំទ្រ ឬធ្វើការទូទាត់តាមតំណភ្ជាប់ (Payment Link)។*",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    # --- ឆ្លើយតបពេលជ្រើសរើស TIP ---
    elif data.startswith("tip_"):
        amount = data.split("_")[1]
        keyboard = [[InlineKeyboardButton("🔙 ត្រឡប់ទៅការឧបត្ថម្ភ", callback_data="menu_tips")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"💖 **សូមអរគុណសម្រាប់ការឧបត្ថម្ភចំនួន ${amount}!**\n\n"
            f"សូមបន្តធ្វើការទូទាត់ប្រាក់ដើម្បីបន្តការគាំទ្ររបស់អ្នក។",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )

    # --- ត្រឡប់ទៅម៉ឺនុយមេ ---
    elif data == "menu_main":
        keyboard = [
            [InlineKeyboardButton("⭐ កញ្ចប់សេវាកម្ម (Subscriptions)", callback_data="menu_subscription")],
            [InlineKeyboardButton("💵 ឧបត្ថម្ភ / Tip Us", callback_data="menu_tips")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "👋 **សូមស្វាគមន៍!**\n\nសូមជ្រើសរើសជម្រើសខាងក្រោម ដើម្បីមើលកញ្ចប់សេវាកម្ម ឬឧបត្ថម្ភដល់យើងខ្ញុំ៖",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )


def main():
    if not BOT_TOKEN:
        logger.error("មិនទាន់កំណត់ BOT_TOKEN ក្នុង Environment Variables ទេ!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot កំពុងដំណើរការ...")
    app.run_polling()


if __name__ == "__main__":
    main()
