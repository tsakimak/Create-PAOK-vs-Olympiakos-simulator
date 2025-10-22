import random
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image

class PAOK:
    def __init__(self):
        self.team_name = "PAOK FC"
        self.founded = 1926
        self.stadium = "Toumba Stadium"
        self.coach = "Răzvan Lucescu"
    
    def get_team_info(self):
        return f"{self.team_name}, founded in {self.founded}, plays at {self.stadium}. Coach: {self.coach}"
    
    def chant(self):
        return "PAOK, PAOK! Let's go for the championship!"

class Olympiacos:
    def __init__(self):
        self.team_name = "Olympiacos FC"
        self.founded = 1925
        self.stadium = "Karaiskakis Stadium"
        self.coach = "Jose Luis Mendilibar"
    
    def get_team_info(self):
        return f"{self.team_name}, founded in {self.founded}, plays at {self.stadium}. Coach: {self.coach}"
    
    def chant(self):
        return "Olympiacos, Olympiacos! Gate 7 forever!"

class Player:
    def __init__(self, name, position, goals=0, assists=0, appearances=0, fouls=0, yellow_cards=0, red_cards=0):
        self.name = name
        self.position = position
        self.goals = goals
        self.assists = assists
        self.appearances = appearances
        self.fouls = fouls
        self.yellow_cards = yellow_cards
        self.red_cards = red_cards
    
    def get_stats(self):
        return f"{self.name} ({self.position}): {self.appearances} apps, {self.goals} goals, {self.assists} assists, {self.fouls} fouls, {self.yellow_cards} YC, {self.red_cards} RC"
    
    def update_stats(self, goals=0, assists=0, appearances=1, fouls=0, yellow_cards=0, red_cards=0):
        self.goals += goals
        self.assists += assists
        self.appearances += appearances
        self.fouls += fouls
        self.yellow_cards += yellow_cards
        self.red_cards += red_cards

