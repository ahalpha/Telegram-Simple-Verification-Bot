# 你的机器人 TOKEN
token = "TOKEN"


# 所验证群聊的ID
group_id = -1000000000000
# 你可以使用机器人 @getmyid_bot 获取群聊的ID


# 链接申请最大数量
verified_max = 10


# 你的用户名
admin_username = "Aleph_Studio"
# 用于移除由机器人生成的邀请链接 (非必要)
# 用法 '/delete {链接}'


# 是否记录消息
islogmessages = True


# 输入 /start 提示
rule = ( "*请注意你将会进入* `频道` *||__\(这个分区\)__||*"
+ "\n" + ""
+ "\n" + "||*频道* \- 主要包括你会进入这个频道。||"
+ "\n" + ""
+ "\n" + "||而__进入__：代表你同意这些规则。||"
+ "\n" + ""
+ "\n" + "同意这条规则 XXXXXXXXX ，"
+ "\n" + "同意这些规则 XXXXXXXXX ，"
+ "\n" + "同意所有规则 XXXXXXXXX 。"
+ "\n" + ""
+ "\n" + "*而你，我的朋友。*"
+ "\n" + ""
+ "\n" + "你需要慎重考虑是否进入这里，"
+ "\n" + "进入频道则表示你已阅读并同意以上内容。"
+ "\n" + "提示：你将会回答一个问题"
+ "\n" + "> ||*请了解以上事务后再考虑使用 /verify 继续*||"
)


# 问题
lock = "首先这是个非常有趣的问题？（两个汉字）"


# 答案
key = [ "有趣", "答案" ] # [ "答案A", "答案B", ... ]


# 配置主程序
import tools.global_variable as config
config._init()
config._set("token", token)
config._set("group_id", group_id)
config._set("verified_max", verified_max)
config._set("admin_username", admin_username)
config._set("islogmessages", islogmessages)
config._set("rule", rule)
config._set("lock", lock)
config._set("key", key)