"""
Author: Lancher
Project name: 寒蝉杀机器人
Click star if you like it!
蕾娜赛高！
I love Rena forever!
"""
import asyncio
import nest_asyncio
import random
from time import sleep

from mirai import Mirai, WebSocketAdapter, At, GroupMessage, TempMessage
from mirai_extensions.trigger import InterruptControl, Filter

import character

nest_asyncio.apply()

# 后面会用到的各种列表
admin = [2498561872]  # 管理员qq
id_list = [1, 8]
dog_list = []
hero_list = []
killer_list = []
neutral_list = []
player_list = []  # 玩家列表，字典嵌套数组，这样的结构你喜欢吗
ritsuko_qq = []
voter_list = []
choose_list = []
actions = []

stops_valid = []
protects_valid = []
kills_valid = []
checks_valid = []
kill_rs_valid = []

bot = Mirai(
    qq=2497872808,  # 改成你的机器人的 QQ 号
    adapter=WebSocketAdapter(
        verify_key='GraiaxVerifyKey', host='localhost', port=8080
    )
)

inc = InterruptControl(bot)


# 告诉每个玩家自己的id
async def tell_id(event: GroupMessage):
    msg = []
    for player in player_list:
        msg.append(At(player['qq']))
        msg.append(': ' + str(player['id']) + '号\n')
    await bot.send_group_message(event.group.id, msg)


# 分配角色
# 这里绝路要求做伪随机，尽量提高蕾娜处于前几个位置的概率。不过伪随机挺麻烦的，暂时采用真随机
def distribute():
    random.shuffle(id_list)
    for x in range(0, 2):
        player_list[x].update({'character_id': id_list[x], 'tickets': 0})
    get_ability(player_list)


# 分配角色能力
def get_ability(tar):
    for player in tar:
        player.update({'character': character.init(player['character_id'])})  # 数组装字典再装对象，这样的结构你喜欢吗？


# 通知每个人自己的角色
async def tell_character(event: GroupMessage):
    for player in player_list:
        if player['character'].id > 6:
            dog_list.append(player)
        elif player['character'].id < 5:
            hero_list.append(player)
        elif player['character'].id == 5:
            neutral_list.append(player)
        elif player['character'].id == 6:
            killer_list.append(player)
        await bot.send_temp_message(player['qq'], event.group.id, ['您的角色为', player['character'].name])


# 告诉山狗队员自己的队友
async def tell_company(event: GroupMessage):
    await bot.send_temp_message(dog_list[0]['qq'], event.group.id, ["您的队友是", str(dog_list[1]['id']), "号"])
    await bot.send_temp_message(dog_list[1]['qq'], event.group.id, ["您的队友是", str(dog_list[0]['id']), "号"])


# 提示选择夜晚行动
async def tell_action(event: GroupMessage):
    for player in player_list:
        await bot.send_temp_message(player['qq'], event.group.id, ["请选择您今晚的行动"])


# 选择夜晚行动
@Filter(TempMessage)
def choose_action(event: TempMessage):
    msg = str(event.message_chain)
    params = msg.split(' ')
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
            if res == 0:
                choose_list.append(event.sender.id)
                return ['提交成功', sender_qq]
            elif res == 1:
                return ['技能用完啦', sender_qq]
            elif res == 2:
                return ['不可连续两天保护同一个人', sender_qq]
            elif res == 3:
                return ['不可指定死亡玩家或者未参与游戏玩家', sender_qq]
            elif res == 4:
                return ['队友还没死光，无法使用该技能', sender_qq]
            elif res == 5:
                return ['参数输入错误', sender_qq]
        else:
            return ['指令错误，请重新输入。', sender_qq]


# 提交指令
def check_ability(params, a, character_s, sender_id, p_l, d_l):
    for param in range(0, len(params)):
        if param != 0 and int(params[param]) not in [player['id'] for player in p_l]:
            return 3
    if a == 'stop_k' and len(params) in [2, 3]:
        if character_s.freeze == 1:
            for x in range(1, len(params)):
                actions.append({'sender': sender_id, 'receiver': int(params[x]), 'name': 'stop'})
                return 0
        else:
            return 1
    elif a == 'check' and len(params) == 2:
        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'check'})
        return 0
    elif a == 'stop' and len(params) == 2:
        if character_s.prevent == int(params[1]):
            return 2
        else:
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'stop'})
            return 0
    elif a == 'protect' and len(params) == 2:
        if character_s.prevent == int(params[1]):
            return 2
        else:
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'protect'})
            return 0
    elif a == 'kill_r' and len(params) == 2:
        if character_s.freeze == 1:
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill_r'})
            return 0
        else:
            return 1
    elif a == 'kill' and len(params) == 2:
        actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill'})
        return 0
    elif a == 'kill_t' and len(params) == 2:
        if len(d_l) == 1:
            actions.append({'sender': sender_id, 'receiver': int(params[1]), 'name': 'kill'})
            return 0
        else:
            return 4
    else:
        return 5


