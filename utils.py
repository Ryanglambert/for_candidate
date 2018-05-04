from collections import defaultdict
from io import BytesIO
from itertools import combinations
from memory_profiler import profile

import requests

mask = {'team', 'player_id_code'}


def get_header():
    with open('README.txt', 'r') as f:
        for i, line in enumerate(f):
            if i == 49:
                return line.split(',')


def clean(header):
    return [i.lower().replace(' ', '_') for i in header]


def get_year(year: str):
    result = requests.get('https://s3.amazonaws.com/dd-interview-data'
                          '/data_scientist/baseball/appearances'
                          '/{}/{}-0,000'.format(year, year))
    return result.content


def read_record(byte_record: bytes):
    return byte_record.decode()


def get_local_year(year: str):
    with open('bball_records/{}'.format(year), 'rb') as f:
        return f.read()


def save_years(start: int, end: int):
    for year in range(start, end + 1):
        year_bytes = get_year(year)
        with open('bball_records/{}'.format(year), 'wb') as f:
            f.write(year_bytes)


def marshal_record(string_record: str):
    fields = string_record.split(',')
    return dict(zip(header, fields))


def mask_record(record: dict):
    return {field: record[field]
            for field in list(mask.intersection(record))}


def parse_record(record: bytes):
    return mask_record(marshal_record(read_record(record)))


class BaseBallRecords(object):
    def __init__(self,
                 start_year: int=1871,
                 end_year: int =2014,
                 verbose=True,
                 use_local=True):
        self.years = range(start_year, end_year + 1)
        self.use_local = use_local
        self.verbose = verbose

    def __iter__(self):
        # Paginated by years
        for year in self.years:
            if self.verbose:
                print('for year: {}'.format(year))
            if self.use_local:
                year_bytes = get_local_year(year)
            else:
                year_bytes = get_year(year)
            year_records = BytesIO(year_bytes)
            for record in year_records:
                parsed = parse_record(record)
                yield parsed


@profile
def get_player_team_maps(verbose=True):
    team_to_player_id = defaultdict(set)
    bball_records = BaseBallRecords(verbose=verbose)
    for idx, record in enumerate(bball_records):
        player_id = record['player_id_code']
        team = record['team']
        team_to_player_id[team].add(player_id)
    return team_to_player_id


def check_team_player_intersect(team_i, team_j, team_k, team_to_player_id):
    intersection = team_to_player_id[team_i]\
        .intersection(team_to_player_id[team_j])\
        .intersection(team_to_player_id[team_k])
    return intersection


@profile
def get_shared_player_teams(team_to_player_id, min_players_shared=50):
    teams_that_share = []
    for team_i, team_j, team_k in combinations(team_to_player_id.keys(), 3):
        team_intersection = check_team_player_intersect(team_i,
                                                        team_j,
                                                        team_k,
                                                        team_to_player_id)
        if team_intersection and len(team_intersection) >= min_players_shared:
            teams_that_share.append((team_i, team_j, team_k))

    return teams_that_share


def run():
    # create hash table
    team_to_player_id = get_player_team_maps(verbose=False)
    # aggregate triples of teams that share 50 players
    shared_teams = get_shared_player_teams(team_to_player_id)

    print("total possible team triples: {}"
          .format(len(list(combinations(team_to_player_id, 3)))))
    print("triples that shared 50 players: {}"
          .format(len(shared_teams)))
    print(shared_teams)


header = clean(get_header())


if __name__ == '__main__':
    run()
