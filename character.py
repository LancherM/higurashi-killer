

class Character:
    id = 0
    name = ''
    camp = ''
    life = 1
    is_killer = False
    is_alive = True
    is_god = False
    abilities = []


class Keiichi(Character):
    id = 1
    name = '圭一'
    camp = '主角团'
    freeze = 1
    abilities = {'查验': 'check', '阻止': 'stop_k'}


class Rena(Character):
    id = 2
    name = '蕾娜'
    camp = '主角团'
    freeze = 1
    abilities = {'查验': 'check', '刀': 'kill_r'}


class Mion(Character):
    id = 3
    name = '魅音'
    camp = '主角团'
    prevent = 0
    abilities = {'保护': 'protect'}


class Satoko(Character):
    id = 4
    name = '沙都子'
    camp = '主角团'
    prevent = 0
    abilities = {'阻止': 'stop'}


class Akasaka(Character):
    id = 5
    name = '赤坂'
    camp = '中立'
    abilities = {}


class Ritsuko(Character):
    id = 6
    name = '律子'
    camp = '杀人狂'
    freeze = 1
    life = 2
    abilities = {'刀': 'kill'}


class Dog(Character):
    id = 7
    name = '山狗队员'
    camp = '山狗'
    abilities = {'刀': 'kill'}


class Takano(Character):
    id = 8
    name = '鹰野'
    is_god = True
    prevent = 0
    camp = '山狗'
    abilities = {'刀': 'kill_t', '阻止': 'stop'}


def init(character_id):
    if character_id == 1:
        return Keiichi()
    elif character_id == 2:
        return Rena()
    elif character_id == 3:
        return Mion()
    elif character_id == 4:
        return Satoko()
    elif character_id == 5:
        return Akasaka()
    elif character_id == 6:
        return Ritsuko()
    elif character_id == 7:
        return Dog()
    elif character_id == 8:
        return Takano()