# 计算结果
def calculate(act):
    stops = [a for a in act if a['name'] == 'stop']
    protects = [a for a in act if a['name'] == 'protect']
    kills = [a for a in act if a['name'] == 'kill']
    kill_rs = [a for a in act if a['name'] == 'kill_r']
    checks = [a for a in act if a['name'] == 'check']

    # 阻止效果计算
    def cal_stop(stop_n):
        # 得到上一个stop
        def get_last_stop(st):
            for s in stops:
                if s['receiver'] == st['sender']:
                    return s

        if stop_n['sender'] not in [a['receiver'] for a in stops]:
            return True
        else:
            res = cal_stop(get_last_stop(stop_n))
            return not res

    # 保护效果计算
    def cal_protect(protect_n):
        return protect_n['sender'] not in [stop_n['receiver'] for stop_n in stops_valid]

    # 刀人效果计算，这里强制刀和普通刀一样
    def cal_kill(kill_n):
        return kill_n['sender'] not in [stop_n['receiver'] for stop_n in stops_valid] \
               and kill_n['sender'] not in [protect_n['receiver'] for protect_n in protects_valid]

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
    stops.clear()
    protects.clear()
    kills.clear()
    kill_rs.clear()
    checks.clear()
    actions.clear()


def get_player(i):
    for player in player_list:
        if player['id'] == i:
            return player


# 计算效果
def cal_effect():
    # 圭一阻止
    for player in player_list:
        if player['id'] in [stop['sender'] for stop in stops_valid]:
            player['character'].freeze = 0
    # 蕾娜强制刀
    for player in player_list:
        if player['id'] in [kill_r['sender'] for kill_r in kill_rs_valid]:
            player['character'].freeze -= 1
            for receiver in player_list:
                if receiver['id'] in [kill_r['receiver'] for kill_r in kill_rs_valid]:
                    receiver['character'].life -= 1

    # 普通刀
    for kill in kills_valid:
        if not (get_player(kill['sender'])['character_id'] >= 6 and get_player(kill['receiver'])['character_id'] == 5):
            if not get_player(kill['receiver'])['character'].is_god:
                get_player(kill['receiver'])['character'].life -= 1

    protects_valid.clear()
    kills_valid.clear()
    kill_rs_valid.clear()


# 通知查验
async def tell_check(event: GroupMessage):
    for check in checks_valid:
        camp = get_player(check['receiver'])['character'].camp
        await bot.send_temp_message(get_player(check['sender'])['qq'], event.group.id, [str(check['receiver']), '号玩家是', camp])
    checks_valid.clear()


# 通知阻止
async def tell_stop(event: GroupMessage):
    for stop in stops_valid:
        await bot.send_temp_message(get_player(stop['receiver'])['qq'], event.group.id, ['你今晚的行动被阻止了'])
    stops_valid.clear()


# 判定死亡
def judge_death():
    new_death = []
    for player in player_list:
        if player['character'].life == 0:
            player['character'].is_alive = False
            new_death.append(player)
            player_list.remove(player)
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
    alive_qq_list = [player['qq'] for player in player_list if player['character'].is_alive]
    alive_id_list = [player['id'] for player in player_list if player['character'].is_alive]
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
            player_list[int(str(event.message_chain)) - 1]['tickets'] += 1
            return [At(event.sender.id), ' 投票成功']
    elif str(event.message_chain) == 'pass':
        voter_list.append(event.sender.id)
        return [At(event.sender.id), ' 弃权成功']


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
        await bot.send_group_message(event.group.id, [str(out_player['id']), '号玩家得票最多，即将出局。'])
        for player in player_list:
            if player['character_id'] == 6:
                ritsuko_qq.append(player['qq'])
        if not ritsuko_qq and ritsuko_qq[0] == out_player['qq']:
            if await inc.wait(ritsuko, timeout=60):
                await bot.send_group_message(event.group.id, ['律子玩家使用技能，跳过投票阶段。'])
            else:
                player_list.remove(out_player)
                await bot.send_group_message(event.group.id, [str(out_player['id']), '号玩家已出局。'])
        else:
            player_list.remove(out_player)
            await bot.send_group_message(event.group.id, [str(out_player['id']), '号玩家已出局。'])
    for player in player_list:
        player.update({'tickets': 0})


