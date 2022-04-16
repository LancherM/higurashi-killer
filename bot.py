"""
Author: Lancher
Project name: 寒蝉杀机器人
Click star if you like it!
蕾娜赛高！
I love Rena forever!
"""
import random
from time import sleep

from mirai import Mirai, WebSocketAdapter, At, GroupMessage, FriendMessage
from mirai.models import NewFriendRequestEvent
from mirai_extensions.trigger import InterruptControl, Filter

import character

# 后面会用到的各种列表
admin = [2498561872, 2210939842, 3281894365, 1206010394, 22808716, 2487483917, 751328746, 2392458028, 675578154, 1712826581]  # 管理员qq
# id_list = random.sample([ 3, 4, 9, 13, 12], 3) + [random.choice([14, 5])] + [6, 10] + random.sample([7, 8, 11], 2) + [1, 2]
# id_list = [1, 2, 3, 14, 7, 11, 6, 13]
# id_list = [1, 14, 11]
# id_list = random.sample([ 3, 4, 9, 13, 12 , 1, 2], 4) + [14] + [random.choice([6, 10])] + random.sample([7, 8, 11], 2)
dog_list = []
hero_list = []
killer_list = []
neutral_list = []
player_list = []  # 玩家列表，字典嵌套数组，这样的结构你喜欢吗
ritsuko_s = []
voter_list = []
choose_list = []
actions = []
satoshi_qq = []
satoshi_id = []

stops_valid = []
protects_valid = []
kills_valid = []
checks_valid = []
kill_rs_valid = []
check_os_valid = []
kill_os_valid = []
kill_oos_valid = []
kill_ss_valid = []
stop_double = [0]

bot = Mirai(
    qq=2497872808,  # 改成你的机器人的 QQ 号
    adapter=WebSocketAdapter(
        verify_key='GraiaxVerifyKey', host='localhost', port=8080
    )
)

inc = InterruptControl(bot)

orders = {
    '1': '第一夜免死。可查验一名角色。可阻止两名玩家行动（限1次）。\n指令：\n查验 A  效果：查验编号为A的玩家的阵营  例子：查验 1\n阻止 A B  效果：阻止编号为A和编号为B的玩家  例子：阻止 3 4',
    '2': '第一夜免死。可查验一名角色。可杀人且无视免死（限1次）。\n指令：\n查验 A  效果：查验编号为A的玩家的阵营  例子：查验 1\n刀 A 效果：无视免死杀掉编号为A的玩家  例子：刀 1',
    '3': '可保护一人令其当晚无敌，允许自保，但不可连续保护同一个人。\n指令：\n保护 A  效果：保护编号为A的玩家  例子：保护 3',
    '4': '可阻止1人当晚行动，但无法连续两天阻止同一个人，该行动裁判会告知被阻止者。\n指令：\n阻止 A  效果：阻止编号为A的玩家  例子：阻止 4',
    '5': '免疫山狗队员【山狗队员杀人指令对赤坂无效，该行动裁判不会提前告知山狗队员】，前两夜免死。\n无主动技能',
    '6': '被票时可亮出律子角色身份牌，当日跳过票人阶段；可杀人。\n指令：\n刀 A 效果：杀掉编号为A的玩家  例子：刀 1\n在投票阶段票数最多即将出局时，可在群内回复 我是律子 以避免出局',
    '7': '可杀人\n指令：\n刀 A 效果：杀掉编号为A的玩家',
    '8': '免死。可阻止一人行动（两天内不可同一人）；队员全部阵亡后可杀人\n指令：\n刀 A 效果：杀掉编号为A的玩家  例子：刀 1\n阻止 A  效果：阻止编号为A的玩家  例子：阻止 3',
    '9': '两条命。\n无主动技能',
    '10': '免死，可杀人。\n指令：\n刀 A 效果：杀掉编号为A的玩家',
    '11': '两条命。详细查验（裁判告知小此木玩家被查验角色的角色牌)(冷却一夜）。可杀人（冷却一夜）\n指令：\n查验 A  效果：查验编号为A的玩家的角色  例子：查验 1\n刀 A 效果：杀掉编号为A的玩家  例子：刀 1',
    '12': '阻止对诗音无效。可杀人（冷却一夜）。\n指令：\n刀 A 效果：杀掉编号为A的玩家  例子：刀 1',
    '13': '第一夜免死，可使自己与另一位玩家当夜无敌（限一次）\n指令：\n保护 A  效果：保护编号为A的玩家  例子：保护 4',
    '14': '可杀人（限一次），详细查验（裁判告知大石玩家被查验角色的角色牌）（冷却一夜）\n指令：\n查验 A  效果：查验编号为A的玩家的角色  例子：查验 1\n刀 A 效果：杀掉编号为A的玩家  例子：刀 1',
    '15': '死后可投票。\n无主动技能',
    '16': '可阻止一人行动（冷却一天）。被查验时显示为主角团。失去全部队友后可杀人。\n指令：\n刀 A 效果：杀掉编号为A的玩家  例子：刀 1\n阻止 A  效果：阻止编号为A的玩家  例子：阻止 3',
    '17': '前两夜免死；可杀两人（限一次）\n指令：\n刀 A B  效果：杀掉编号为A和编号为B的玩家  例子：刀 3 4',
    '18': '第一夜免死；免疫阻止；查验（限一次）；可杀人且无视免死\n指令：\n查验 A  效果：查验编号为A的玩家的阵营  例子：查验 1\n刀 A 效果：无视免死杀掉编号为A的玩家  例子：刀 1',
    '19': '可杀人且无视两条命\n指令：\n刀 A 效果：杀掉编号为A的玩家',
    '20': '可杀人且无视两条命（冷却一天）\n指令：\n刀 A 效果：杀掉编号为A的玩家',
    '21': '两条命，可杀两人（冷却一天）\n指令：\n刀 A 效果：杀掉编号为A的玩家'
}


