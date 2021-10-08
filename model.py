from tinydb import TinyDB, Query


class Tournament:
    def __init__(self):
        info = TinyDB('json').search(Query().type == 'tournament')
        self.tournament_name = info['name']
        self.tournament_location = info['location']
        self.tournament_date = info['date']
        self.tournament_nbrounds = 4
        self.tournament_timecontrol = info['timecontrol']
        self.tournament_description = info['description']
        self.tournament_players = info['first name', 'last name']


class Player:
    def __init__(self):
        info = TinyDB('json').search(Query().type == 'player')
        self.player_first_name = info['first name']
        self.player_last_name = info['last name']
        self.player_phonenumber = info['phonenumber']
        self.player_gender = info['gender']
        self.player_birthday = info['birthday']
        self.player_rank = info['ranking']


class Round:
    def __init__(self):
        info = TinyDB('json').search(Query().type == 'tournament')
        self.round_number = info['round']


class Match:
    def __init__(self):
        info = TinyDB('json').search(Query().type == 'tournament')
        self.match = info['round']
