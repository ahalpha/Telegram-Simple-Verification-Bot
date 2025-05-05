import json
import time
import tools.global_variable as config
from telegram import Update, Bot
from telegram.ext import ContextTypes
from tools.print_info import print_info
from tools.link_md import link_md


async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print_info( update ) # 输出消息
    with open('data.json', 'r', encoding='utf-8') as data_files: # 读取数据
        data = json.loads(data_files.read())

# ==================================== 如果未使用过 /start ====================================

    if data.get(str(update.effective_chat.id)) is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="请优先使用 /start 阅读必要内容。",
            parse_mode = "MarkdownV2"
        )
        
# ==================================== 如果用户被封禁 ====================================

    else:
        user = data[str(update.effective_chat.id)] # 获取该用户数据
        if user.get('isban') is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text = "无法进行验证，你已被封锁。"
                +"\n"+ ""
                +"\n"+f"原因：`{ user.get('isban') }`",
                parse_mode = "MarkdownV2"
            )
        
# ==================================== 如果用户通过验证，并拥有链接 ====================================
            
        elif user.get('verified') is not None:
            if user.get('link', "") != "": 
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text = "你已完成验证，请在链接生成24小时内加入。"
                    +"\n"+ ""
                    +"\n"+ "你的专属链接为：" 
                    +"\n"+f"> *{ await link_md(user.get('link')) }*" 
                    +"\n"+ ""
                    +"\n"+ "_切勿使用此链接邀请多名用户，否则你将被封锁。_",
                    parse_mode = "MarkdownV2"
                )
                
# ==================================== 如果用户通过验证，未拥有链接，但存在剩余配额 ====================================

            else:
                if data['verified_num'] < config._get("verified_max"):
                    try:
                        link_bot = Bot(config._get("token"))
                        user['link'] = (await link_bot.create_chat_invite_link(chat_id=config._get("group_id"), expire_date=time.time()+604800, member_limit=10, name=str(update.effective_chat.id))).invite_link
                        data['verified_num'] += 1
                        data[str(update.effective_chat.id)] = user #保存用户数据
                        with open("data.json", 'w', encoding='utf-8') as data_files:
                            data_files.write(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':')))

                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text = "已生成链接，请在链接生成24小时内加入。"
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
                            text = "你已完成验证，链接生成过于频繁。"
                            +"\n"+ ""
                            +"\n"+ "> *请稍后使用 /verify 生成链接。*",
                            parse_mode = "MarkdownV2"
                        )

# ==================================== 如果用户通过验证，未拥有链接，未存在剩余配额 ====================================

                else:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text = "你已完成验证，目前邀请配额已达上限。"
                        +"\n"+ ""
                        +"\n"+ "> *请稍后使用 /verify 生成链接。*",
                        parse_mode = "MarkdownV2"
                    )   

# ==================================== 如果用户开始验证，无剩余验证次数 ====================================

        elif user.get('verify_num') == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text = "无法进行验证，你已被封锁。"
                +"\n"+ ""
                +"\n"+ "原因：`验证超过次数`",
                parse_mode = "MarkdownV2"
            )

# ==================================== 如果用户开始验证，有剩余验证次数 ====================================

        elif user.get('verify_num') is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text = "验证进行中，你需要正确回答："
                +"\n"+ ""
                +"\n"+f"> { config._get('lock') }"
                +"\n"+ ""
                +"\n"+f"你还有 `{ str(user['verify_num']) }` 次机会。",
                parse_mode = "MarkdownV2"
            )

# ==================================== 如果用户未开始验证，但存在剩余配额 ====================================

        else:
            if data['verified_num'] < config._get("verified_max"):
                user['verify_num'] = 5
                data[str(update.effective_chat.id)] = user #保存用户数据
                with open("data.json", 'w', encoding='utf-8') as data_files:
                    data_files.write(json.dumps(data, ensure_ascii=False, indent=4, separators=(',', ':')))

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text = "验证开始，你需要正确回答："
                    +"\n"+ ""
                    +"\n"+f"> { config._get('lock') }"
                    +"\n"+ ""
                    +"\n"+f"你还有 `{ str(user['verify_num']) }` 次机会。",
                    parse_mode = "MarkdownV2"
                )

# ==================================== 如果用户未开始验证，未存在剩余配额 ====================================

            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text = "目前邀请配额已达上限。"
                    +"\n"+ ""
                    +"\n"+ "> *请稍后使用 /verify 开始验证。*",
                    parse_mode = "MarkdownV2"
                )