# 初始化
def init():
    dog_list.clear()
    hero_list.clear()
    killer_list.clear()
    neutral_list.clear()
    player_list.clear()
    ritsuko_s.clear()
    voter_list.clear()
    choose_list.clear()
    actions.clear()
    satoshi_qq.clear()
    satoshi_id.clear()



# 告诉每个玩家自己的id
async def tell_id(event: GroupMessage):
    msg = []
    for player in player_list:
        msg.append(At(player['qq']))
        msg.append(': ' + str(player['id']) + '号\n')
    await bot.send_group_message(event.group.id, msg)


# 分配角色
# 这里绝路要求做伪随机，尽量提高蕾娜处于前几个位置的概率。不过伪随机挺麻烦的，暂时采用真随机
def distribute(id_list):
    random.shuffle(id_list)
    if id_list is not None:
        for x in range(0, len(id_list)):
            player_list[x].update({'character_id': id_list[x], 'tickets': 0})
    get_ability(player_list)


# 分配角色能力
def get_ability(tar):
    for player in tar:
        player.update({'character': character.init(player['character_id'])})  # 数组装字典再装对象，这样的结构你喜欢吗？


# 通知每个人自己的角色
async def tell_character():
    for player in player_list:
        if player['character'].id in [7, 8, 11, 16]:
            dog_list.append(player)
        elif player['character'].id in [1, 2, 3, 4, 9, 12, 13, 15, 17, 18, 19, 20]:
            hero_list.append(player)
            if player['character'].id == 15:
                satoshi_qq.append(player['qq'])
                satoshi_id.append(player['id'])
        elif player['character'].id in [5, 14]:
            neutral_list.append(player)
        elif player['character'].id in [6, 10, 21]:
            killer_list.append(player)
        await bot.send_friend_message(player['qq'],
                                      ['您的角色为', player['character'].name, '\n技能是：',
                                       orders[str(player['character_id'])]])
        sleep(1)


# 告诉山狗队员自己的队友
async def tell_company():
    dog_id = [str(dog['id']) + '号' for dog in dog_list]
    for dog in dog_list:
        await bot.send_friend_message(dog['qq'], ["山狗阵营成员是"] + dog_id)


# 提示选择夜晚行动
async def tell_action():
    for player in player_list:
        await bot.send_friend_message(player['qq'], ["请选择您今晚的行动"])


