from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'framing'
    players_per_group = None
    num_rounds = 3
    endowment = 5
    efficiency_factor = 2
    initial_tank = 10
    usage_trial1 = 3
    usage_trial2 = 6

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    Tank = models.CurrencyField()
    Tank_trial = models.CurrencyField()
    Tank_in_Sum = models.CurrencyField()
    Tank_out_Sum = models.CurrencyField()
    Tank_in_Sum_trial = models.CurrencyField()
    Tank_out_Sum_trial = models.CurrencyField()
    prev_Tank = models.CurrencyField()
    
    
    def set_Tank(self):
        if self.round_number == 1:
            self.prev_Tank = Constants.initial_tank
        else:
            p_Tank = self.in_round(self.round_number - 1)
            self.prev_Tank = p_Tank.Tank
            
    
    def set_Tank_in(self):
        self.Tank_in_Sum = sum([p.Tank_in for p in self.get_players()])
            
        if self.round_number == 1:
            self.Tank = Constants.initial_tank + self.Tank_in_Sum
        else:
            p_Tank = self.in_round(self.round_number - 1)
            # tank_in_list =  [3,4,5,3,2,1,2,3,2,4]
            
            self.Tank = p_Tank.Tank + self.Tank_in_Sum
            
    def set_Tank_out(self):
        self.Tank_out_Sum = sum([p.Tank_out for p in self.get_players()])
        # tank_out_list = [2,2,3,1,4,5,6,7,5,2]
        self.Tank = self.Tank - self.Tank_out_Sum
            
            
    def set_Tank_in_trial(self):
        self.Tank_in_Sum_trial = sum([p.Tank_in_trial for p in self.get_players()])  + 5
        self.Tank_trial = Constants.initial_tank + self.Tank_in_Sum_trial
    
    def set_Tank_out_trial(self):
        self.Tank_out_Sum_trial = sum([p.Tank_out_trial for p in self.get_players()]) + 2
        self.Tank_trial = self.Tank_trial - self.Tank_out_Sum_trial
        
    def set_Tank_in_trial2(self):
        self.Tank_in_Sum_trial = sum([p.Tank_in_trial for p in self.get_players()])  - 3
        self.Tank_trial = self.Tank_trial + self.Tank_in_Sum_trial
        
    def set_Tank_out_trial2(self):
        self.Tank_out_Sum_trial = sum([p.Tank_out_trial2 for p in self.get_players()]) + 2
        self.Tank_trial = self.Tank_trial - self.Tank_out_Sum_trial
    
class Player(BasePlayer):
    assignment = models.LongStringField()
    remain = models.CurrencyField()
    remain_prev = models.CurrencyField(initial=0)
    Tank_out = models.CurrencyField(choices=currency_range(cu(0), cu(2), cu(1)),)
    Tank_in = models.CurrencyField()
    usage = models.IntegerField()
    paypay_prev = models.CurrencyField(initial=0)
    paypay = models.CurrencyField(initial=0)
    tank = models.CurrencyField()
    
    remain_trial = models.CurrencyField()
    remain_trial_prev = models.CurrencyField(initial=0)
    Tank_out_trial = models.CurrencyField(choices=currency_range(cu(0), cu(2), cu(1)),)
    Tank_out_trial2 = models.CurrencyField(choices=currency_range(cu(0), cu(2), cu(1)),)
    Tank_in_trial = models.CurrencyField()
    usage_trial = models.IntegerField()
    paypay_trial = models.CurrencyField(initial=0)
    paypay_trial_prev = models.CurrencyField(initial=0)
    
def Tank_in_max(player):
    return player.remain
    
def Tank_in_trial_max(player):
    return player.remain_trial


def creating_session(subsession):
    import random
    if subsession.round_number == 1:
        for player in subsession.get_players():
            participant = player.participant
            participant.assignment = random.choice(['互恵条件', '利己条件','利他条件'])
            player.assignment = participant.assignment
    else:
        for player in subsession.get_players():
            participant = player.participant
            player.assignment = participant.assignment

    
    
# PAGES
class reciprocity_intro1(Page):
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '互恵条件' 
        
