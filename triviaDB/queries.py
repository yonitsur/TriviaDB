import mysql.connector
import pandas as pd
import random
import time
import os
import msvcrt

def  q1():
    height_weight = random.choice(['height', 'weight'])
    max_min_avg_sum = random.choice(['max', 'min', 'avg', 'sum'])
    random_par_teem_year ="""\
SELECT Teams.team, Players.year
FROM Teams
JOIN Players ON Teams.team_id = Players.team_id
ORDER BY RAND() LIMIT 1""".format()
    cursor.execute(random_par_teem_year)
    teem_year = cursor.fetchall()
    team_param = teem_year[0][0]
    year_param = teem_year[0][1]
    query = """\
SELECT {}(Players.{})
FROM Players
JOIN Teams ON Players.team_id = Teams.team_id
WHERE Players.year = '{}'
AND Teams.team = '{}'
GROUP BY Teams.team_id""".format(max_min_avg_sum,height_weight,year_param,team_param)
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    question = "What is the {} {} of players in team '{}' in {}?".format(max_min_avg_sum,height_weight,team_param,year_param)
    # get two wrong answers:
    wrong_answers1 = correct_answer+random.randint(1,3)
    wrong_answers2 = correct_answer-random.randint(1,3)
    return [[question, correct_answer, wrong_answers1, wrong_answers2]]
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))


def q2():
    max_min_avg_sum = random.choice(['max', 'min', 'avg','sum'])
    random_par_teem_year_stat_name ="""\
SELECT Teams.team, Players_Season_Stats.year, Players_Season_Stats.stat_name
FROM Teams
JOIN Players ON Teams.team_id = Players.team_id
JOIN Players_Season_Stats ON Players.player_id = Players_Season_Stats.player_id
ORDER BY RAND() LIMIT 1""".format()
    cursor.execute(random_par_teem_year_stat_name)
    teem_year_stat_name = cursor.fetchall()
    team_param = teem_year_stat_name[0][0]
    year_param = teem_year_stat_name[0][1]
    stat_name_param = teem_year_stat_name[0][2]
    query="""\
SELECT {}(Players_Season_Stats.stat_value)
FROM Players_Season_Stats
JOIN Players ON Players_Season_Stats.player_id = Players.player_id
WHERE Players_Season_Stats.year = '{}'
AND Players.team_id = (SELECT team_id FROM Teams WHERE team = '{}')
AND Players_Season_Stats.stat_name = '{}'""".format(max_min_avg_sum,year_param,team_param,stat_name_param)
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    question = "what is the {} {} made by players from {} in {}?".format(max_min_avg_sum,stat_name_param,team_param,year_param)
    # get two wrong answers:
    wrong_answers1 = correct_answer+random.randint(1,3)
    wrong_answers2 = max(correct_answer-random.randint(1,3),0)
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    return [[question, correct_answer, wrong_answers1, wrong_answers2]]


def q3():
    highest_lowest = random.choice([['highest', 'DESC'], ['lowest', 'ASC']])
    type_outlet = random.choice(['media_type', 'outlet'])
    random_par_year_type ="""\
SELECT Games.year, Games_Media.{}
FROM Games
JOIN Games_Media ON Games.id = Games_Media.id
ORDER BY RAND() LIMIT 1""".format(type_outlet)
    cursor.execute(random_par_year_type)
    year_type = cursor.fetchall()
    year_param = year_type[0][0]
    type_param = year_type[0][1]
    query = """\
SELECT Venue.stadium_name, COUNT(*) as coverage_count
FROM Games_Media
JOIN Games ON Games_Media.id = Games.id
JOIN Teams ON Teams.team_id = Games.home_team_id
JOIN Venue ON Venue.stadium_id = Teams.stadium_id
WHERE Games.year = '{}'
AND Games_Media.{} = '{}'
GROUP BY Venue.stadium_name
ORDER BY coverage_count {}""".format(year_param,type_outlet,type_param, highest_lowest[-1])
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    question = "Which venue had the {} coverage by {} {} in {}?".format(highest_lowest[0], type_outlet, type_param,year_param)
    get_wrong_answers = """\
SELECT Venue.stadium_name
FROM Venue
WHERE Venue.stadium_name != '{}' ORDER BY RAND() LIMIT 2""".format(correct_answer)
    cursor.execute(get_wrong_answers)
    wrong_answers = cursor.fetchall()
    wrong_answers1 = wrong_answers[0][0]
    wrong_answers2 = wrong_answers[1][0]
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    return [[question, correct_answer, wrong_answers1, wrong_answers2]]

