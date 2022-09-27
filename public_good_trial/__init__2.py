from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'public_good_trial'
    players_per_group = 3
    num_rounds = 1
    endowment = cu(5)
    multiplier = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution=models.CurrencyField()
    individual_share =models.CurrencyField()
   
    
    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = self.total_contribution * Constants.multiplier / Constants.players_per_group
        for player in players:
            player.payoff = Constants.endowment - player.contribution + self.individual_share
            
    def sent_back_amount_choices(self):
        return currency_range(
                                0,
                                Constants.multiplication_factor,
                                1
                                )

class Player(BasePlayer):
    contribution = models.CurrencyField(
                                        min=0,
                                        max=Constants.endowment,
                                        label ="How much will you contribute?"
                                        )
    time_pressure = models.StringField()
    remain = models.IntegerField()

def creating_session(subsession):
    import random
    for player in subsession.get_players():
        player.time_pressure = random.choice(['互恵条件','利己条件','利他条件'])
        player.remain = random.randint(0,2)
        print('set time_pressure to', player.time_pressure)

# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution'] 

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        


class Results(Page):
    pass


page_sequence = [Contribute, ResultsWaitPage, Results]
