
import mysql.connector
import pandas as pd
import numpy as np
import random
import sqlite3



def create_Table(table_name,attrs,primery_key,index_key):
    table_params = ",\n\t".join(attrs)+",\n\tPRIMARY KEY ({})".format(primery_key)
    table = """CREATE TABLE IF NOT EXISTS {} ({})""".format(table_name,table_params)
    data_params = ', '.join([s.split()[0] for s in attrs])
    add_item = ("INSERT IGNORE INTO {}\n({})\nVALUES ({})".format(table_name,data_params,', '.join(['%s']*len(attrs))))
    check_table = "SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema = '{}' AND table_name = '{}'".format(db_name, table_name)
    cursor.execute(check_table)
    if cursor.fetchone()[0]:
        cursor.execute("DROP TABLE {}".format(table_name))
    cursor.execute(table)
    index = "CREATE INDEX {}_index ON {} ({})".format(table_name, table_name, index_key)
    cursor.execute(index)
    df = pd.read_csv("{}.csv".format(table_name))
    df = df.dropna()
    for i, row in df.iterrows():
        data_winner=()
        for att in attrs:
            a = att.split()
            if "INT" in a[-1]:
                data_winner+=(int(row[a[0]]),)
            elif "BIGINT" in a[-1]:
                data_winner+=(int(row[a[0]]),)
            elif "FLOAT" in a[-1]:
                data_winner+=(float(row[a[0]]),)
            else:
                data_winner+=(row[a[0]],)
        cursor.execute(add_item, data_winner)

    cnx.commit()
def create_tables():
    #create_Table("Winner_Season",["year INT(8)","team_id INT(11)","coach_id INT(11)","winner_score INT(8)","runner_up_score INT(11)","runner_up_id INT(11)"],"year","year")
    #print("Winner_Season Table Created")
    create_Table("Coach", ["coach_id INT(11)","full_name VARCHAR(255)"], "coach_id", "coach_id")
    print("Coach Table Created")
    # create_Table("Coach_team", ["coach_id INT(11)","team_id INT(11)","year INT(11)"], "team_id, year", "year")
    # print("Coach_team Table Created")
    #create_Table("Venue", ["stadium_id INT(11)", "stadium_name VARCHAR(255)","staduim_capacity INT(11)", "year_constructed INT(11)"], "stadium_id", "stadium_id")
    #print("Venue Table Created")
    #create_Table("Teams_Season_Stats", ["year INT(11)","team_id INT(11)","stat_name VARCHAR(255)","stat_value INT(11)"], "year, team_id, stat_name", "team_id, stat_name")
    #print("Teams_Season_Stats Table Created")
    #create_Table("Games", ["id BIGINT(20)","year  INT(11)","week  INT(11)","home_team_id INT(11)","home_points  INT(11)","away_team_id INT(11)","away_points  INT(11)","home_win INT(11)","away_win INT(11)"], "id", "id")
    #print("Games Table Created")
    #create_Table("Games_Media", ["id INT(11)","media_type VARCHAR(255)","outlet VARCHAR(255)"], "id, media_type, outlet", "id, media_type, outlet")
    #print("Games_Media Table Created")
    #create_Table("Teams",["team_ID INT(11)","team VARCHAR(255)","color VARCHAR(255)",
    #                       "hometown VARCHAR(255)","stadium_id INT(11)"],"team_ID","team_ID, team")
    #print("Teams Table Created")
    #create_Table("Players",["player_id INT(11)", "nfl_team VARCHAR(255)","team_id INT(11)","year INT(11)","round INT(11)", "pick INT(11)",
    #                       "name VARCHAR(255)","position VARCHAR(255)","height INT(11)","weight INT(11)","hometown VARCHAR(255)"],
    #                       "player_id","player_id")
    #print("Players Table Created")
    #create_Table("Players_Season_Stats", ["year INT(11)","player_id INT(11)","team_id INT(11)","stat_name VARCHAR(255)","stat_value INT(11)"], "year, player_id, stat_name", "stat_name")
    #print("Players_Season_Stats Table Created")
    print("Done")

def create_db():
    cnx = mysql.connector.connect(user='', password='', host='localhost', port=3306)
    cursor = cnx.cursor(buffered=True)
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_name))
    cnx.commit()
    cursor.close()
    cnx.close()



db_name = "TriviaDB"
#create_db()
cnx = mysql.connector.connect(user='', password='', host='localhost', port=3306, database=db_name)
cursor = cnx.cursor()
create_tables()
cursor.close()
cnx.close()
p=0
