from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'public_good_trial'
    players_per_group = 3
    num_rounds = 1
    endowment = cu(10)
    multiplier = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution=models.CurrencyField()
    individual_share =models.CurrencyField()
    
    
def set_payoffs(group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = group.total_contribution * Constants.multiplier / Constants.players_per_group
    for player in players:
        player.payoff = Constants.endowment - player.contribution + group.individual_share
    
        
class Player(BasePlayer):
    
    usage = models.IntegerField()       
    remain = models.IntegerField()
    contribution = models.CurrencyField(
                                        label ="How much will you contribute?"
                                        )

                                        
def creating_session(subsession):
    import random
    for player in subsession.get_players():
        player.usage = random.randint(0,5)
        player.remain = 10- player.usage

def contribution_max(player):
    return player.remain

def contribution_error_message(player, value):
    print('value is', value)
    if value > player.remain:
        return 'Cannot offer more than your remaining budget'

#def contribution_choice(player):
#    return currency_range(cu(0),player.remain,cu(1))

# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution'] 
    


class ResultsWaitPage(WaitPage):
    after_all_players_arrive=set_payoffs
        


class Results(Page):
    pass


page_sequence = [Contribute, ResultsWaitPage, Results]
