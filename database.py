from pymysql import cursors
import pymysql
from config import user, password, port, host, db_name, groups, groups_text


def database(query):
    try:
        connection = pymysql.connect(port=port, host=host, user=user, password=password,
                                     database=db_name, cursorclass=cursors.DictCursor)
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return result
        except Exception as ex:
            print(f"Something Wrong: {ex}")
            return "Error"
        finally:
            connection.close()
    except Exception as ex:
        print(f"Connection was not completed because {ex}")
        return "Error"


def create_table_publications():
    query = """CREATE TABLE publications (channel_id VARCHAR(100), channel_name VARCHAR(500), 
               publication_name VARCHAR(500), publication_type VARCHAR(50), publication_date VARCHAR(50), views INT, 
               end_views INT, percent_end_views INT, views_time FLOAT, comments INT, likes INT);"""
    result = database(query=query)
    if result != "Error":
        print('[INFO] Таблица publications успешно создана в базе данных')


def create_table_channels():
    query = """CREATE TABLE channels (channel_id VARCHAR(100) UNIQUE, channel_name VARCHAR(500), 
                                group_id INT, group_name VARCHAR(50), channel_id_type VARCHAR(50));"""
    result = database(query=query)
    if result != "Error":
        print('[INFO] Таблица channels успешно создана в базе данных')


def get_all_channels():
    query = "SELECT channel_id, channel_id_type, channel_name FROM channels;"
    result = database(query=query)
    return result


def clean_table_publications():
    query = "DROP TABLE publications;"
    result = database(query=query)
    if result != "Error":
        print("[INFO] Таблица publications очищена")
    create_table_publications()


def record_publication_info(channel_id, channel_name, publication_name, publication_type, publication_date, views,
                            end_views, percent_end_views, views_time, comments, likes):
    query = f"""INSERT INTO publications VALUES ('{channel_id}', '{channel_name}', '{publication_name}', 
                '{publication_type}', '{publication_date}', {views}, {end_views}, {percent_end_views}, {views_time},
                {comments}, {likes});"""
    result = database(query=query)
    if result != "Error":
        print(f'[INFO] Запись "{publication_name[:40]}..." успешно добавлена в базу данных')


def add_channel(channel_url, channel_name, group_id):
    channel_id = channel_url.split("/")[-1]
    if "id" in channel_url:
        channel_id_type = "id"
    else:
        channel_id_type = "name"
    group_name = groups[group_id]
    query = f"""INSERT INTO channels VALUES ('{channel_id}', '{channel_name}', {group_id}, 
                                             '{group_name}', '{channel_id_type}');"""
    result = database(query=query)
    if result != "Error":
        print("[INFO] Канал добавлен в базу данных")


def main():
    mode = input("[INPUT] Выберете режим (1 - создание таблиц базы данных, 2 - добавить канал): >>> ")
    if mode == "1":
        create_table_publications()
        create_table_channels()
    elif mode == "2":
        continue_text = ""
        while continue_text != "2":
            channel_url = input("[INPUT] Введите url канала: >>> ")
            channel_name = input("[INPUT] Введите название: >>> ").strip().lower()
            print(groups_text)
            group_id = int(input('[INFO] Выберете группу канала из вышеперечисленных: >>> '))
            add_channel(channel_url=channel_url, channel_name=channel_name, group_id=group_id)
            continue_text = input("[INPUT] Продолжить добавлять каналы? (1 - продолжить, 2 - выйти из программы): >>> ")


if __name__ == "__main__":
    main()
