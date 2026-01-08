# Statistical Sport Betting Model
This is a project only for showcasing my knowledge and skills, it's not (and must not be used as) financial advice. The main build uses Selenium for web-scraping the data, Poisson distribution for finding an edge, and Kelly Criterion for allocating money amongst bets.

## 1. Getting the data
For this, I used Selenium to get data from "Flashscore.com".
The function responsible for this takes in 3 parameters:
"team_name" -> should be the name of the team you want to get data for;
"opponent" -> should be a specific team's name that you want to get data for the "head to head" results);
"start_year" -> the year the game should be started from (e.g. 2020).

First, a dictionary "goals_scored" is created to hold in 4 lists: 
"goals" -> stores the amount of goals scored by the searched team for each game played in the given period;
"results" -> stores "Win"/"Lose"/"Draw" for every game played by the team in the selected period;
"home" -> stores the amount of goals scored by the team for every game played at home;
"away" -> stores the amount of goals scored by the team for every game played away.

Then, the Selenium bot goes on "Flashscore" and searches for the team, it then go to the "Results" tab and for every year in a list of years (start_year, 2025+1) it presses the "Search more matches". Every game's information is stored in a list "res". Now the elements in "res" should look like this:
(date, team1, team2, goals1, goals2, result).
(Another dictionary "head_to_head" is created to store the direct games between 2 teams)
The "for-loop" first verifies that the year is not smaller than the "start_year" parameter.
Then it takes the "team_name"'s goals, home goals, away goals and results, and adds them in the corresponding lists.
It also checks if the opponent team's name matches "opponent", if it does, it adds the game results in the corresponding lists.
Finally the function returns 2 dictionaries: "goals_scored" and "head_to_head".

## 2. Finding the "edge"
I use the Poisson distribution for this. The function "prob" takes in 4 parameters:
"avg1" -> will be the mean of the first team's goals;
"avg2" -> will be the mean of the second team's goals;
"n" -> will be a list containing the names of the teams in the order of the "avg1" and "avg2" parameters (n[0] should correspond to "avg1" team's name and n[1] should correspond to "avg2" team's name);
"goals" -> the maximum number of goals (no more than 6).
The function first creates a dictionary "goal_p" which stores for both teams a list "goals" and a list "p" (probabilities).
For every goal in the range 0-6, the "for-loop" uses the function "poisson_dist" to get the probability of team1, respectively team2, to score "i" goals, using their mean.
The function "prob_dist" (which takes in the same parameters as "prob") plots those results.

## 3. Allocation
The amount of money allocated for each bet is done using Kelly Criterion.
For an event to be taken into consideration, its expected value (considering the found probability and the event's odds) has to be positive.
The function "alloc" takes 3 parameters:
"odds" -> list of odds for each event;
"p" -> list of probabilities for each event;
"balance" -> available balance to use for the bets.
First the function creates an empty dictionary "kelly_fractions". For every pair of (odds, probability) fractional kelly will be calculated, if the value is positive, it will be added into the dictionary with "Decision": "Bet", else it will be "No bet". 
Then the sum of those fractions will be calculated, if "Decision" is "Bet", and each one will be normalized.
Finally, the function will return a list of money to put on every event given.
