import json
import tools.global_variable as config
from telegram import Update
from telegram.ext import ContextTypes
from tools.print_info import print_info


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print_info( update ) # 输出消息
    with open('data.json', 'r', encoding='utf-8') as data_files: # 读取数据
        data = json.loads(data_files.read())

# ==================================== 如果未使用过 /start ====================================

    if data.get(str(update.effective_chat.id)) is None:
        new_user = {}
        new_user['id'] = len(data)-1
        new_user['username'] = update.effective_chat.username
        new_user['first_name'] = update.effective_chat.first_name
        new_user['last_name'] = update.effective_chat.last_name

        data[str(update.effective_chat.id)] = new_user # 保存用户数据
        with open("data.json", 'w', encoding='utf-8') as data_files:
            data_files.write(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':')))

# ==================================== 通用 ====================================

    await context.bot.send_message( # 发送规则
        chat_id=update.effective_chat.id,
        text=config._get("rule"),
        parse_mode = "MarkdownV2"
    )