class reciprocity_intro2(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '互恵条件' 
            
class reciprocity_intro3(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '互恵条件' 
            
class self_intro1(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '利己条件' 
            
class self_intro2(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '利己条件' 
            
class self_intro3(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '利己条件' 
            
class alt_intro1(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '利他条件' 
            
class alt_intro2(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '利他条件' 
            
class alt_intro3(Page):
    
    @staticmethod
    def is_displayed(player):
        if player.round_number == 1:
            return player.assignment == '利他条件' 
        
class trial_Main(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1 
    
    def before_next_page(self, timeout_happened):
        if self.round_number==1:
            self.remain_trial = Constants.endowment - Constants.usage_trial1


class trial_Give(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1 

    form_model = 'player'
    form_fields = ['Tank_in_trial'] 
    
    def before_next_page(self, timeout_happened):
        if self.round_number==1:
            self.remain_trial = self.remain_trial - self.Tank_in_trial
            self.group.set_Tank_in_trial()
    
    
class trial_Take(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1 

    form_model = 'player'
    form_fields = ['Tank_out_trial'] 

    def before_next_page(self, timeout_happened):
        if self.round_number==1:
            self.remain_trial_prev = self.remain_trial
            self.remain_trial = self.remain_trial + self.Tank_out_trial * Constants.efficiency_factor
            self.paypay_trial = self.remain_trial
            self.paypay_trial_prev = self.paypay_trial
            
        
class trial_ResultsWaitPage(WaitPage):
   def after_all_players_arrive(self):
        if self.round_number==1:
            self.group.set_Tank_out_trial()
       
class trial_Results(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1 
    

class trial_Main2(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1 
        
    def before_next_page(self, timeout_happened):
        if self.round_number==1:
            self.remain_trial = Constants.endowment - Constants.usage_trial2

class trial_Give2(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1 
    
    def before_next_page(self, timeout_happened):
        if self.round_number==1:
            self.Tank_in_trial = 0
            self.group.set_Tank_in_trial2()
        
class trial_Take2(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1  

    form_model = 'player'
    form_fields = ['Tank_out_trial2'] 

    def before_next_page(self, timeout_happened):
        if self.round_number==1:
            self.remain_trial = self.remain_trial + self.Tank_out_trial2 * Constants.efficiency_factor
            self.paypay_trial = self.paypay_trial + self.remain_trial
            
class trial_ResultsWaitPage2(WaitPage):
    def after_all_players_arrive(self):
        if self.round_number==1:
            self.group.set_Tank_out_trial2()
            
    
    def before_next_page(self, timeout_happened):
        if self.round_number==1:
            self.paypay_trial = self.paypay_trial_prev + self.remain_trial
            


class trial_Results2(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1





##本番
class Main(Page):
    @staticmethod
    def is_displayed(self):
        return self.round_number == 1
        
class Main2(Page):        
    def before_next_page(self, timeout_happened):
        self.group.set_Tank()    

class intro(Page):
    def before_next_page(self, timeout_happened):
        import random
        self.usage = random.randint(3,7)
        #　ランダムではなく固定の場合は下記2行
        # usage_list = [4,2,6,3,8,2,5,6,3,1]
        # self.usage = usage_list[self.round_number - 1]
        self.remain = Constants.endowment - self.usage

class Give_minus(Page):
    @staticmethod
    def is_displayed(player):
        return player.remain <= 0 
        
    def before_next_page(self, timeout_happened):
        self.Tank_in = 0
        self.group.set_Tank_in()
        self.tank = self.group.Tank
        
class Give(Page):
    form_model = 'player'
    form_fields = ['Tank_in'] 
    def is_displayed(player):
        return player.remain > 0
    
    def before_next_page(self, timeout_happened):
        self.group.set_Tank_in()
        self.tank = self.group.Tank
        self.remain = self.remain - self.Tank_in
            


class Take(Page):
    @staticmethod
    def is_displayed(player):
        return player.tank > 2
        
    form_model = 'player'
    form_fields = ['Tank_out'] 
    
    def before_next_page(self, timeout_happened):
        if self.round_number == 1:
            self.paypay_prev = 0
        else:
            prev_player = self.in_round(self.round_number - 1)
            self.paypay_prev = prev_player.paypay
        
        self.remain_prev = self.remain
        self.remain = self.remain + self.Tank_out* Constants.efficiency_factor
        self.paypay = self.paypay_prev + self.remain
        
    
class Take_minus(Page):
    @staticmethod
    def is_displayed(player):
        return player.tank <= 2 
        
    def before_next_page(self, timeout_happened):
        self.Tank_out = 0
        
        if self.round_number == 1:
            self.paypay_prev = 0
        else:
            prev_player = self.in_round(self.round_number - 1)
            self.paypay_prev = prev_player.paypay
        
        self.remain_prev = self.remain
        self.remain = self.remain + self.Tank_out* Constants.efficiency_factor
        self.paypay = self.paypay_prev + self.remain
        
class ResultsWaitPage(WaitPage):
     def after_all_players_arrive(self):
        self.group.set_Tank_out()
     
class ResultsWait(Page):
    import random
    timeout_seconds = random.randint(3,10)
    
    
class Results(Page):
    pass


page_sequence = [reciprocity_intro1,reciprocity_intro2, reciprocity_intro3, 
self_intro1,self_intro2, self_intro3, 
alt_intro1,alt_intro2,alt_intro3,

trial_Main,trial_Give, trial_Take, trial_ResultsWaitPage, trial_Results, 
trial_Main2,trial_Give2, trial_Take2, trial_ResultsWaitPage2, trial_Results2,
Main, Main2,intro, Give_minus, Give, Take, Take_minus, ResultsWaitPage, ResultsWait, Results]