# 选择夜晚行动
@Filter(FriendMessage)
def choose_action(event: FriendMessage):
    msg = str(event.message_chain)
    params = msg.split(' ')
    if params[0] == '结束' and event.sender.id in admin:
        return ['结束']
    if params[0] == '停止' and event.sender.id in admin:
        return ['停止']
    if params[0] == 'pass':
        choose_list.append(event.sender.id)
        return ['跳过成功', event.sender.id]
    else:
        character_s = character.Character()
        sender_qq = event.sender.id
        sender_id = 0
        for player in player_list:
            if player['qq'] == sender_qq:
                character_s = player['character']
                sender_id = player['id']
        if params[0] in [key for key, value in character_s.abilities.items()]:
            a = character_s.abilities[params[0]]
            res = check_ability(params, a, character_s, sender_id, player_list, dog_list)
            if event.sender.id in choose_list:
                return ['只可提交一次', sender_qq]
            if res == 0:
                choose_list.append(event.sender.id)
                return ['提交成功', sender_qq]
            elif res == 1:
                return ['技能用完啦', sender_qq]
            elif res == 2:
                return ['不可连续两天保护/阻止同一个人', sender_qq]
            elif res == 3:
                return ['不可指定死亡玩家或者未参与游戏玩家', sender_qq]
            elif res == 4:
                return ['队友还没死光，无法使用该技能', sender_qq]
            elif res == 5:
                return ['参数输入错误', sender_qq]
            elif res == 6:
                return ['该技能无法作用于自己', sender_qq]
            elif res == 7:
                return ['技能冷却中', sender_qq]
        else:
            return ['指令错误，请重新输入。', sender_qq]


# 提交指令
def check_ability(params, a, character_s, sender_id, p_l, d_l):
    if len(params) == 1:
        return 5
    for param in range(1, len(params)):
        if not params[param].isdigit():
            return 5
    for param in range(0, len(params)):
        if param != 0 and int(params[param]) not in [player['id'] for player in p_l]:
            return 3
    if a == 'stop_k' and len(params) in [2, 3]:
        if character_s.freeze == 1:
            for x in range(1, len(params)):
                if int(params[x]) == sender_id:
                    return 6
                actions.append({'sender': sender_id, 'receiver': int(params[x]), 'name': 'stop'})
            stop_double[0] = len(params) - 1
            get_player(sender_id)['character'].freeze = 0
            return 0
        else:
            return 1
    elif a == 'check' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6

        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'check'})
        return 0
    elif a == 'check_o' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        elif character_s.cooling['check_o'] > 0:
            return 7
        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'check_o'})
        return 0
    elif a == 'check_r' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if character_s.freeze == 1:
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'check'})
            return 0
        else:
            return 1
    elif a == 'stop' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if character_s.prevent == int(params[1]):
            return 2
        else:
            get_player(sender_id)['character'].prevent = int(params[1])
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'stop'})
            return 0
    elif a == 'protect' and len(params) == 2:
        if character_s.prevent == int(params[1]):
            return 2
        else:
            get_player(sender_id)['character'].prevent = int(params[1])
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'protect'})
            return 0
    elif a == 'kill_r' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if character_s.freeze == 1:
            get_player(sender_id)['character'].freeze = 0
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill_r'})
            return 0
        else:
            return 1
    elif a == 'kill_r5' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill_r'})
        return 0
    elif a == 'kill' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill'})
        return 0
    elif a == 'kill_o' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if character_s.cooling['kill_o'] > 0:
            return 7
        else:
            get_player(sender_id)['character'].cooling['kill_o'] = 2
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill_o'})
            return 0
    elif a == 'kill_oo' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if character_s.freeze == 1:
            get_player(sender_id)['character'].freeze = 0
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill_oo'})
            return 0
        else:
            return 1
    elif a == 'kill_k' and len(params) in [2, 3]:
        if sender_id in [int(params[x]) for x in range(1, len(params))]:
            return 6
        if character_s.freeze == 1:
            get_player(sender_id)['character'].freeze = 0
            for x in range(1, len(params)):
                actions.append({'sender': sender_id, 'receiver': int(params[x]), 'name': 'kill'})
        else:
            return 1
    elif a == 'kill_s' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill_s'})
        return 0
    elif a == 'kill_na' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if character_s.cooling['kill_na'] > 0:
            return 7
        get_player(sender_id)['character'].cooling['kill_na'] = 2
        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill_s'})
        return 0
    elif a == 'kill_ca' and len(params) in [2, 3]:
        if sender_id in [int(params[x]) for x in range(1, len(params))]:
            return 6
        if character_s.cooling['kill_ca'] > 0:
            return 7
        get_player(sender_id)['character'].cooling['kill_na'] = 2
        for x in range(1, len(params)):
            actions.append({'sender': sender_id, 'receiver': int(params[x]), 'name': 'kill'})
        return 0

    elif a == 'stop_h' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if character_s.freeze == 1:
            get_player(sender_id)['character'].freeze = 0
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'protect'})
            actions.append({'sender': sender_id, 'receiver': sender_id, 'name': 'protect'})
            return 0
        else:
            return 1
    elif a == 'kill_t' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        if len(d_l) == 1:
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill'})
            return 0
        else:
            return 4
    elif a == 'stop_n' and len(params) == 2:
        if int(params[1]) == sender_id:
            return 6
        elif character_s.cooling['stop_n'] > 0:
            return 7
        else:
            get_player(sender_id)['character'].cooling['stop_n'] = 2
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'stop'})
            return 0
    else:
        return 5


