from tinydb import TinyDB, Query
from view import View, Prints
import datetime as dt

query = Query()
database = TinyDB('db.json')


class Controller:

    def __init__(self):
        self.view = View()
        self.print = Prints()

    def main_menu(self):
        answer = int(self.view.menu())
        if answer == 1:
            self.write_player()

        elif answer == 2:
            self.write_tournament()

        elif answer == 3:
            self.write_players_to_tournament()

        elif answer == 4:
            self.get_pairings()

        elif answer == 5:
            self.write_results_of_round()

        elif answer == 6:
            self.display_reports()

        elif answer == 7:
            self.modify_elo()

    def write_player(self):
        new_player = self.view.create_player()
        first_name = new_player['firstname']
        last_name = new_player['lastname']
        test = self.check_players_existence(first_name, last_name)
        if test == 0:
            database.insert(new_player)
            self.print.print_player_added_to_db(first_name, last_name)

    def write_tournament(self):
        new_tournament = self.view.create_tournament()
        tournament = new_tournament['name']
        test = self.check_tournament_existence(tournament)
        if test is None:  # confirme que le tournoi n'existe pas déjà
            database.insert(new_tournament)
            self.print.print_tournament_successfully_created(tournament)
        elif test != []:  # le tournoi existe déjà
            self.print.print_tournament_already_exists(tournament)

    def write_players_to_tournament(self):
        results = self.view.add_players_to_tournament()
        tournament = str(results[0])
        first_name = results[1]
        last_name = results[2]
        test = self.check_tournament_existence(tournament)
        if test is not None:  # veut dire que le tournament existe
            elo = self.check_player_exists_via_elo(first_name, last_name)
            if elo >= 1600:
                player_in_tournament = self.check_players_existence_in_tournament(tournament, first_name, last_name)
                if player_in_tournament is False:  # signifie le player n'est pas dans le tournament
                    spot = self.create_new_player_id(tournament)
                    if spot != []:  # signifie qu'on a de la place dans la player list
                        self.add_player_to_player_list(tournament, spot, first_name, last_name, elo)
                    else:  # la player list est full
                        self.print.print_player_list_is_full()
                else:  # ca c'est quand le player est déjà dans le tournament
                    self.print.print_player_already_in_tournament()
            else:  # signigie que le player n'existe pas
                self.print.print_player_does_not_exists(first_name, last_name)
        else:  # veut dire que le tournament n'existe pas
            self.print.print_tournament_does_not_exists(tournament)

    def get_pairings(self):  # assignation des matchs d'un round
        self.print.print_menu_choice_get_pairings()
        tournament = self.view.get_input_pairings()  # permet de connaitre le tournoi pour lequel créer un newround
        verification = self.check_tournament_can_start(tournament)  # permet de connaitre si la player list est full
        possible_rounds = [2, 3, 4]
        if verification == 'ok':  # cela signifie que le tournoi peut commencer/continuer
            round_to_be_written = self.check_round(tournament)
            if round_to_be_written == 1:
                self.create_first_pairings(tournament, round_to_be_written)
            elif round_to_be_written in possible_rounds:
                previous_round = round_to_be_written - 1
                test = self.check_round_has_ended(tournament, previous_round)
                if test == 1:  # signifie que le round avant est bien terminé
                    self.create_pairings(tournament, round_to_be_written)
            else:
                self.print.print_pairing_process_impossible()
        else:
            self.print.print_player_list_not_full()

    def create_first_pairings(self, tournament, round_to_be_written):
        sorted_player_list = self.sorting_tournament_participants_by_score(tournament)
        half = int(len(sorted_player_list) / 2)
        player_list_top = sorted_player_list[:half]
        player_list_botton = sorted_player_list[half:]
        pairings = {}
        pairings['starttime'] = str(dt.datetime.now())
        match_number = 1
        while match_number <= 4:
            for (x, y) in zip(player_list_top, player_list_botton):
                pairings[match_number] = (x, y)
                match_number += 1
        self.write_pairings(tournament, pairings, round_to_be_written)

    def create_pairings(self, tournament, round_to_be_written):
        sorted_list_by_score = self.sorting_tournament_participants_by_score(tournament)
        pairings = {}
        pairings['starttime'] = str(dt.datetime.now())
        check = self.have_p1_and_p2_played(tournament, sorted_list_by_score, round_to_be_written)
        if check[0] == 'yes':
            sorted_list_by_score = check[1]
        match_number = 1
        every_impair_elements = sorted_list_by_score[0::2]
        every_pairs_elements = sorted_list_by_score[1::2]
        while match_number <= 4:
            for x, y in zip(every_impair_elements, every_pairs_elements):
                pair = (x, y)
                pairings[match_number] = pair
                match_number += 1
        self.write_pairings(tournament, pairings, round_to_be_written)

    def have_p1_and_p2_played(self, tournament, sorted_list_by_score, round_to_be_written):
        data = database.get((query.type == 'tournament') & (query.name == tournament))
        p1 = sorted_list_by_score[0][0]
        p2 = sorted_list_by_score[1][0]
        list_previous_rounds = self.get_list_of_previous_rounds(round_to_be_written)
        for elem in list_previous_rounds:
            round_data = data[elem]
            for matches in round_data:
                check = round_data[matches]
                if (check[0][0] == p1 and check[1][0] == p2) or (check[0][0] == p2 and check[1][0] == p1):
                    my_order = [1, 2, 0, 3, 4, 5, 6, 7]
                    sorted_list_by_score = [sorted_list_by_score[i] for i in my_order]
                    message = 'yes'
                else:
                    message = 'no'
        return message, sorted_list_by_score

    def get_list_of_previous_rounds(self, round_to_be_written):
        list_previous_rounds = []
        if round_to_be_written == 2:
            list_previous_rounds.append('round1')
        elif round_to_be_written == 3:
            list_previous_rounds.append('round1')
            list_previous_rounds.append('round2')
        elif round_to_be_written == 4:
            list_previous_rounds.append('round1')
            list_previous_rounds.append('round2')
            list_previous_rounds.append('round3')
        return list_previous_rounds

    def sorting_tournament_participants_by_score(self, tournament):
        player_list = database.get((query.type == 'tournament') & (query.name == tournament))['player list']
        dict = {}
        for stuff in player_list.values():
            for id in stuff:
                level = (stuff[id]['score'])
                dict.update({id: level})
        sorted_list = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_list

    def write_pairings(self, tournament, pairings, round_to_be_written):
        round_name = ('round' + str(round_to_be_written))
        database.upsert({round_name: pairings}, ((query.type == 'tournament') & (query.name == tournament)))
        self.print.print_pairings(round_name, pairings)

    def check_round_has_ended(self, tournament, previous_round):
        round_name = 'round' + str(previous_round)
        data = database.get((query.type == 'tournament') & (query.name == tournament))
        detail = data[round_name]
        if detail["endtime"] != []:
            return 1
        else:
            self.print_print_round_hasnt_ended()

    def write_results_of_round(self):
        raw_results = self.view.results_of_round()
        tournament = raw_results[0]
        round_number = raw_results[1]
        round_name = 'round'+str(round_number)
        results = raw_results[2:]
        blueprint = self.check_round_existence(tournament, round_number)
        if blueprint is not None:
            # first match
            blueprint['1'][0][1] = results[0][0]
            blueprint['1'][1][1] = results[0][1]
            # second match
            blueprint['2'][0][1] = results[1][0]
            blueprint['2'][1][1] = results[1][1]
            # third match
            blueprint['3'][0][1] = results[2][0]
            blueprint['3'][1][1] = results[2][1]
            # fourth match
            blueprint['4'][0][1] = results[3][0]
            blueprint['4'][1][1] = results[3][1]
            # ajout de l'heure et date de fin
            blueprint['endtime'] = str(dt.datetime.now())
            database.update({round_name: blueprint}, (query.type == 'tournament') & (query.name == tournament))
            self.update_scores_in_player_list(tournament, round_name)

    def check_round_existence(self, tournament, round_number):
        true_round = "round" + str(round_number)
        print(true_round)
        data_tournament = database.get((query.type == 'tournament') & (query.name == tournament))
        print(data_tournament)
        if data_tournament is not None:
            try:
                round_data = data_tournament[true_round]
                if 'endtime' not in round_data:  # permet de checker que le round n'est pas déjà terminé
                    if round_data != []:
                        return round_data
                else:
                    self.print.print_round_already_ended(tournament, round_number)
            except round_data.doesnotexist:
                self.print.print_round_does_not_exists(true_round, tournament)
        else:
            self.print.print_tournament_does_not_exists(tournament)

    def update_scores_in_player_list(self, tournament, round_name):
        data = database.get((query.type == 'tournament') & (query.name == tournament))
        player_list = data['player list']
        round_results = data[round_name]
        dict_results = {}
        tool = 1
        while tool <= 4:
            id_p1 = round_results[str(tool)][0][0]
            score_p1 = round_results[str(tool)][0][1]
            id_p2 = round_results[str(tool)][1][0]
            score_p2 = round_results[str(tool)][1][1]
            dict_results[id_p1] = score_p1
            dict_results[id_p2] = score_p2
            sorted_dict_results = sorted(dict_results.items())
            tool += 1
        if round_name == 'round1':
            for info in sorted_dict_results:
                id = info[0]
                score = info[1]
                tool_2 = 0
                while tool_2 <= 7:
                    if id in player_list[str(tool_2)]:
                        player_list[str(tool_2)][id]['score'] = score
                    tool_2 += 1
                tool += 1
        elif round_name != 'round1':
            for info in sorted_dict_results:
                id = info[0]
                score = info[1]
                tool_2 = 0
                while tool_2 <= 7:
                    if id in player_list[str(tool_2)]:
                        player_list[str(tool_2)][id]['score'] = player_list[str(tool_2)][id]['score'] + score
                    tool_2 += 1
                tool += 1
        database.update({'player list': player_list}, ((query.type == 'tournament') & (query.name == tournament)))
        self.print.print_round_updated(round_name, tournament)

    def display_reports(self):  # this function allows to get reports from the database
        intel = self.view.get_input_reports()

        if intel == 1:  # search all players in the database and sort them by ranking (from top to bottom)
            self.report_one()
        elif intel == 2:  # results = all players by alphabetical order
            self.report_two()
        elif intel == 3:  # liste de tous les tournois
            self.report_three()
        elif intel[0] == 4:  # liste de tous les rounds d'un tournoi
            self.report_four(intel)
        elif int(intel[0]) == 5:  # tous les matchs d'un tournoi
            self.report_five(intel)
        elif int(intel[0]) == 6:  # all players of a specific tournament by alphabetical order
            self.report_six(intel)
        elif intel[0] == 7:  # all players of a specific tournament by score
            self.report_seven(intel)
        else:
            report = " This didn't follow the decision tree, there might be a typo"
            self.print.print(report)

    def report_one(self):
        raw_report = database.search(query.type == "player")
        raw_report.sort(key=lambda k: k['elo'])
        raw_report.reverse()
        clean_report = []
        for player in raw_report:
            clean_report.append(str(player['firstname']) + " " + player['lastname'] + " " + str(player['elo']))
        self.print.print_report_all_players_by_score(clean_report)

    def report_two(self):
        raw_report = database.search(query.type == "player")
        print(raw_report)
        clean_report = []
        raw_report.sort(key=lambda k: k['lastname'])
        for player in raw_report:
            print(player)
            clean_report.append(str(player['firstname']) + " " + player['lastname'])
        self.print.print_report_list_of_players_alpha(clean_report)

    def report_three(self):
        report = database.search(query.type == 'tournament')
        list_of_tournament = []
        for tournament in report:
            list_of_tournament.append(tournament['name'])
        self.print.print_report_list_of_tournaments(list_of_tournament)

    def report_four(self, intel):
        report = database.get((query.type == 'tournament') & (query.name == str(intel[1])))
        tool_rounds = []
        rounds = {}
        for elem in report:
            print(elem)
            if elem.startswith('round'):
                tool_rounds.append(elem)
                for round in tool_rounds:
                    rounds[round] = report[round]
        self.print.print_report_round_of_tournament(rounds)

    def report_five(self, intel):
        report = database.get((query.type == 'tournament') & (query.name == str(intel[1])))
        tool_rounds = []
        rounds = {}
        for elem in report:
            if elem.startswith('round'):
                tool_rounds.append(elem)
        for round in tool_rounds:
            rounds[round] = [report[round]['1'], report[round]['2'], report[round]['3'], report[round]['4']]
        self.print.print_report_matches_of_tournament(rounds)

    def report_six(self, intel):
        tournament = str(intel[1])
        player_list = database.get((query.type == 'tournament') & (query.name == tournament))['player list']
        dict = {}
        for stuff in player_list.values():
            for id in stuff:
                level = (stuff[id]['name'])
                dict.update({id: level})
        sorted_list = sorted(dict.items(), key=lambda x: x[1], reverse=False)
        self.print.print_report_all_player_of_t_by_alpha(sorted_list)

    def report_seven(self, intel):
        tournament = str(intel[1])
        player_list = database.get((query.type == 'tournament') & (query.name == tournament))['player list']
        dict = {}
        for stuff in player_list.values():
            for id in stuff:
                level = (stuff[id]['score'])
                name = (stuff[id]['name'])
                dict.update({id: [name, level]})
        sorted_list = sorted(dict.items(), key=lambda x: x[1], reverse=False)
        self.print.print_report_all_player_of_t_by_score(sorted_list)

    def modify_elo(self):
        input = self.view.input_elo()
        player_first_name = input[0]
        player_last_name = input[1]
        player_elo = input[2]
        player_in_db = database.search((query.firstname == player_first_name) & (query.lastname == player_last_name) & (
                query.type == "player"))  # check if player exists:
        if player_in_db is not None:
            database.update({'elo': player_elo}, (
                    (query.firstname == player_first_name) & (query.lastname == player_last_name) & (query.type == "player")))
            self.print.print_update_elo_successul(player_first_name, player_last_name)
        else:
            self.print.print_player_does_not_exists()

    def check_players_existence(self, first_name, last_name):
        player_in_db = database.get((query.firstname == first_name) & (query.lastname == last_name) & (query.type == "player"))
        if player_in_db is None:
            score = 0
            return score
        else:  # quand le player est déja dans la base
            self.print.print_player_already_exists(first_name, last_name)

    def check_players_existence_in_tournament(self, tournament, first_name, last_name):
        tournament_data = database.get((query.name == tournament) & (query.type == 'tournament'))
        player_list = tournament_data['player list']
        if (first_name not in str(player_list) or last_name not in str(player_list)):
            response = False
            return response

    def check_tournament_existence(self, tournament):  # permet de vérifier que le tournoi existe ou pas
        find = database.get((query.name == tournament) & (query.type == 'tournament'))
        return find

    def check_tournament_can_start(self, tournament):  # permet de voir si le player 8 est bien entré
        response = database.get(query.name == tournament)
        if response is not None:
            player_list = response['player list']
            if len(player_list) == 8:
                message = 'ok'
                return message
        else:
            self.print.print_tournament_cant_start()

    def create_new_player_id(self, tournament):
        player_list = (database.get((query.type == 'tournament') & (query.name == tournament)))['player list']
        id = len(player_list) + 1
        if id <= 8:
            return id

    def add_player_to_player_list(self, tournament, spot, first_name, last_name, elo):
        new_player = {str('player' + str(spot)): {'name': str(first_name + " " + last_name), 'score': elo}}
        player_list = database.get((query.type == 'tournament') & (query.name == tournament))[
            'player list']  # récupération du blueprint player_list
        player_list[int(spot-1)] = new_player
        database.update({'player list': player_list}, (query.type == 'tournament') & (
                query.name == tournament))  # insertion de la player_list modifiée dans la database
        self.print.print_player_added_to_the_player_list(first_name, last_name, spot, tournament)

    def check_round(self, tournament):  # permet de connaitre le prochain numéro du round qui devra être créé
        response = database.get((query.type == 'tournament') & (query.name == tournament))
        next_round_to_create = len(
            response) - 6
        return next_round_to_create

    def check_player_exists_via_elo(self, first_name, last_name):
        elo = database.get((query.type == 'player') & (query.firstname == first_name) & (query.lastname == last_name))['elo']
        print(elo)
        if elo is not None:
            return elo
        else:
            self.print.print_player_non_existent()