# 律子的特殊技能
@Filter(GroupMessage)
def ritsuko(event: GroupMessage):
    if str(event.message_chain) == '我是律子' and event.sender.id == ritsuko_qq[0]:
        return True


# 赤坂特殊技能失效
def disable_akasaka(night):
    if night > 2:
        for player in player_list:
            if player['character_id'] == 5:
                player['character'].is_god = False


# 判定死亡与确定存活人数。如果有人死亡就把他从player_list中删去
def confirm_alive():
    for player in player_list:
        if not player['character'].is_alive:
            player_list.remove(player)


# 投票后的广播
async def broadcast_alive(event: GroupMessage):
    msg = '当前存活：\n'
    for player in player_list:
        msg += str(player['id']) + '号玩家\n'
    await bot.send_group_message(event.group.id, msg)


# 胜利条件
async def victory(event: GroupMessage):
    # 为什么垃圾python没有switch？？？
    # 全是if elif，这样的代码你喜欢吗？
    if len(dog_list) == 0 and len(killer_list) == 0 and len(neutral_list) == 0 and len(hero_list) == 0:
        await bot.send_group_message(event.group.id, ["游戏结束，无人生还，平局。"])
    elif len(dog_list) == 0 and len(killer_list) == 0 and len(hero_list) == 0:
        await bot.send_group_message(event.group.id, ["游戏结束，胜利者为赤坂！"])
    elif len(dog_list) == 0 and len(killer_list) == 0:
        if len(neutral_list) == 0:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为主角团！"])
        else:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为主角团和赤坂！"])
        return False
    elif len(hero_list) == 0 and len(killer_list) == 0:
        if len(neutral_list) == 0:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为山狗！"])
        else:
            await bot.send_group_message(event.group.id, ["游戏结束，胜利者为山狗和赤坂！"])
        return False
    elif len(hero_list) == 0 and len(killer_list) == 0 and len(neutral_list) == 0:
        await bot.send_group_message(event.group.id, ["游戏结束，胜利者为杀人狂！"])
        return False
    else:
        return True


# 主程序
if __name__ == '__main__':

    @bot.on(GroupMessage)
    async def start_game(event: GroupMessage, i=1, night=1):
        if event.sender.id in admin and str(event.message_chain) == '开始游戏':
            await bot.send_group_message(event.group.id, "寒蝉杀准备开始，游戏玩法请见群公告。输入 加入 以参与游戏")
            while len(player_list) < 2:
                @Filter(GroupMessage)
                def waiter_join(event_n: GroupMessage):
                    if event_n.sender.id in [player['qq'] for player in player_list]:
                        return 0
                    if str(event_n.message_chain) == '加入':
                        player_list.append({'id': i, 'qq': event_n.sender.id})
                        return event_n.sender.id

                attender_id = await inc.wait(waiter_join)
                if attender_id == 0:
                    await bot.send_group_message(event.group.id, ["请不要重复报名"])
                else:
                    await bot.send_group_message(event.group.id,
                                                 [At(attender_id), " 报名成功！当前报名人数为：", str(len(player_list))])
                i += 1
            await bot.send_group_message(event.group.id, "人数已凑齐，游戏将在10秒钟后开始！")
            sleep(5)
            await tell_id(event)
            distribute()
            await tell_character(event)
#            await tell_company(event)
            while await victory(event):
                print(checks_valid)
                await bot.send_group_message(event.group.id, ["第", str(night), "天夜晚开始。"])
                await tell_action(event)

                while len(choose_list) < len(player_list):
                    list1 = await inc.wait(choose_action)
                    msg1 = list1[0]
                    sender_id = list1[1]
                    await bot.send_temp_message(sender_id, event.group.id, msg1)

                choose_list.clear()
                calculate(actions)
                cal_effect()
                new_death = judge_death()
                await tell_check(event)
                await tell_stop(event)
                await tell_result(event, new_death)
                await broadcast_alive(event)
                if victory(event):
                    break
                await bot.send_group_message(event.group.id, ["进入讨论阶段"])
                sleep(5)
                await bot.send_group_message(event.group.id, ["讨论阶段结束，开始投票。"])
                while len(voter_list) < len(player_list):
                    msg = await inc.wait(vote)
                    await bot.send_group_message(event.group.id, msg)

                await vote_result(event)
                await broadcast_alive(event)
                voter_list.clear()
                night += 1
                disable_akasaka(night)
            return


    bot.run()
