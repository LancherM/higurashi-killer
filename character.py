class Character:
    def __init__(self):
        self.cooling = None
        self.id = 0
        self.name = ''
        self.camp = ''
        self.life = 1
        self.is_alive = True
        self.is_god = False
        self.l5 = False
        self.is_zombie = False
        self.abilities = {}

    def infect(self):
        self.name = '感染者'
        self.camp = '感染者'
        self.is_zombie = True
        self.is_god = False
        self.cooling = {'kill_o': 0}
        self.abilities = {'刀': 'kill_o'}
        self.l5 = True
        if self.life > 0:
            self.life = 1


class Keiichi(Character):
    def __init__(self):
        super(Keiichi, self).__init__()
        self.id = 1
        self.name = '圭一'
        self.camp = '主角团'
        self.freeze = 1
        self.abilities = {'查验': 'check', '阻止': 'stop_k'}
        self.is_god = True

    def l5_change(self):
        self.name = 'L5圭一'
        self.freeze = 1
        self.l5 = True
        self.abilities = {'刀': 'kill_k'}


class Rena(Character):
    def __init__(self):
        super(Rena, self).__init__()
        self.id = 2
        self.name = '蕾娜'
        self.camp = '主角团'
        self.freeze = 1
        self.abilities = {'查验': 'check', '刀': 'kill_r'}
        self.is_god = True

    def l5_change(self):
        self.name = 'L5蕾娜'
        self.freeze = 1
        self.l5 = True
        self.abilities = {'查验': 'check_r', '刀': 'kill_r5'}



class Mion(Character):
    def __init__(self):
        super(Mion, self).__init__()
        self.freeze = 0
        self.id = 3
        self.name = '魅音'
        self.camp = '主角团'
        self.prevent = [0, 0]
        self.abilities = {'保护': 'protect'}

    def l5_change(self):
        self.name = 'L5魅音'
        self.freeze = 1
        self.l5 = True
        self.abilities = {'刀': 'kill_m5'}


class Satoko(Character):
    def __init__(self):
        super(Satoko, self).__init__()
        self.freeze = 0
        self.id = 4
        self.name = '沙都子'
        self.camp = '主角团'
        self.prevent = [0, 0]
        self.abilities = {'阻止': 'stop'}
        
    def l5_change(self):
        self.freeze = 1
        self.name = 'L5沙都子'
        self.l5 = True
        self.abilities = {'刀': 'kill_s5'}


class Akasaka(Character):
    def __init__(self):
        super(Akasaka, self).__init__()
        self.id = 5
        self.name = '赤坂'
        self.camp = '中立'
        self.freeze = 1
        self.abilities = {'阻止': 'stop_ak'}



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
        self.prevent = [0, 0]
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
        self.resurrect = False
        self.abilities = {'复活': 'resurrect'}


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

    def l5_change(self):
        self.name = 'L5诗音'
        self.l5 = True
        self.abilities = {'刀': 'kill_s'}


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
        self.freeze = 0
        self.id = 15
        self.name = '悟史'
        self.camp = '主角团'
        self.abilities = {}

    def l5_change(self):
        self.freeze = 1
        self.name = 'L5悟史'
        self.l5 = True
        self.abilities = {"刀": 'kill_sa5'}


class Nomura(Character):
    def __init__(self):
        super(Nomura, self).__init__()
        self.id = 16
        self.name = '野村'
        self.camp = '主角团'  # 挂羊头卖狗肉，其实还是山狗
        self.cooling = {'kill_no': 0}
        self.freeze2 = 1
        self.abilities = {'刀': 'kill_no', '复活': 'resurrect_no'}


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


class Nacumi(Character):
    def __init__(self):
        super(Nacumi, self).__init__()
        self.id = 20
        self.name = '夏美'
        self.camp = '主角团'
        self.cooling = {'kill_na': 0}
        self.abilities = {'刀': 'kill_na'}


class Cando_l5(Character):
    def __init__(self):
        super(Cando_l5, self).__init__()
        self.id = 21
        self.name = '水坝监督'
        self.camp = '杀人狂'
        self.life = 2
        self.cooling = {'kill_ca': 0}
        self.abilities = {'刀': 'kill_ca'}


class Tomitake(Character):
    def __init__(self):
        super(Tomitake, self).__init__()
        self.id = 22
        self.name = '富竹'
        self.camp = '中立'
        self.freeze = 1
        self.abilities = {'刀': 'kill_r'}

class Irie(Character):
    def __init__(self):
        super(Irie, self).__init__()
        self.id = 23
        self.name = '入江'
        self.camp = '中立'
        self.freeze = 1
        self.cooling = {'protect_i': 0}
        self.abilities = {'阻止': 'stop_i', '保护': 'protect_i'}


class Sniper(Character):
    def __init__(self):
        super(Sniper, self).__init__()
        self.id = 24
        self.name = '山狗狙击手'
        self.camp = '山狗'
        self.killable = False
        self.abilities = {'刀': 'kill_sn'}


class Akatsuki(Character):
    def __init__(self):
        super(Akatsuki, self).__init__()
        self.id = 25
        self.name = '晓'
        self.camp = '主角团'
        self.freeze = 2
        self.abilities = {'阻止': 'stop_aka'}


class Mother1(Character):
    def __init__(self):
        super(Mother1, self).__init__()
        self.id = 26
        self.name = '田村媛命'
        self.camp = '感染者'
        self.life = 2
        self.freeze = 3
        self.freeze1 = 1
        self.abilities = {'感染': 'infect'}


class Mother2(Character):
    def __init__(self):
        super(Mother2, self).__init__()
        self.id = 27
        self.name = '采'
        self.camp = '中立'
        self.is_god = True
        self.freeze = 1
        self.prevent = [0, 0]
        self.abilities = {'感染': 'infect_2', '阻止': 'stop'}



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
    elif character_id == 20:
        return Nacumi()
    elif character_id == 21:
        return Cando_l5()
    elif character_id == 22:
        return Tomitake()
    elif character_id == 23:
        return Irie()
    elif character_id == 24:
        return Sniper()
    elif character_id == 25:
        return Akatsuki()
    elif character_id == 26:
        return Mother1()
    elif character_id == 27:
        return Mother2()
