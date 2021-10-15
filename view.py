class View:

    def __init__(self):
        pass

    def menu(self):
        intro = str("Welcome to the chess tournament management software.\n")
        instructions = str("Before adding any player to a tournament you should enter its information in the database")
        add_player = str("To add a player to the database press 1.\n")
        create_tournament = str("To create a tournament press 2.\n")
        add_players_to_a_tournament = str("To add players to a tournament press 3.\n")
        get_pairs = str("To get pairings for a tournament press 4.\n")
        enter_results = str("To enter results of matches/rounds enter 5.\n")
        reports = str("To access reports press 6.\n")
        modif_elo = str("Modify the elo score of a player 7.\n")
        print(instructions)
        choice = int(input(intro + add_player + create_tournament + add_players_to_a_tournament + get_pairs + enter_results + reports + modif_elo))
        print(choice)
        return choice

    def create_player(self):
        statement = "you chose to add a player to db"
        print(statement)
        type = "player"

        def get_name():
            try:
                valuename = input("Please enter your first name without numeric symbols:\n")
                if not valuename.isalpha():
                    raise Exception()
                return valuename
            except valuename.isnotalpha:
                return get_name()

        def get_last_name():
            try:
                val = input("Please enter your last name (only letters): \n")
                if not val.isalpha():
                    raise Exception()
                return val
            except val.isnotalpha:
                return get_last_name()

        def get_gender():
            possible = ("M", "F")
            try:
                gender = input("Press F if  is a female, M if  is a male: \n")
                if gender not in possible:
                    raise Exception()
                return gender
            except gender.impossible:
                return get_gender()

        def get_phone():

            try:
                valuephone = input("Please enter phonenumber:\n")
                if not valuephone.isnumeric():
                    raise Exception()
                return valuephone
            except valuephone.isnotnumeric:
                return get_phone()

        def get_birthday():
            try:
                birthday = input("PLease enter  birthday: DDMMYYYY \n")
                if not birthday.isnumeric():
                    raise Exception()
                return birthday
            except birthday.isnotnumeric:
                return get_birthday()

        def get_elo():
            try:
                elo = int(input("Please enter elo ranking : \n"))
                if elo < 1600:
                    raise Exception()
                return elo
            except elo.isnotpossible:
                return get_elo()

        data = {'type': type,
                'firstname': get_name(),
                'lastname': get_last_name(),
                'phonenumber': get_phone(),
                'gender': get_gender(),
                'birthday': get_birthday(),
                'elo': get_elo()}

        return data

    def create_tournament(self):

        statement = "You chose to create a new tournament"
        print(statement)
        type = 'tournament'

        def get_tname():
            tname = input("Please enter the tournament name: \n")
            return tname

        def get_tdate():
            tdate = input("Please enter the date of the tournament following the DDMMYYYY structure: \n")
            return tdate

        def get_tlocation():
            tlocation = input("Please enter the city of location of the tournament :\n")
            return tlocation

        def get_tdescription():
            tdescription = input("Enter a tournament description: \n")
            return tdescription

        def get_ttimecontrol():
            standards = ['Blitz', 'Bullet', 'Coup Rapide']
            try:
                ttimecontrol = input("Enter the tournament time-control : Blitz or Bullet or Coup Rapide \n")
                if ttimecontrol not in standards:
                    raise Exception()
                return ttimecontrol
            except ttimecontrol.notinrange:
                return get_ttimecontrol()

        tinfo = {'type': type, 'name': get_tname(), 'date': get_tdate(), 'location': get_tlocation(), 'description': get_tdescription(),
                 'timecontrol': get_ttimecontrol(), 'player list': {}}
        print(tinfo)
        return tinfo

    def add_players_to_tournament(self):
        statement = "You chose to add players to a tournament"
        print(statement)
        tournament = input("Enter the name of the tournament you want to add players to:\n")
        first_name = input("Enter the first name of the player you want to add to the tournament:\n")
        last_name = input("Enter the last name of the player you want to add to the tournament:\n")
        new_player = (tournament, first_name, last_name)
        return new_player

    def get_input_pairings(self):
        info = input("Enter the name of the tournament you wish to get pairings for:\n")
        return info

    def results_of_round(self):
        print("You chose to add results to a round")
        results = []
        tournament = str(input("Please enter the name of the tournament:\n"))
        results.append(tournament)
        round_number = str(input("Please enter the round number:\n"))
        results.append((round_number))
        count = 1
        while count < 5:
            result_p1 = self.test_results(count)
            result_p2 = []
            if result_p1 == 1:
                result_p2 = 0
            elif result_p1 == 0:
                result_p2 = 1
            elif result_p1 == 0.5:
                result_p2 = 0.5
            data = [result_p1, result_p2]
            results.append(data)
            print(results)
            count += 1
        return results

    def test_results(self, count):
        possibilities = [0, 0.5, 1]
        try:
            result_p1 = float(input("Enter the result of the 1st player of the n°" + str(count) + " match:\n"))
            if (result_p1 not in possibilities):
                raise Exception()
            return result_p1
        except result_p1.notinpossib:
            return self.test_results(count)

    def get_input_reports(self):
        print("You chose to access the reports section \n")
        one = "To create a report of all players by score press 1 \n"
        two = "for all players by alphabetical order press 2 \n"
        three = "for all tournaments press 3\n "
        four = "for all rounds of a tournament press 4\n"
        five = "for all matches of a tournament press 5\n"
        six = "for all players of a tournament by alphabetical order press 6\n"
        seven = "for all players of a tournament by score press 7: \n"
        value = int(input(one + two + three + four + five + six + seven))
        psoft = [1, 2, 3]
        pround = [4]
        pmatch = [5]
        advanced_alpha = [6]
        advanced_score = [7]
        if value in psoft:
            return value
        elif value in pround:
            second = input("Enter the name of the tournament you are looking for: \n")
            return value, second
        elif value in pmatch:
            second = input("Enter the name of the tournament where you are looking to get the matches list: \n")
            return value, second
        elif value in advanced_alpha:
            second = input("Enter the tournament you wish to get all players from by alphabetical order: \n")
            return value, second
        elif value in advanced_score:
            second = input("Enter the name of the tournament you are looking to get all players by score: \n")
            return value, second
        else:
            print("There must be a typo in the view.py in the function def get_input_reports(self)")
            return

    def input_elo(self):  # permet de mettre à jour les elo suite à un tournament
        print("You chose to modify the elo score of a player: \n")
        try:
            player_1stname = input("Enter the first name of the player:\n")
            player_lastname = input("Enter the last name of the player:\n")
            new_elo = int(input("Enter the new elo of the player:\n"))
            intel = (player_1stname, player_lastname, new_elo)
            if new_elo < 1599:
                raise Exception()
            return intel
        except new_elo.notpossible:
            self.view.input_elo()