class MatchSimulator:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.events = []
        self.home_saves = 0
        self.away_saves = 0
        # Updated PAOK players based on 2025/2026 squad
        self.paok_players = {
            # Starting XI
            'Jiri Pavlenka': Player('Jiri Pavlenka', 'GK', 0, 0, 15, 0, 0, 0),
            'Jonny Otto': Player('Jonny Otto', 'DF', 1, 2, 16, 5, 2, 0),
            'Dejan Lovren': Player('Dejan Lovren', 'DF', 0, 1, 12, 3, 1, 0),  # Updated
            'Abdoulaye Meite': Player('Abdoulaye Meite', 'DF', 0, 2, 14, 4, 3, 0),
            'Mads Roerslev': Player('Mads Roerslev', 'DF', 1, 1, 11, 2, 1, 0),
            'Andrija Zivkovic': Player('Andrija Zivkovic', 'MF', 5, 7, 15, 6, 4, 0),
            'Ilia Gruev': Player('Ilia Gruev', 'MF', 2, 3, 13, 3, 2, 0),  # Updated from sources
            'Sotiris Ninis': Player('Sotiris Ninis', 'MF', 2, 5, 13, 4, 2, 0),
            'Thomas Muldrow': Player('Thomas Muldrow', 'FW', 8, 3, 12, 2, 1, 0),
            'Kiril Despodov': Player('Kiril Despodov', 'FW', 6, 4, 14, 3, 2, 0),
            'Vangelis Pavlidis': Player('Vangelis Pavlidis', 'FW', 10, 2, 11, 1, 0, 0),
            # Substitutes
            'Dimitris Pelkas': Player('Dimitris Pelkas', 'MF', 4, 6, 13, 5, 3, 0),
            'Taison': Player('Taison', 'FW', 7, 5, 14, 3, 2, 0),
            'Giorgos Konstantelias': Player('Giorgos Konstantelias', 'MF', 4, 3, 12, 2, 1, 0),
            'Pheo van der Sluys': Player('Pheo van der Sluys', 'MF', 1, 1, 8, 1, 0, 0),  # New from squad
            'Tomasz Kedziora': Player('Tomasz Kedziora', 'DF', 0, 2, 10, 4, 2, 0)
        }
        # Updated Olympiacos players based on 2025/2026 squad
        self.olympiacos_players = {
            # Starting XI
            'Konstantinos Tzolakis': Player('Konstantinos Tzolakis', 'GK', 0, 0, 14, 0, 0, 0),
            'Omar Richards': Player('Omar Richards', 'DF', 0, 1, 13, 3, 1, 0),
            'Panagiotis Retsos': Player('Panagiotis Retsos', 'DF', 1, 2, 15, 5, 3, 0),
            'David Carmo': Player('David Carmo', 'DF', 0, 1, 12, 4, 2, 0),
            'Santiago Hezze': Player('Santiago Hezze', 'DF', 0, 3, 14, 3, 2, 0),
            'Sotiris Alexandropoulos': Player('Sotiris Alexandropoulos', 'MF', 2, 4, 13, 6, 4, 0),
            'Kostas Fortounis': Player('Kostas Fortounis', 'MF', 5, 6, 15, 4, 3, 0),
            'Daniel Podence': Player('Daniel Podence', 'MF', 4, 5, 14, 5, 2, 0),
            'Ayoub El Kaabi': Player('Ayoub El Kaabi', 'FW', 9, 3, 12, 2, 1, 0),
            'Georgios Masouras': Player('Georgios Masouras', 'FW', 6, 4, 13, 3, 2, 0),
            'Rodrigo Elishak': Player('Rodrigo Elishak', 'FW', 3, 2, 11, 1, 1, 0),
            # Substitutes
            'Fran Navarro': Player('Fran Navarro', 'FW', 7, 2, 10, 2, 1, 0),
            'Joao Carvalho': Player('Joao Carvalho', 'MF', 1, 3, 9, 3, 2, 0),
            'Pepo': Player('Pepo', 'MF', 2, 1, 8, 4, 3, 0),
            'Theofilos Chatzitheodoridis': Player('Theofilos Chatzitheodoridis', 'DF', 0, 1, 7, 2, 1, 0),
            'Kostas Koulierakis': Player('Kostas Koulierakis', 'DF', 1, 1, 9, 3, 2, 0)  # Added from recent transfers
        }
        self.current_scorer = None
        # Track active players and subs for home (PAOK)
        self.home_active_players = list(self.paok_players.keys())[:11]  # First 11 as starting
        self.home_available_subs = list(self.paok_players.keys())[11:]
        self.home_substitutions_made = 0
        self.home_max_substitutions = 3
        # Track active players and subs for away (Olympiacos)
        self.away_active_players = list(self.olympiacos_players.keys())[:11]
        self.away_available_subs = list(self.olympiacos_players.keys())[11:]
        self.away_substitutions_made = 0
        self.away_max_substitutions = 3
        # Derby-specific
        self.is_derby = True  # Always for PAOK vs Olympiacos
        self.gate7_chants = ["Gate 7 roars!", "Thrylos forever!", "Brothers, you live!"]
    
    def make_home_substitution(self, minute):
        if self.home_substitutions_made >= self.home_max_substitutions or not self.home_available_subs:
            return None
        out_player = random.choice([p for p in self.home_active_players if self.paok_players[p].position != 'GK'])
        eligible_subs = [sub for sub in self.home_available_subs if self.paok_players[sub].position == self.paok_players[out_player].position]
        if not eligible_subs:
            eligible_subs = self.home_available_subs
        in_player = random.choice(eligible_subs)
        self.home_active_players.remove(out_player)
        self.home_active_players.append(in_player)
        self.home_available_subs.remove(in_player)
        self.home_substitutions_made += 1
        self.paok_players[in_player].update_stats(appearances=1)
        event = f"Minute {minute}: {self.home_team} Sub - {in_player} for {out_player}."
        self.events.append(event)
        return event
    
    def make_away_substitution(self, minute):
        if self.away_substitutions_made >= self.away_max_substitutions or not self.away_available_subs:
            return None
        out_player = random.choice([p for p in self.away_active_players if self.olympiacos_players[p].position != 'GK'])
        eligible_subs = [sub for sub in self.away_available_subs if self.olympiacos_players[sub].position == self.olympiacos_players[out_player].position]
        if not eligible_subs:
            eligible_subs = self.away_available_subs
        in_player = random.choice(eligible_subs)
        self.away_active_players.remove(out_player)
        self.away_active_players.append(in_player)
        self.away_available_subs.remove(in_player)
        self.away_substitutions_made += 1
        self.olympiacos_players[in_player].update_stats(appearances=1)
        event = f"Minute {minute}: {self.away_team} Sub - {in_player} for {out_player}."
        self.events.append(event)
        return event
    
    def issue_foul(self, team_players, active_players, minute, is_home=True):
        player = random.choice(active_players)
        team_players[player].update_stats(fouls=1)
        team_name = self.home_team if is_home else self.away_team
        event = f"Minute {minute}: Foul by {player} ({team_name}). "
        # Yellow card chance (10% after foul)
        if random.random() < 0.1 and team_players[player].yellow_cards < 2:
            team_players[player].update_stats(yellow_cards=1)
            event += f"Yellow card! "
        # Red card chance (2% direct, or 2nd yellow)
        if random.random() < 0.02 or (team_players[player].yellow_cards == 2):
            team_players[player].update_stats(red_cards=1)
            active_players.remove(player)  # Sent off
            event += f"Red card! {player} sent off! "
        self.events.append(event)
        return event
    
    def derby_event(self, minute):
        if not self.is_derby:
            return None
        event_type = random.choice(['chant', 'tension'])
        if event_type == 'chant':
            chant = random.choice(self.gate7_chants)
            event = f"Minute {minute}: Derby fever! {chant} echoes through the stadium."
        else:
            event = f"Minute {minute}: High tension in the derby - fans on edge!"
        self.events.append(event)
        return event
    
    def simulate_minute(self, minute):
        home_chance = random.random()
        away_chance = random.random()
        home_sub_chance = random.random()
        away_sub_chance = random.random()
        foul_chance = random.random()
        derby_chance = random.random()
        
        event = f"Minute {minute}: "
        
        if derby_chance < 0.005:  # Rare derby event
            derby_ev = self.derby_event(minute)
            if derby_ev:
                return derby_ev
        elif home_chance < 0.03:
            self.home_score += 1
            scorers = [p for p in self.home_active_players if self.paok_players[p].position != 'GK']
            scorer = random.choice(scorers)
            self.paok_players[scorer].update_stats(goals=1)
            event += f"{scorer} ({self.home_team}) GOAL! (Score: {self.home_score}-{self.away_score})"
        elif away_chance < 0.025:
            if random.random() < 0.3:
                self.away_saves += 1
                event += f"Great save by Konstantinos Tzolakis ({self.away_team})! (Score: {self.home_score}-{self.away_score})"
            else:
                self.away_score += 1
                scorers = [p for p in self.away_active_players if self.olympiacos_players[p].position != 'GK']
                scorer = random.choice(scorers)
                self.olympiacos_players[scorer].update_stats(goals=1)
                event += f"{scorer} ({self.away_team}) GOAL! (Score: {self.home_score}-{self.away_score})"
        elif foul_chance < 0.05:  # 5% foul chance
            if random.random() < 0.5:  # Home foul
                self.issue_foul(self.paok_players, self.home_active_players, minute, True)
            else:
                self.issue_foul(self.olympiacos_players, self.away_active_players, minute, False)
            event += "Foul committed."
        elif minute >= 60 and home_sub_chance < 0.015 and minute % 10 == 0:
            sub_ev = self.make_home_substitution(minute)
            if sub_ev:
                return sub_ev
            event += "No major events."
        elif minute >= 60 and away_sub_chance < 0.015 and minute % 10 == 0:
            sub_ev = self.make_away_substitution(minute)
            if sub_ev:
                return sub_ev
            event += "No major events."
        else:
            event += "Quiet minute."
        
        self.events.append(event)
        return event
    
    def simulate_full_match(self):
        self.home_score = 0
        self.away_score = 0
        self.events = []
        self.home_saves = 0
        self.away_saves = 0
        self.home_substitutions_made = 0
        self.away_substitutions_made = 0
        # Reset match-specific stats
        for players_dict in [self.paok_players, self.olympiacos_players]:
            for player in players_dict.values():
                player.goals = 0
                player.fouls = 0
                player.yellow_cards = 0
                player.red_cards = 0
                player.appearances = 0
        # Set appearances for starters
        for player in self.home_active_players:
            self.paok_players[player].update_stats(appearances=1)
        for player in self.away_active_players:
            self.olympiacos_players[player].update_stats(appearances=1)
        
        print(f"Derby Simulation: {self.home_team} vs {self.away_team}")
        print("-" * 60)
        
        for minute in range(1, 91):
            self.simulate_minute(minute)
            if minute % 10 == 0:
                print(self.events[-1])
        
        injury_time = random.randint(1, 5)
        print(f"\nInjury time: {injury_time} mins")
        for minute in range(91, 91 + injury_time):
            self.simulate_minute(minute)
            print(self.events[-1])
        
        print("-" * 60)
        print(f"Final Score: {self.home_team} {self.home_score} - {self.away_score} {self.away_team}")
        winner = "Home" if self.home_score > self.away_score else "Away" if self.away_score > self.home_score else "Draw"
        print(f"Result: {winner} wins!" if winner != "Draw" else "It's a draw!")
        
        # Stats
        print(f"\n{self.home_team} Stats:")
        print("-" * 30)
        for name, player in self.paok_players.items():
            if player.appearances > 0:
                print(player.get_stats())
        print(f"GK Saves: {self.home_saves}")
        
        print(f"\n{self.away_team} Stats:")
        print("-" * 30)
        for name, player in self.olympiacos_players.items():
            if player.appearances > 0:
                print(player.get_stats())
        print(f"GK Saves: {self.away_saves}")
        
        # Generate charts
        self.generate_charts()
        
        return self.home_score, self.away_score
    
    def generate_charts(self):
        # Chart 1: Goal distribution by team
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        home_goals = [p.goals for p in self.paok_players.values() if p.appearances > 0]
        ax1.bar(range(len(home_goals)), home_goals)
        ax1.set_title(f"{self.home_team} Goals")
        ax1.set_xlabel("Players")
        ax1.set_ylabel("Goals")
        
        away_goals = [p.goals for p in self.olympiacos_players.values() if p.appearances > 0]
        ax2.bar(range(len(away_goals)), away_goals)
        ax2.set_title(f"{self.away_team} Goals")
        ax2.set_xlabel("Players")
        ax2.set_ylabel("Goals")
        
        plt.tight_layout()
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        img.show()  # Display in environment
        buf.close()
        plt.close()
        
        # Chart 2: Fouls by team
        fig, ax = plt.subplots()
        home_fouls = sum(p.fouls for p in self.paok_players.values())
        away_fouls = sum(p.fouls for p in self.olympiacos_players.values())
        ax.bar([self.home_team, self.away_team], [home_fouls, away_fouls])
        ax.set_title("Fouls Distribution")
        ax.set_ylabel("Fouls")
        plt.show()
        plt.close()
    
    # Future enhancement: Fetch real-time stats via API
    def fetch_real_stats(self, api_key=None):
        """
        Future enhancement: Integrate with free API like API-Football.
        Example usage:
        import requests
        url = "https://v3.football.api-sports.io/players"
        headers = {"x-apisports-key": api_key}
        params = {"team": "PAOK", "season": 2025}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
        """
        print("Future: Real-time stats fetched via API-Football (requires API key).")
        return {"message": "Placeholder for real stats"}

# Example usage
if __name__ == "__main__":
    paok = PAOK FC()
    print(paok.get_team_info())
    print(paok.chant())
    
    olympiacos = Olympiacos FC()
    print(olympiacos.get_team_info())
    print(olympiacos.chant())
    
    simulator = MatchSimulator("PAOK FC", "Olympiacos FC")
    final_scores = simulator.simulate_full_match()
    
    # Future API call
    # stats = simulator.fetch_real_stats("your_api_key")