# 计算结果
def calculate(act):
    stops = [a for a in act if a['name'] == 'stop']
    protects = [a for a in act if a['name'] == 'protect']
    kills = [a for a in act if a['name'] == 'kill']
    kill_rs = [a for a in act if a['name'] == 'kill_r']
    checks = [a for a in act if a['name'] == 'check']
    check_os = [a for a in act if a['name'] == 'check_o']
    kill_os = [a for a in act if a['name'] == 'kill_o']
    kill_oos = [a for a in act if a['name'] == 'kill_oo']
    kill_ss = [a for a in act if a['name'] == 'kill_s']
    times = [0]

    # 阻止效果计算
    def cal_stop(stop_n):
        if times[0] > 100:
            times[0] = 0
            return True
        if get_player(stop_n['receiver'])['character_id'] in [12, 18]:
            return False

        # 得到上一个stop
        def get_last_stop(st):
            for s in stops:
                if s['receiver'] == st['sender']:
                    return s

        if stop_double[0] == 2:
            if get_player(stop_n['sender'])['character_id'] == 1 and get_last_stop(stop_n) is not None:
                return False

        if stop_n['sender'] not in [a['receiver'] for a in stops]:
            return True
        else:
            times[0] += 1
            res = cal_stop(get_last_stop(stop_n))
            return not res

    # 保护效果计算
    def cal_protect(protect_n):
        return protect_n['sender'] not in [stop_n['receiver'] for stop_n in stops_valid]

    # 刀人效果计算，这里强制刀和普通刀一样
    def cal_kill(kill_n):
        if kill_n['sender'] not in [stop_n['receiver'] for stop_n in stops_valid]:
            if kill_n['receiver'] not in [protect_n['receiver'] for protect_n in protects_valid]:
                return True
            else:
                return False
        else:
            return False

    # 查验结果计算
    def cal_check(check_n):
        return check_n['sender'] not in [stop_n['receiver'] for stop_n in stops_valid]

    for stop in stops:
        if cal_stop(stop):
            stops_valid.append(stop)
    for protect in protects:
        if cal_protect(protect):
            protects_valid.append(protect)
    for kill in kills:
        if cal_kill(kill):
            kills_valid.append(kill)
    for kill_r in kill_rs:
        if cal_kill(kill_r):
            kill_rs_valid.append(kill_r)
    for check in checks:
        if cal_check(check):
            checks_valid.append(check)
    for check_o in check_os:
        if cal_check(check_o):
            check_os_valid.append(check_o)
    for kill_o in kill_os:
        if cal_kill(kill_o):
            kill_os_valid.append(kill_o)
    for kill_oo in kill_oos:
        if cal_kill(kill_oo):
            kill_oos_valid.append(kill_oo)
    for kill_s in kill_ss:
        if cal_kill(kill_s):
            kill_ss_valid.append(kill_s)

    stops.clear()
    protects.clear()
    kills.clear()
    kill_rs.clear()
    checks.clear()
    actions.clear()
    check_os.clear()
    kill_os.clear()
    kill_oos.clear()
    kill_ss.clear()