class Prints:  # This gives information to the user
    def __init__(self):
        pass

    def print(self, report):
        print(report)

    def print_report_all_players_by_score(self, clean_report):
        print(clean_report)

    def print_report_list_of_players_alpha(self, clean_report):
        print(clean_report)

    def print_report_list_of_tournaments(self, list_of_tournament):
        print(list_of_tournament)

    def print_report_round_of_tournament(self, rounds):
        print(rounds)

    def print_report_matches_of_tournament(self, rounds):
        print(rounds)

    def print_report_all_player_of_t_by_alpha(self, sorted_list):
        print(sorted_list)

    def print_report_all_player_of_t_by_score(self, sorted_list):
        print(sorted_list)

    def print_menu_choice_get_pairings(self):
        print("You chose to get the pairings")

    def print_player_list_is_full(self):
        statement = ' The player list for the tournament in question is already full'
        print(statement)

    def print_player_added_to_the_player_list(self, first_name, last_name, spot, tournament):
        statement = 'Player: ' + first_name + " " + last_name + " was added as: " + str(spot) + " in: " + tournament
        print(statement)

    def print_player_already_in_tournament(self):
        statement = "It seems like the player is already in the tournament"
        print(statement)

    def print_player_does_not_exists(self, first_name, last_name):
        statement = "It seems like the player you entered doesn't exist in the db"
        print(statement)

    def print_player_added_to_db(self, first_name, last_name):
        statement = "The player: " + first_name + " " + last_name + " was successfully added to the database"
        print(statement)

    def print_player_already_exists(self, first_name, last_name):
        statement = "The player " + first_name + " " + last_name + " already exists in the database"
        print(statement)

    def print_tournament_already_exists(self, tournament):
        statement = "The tournament : " + tournament + " already exists in the database"
        print(statement)

    def print_tournament_successfully_created(self, tournament):
        statement = " The tournament: " + tournament + " has been successfully created."
        print(statement)

    def print_update_elo_successul(self, player_first_name, player_last_name):
        statement = "Update of the elo score for player : " + player_first_name + " " + player_last_name + " done"
        print(statement)

    def print_player_list_incomplete_or_tournament_does_not_exists(self):
        statement = "The player list for this tournament is not complete or the tournament inexistent"
        print(statement)

    def print_pairings(self, round_name, pairings):
        statement = ' The ' + round_name + " will see the following matches: " + str(pairings)
        print(statement)

    def print_round_already_ended(self, tournament, round_number):
        first = "There seems to be an error with the round number "
        second = " of the tournament: "
        statement = first + round_number + second + tournament + " The round has already ended"
        print(statement)

    def print_round_updated(self, round_name, tournament):
        statement = "The " + round_name + " of the tournament: " + str(tournament) + " has been completed&updated."
        print(statement)

    def print_round_hasnt_ended(self):
        statement = "Before getting new pairings make sure that the previous round results have been recorded"
        print(statement)

    def print_pairing_process_impossible(self):
        statement = "Pairing impossible, check that the tournament hasn't already ended"
        print(statement)

    def print_tournament_cant_start(self):
        statement = "Pairing could not start, check that the tournament exists"
        print(statement)

    def print_player_list_not_full(self):
        statement = "It seems like the player list is not full, hence the pairing can not be done"
        print(statement)

    def print_round_does_not_exists(self, true_round, tournament):
        statement = "The " + true_round + " in the tournament : " + tournament + " does not exists."
        print(statement)

    def print_tournament_does_not_exists(self, tournament):
        statement = " The tournament " + tournament + " does not exists."
        print(statement)

    def print_player_non_existant(self):
        statement = " The player entered doesn't exists in the database "
        print(statement)
