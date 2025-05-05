from datetime import timezone, timedelta
import tools.global_variable as config

def print_info( info ):
    
    global islogmessages

    date = info.effective_message.date.astimezone(timezone(timedelta(hours=8)))

    first_name = info.effective_chat.first_name

    last_name = ""
    if info.effective_chat.last_name is not None:
        last_name = " " + info.effective_chat.last_name

    id = "#" + str(info.effective_chat.id)

    username = ""
    if info.effective_chat.username is not None:
        username = info.effective_chat.username
    
    is_bot = ""
    if info.effective_user.is_bot:
        is_bot = "<Bot>"

    is_premium = ""
    if info.effective_user.is_premium:
        is_premium = "<Premium>"

    text = info.effective_message.text

    # language_code = " --" + info.effective_user.language_code

    # message_id = "#" + str(info.effective_message.message_id)

    print(f"[{str(date)}] {first_name}{last_name}({username}{id}){is_bot}{is_premium}: {text}")

    if config._get("islogmessages"):
        with open(f"messages.log", 'a+', encoding='utf-8') as f:
            f.write(f"[{str(date)}] {first_name}{last_name}({username}{id}){is_bot}{is_premium}: {text}\n")

    return