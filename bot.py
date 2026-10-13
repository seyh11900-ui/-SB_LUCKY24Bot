import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables (Railway provides PORT and token configurations)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # Set your Telegram user ID here for admin actions

# Simple in-memory user subscription database simulation (Use PostgreSQL/MongoDB for production)
subscribers = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with subscription options and main menu."""
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("⚽ View Today's Free Tips", callback_data="free_tips")],
        [InlineKeyboardButton("⭐ VIP Subscription Plans", callback_data="vip_plans")],
        [InlineKeyboardButton("👤 My Account Status", callback_data="account_status")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"Hello, <b>{user.first_name}</b>! 👋\n\n"
        "Welcome to the <b>Pro Football Tips Bot</b>.\n"
        "Get daily high-accuracy match predictions, analysis, and VIP accumulator slips.\n\n"
        "Choose an option below:"
    )
    await update.message.reply_html(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button clicks."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id

    if query.data == "free_tips":
        tips_text = (
            "<b>⚽ Today's Free Football Tips:</b>\n\n"
            "1️⃣ <b>Premier League</b>\n"
            "Match: Arsenal vs. Chelsea\n"
            "Tip: Both Teams to Score (BTTS) @ 1.75\n"
            "Confidence: 🟢🟢🟢⚪⚪ (3/5)\n\n"
            "2️⃣ <b>La Liga</b>\n"
            "Match: Real Madrid vs. Valencia\n"
            "Tip: Real Madrid to Win & Over 1.5 @ 1.60\n"
            "Confidence: 🟢🟢🟢🟢⚪ (4/5)"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        await query.edit_message_text(text=tips_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "vip_plans":
        vip_text = (
            "<b>⭐ VIP Subscription Packages:</b>\n\n"
            "Unlock daily VIP slips, 90+ accuracy accumulator codes, and live insider updates!\n\n"
            "• <b>1 Week Pass:</b> $10\n"
            "• <b>1 Month Pass:</b> $30 <i>(Best Value)</i>\n"
            "• <b>Season Pass:</b> $120\n\n"
            "To subscribe, click below to contact management and complete payment:"
        )
        keyboard = [
            [InlineKeyboardButton("💳 Pay / Subscribe Now", url="https://t.me/YourAdminUsername")],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text(text=vip_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "account_status":
        is_vip = user_id in subscribers
        status_str = "⭐ VIP Member (Active)" if is_vip else "🆓 Free Tier User"
        account_text = (
            f"<b>👤 Account Information:</b>\n\n"
            f"• <b>User ID:</b> <code>{user_id}</code>\n"
            f"• <b>Status:</b> {status_str}\n\n"
            f"<i>Upgrade to VIP to access exclusive picks!</i>"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]]
        await query.edit_message_text(text=account_text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "main_menu":
        keyboard = [
            [InlineKeyboardButton("⚽ View Today's Free Tips", callback_data="free_tips")],
            [InlineKeyboardButton("⭐ VIP Subscription Plans", callback_data="vip_plans")],
            [InlineKeyboardButton("👤 My Account Status", callback_data="account_status")]
        ]
        await query.edit_message_text(
            text="<b>Main Menu:</b> Choose an option below:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def grant_vip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin command to grant VIP access: /grant <user_id>"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ You are not authorized to use this command.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /grant [telegram_user_id]")
        return

    try:
        target_id = int(context.args[0])
        subscribers.add(target_id)
        await update.message.reply_text(f"✅ Successfully granted VIP access to user {target_id}.")
        
        # Optionally notify the user
        await context.bot.send_message(
            chat_id=target_id,
            text="🎉 <b>Your VIP Subscription has been activated!</b> Check back to access VIP areas.",
            parse_mode="HTML"
        )
    except ValueError:
        await update.message.reply_text("❌ Invalid User ID format. Must be an integer.")

def main() -> None:
    """Start the bot."""
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN environment variable found!")
        return

    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("grant", grant_vip))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Start polling
    logger.info("Bot is starting up...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
