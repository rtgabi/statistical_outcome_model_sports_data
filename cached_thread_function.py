from functools import cache
from concurrent.futures import ThreadPoolExecutor

@cache
def open_web_scraper(max_workers_, function, name_1, name_2, year):
    with ThreadPoolExecutor(max_workers=max_workers_) as executor:
        res1=executor.submit(function, name_1, name_2, year)
        res2=executor.submit(function, name_2, name_1, year)

        team_1=res1.result()
        team_2=res2.result()

    return team_1, team_2