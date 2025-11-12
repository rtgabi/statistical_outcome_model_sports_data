from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import date

def res_goals(res_, team_name__, goals_scored__, opponent__, head_to_head_, i_):

    if res_[i_][1] == team_name__:
        # Store the third element (the first team's amount of goals)
        goals = int(res_[i_][3])
        # Add the object in the "goals" and "home" lists
        goals_scored__['goals'].append(goals)
        goals_scored__['home'].append(goals)

        # Check the result of the game
        match res_[i_][-1]:
            case 'W':
                goals_scored__['results'].append('Win')
            case 'L':
                goals_scored__['results'].append('Loss')
            case 'D':
                goals_scored__['results'].append('Draw')

        # Check if the team played against is the team we want the h2h results
        if res_[i_][2] == opponent__:
            head_to_head_[f'{team_name__}'].append(goals)
            head_to_head_[f'{opponent__}'].append(int(res_[i_][4]))
    elif res_[i_][2] == team_name__:
        goals = int(res_[i_][4])
        goals_scored__['goals'].append(goals)
        goals_scored__['away'].append(goals)

        match res_[i_][-1]:
            case 'W':
                goals_scored__['results'].append('Win')
            case 'L':
                goals_scored__['results'].append('Loss')
            case 'D':
                goals_scored__['results'].append('Draw')

        if res_[i_][1] == opponent__:
            head_to_head_[f'{team_name__}'].append(goals)
            head_to_head_[f'{opponent__}'].append(int(res_[i_][3]))

def function2(_team_name, _opponent, _driver, _start_year, goals_scored_):

    # Store the 'WebDriverWait' object returned
    match_elements=WebDriverWait(_driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.event__match'))
    )

    # Get the 'Head to head' results of a team and its opponent
    head_to_head={
        f'{_team_name}': [],
        f'{_opponent}': []
    }

    # Store the 'text' of each object from 'match_elements', split by ','
    res=[match_elements[i].text.split('\n') for i in range(len(match_elements))]

    # Check if the year is in bounds:
    # If not, stop
    # If yes, continue with the next 'try' block
    # If a 'ValueError' is present, skip the game (this is for games where penalties are present,
                                                #  they are not taken into consideration, the team's name or date
                                                #  appears instead of the year. to be fixed)
    for i in range(len(res)):
        try:
            if int(res[i][0][-4:])<_start_year:
                break
        except ValueError:
            pass

        try:
            res_goals(res, _team_name, goals_scored_, _opponent, head_to_head, i)
        except:
            continue

    return head_to_head

def search_results(team_name_, start_year_, driver_):

    # Reject cookies when they show up
    try:
        WebDriverWait(driver_, 10).until(
            EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler'))
        ).click()
    except:
        pass

    # Click the search window
    search_box = WebDriverWait(driver_, 10).until(
        EC.element_to_be_clickable((By.ID, 'search-window'))
    )
    search_box.click()

    # Type the team's name into the search box.
    search_input = WebDriverWait(driver_, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'searchInput__input'))
    )
    search_input.send_keys(team_name_)

    time.sleep(3)

    # Click on the searched team
    team_link = WebDriverWait(driver_, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "searchResult"))
    )
    team_link.click()

    # Go to the "Results" tab
    results_tab = WebDriverWait(driver_, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='Results']"))
    )
    results_tab.click()

    current_year = date.today().year
    # Number of times to press the "Show more matches" button
    years_to_scrape = range(start_year_, current_year + 1)
    actions = ActionChains(driver_)

    for year in reversed(years_to_scrape):
        try:
            time.sleep(1)

            # Click the "Show more matches" button
            show_more_button = WebDriverWait(driver_, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[text()='Show more matches']"))
            )
            actions.move_to_element(show_more_button).click()
            show_more_button.click()
            time.sleep(3)
        except:
            print(f'No more matches to load for {year} or button not found.')

def get_team_goals(team_name: str, opponent: str, start_year: int) -> ({}, {}):
    """
    :param team_name: Name of the wanted team to look for (exactly as it can be found on "Flashscore")
    :param opponent: Name of the wanted team's opponent (exactly as it can be found on "Flashscore")
    :param start_year: The year the games should be started from (e.g. 2020)
    :return: Tuple of 2 dictionaries: 1. "goals scored", 2. "head_to_head"
    """
    # Set up the driver to open on "Flashscore"
    driver = webdriver.Chrome()
    driver.maximize_window()
    base_url = 'https://www.flashscore.com/'

    # "goals" -> list which contains all the goals a team scored in the selected period
    # "results" -> list of "Win"/"Lose"/"Draw" for every game played by the team in the selected period
    # "home" -> list of goals scored by the team in Home games
    # "away" -> list of goals scored by the team in Away games
    goals_scored = {
        'goals': [],
        'results': [],
        'home': [],
        'away': []
    }

    try:
        driver.get(base_url)

        search_results(team_name, start_year, driver)

        head_to_head_=function2(team_name, opponent, driver, start_year, goals_scored)

    finally:
        driver.quit()

    return goals_scored, head_to_head_