def get_player(i):
    for player in player_list:
        if player['id'] == i:
            return player


# 计算效果
def cal_effect():
    # 蕾娜强制刀
    for player in player_list:
        if player['id'] in [kill_r['sender'] for kill_r in kill_rs_valid]:
            for receiver in player_list:
                if receiver['id'] in [kill_r['receiver'] for kill_r in kill_rs_valid]:
                    receiver['character'].life -= 1

    # 普通刀
    for kill in kills_valid:
        if not (get_player(kill['sender'])['character_id'] == 7 and get_player(kill['receiver'])['character_id'] == 5):
            if not get_player(kill['receiver'])['character'].is_god:
                get_player(kill['receiver'])['character'].life -= 1

    # 冷却刀
    for kill_o in kill_os_valid:
        if not get_player(kill_o['receiver'])['character'].is_god:
            get_player(kill_o['receiver'])['character'].life -= 1

    # 一次性刀
    for kill_oo in kill_oos_valid:
        if not get_player(kill_oo['receiver'])['character'].is_god:
            get_player(kill_oo['receiver'])['character'].life -= 1

    # 两条命刀
    for kill_s in kill_ss_valid:
        if not get_player(kill_s['receiver'])['character'].is_god:
            get_player(kill_s['receiver'])['character'].life -= 2

    protects_valid.clear()
    kills_valid.clear()
    kill_rs_valid.clear()
    kill_os_valid.clear()
    kill_oos_valid.clear()
    kill_ss_valid.clear()


# 通知查验
async def tell_check():
    for check in checks_valid:
        if get_player(check['sender']) is not None and get_player(check['receiver']) is not None:
            camp = get_player(check['receiver'])['character'].camp
            await bot.send_friend_message(get_player(check['sender'])['qq'],
                                          [str(check['receiver']), '号玩家是', camp])
    checks_valid.clear()


# 通知精准查验
async def tell_check_detail():
    for check_o in check_os_valid:
        if get_player(check_o['sender']) is not None and get_player(check_o['receiver']) is not None:
            name = get_player(check_o['receiver'])['character'].name
            await bot.send_friend_message(get_player(check_o['sender'])['qq'],
                                          [str(check_o['receiver']), '号玩家是', name])
    check_os_valid.clear()


# 通知阻止
async def tell_stop():
    for stop in stops_valid:
        if get_player(stop['receiver']) is not None:
            await bot.send_friend_message(get_player(stop['receiver'])['qq'], ['你今晚的行动被阻止了'])
    stop_double[0] = 0
    stops_valid.clear()


# 判定死亡
def judge_death():
    new_death = []
    for player in player_list:
        print('血量', player['character'].life, player['character'].life <= 0)
        if player['character'].life <= 0:
            player['character'].is_alive = False
            new_death.append(player)
            if player in dog_list:
                dog_list.remove(player)
            elif player in hero_list:
                hero_list.remove(player)
            elif player in neutral_list:
                neutral_list.remove(player)
            elif player in killer_list:
                killer_list.remove(player)
    for death in new_death:
        player_list.remove(death)
    return new_death


# 通知死亡
async def tell_result(event: GroupMessage, new_death):
    if len(new_death) == 0:
        await bot.send_group_message(event.group.id, ['昨夜风平浪静，无人死亡'])
    else:
        msg = ['昨夜死亡人数：', str(len(new_death)), '，分别是：\n']
        for death in new_death:
            msg.append(str(death['id']) + '号玩家')
            msg.append(At(death['qq']))
            msg.append('，其身份是' + death['character'].name + '\n')
        await bot.send_group_message(event.group.id, msg)


