

class Character:
    id = 0
    name = ''
    camp = ''
    life = 1
    is_killer = False
    is_alive = True
    is_god = False
    abilities = {}


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
    is_god = True


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


class Rika(Character):
    id = 9
    name = '梨花'
    camp = '主角团'
    life = 2
    abilities = {}


class Teppei(Character):
    id = 10
    name = '铁平'
    camp = '杀人狂'
    is_god = True
    abilities = {'刀': 'kill'}


class Okonogi(Character):
    id = 11
    name = '小此木'
    camp = '山狗'
    life = 2
    cooling = {'check_o': 0, 'kill_o': 0}
    abilities = {'查验': 'check_o', '刀': 'kill_o'}


class Shion(Character):
    id = 12
    name = '诗音'
    camp = '主角团'
    cooling = {'kill_o': 0}
    abilities = {'刀': 'kill_o'}


class Hanyuu(Character):
    id = 13
    name = '羽入'
    camp = '主角团'
    is_god = True
    freeze = 1
    abilities = {'阻止': 'stop_h'}


class Ooishi(Character):
    id = 14
    name = '大石'
    camp = '中立'
    freeze = 1
    cooling = {'check_o': 0}
    abilities = {'查验': 'check_o', '刀': 'kill_oo'}


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
    elif character_id == 9:
        return Rika()
    elif character_id == 10:
        return Teppei()
    elif character_id == 12:
        return Shion()
    elif character_id == 11:
        return Okonogi()
    elif character_id == 13:
        return Hanyuu()
    elif character_id == 14:
        return Ooishi()