def q4():
    max_min_avg_sum = random.choice(['max', 'min', 'avg','sum'])
    random_par_hometown_year_stat_name ="""\
SELECT Players.hometown, Players_Season_Stats.year, Players_Season_Stats.stat_name
FROM Players
JOIN Players_Season_Stats ON Players.player_id = Players_Season_Stats.player_id
ORDER BY RAND() LIMIT 1""".format()
    cursor.execute(random_par_hometown_year_stat_name)
    hometown_year_stat_name = cursor.fetchall()
    hometown_param = hometown_year_stat_name[0][0]
    year_param = hometown_year_stat_name[0][1]
    stat_name_param = hometown_year_stat_name[0][2]
    query="""\
SELECT {}(Players_Season_Stats.stat_value)
FROM Players_Season_Stats
JOIN Players ON Players_Season_Stats.player_id = Players.player_id
WHERE Players_Season_Stats.year = '{}'
AND Players.hometown = '{}'
AND Players_Season_Stats.stat_name = '{}'; """.format(max_min_avg_sum,year_param,hometown_param,stat_name_param)
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    question = "what is the {} {} made by players from hometown {} in {}?".format(max_min_avg_sum,stat_name_param,hometown_param,year_param)
    # get two wrong answers:
    wrong_answers1 = correct_answer+random.randint(1,3)
    wrong_answers2 = max(correct_answer-random.randint(1,3),0)
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    return [[question, correct_answer, wrong_answers1, wrong_answers2]]

def q5():
    max_min_avg_sum = random.choice(['max', 'min', 'avg','sum'])
    highest_lowest = random.choice([['highest', 'max'], ['lowest', 'min']])
    player_team = random.choice(['Players', 'Teams'])
    random_par_year_stat_name ="""\
SELECT {0}_Season_Stats.year, {0}_Season_Stats.stat_name
FROM {0}_Season_Stats
ORDER BY RAND() LIMIT 1""".format(player_team)
    cursor.execute(random_par_year_stat_name)
    year_stat_name = cursor.fetchall()
    year_param = year_stat_name[0][0]
    stat_name_param = year_stat_name[0][1]
    year_param = random.choice([year_param])
    query = """\
WITH stat_by AS (
    SELECT {0}.hometown, {4}({0}_Season_Stats.stat_value) as stat
    FROM {0}
    JOIN {0}_Season_Stats ON {0}.team_id = {0}_Season_Stats.team_id
    WHERE {0}_Season_Stats.stat_name = '{1}'
    AND {0}_Season_Stats.year = '{2}'
    GROUP BY {0}.hometown )
SELECT hometown, stat
FROM stat_by
WHERE stat = (SELECT {3}(stat) FROM stat_by);""".format(player_team,stat_name_param,year_param,highest_lowest[-1],max_min_avg_sum)
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    question = "Which {}'s hometown had the {} {} of {} made by {} from that hometown in {}?".format(player_team,highest_lowest[0],max_min_avg_sum, stat_name_param,player_team,year_param)
    # get two wrong answers:
    get_wrong_answers = """\
SELECT {0}.hometown
FROM {0}
WHERE {0}.hometown != '{1}' ORDER BY RAND() LIMIT 2""".format(player_team,correct_answer)
    cursor.execute(get_wrong_answers)
    wrong_answers = cursor.fetchall()
    wrong_answers1 = wrong_answers[0][0]
    wrong_answers2 = wrong_answers[1][0]
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    return [[question, correct_answer, wrong_answers1, wrong_answers2]]