# 投票
@Filter(GroupMessage)
def vote(event: GroupMessage):
    alive_qq_list = [player['qq'] for player in player_list if player['character'].is_alive] + satoshi_qq
    alive_id_list = [player['id'] for player in player_list if player['character'].is_alive]
    if str(event.message_chain) == '停止' and event.sender.id in admin:
        return ['停止']
    if str(event.message_chain) == '结束' and event.sender.id in admin:
        return ['结束']
    if str(event.message_chain).isdigit():
        if event.sender.id not in alive_qq_list:
            return [At(event.sender.id), ' 抱歉，您已死亡或不是玩家，无法投票']
        elif int(str(event.message_chain)) not in alive_id_list:
            return [At(event.sender.id), ' 抱歉，无法投给不存在或已死亡的玩家']
        elif event.sender.id in voter_list:
            return [At(event.sender.id), ' 抱歉，一人只能投一次票']
        elif get_player(int(str(event.message_chain)))['qq'] == event.sender.id:  # 两层嵌套，这样的代码你喜欢吗
            return [At(event.sender.id), ' 抱歉，无法投给自己']

        elif int(str(event.message_chain)) in alive_id_list:  # int套str，这样的代码你喜欢吗？（滑稽）
            voter_list.append(event.sender.id)
            get_player(int(str(event.message_chain)))['tickets'] += 1
            return [At(event.sender.id), ' 投票成功']
    elif str(event.message_chain) == 'pass':
        if event.sender.id in voter_list:
            return [At(event.sender.id), ' 抱歉，一人只能投一次票']
        elif event.sender.id not in alive_qq_list:
            return [At(event.sender.id), ' 抱歉，您已死亡或不是玩家，无法投票']
        else:
            voter_list.append(event.sender.id)
            return [At(event.sender.id), ' 弃权成功']
    else:
        return []


# 投票结束后判定是否有人淘汰
async def vote_result(event: GroupMessage):
    msg = ''
    vote_list = []
    for player in player_list:
        msg += str(player['id']) + '号玩家的票数是' + str(player['tickets']) + '\n'
        vote_list.append(player['tickets'])
    await bot.send_group_message(event.group.id, msg)
    max_tickets = max(vote_list)
    count = vote_list.count(max_tickets)
    if count > 1:
        await bot.send_group_message(event.group.id, ['有多名玩家票数相同，无结果。'])
    else:
        out_player = player_list[vote_list.index(max_tickets)]
        await bot.send_group_message(event.group.id, [str(out_player['id']), '号玩家', At(out_player['qq']), '得票最多，即将出局。'])
        for player in player_list:
            if player['character_id'] == 6:
                ritsuko_s.append(player)
        if len(ritsuko_s) > 0 and ritsuko_s[0]['qq'] == out_player['qq'] and get_player(ritsuko_s[0]['id'])[
            'character'].freeze == 1:
            if await inc.wait(ritsuko, timeout=60):
                get_player(ritsuko_s[0]['id'])['character'].freeze = 0
                await bot.send_group_message(event.group.id, ['律子玩家使用技能，跳过投票阶段。'])
            else:
                player_list.remove(out_player)
                if out_player in dog_list:
                    dog_list.remove(out_player)
                elif out_player in hero_list:
                    hero_list.remove(out_player)
                elif out_player in neutral_list:
                    neutral_list.remove(out_player)
                elif out_player in killer_list:
                    killer_list.remove(out_player)
                if out_player['character'].id == 16:
                    camp = '山狗'
                else:
                    camp = out_player['character'].camp

                await bot.send_group_message(event.group.id,
                                             [str(out_player['id']), '号玩家', At(out_player['qq']), '已出局。其阵营为',
                                              camp])
        else:
            player_list.remove(out_player)
            if out_player in dog_list:
                dog_list.remove(out_player)
            elif out_player in hero_list:
                hero_list.remove(out_player)
            elif out_player in neutral_list:
                neutral_list.remove(out_player)
            elif out_player in killer_list:
                killer_list.remove(out_player)
            if out_player['character'].id == 16:
                camp = '山狗'
            else:
                camp = out_player['character'].camp
            await bot.send_group_message(event.group.id,
                                         [str(out_player['id']), '号玩家', At(out_player['qq']), '已出局。其阵营为',
                                          camp])
    for player in player_list:
        player.update({'tickets': 0})


# 律子的特殊技能
@Filter(GroupMessage)
def ritsuko(event: GroupMessage):
    if str(event.message_chain) == '我是律子' and event.sender.id == ritsuko_s[0]['qq']:
        return True


# 赤坂特殊技能失效
def disable_akasaka(night):
    if night > 2:
        for player in player_list:
            if player['character_id'] in [5, 17]:
                player['character'].is_god = False


