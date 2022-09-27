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

class Subsession(BaseSubsession):
     def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        return {'payoffs': payoffs}


class Group(BaseGroup):
    remain = models.CurrencyField()
    take = models.CurrencyField(choices=currency_range(cu(0), Constants.endowment, cu(1)),)
    give = models.CurrencyField()
    temp = models.IntegerField()
    
    
class Player(BasePlayer):
    time_pressure = models.LongStringField()
    remain2 = models.CurrencyField()

def creating_session(subsession):
    import random
    if subsession.round_number == 1:
        for player in subsession.get_players():
            participant = player.participant
            participant.time_pressure = random.choice(
                                    ['互恵条件：このゲームは他者と助け合って、皆でどれだけ多くの利得を得られるかを試すゲームです。',
                                     '利己条件：このゲームは、自分がどれだけ多くの利益を得られるかを試すゲームです。',
                                     '利他条件：このゲームは、寄付や慈善行為がどの程度見られるかを調べるゲームです。'])
            player.time_pressure = participant.time_pressure
    else:
        for player in subsession.get_players():
            participant = player.participant
            player.time_pressure = participant.time_pressure

        
def give_max(group):
    return group.remain
    
    
# PAGES
class Main(Page):
    def before_next_page(self, timeout_happened):
        import random
        self.group.temp = random.randint(3,7)
        self.group.remain = Constants.endowment - self.group.temp
        self.remain2=self.group.remain
         
        
        
class Give(Page):
    form_model = 'group'
    form_fields = ['give'] 
    def is_displayed(player):
        return player.remain2 > 0
    
    
class Give_minus(Page):
    @staticmethod
    def is_displayed(player):
        return player.remain2 <= 0 

class Take(Page):
    form_model = 'group'
    form_fields = ['take'] 


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Main, Give, Give_minus, Take, ResultsWaitPage, Results]