def q6():

    # create random view

    params2=[["home_wins","CASE WHEN home_team_id = Teams.team_id AND home_points > away_points THEN 1 ELSE 0 END"],
            ["home_losses","CASE WHEN home_team_id = Teams.team_id AND home_points < away_points THEN 1 ELSE 0 END"],
            ["away_wins","CASE WHEN away_team_id = Teams.team_id AND away_points > home_points THEN 1 ELSE 0 END"],
            ["away_losses", "CASE WHEN away_team_id = Teams.team_id AND away_points < home_points THEN 1 ELSE 0 END"],
            ["wins","CASE WHEN home_team_id = Teams.team_id AND home_points > away_points THEN 1 WHEN away_team_id = Teams.team_id AND away_points > home_points THEN 1 ELSE 0 END"],
            ["losses","CASE WHEN home_team_id = Teams.team_id AND home_points < away_points THEN 1 WHEN away_team_id = Teams.team_id AND away_points < home_points THEN 1 ELSE 0 END"],
            ["home_games","CASE WHEN home_team_id = Teams.team_id THEN 1 ELSE 0 END"],
            ["away_games","CASE WHEN away_team_id = Teams.team_id THEN 1 ELSE 0 END"],
            ["games","CASE WHEN home_team_id = Teams.team_id THEN 1 WHEN away_team_id = Teams.team_id THEN 1 ELSE 0 END"]]

    params=[["home_points","CASE WHEN home_team_id = Teams.team_id THEN home_points ELSE 0 END"],
            ["away_points", "CASE WHEN away_team_id = Teams.team_id THEN away_points ELSE 0 END"],
            ["points","CASE WHEN home_team_id = Teams.team_id THEN home_points ELSE away_points END"],
            ["home_points_conceded","CASE WHEN home_team_id = Teams.team_id THEN away_points ELSE home_points END"],
            ["away_points_conceded","CASE WHEN away_team_id = Teams.team_id THEN home_points ELSE away_points END"],
            ["points_conceded","CASE WHEN home_team_id = Teams.team_id THEN away_points ELSE home_points END"]]
    params = random.sample(params, 2)
    params2 = random.sample(params2, 2)
    par1 = params[0]
    par2 = params[1]
    par3 = params2[0]
    par4 = params2[1]
    avg_sum_max_min_1 = random.choice(['avg','sum', 'max', 'min'])
    avg_sum_max_min_2 = random.choice(['avg','sum', 'max', 'min'])
    col1 ="{}_{}".format(avg_sum_max_min_1,par1[0])
    col2 ="{}_{}".format(avg_sum_max_min_2,par2[0])
    col3 ="sum_{}".format(par3[0])
    col4 ="sum_{}".format(par4[0])
    # check if a view called  stats already exists
    cursor.execute("DROP VIEW IF EXISTS stats;")
    query = """\
CREATE VIEW stats AS
SELECT Teams.team, Games.year, Coach.full_name as 'coach',
{}({}) as {},
{}({}) as {},
SUM({}) as {},
SUM({}) as {}
FROM Games
JOIN Teams ON home_team_id = Teams.team_ID OR away_team_id = Teams.team_ID
JOIN Coach_team ON Coach_team.team_id = Teams.team_ID
AND Coach_team.year = Games.year
JOIN Coach ON Coach.coach_id = Coach_team.coach_id
GROUP BY Teams.team, Games.year; """.format(avg_sum_max_min_1,par1[1],col1,avg_sum_max_min_1,par2[1],col2, par3[1],col3, par4[1],col4)
    cursor.execute(query)
    # generate question from the view
    ret=[]
    # q1
    rand_col = random.choice([col1,col2,col3,col4])
    team_coach = random.choice(['team','coach'])
    highest_lowest = random.choice([['highest','DESC'],['lowest','ASC']])
    rand_par_year = """\
SELECT DISTINCT year
FROM stats
ORDER BY RAND()
LIMIT 1;"""
    cursor.execute(rand_par_year)
    rand_par_year = cursor.fetchall()[0][0]
    query = """\
SELECT {}
FROM stats
WHERE year = {}
ORDER BY {} {}
LIMIT 1;""".format(team_coach,rand_par_year,rand_col,highest_lowest[-1])
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    rand_col = rand_col.replace('_',' ').replace('avg','average of').replace('sum','sum of')
    question = """\
Which {} had the {} {} in {}?""".format(team_coach,highest_lowest[0],rand_col,rand_par_year)
    get_wrong_answers = """\
SELECT DISTINCT {}
FROM stats
WHERE {} != '{}'
ORDER BY RAND()
LIMIT 2;""".format(team_coach,team_coach,correct_answer)
    cursor.execute(get_wrong_answers)
    wrong_answers = cursor.fetchall()
    wrong_answers1 = wrong_answers[0][0]
    wrong_answers2 = wrong_answers[1][0]
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    ret+= [[question,correct_answer,wrong_answers1,wrong_answers2]]
    # q2
    rand_col = random.choice([col1,col2,col3,col4])
    team_coach = random.choice(['team','coach'])
    rand_par_year_Coach_team = """\
SELECT year, {}, {}
FROM stats
ORDER BY RAND() LIMIT 1;""".format(team_coach, rand_col)
    cursor.execute(rand_par_year_Coach_team)
    rand_par_year_Coach_team = cursor.fetchall()
    rand_par_year = rand_par_year_Coach_team[0][0]
    rand_par_Coach_team = rand_par_year_Coach_team[0][1]
    correct_answer = rand_par_year_Coach_team[0][2]
    rand_col = rand_col.replace('_',' ').replace('avg','average of').replace('sum','sum of').replace('max','maximum of').replace('min','minimum of')
    question = """\
what is the {} that {} {} had in {}?""".format(rand_col,team_coach,rand_par_Coach_team,rand_par_year)
    wrong_answers1 = correct_answer+random.randint(1,3)
    wrong_answers2 = max(correct_answer-random.randint(1,3),0)
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    ret+= [[question,correct_answer,wrong_answers1,wrong_answers2]]
    # q3
    rand_col = random.choice([col1,col2,col3,col4])
    team_coach = random.choice(['team','coach'])
    highest_lowest = random.choice([['highest','DESC'],['lowest','ASC']])
    rand_par_team_coach = """\
SELECT DISTINCT {}
FROM stats
ORDER BY RAND()
LIMIT 1;""".format(team_coach)
    cursor.execute(rand_par_team_coach)
    rand_par_team_coach = cursor.fetchall()[0][0]
    query = """\
SELECT year, {}
FROM stats
WHERE {} = '{}'
ORDER BY {} {}
LIMIT 1;""".format(rand_col,team_coach,rand_par_team_coach,rand_col,highest_lowest[-1])
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    rand_col = rand_col.replace('_',' ').replace('avg','average of').replace('sum','sum of')
    question = """\
Which year did {} {} have the {} {}?""".format(team_coach,rand_par_team_coach,highest_lowest[0],rand_col)
    get_wrong_answers = """\
SELECT DISTINCT year
FROM stats
WHERE year != {}
ORDER BY RAND()
LIMIT 2;""".format(correct_answer)
    cursor.execute(get_wrong_answers)
    wrong_answers = cursor.fetchall()
    wrong_answers1 = wrong_answers[0][0]
    wrong_answers2 = wrong_answers[1][0]

    ret+= [[question,correct_answer,wrong_answers1,wrong_answers2]]


    delete_view = """DROP VIEW stats;"""
    cursor.execute(delete_view)

    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    return ret

