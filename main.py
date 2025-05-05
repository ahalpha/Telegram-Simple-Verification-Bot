import configs
import tools.global_variable as config
from telegram import Update, Bot
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from tools.print_info import print_info
from tools.link_md import link_md

from start import start
from verify import verify
from echo import echo
from delete import delete

'''
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
'''

if __name__ == '__main__':
    
    # 检测数据文件是否存在
    try:
        with open("data.json", "r") as f:
            pass
    except FileNotFoundError:
        with open("data.json", 'wb') as f:
            f.write("{\n    \"verified_num\":0,\n    \"fail_num\":0\n}".encode())


    # 配置机器人
    application = ApplicationBuilder().token(config._get("token")).build()
    

    # 执行 /start 命令
    start_handler = CommandHandler('start', start, filters.ChatType.PRIVATE)
    application.add_handler(start_handler)


    # 执行 /verify 命令
    verify_handler = CommandHandler('verify', verify, filters.ChatType.PRIVATE)
    application.add_handler(verify_handler)


    # 执行常规讯息
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.ChatType.PRIVATE, echo)
    application.add_handler(echo_handler)


    # 执行 /delete 命令
    delete_handler = CommandHandler('delete', delete)
    application.add_handler(delete_handler)


    application.run_polling()
