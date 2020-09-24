import csv

CANDIDATE_CSV_FILENAME = 'config/candidatos_saoluis_2020.csv'

def get_cadidates_twitter_user_id():

    users_id = []

    with open(CANDIDATE_CSV_FILENAME, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            users_id.append(row['Twitter UserId'])

    return users_id

def main():
    print(get_cadidates_twitter_user_id())

if __name__ == "__main__":
    main()