# 羽入特殊技能失效
def disable_hanyuu(night):
    if night > 1:
        for player in player_list:
            if player['character_id'] in [1, 2, 13, 18]:
                player['character'].is_god = False


# 冷却
def cooling_down():
    for player in player_list:
        if player['character_id'] in [11, 12, 14, 16, 20, 21]:
            for key, value in player['character'].cooling.items():
                if player['character'].cooling[key] > 0:
                    player['character'].cooling[key] -= 1


# 判定死亡与确定存活人数。如果有人死亡就把他从player_list中删去
def confirm_alive():
    for player in player_list:
        if not player['character'].is_alive:
            player_list.remove(player)


# 投票后的广播
async def broadcast_alive(event: GroupMessage):
    msg = ['当前存活：\n']
    for player in player_list:
        msg.append(str(player['id']) + '号玩家')
        msg.append(At(player['qq']))
        msg.append('\n')
    await bot.send_group_message(event.group.id, msg)


# 胜利条件
async def victory(event: GroupMessage):
    # 为什么垃圾python没有switch？？？
    # 全是if elif，这样的代码你喜欢吗？
    if len(dog_list) == 0 and len(killer_list) == 0 and len(neutral_list) == 0 and len(hero_list) == 0:
        await bot.send_group_message(event.group.id, ["游戏结束，无人生还，平局。"])
        return False
    elif len(dog_list) == 0 and len(killer_list) == 0 and len(hero_list) == 0:
        await bot.send_group_message(event.group.id, ["游戏结束，胜利者为中立！"])
        return False
    elif len(dog_list) == 0 and len(killer_list) == 0:
        if len(neutral_list) == 0:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为主角团！"])
        else:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为主角团和中立！"])
        return False
    elif len(hero_list) == 0 and len(killer_list) == 0:
        if len(neutral_list) == 0:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为山狗！"])
        else:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为山狗和中立！"])
        return False
    elif len(hero_list) == 0 and len(dog_list) == 0 and len(neutral_list) == 0:
        await bot.send_group_message(event.group.id, ["游戏结束，胜利者为杀人狂！"])
        return False
    elif len(hero_list) == 0 and len(neutral_list) == 0 and len(dog_list) == 1 and len(killer_list) == 1:
        if dog_list[0]['character_id'] == 8 and killer_list[0]['character_id'] == 10:
            await bot.send_group_message(event.group.id, ["游戏结束，鹰野和铁平幸存，平局"])
            return False
        else:
            return True
    else:
        return True


