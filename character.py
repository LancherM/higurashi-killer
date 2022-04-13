class Character:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.camp = ''
        self.life = 1
        self.is_alive = True
        self.is_god = False
        self.abilities = {}


class Keiichi(Character):
    def __init__(self):
        super(Keiichi, self).__init__()
        self.id = 1
        self.name = '圭一'
        self.camp = '主角团'
        self.freeze = 1
        self.abilities = {'查验': 'check', '阻止': 'stop_k'}
        self.is_god = True


class Rena(Character):
    def __init__(self):
        super(Rena, self).__init__()
        self.id = 2
        self.name = '蕾娜'
        self.camp = '主角团'
        self.freeze = 1
        self.abilities = {'查验': 'check', '刀': 'kill_r'}
        self.is_god = True


class Mion(Character):
    def __init__(self):
        super(Mion, self).__init__()
        self.id = 3
        self.name = '魅音'
        self.camp = '主角团'
        self.prevent = 0
        self.abilities = {'保护': 'protect'}


class Satoko(Character):
    def __init__(self):
        super(Satoko, self).__init__()
        self.id = 4
        self.name = '沙都子'
        self.camp = '主角团'
        self.prevent = 0
        self.abilities = {'阻止': 'stop'}


class Akasaka(Character):
    def __init__(self):
        super(Akasaka, self).__init__()
        self.id = 5
        self.name = '赤坂'
        self.camp = '中立'
        self.is_god = True
        self.abilities = {}


class Ritsuko(Character):
    def __init__(self):
        super(Ritsuko, self).__init__()
        self.id = 6
        self.name = '律子'
        self.camp = '杀人狂'
        self.freeze = 1
        self.abilities = {'刀': 'kill'}


class Dog(Character):
    def __init__(self):
        super(Dog, self).__init__()
        self.id = 7
        self.name = '山狗队员'
        self.camp = '山狗'
        self.abilities = {'刀': 'kill'}


class Takano(Character):
    def __init__(self):
        super(Takano, self).__init__()
        self.id = 8
        self.name = '鹰野'
        self.prevent = 0
        self.camp = '山狗'
        self.is_god = True
        self.abilities = {'刀': 'kill_t', '阻止': 'stop'}


class Rika(Character):
    def __init__(self):
        super(Rika, self).__init__()
        self.id = 9
        self.name = '梨花'
        self.life = 2
        self.camp = '主角团'
        self.abilities = {}


class Teppei(Character):
    def __init__(self):
        super(Teppei, self).__init__()
        self.id = 10
        self.name = '铁平'
        self.is_god = True
        self.camp = '杀人狂'
        self.abilities = {'刀': 'kill'}


class Okonogi(Character):
    def __init__(self):
        super(Okonogi, self).__init__()
        self.id = 11
        self.name = '小此木'
        self.life = 2
        self.camp = '山狗'
        self.cooling = {'check_o': 0, 'kill_o': 0}
        self.abilities = {'查验': 'check_o', '刀': 'kill_o'}


class Shion(Character):
    def __init__(self):
        super(Shion, self).__init__()
        self.id = 12
        self.name = '诗音'
        self.camp = '主角团'
        self.cooling = {'kill_o': 0}
        self.abilities = {'刀': 'kill_o'}


class Hanyuu(Character):
    def __init__(self):
        super(Hanyuu, self).__init__()
        self.id = 13
        self.name = '羽入'
        self.camp = '主角团'
        self.is_god = True
        self.freeze = 1
        self.abilities = {'保护': 'stop_h'}


class Ooishi(Character):
    def __init__(self):
        super(Ooishi, self).__init__()
        self.id = 14
        self.name = '大石'
        self.camp = '中立'
        self.freeze = 1
        self.cooling = {'check_o': 0}
        self.abilities = {'查验': 'check_o', '刀': 'kill_oo'}


class Satoshi(Character):
    def __init__(self):
        super(Satoshi, self).__init__()
        self.id = 15
        self.name = '悟史'
        self.camp = '主角团'
        self.abilities = {}


class Nomura(Character):
    def __init__(self):
        super(Nomura, self).__init__()
        self.id = 16
        self.name = '野村'
        self.cooling = {'stop_n': 0}
        self.camp = '主角团'  # 挂羊头卖狗肉，其实还是山狗
        self.abilities = {'刀': 'kill_t', '阻止': 'stop_n'}


class Keiichi_l5(Character):
    def __init__(self):
        super(Keiichi_l5, self).__init__()
        self.id = 17
        self.name = 'L5圭一'
        self.camp = '主角团'
        self.is_god = True
        self.freeze = 1
        self.abilities = {'刀': 'kill_k'}


class Rena_l5(Character):
    def __init__(self):
        super(Rena_l5, self).__init__()
        self.id = 18
        self.name = 'L5蕾娜'
        self.camp = '主角团'
        self.is_god = True
        self.freeze = 1
        self.abilities = {'查验': 'check_r', '刀': 'kill_r5'}


class Shion_l5(Character):
    def __init__(self):
        super(Shion_l5, self).__init__()
        self.id = 19
        self.name = 'L5诗音'
        self.camp = '主角团'
        self.abilities = {'刀': 'kill_s'}


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
    elif character_id == 15:
        return Satoshi()
    elif character_id == 16:
        return Nomura()
    elif character_id == 17:
        return Keiichi_l5()
    elif character_id == 18:
        return Rena_l5()
    elif character_id == 19:
        return Shion_l5()
