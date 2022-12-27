import json
from datetime import datetime
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
from connect import get_channel_list, record_publication
import time
import schedule


timeout = 30
ua_chrome = " ".join(["Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                      "AppleWebKit/537.36 (KHTML, like Gecko)",
                      "Chrome/108.0.0.0 Safari/537.36"])
headers = {"user-agent": ua_chrome}
amount_publication = 0


def get_info_about_channel_page(url, channel_id, channel_name):
    global amount_publication
    try:
        response = requests.get(url=url, headers=headers, timeout=timeout)
    except TimeoutError:
        response = requests.get(url=url, headers=headers, timeout=timeout)
    json_object = response.json()
    publications = json_object["items"]
    for publication in publications:
        publication_link = publication["link"]
        publication_date = publication["publication_date"]
        publication_date = datetime.utcfromtimestamp(int(publication_date))
        today = datetime.today()
        month = timedelta(days=30)
        last_publication_date = today - month
        if publication_date < last_publication_date:
            next_page = "stop"
            return next_page
        publication_type = publication["type"]
        if publication_type != "gif":
            publication_type = "brief/article"
            response = requests.get(publication["link"])
            bs_object = BeautifulSoup(response.content, "lxml")
            start_index = str(bs_object).index('"views')
            stop_index = str(bs_object).index('"comments"')
            views_json = "{" + str(bs_object)[start_index:stop_index-1] + "}"
            views_json = json.loads(views_json)
            views = views_json["views"]
            end_views = views_json["viewsTillEnd"]
            views_time = views_json["sumViewTimeSec"]
        else:
            publication_type = "gif/video"
            video_object = publication["video"]
            views = video_object["views"]
            views_time = video_object["duration"]
            end_views = 0
        percent_end_views = int((end_views / views) * 100)
        publication_title = publication["title"]
        social_info = publication["socialInfo"]
        if 'likesCount' in social_info.keys():
            likes = publication["socialInfo"]["likesCount"]
        else:
            likes = 0
        if "commentCount" in social_info.keys():
            comments = publication["socialInfo"]["commentCount"]
        else:
            comments = 0
        amount_publication += 1
        print(amount_publication)
        record_publication(channel_id=channel_id, channel_name=channel_name, publication_name=publication_title,
                           publication_type=publication_type, publication_date=publication_date, views=views,
                           end_views=end_views, percent_end_views=percent_end_views, views_time=views_time,
                           comments=comments, likes=likes, amount_publication=amount_publication,
                           publication_link=publication_link)
    if len(publications) == 0:
        next_page = "stop"
    else:
        next_page = json_object["more"]["link"]
    return next_page


def get_info_about_channel(channel_id_type, channel_id, channel_name):
    if channel_id_type == "id":
        url = f"https://dzen.ru/api/v3/launcher/more?country_code=ru&clid=1400&_csrf=983f46c25c2beadf84b4683c1144fd427965e7ca-1671798481750-0-8310718861670787050%3A0&lang=ru&channel_id={channel_id}"
    else:
        url = f"https://dzen.ru/api/v3/launcher/more?country_code=ru&_csrf=c73948b0048de8b220f09b542e74deda2c3ae7e7-1671881111947-0-8310718861670787050%3A0&clid=1400&lang=ru&channel_name={channel_id}"
    next_page = get_info_about_channel_page(url=url, channel_id=channel_id, channel_name=channel_name)
    amount_page = 0
    while next_page != "stop" and next_page != "":
        amount_page += 1
        next_page = get_info_about_channel_page(url=next_page, channel_id=channel_id, channel_name=channel_name)
        if next_page != "stop" and next_page != "":
            print(f'Страница {amount_page} канала "{channel_name}" успешно обработана')


def parsing():
    channels = get_channel_list()
    for channel in channels:
        channel_name = channel["channel_name"]
        channel_url = channel["channel_url"]
        channel_id = channel_url.split("/")[-1]
        if "id" in channel_url:
            channel_id_type = "id"
        else:
            channel_id_type = "name"
        print(f'[INFO] Начался анализ канала "{channel_name}"')
        get_info_about_channel(channel_id=channel_id, channel_id_type=channel_id_type,
                               channel_name=channel_name)
        print(f'[INFO] Анализ канала "{channel_name}" закончен')


def main():
    mode = input("Выберете режим запуска парсера: 1 - в штатном режиме, 2 - запустить сейчас")
    if mode == "1":
        print('[INFO] Программа запущена в штатном режиме')
        schedule.every().days.at("08:30").do(parsing)
        while True:
            schedule.run_pending()
            time.sleep(1)
    elif mode == "2":
        print("[INFO] Программа запущена в срочном режиме")
        parsing()


if __name__ == "__main__":
    main()