# 主程序
if __name__ == '__main__':
    @bot.on(NewFriendRequestEvent)
    async def allow_request(event: NewFriendRequestEvent):
        await bot.allow(event)


    @bot.on(GroupMessage)
    async def start_game(event: GroupMessage, i=1, night=1):
        #        init()
        if event.sender.id in admin and str(event.message_chain) == '开始游戏 8':
            id_list = random.sample([3, 4, 9, 13, 12, 15, 20], 3) + [14] + [random.choice([6, 10, 21])] + random.sample(
                [7, 8, 11, 16], 2) + [random.choice([1, 2])]
            await bot.send_group_message(event.group.id, "寒蝉杀准备开始，游戏玩法请见群公告。输入 加入 以参与游戏。当前为8人局。不要发表情包！！！")
        elif event.sender.id in admin and str(event.message_chain) == '开始游戏 10':
            id_list = random.sample([3, 4, 9, 13, 12, 15, 20], 3) + [random.choice([14, 5])] + random.sample([6, 10, 21], 2) + random.sample(
                [7, 8, 11, 16], 2) + [1, 2]
            await bot.send_group_message(event.group.id, "寒蝉杀准备开始，游戏玩法请见群公告。输入 加入 以参与游戏。当前为10人局。不要发表情包！！！")
        elif event.sender.id in admin and str(event.message_chain) == '开始游戏 11':
            id_list = random.sample([3, 4, 9, 13, 12, 15, 1, 18, 20], 6) + [random.choice([6, 10, 21])] + random.sample(
                [7, 8, 11, 16], 3) + [random.choice([14, 5])]
            await bot.send_group_message(event.group.id, "寒蝉杀准备开始，游戏玩法请见群公告。输入 加入 以参与游戏。当前为11人局。不要发表情包！！！")
        elif event.sender.id in admin and str(event.message_chain) == '开始游戏 12':
            id_list = random.sample([3, 4, 9, 13, 12, 15, 17, 18, 20], 6) + random.sample([6, 10, 21], 2) + random.sample(
                [7, 8, 11, 16], 3) + [random.choice([14, 5])]
            await bot.send_group_message(event.group.id, "寒蝉杀准备开始，游戏玩法请见群公告。输入 加入 以参与游戏。当前为12人局。不要发表情包！！！")
        elif event.sender.id in admin and str(event.message_chain) == '测试':
            id_list = [4, 8]
            await bot.send_group_message(event.group.id, "寒蝉杀准备开始，游戏玩法请见群公告。输入 加入 以参与游戏。当前为12人局。不要发表情包！！！")
        else:
            return

        while len(player_list) < len(id_list):
            @Filter(GroupMessage)
            def waiter_join(event_n: GroupMessage):
                if str(event_n.message_chain) == '停止' and event_n.sender.id in admin:
                    return 1
                if str(event_n.message_chain) == '加入':
                    if event_n.sender.id in [player['qq'] for player in player_list]:
                        return 0
                    player_list.append({'id': i, 'qq': event_n.sender.id})
                    return event_n.sender.id

            attender_id = await inc.wait(waiter_join)
            if attender_id == 1:
                await bot.send_group_message(event.group.id, ['游戏已停止'])
                init()
                return
            if attender_id == 0:
                await bot.send_group_message(event.group.id, ["请不要重复报名"])
            else:
                i += 1
                await bot.send_group_message(event.group.id,
                                             [At(attender_id), " 报名成功！当前报名人数为：", str(len(player_list))])

        await bot.send_group_message(event.group.id, "人数已凑齐，游戏将在5秒钟后开始！")
        sleep(5)
        await tell_id(event)
        distribute(id_list)
        await tell_character()
        await tell_company()
        while await victory(event):
            await bot.send_group_message(event.group.id, ["第", str(night), "天夜晚开始。"])
            await tell_action()
            for player in player_list:
                if player['character_id'] == 3:
                    print('protectM:', player['character'].prevent)
                if player['character_id'] == 4:
                    print('StopS:', player['character'].prevent)
                if player['character_id'] == 8:
                    print('stopT:', player['character'].prevent)

            while len(choose_list) < len(player_list):
                print(satoshi_qq)
                list1 = await inc.wait(choose_action)
                if list1 == ['停止']:
                    await bot.send_group_message(event.group.id, ['游戏已停止'])
                    init()
                    return
                if list1 == ['结束']:
                    await bot.send_group_message(event.group.id, ['选择阶段结束'])
                    break

                msg1 = list1[0]
                sender_id = list1[1]
                print('choose:', choose_list)
                await bot.send_friend_message(sender_id, msg1)

            choose_list.clear()
            calculate(actions)
            cal_effect()
            for player in player_list:
                if player['character_id'] == 3:
                    print('protectM:', player['character'].prevent)
                if player['character_id'] == 4:
                    print('StopS:', player['character'].prevent)
                if player['character_id'] == 8:
                    print('stopT:', player['character'].prevent)

            await tell_stop()
            new_death = judge_death()
            await tell_check()
            await tell_check_detail()
            print(new_death)
            await tell_result(event, new_death)
            await broadcast_alive(event)

            if not await victory(event):
                break
            await bot.send_group_message(event.group.id, ["进入讨论阶段"])
            sleep(5)
            await bot.send_group_message(event.group.id, ["讨论阶段结束，开始投票。"])
            if len(satoshi_qq) > 0 and get_player(satoshi_id[0]) is None:
                voter = len(player_list) + 1
            else:
                voter = len(player_list)
            while len(voter_list) < voter:
                msg = await inc.wait(vote)
                if msg == ['停止']:
                    await bot.send_group_message(event.group.id, ['游戏已停止'])
                    init()
                    return
                if msg == ['结束']:
                    break
                if not msg == []:
                    await bot.send_group_message(event.group.id, msg)

            await vote_result(event)
            await broadcast_alive(event)
            voter_list.clear()
            night += 1
            disable_akasaka(night)
            disable_hanyuu(night)
            cooling_down()
        init()
        return


    bot.run()
