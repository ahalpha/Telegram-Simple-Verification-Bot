import json
import time
import tools.global_variable as config
from telegram import Update, Bot
from telegram.ext import ContextTypes
from tools.print_info import print_info
from tools.link_md import link_md


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print_info( update ) # 输出消息
    with open('data.json', 'r', encoding='utf-8') as data_files: # 读取数据
        data = json.loads(data_files.read())

    if data.get(str(update.effective_chat.id)) is not None: # 如果使用过 /start
        user = data[str(update.effective_chat.id)] # 获取该用户数据
        if user.get("verify_num", 0) > 0 and user.get("verified", False) is not True and user.get("isban", False) is not True: # 是否为进行验证对象

# ==================================== 如果用户回答正确，链接未超过最大数 ====================================

            if update.message.text in config._get("key"): # 回答正确
                user['verified'] = True
                if data['verified_num'] < config._get("verified_max"):
                    try:
                        link_bot = Bot(config._get("token"))
                        user['link'] = (await link_bot.create_chat_invite_link(chat_id=config._get("group_id"), expire_date=time.time()+604800, member_limit=10, name=str(update.effective_chat.id))).invite_link
                        data['verified_num'] += 1
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text = "验证成功，请在链接生成24小时内加入。"
                            +"\n"+ ""
                            +"\n"+ "你的专属链接为：" 
                            +"\n"+f"> *{ await link_md(user.get('link')) }*" 
                            +"\n"+ ""
                            +"\n"+ "_切勿使用此链接邀请多名用户，否则你将被封锁。_",
                            parse_mode = "MarkdownV2"
                        )
                    except:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text = "验证成功，链接生成过于频繁。"
                            +"\n"+ ""
                            +"\n"+ "> *请稍后使用 /verify 生成链接。*",
                            parse_mode = "MarkdownV2"
                        )

# ==================================== 如果用户回答正确，链接已超过最大数 ====================================

                else: # 链接超过最大数
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text = "验证成功，目前邀请配额已达上限。"
                        +"\n"+ ""
                        +"\n"+ "> *请稍后使用 /verify 生成链接。*",
                        parse_mode = "MarkdownV2"
                    )

# ==================================== 如果用户回答错误，存在验证次数 ====================================

            else: # 回答错误
                k = user.get('k',{})
                k[len(k)+1] = update.message.text
                user['k'] = k # 记录回答
                user['verify_num'] -= 1
                if user['verify_num'] != 0:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text =f"验证失败，你还有 `{ str(user.get('verify_num')) }` 次机会。",
                        parse_mode = "MarkdownV2"
                    )

# ==================================== 如果用户回答错误，没有验证次数 ====================================

                else:
                    data['fail_num'] += 1
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text = "验证失败，你已被封锁。"
                        +"\n"+ ""
                        +"\n"+ "原因：`验证超过次数`",
                        parse_mode = "MarkdownV2"
                    )

# ==================================== 通用 ====================================

            data[str(update.effective_chat.id)] = user #保存用户数据
            with open("data.json", 'w', encoding='utf-8') as data_files:
                data_files.write(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':')))