def  q7():
    # check if fulltext index exists:
    cursor.execute("SHOW INDEX FROM Players WHERE Key_name = 'hometown'")
    indexed = cursor.fetchall()
    if not indexed:
        fulltext_index ="""\
ALTER TABLE Players ADD FULLTEXT(hometown)""".format()
        cursor.execute(fulltext_index)

    hometown_rand ="""\
SELECT Players.hometown
FROM Players
ORDER BY RAND() LIMIT 1""".format()
    max_min_avg_sum = random.choice(['MAX', 'MIN', 'AVG', 'SUM'])
    weight_height_pick = random.choice(['weight', 'height', 'pick'])
    par1 = "{}({})".format(max_min_avg_sum,weight_height_pick)
    random_question = random.choice([par1,par1,par1, 'COUNT(player_id)'])
    cursor.execute(hometown_rand)
    hometown = cursor.fetchall()[0][0]
    query = """\
SELECT {}
FROM Players
WHERE Match(hometown) Against('{}')
""".format(random_question, hometown)
    cursor.execute(query)
    correct_answer = cursor.fetchall()[0][0]
    question = "What is the {} of players originally from '{}'?".format(random_question ,hometown)
    # get two wrong answers:
    wrong_answers1 = correct_answer+random.randint(1,3)
    wrong_answers2 = max(correct_answer-random.randint(1,3), 0)
    # print(question)
    # print("A. {}".format(correct_answer))
    # print("B. {}".format(wrong_answers1))
    # print("C. {}".format(wrong_answers2))
    return [[question,correct_answer,wrong_answers1,wrong_answers2]]


db_name = "TriviaDB"
cnx = mysql.connector.connect(user='root', password='Sisma4148@', host='localhost', port=3306, database=db_name)
cursor = cnx.cursor()

questions = []
questions += q1()
questions += q2()
questions += q3()
questions += q4()
questions += q5()
questions += q6()
questions += q7()

random.shuffle(questions)
print("Welcome to the the CFDB-Trivia Game!")
input("Press 'Enter' to start the game")
os.system('cls' if os.name == 'nt' else 'clear')
score = 0

for k,question in enumerate(questions):
    print("*****************")
    print ("    QUESTION {} ".format(k+1))
    print("*****************")
    correct_answer = question[1]
    print(question[0])
    question = question[1:]
    random.shuffle(question)
    for i, answer in enumerate(question):
        print("{}. {}".format(i+1,answer))

    start_time = time.time()
    print()
    over_time = False
    user_answer = ''
    while user_answer>'3' or user_answer<'1' and not over_time:
        user_answer = input("Enter the number of your answer (1-3)")
        elapsed_time = time.time() - start_time
        if elapsed_time > 10:
            over_time = True
            print("You took too long to answer.")
            break

    if not over_time:
        if question[int(user_answer)-1] == correct_answer:
            print("Correct!")
            score += 1
        else:
            print("Incorrect.")

    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
print("Your final score is {} out of {}.".format(score, len(questions)))


cursor.close()
cnx.close()
p=0


