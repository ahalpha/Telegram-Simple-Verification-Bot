import tools.global_variable as config
from telegram import Update, Bot
from telegram.ext import ContextTypes
from tools.print_info import print_info


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print_info( update ) # 输出消息
    
    if update.effective_chat.username == config._get("admin_username"):
        delete_link = ' '.join(context.args)
        link_bot = Bot(config._get("token"))
        print(delete_link)
        await link_bot.revoke_chat_invite_link(chat_id=config._get("group_id"), invite_link=delete_link)