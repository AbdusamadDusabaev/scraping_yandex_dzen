import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import time


api_json = {
  "type": "service_account",
  "project_id": "temporal-web-372917",
  "private_key_id": "714c09acf62f8dde1833711013f5364b8407341f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDBRi1JB23Qf/Vj\nuIPq485XzSl102AcXpoHIBsUxSifTYYqU1AUE9+defnInp93sqXlCYd4FhXYkZDI\nN4HPswSOYDgOKoRz3IqseEFScaWtiN+5Ch6KLG3tie1bU9EvJ/WoHS3DncQ34zVj\nu4ZlREHPksHjhGNBcRqEFnxDeOsXE+HjNC4EBb2N+WMTrXVWK74shpFoeOtadZ2h\nNLhhkc3r8G1zhfM24c6Vktqp36a/piJpgyFWXiyMTdVhaqKQI5dwhn7qFwDhKBfm\n4BdM2ILOBrIAKxg3YxjZJuZWLN4wLTyCnT0bHHqNOeyF/ilI1EQhnSmSoI7Z+GGY\ng5WjYG9/AgMBAAECggEAOHq4/hfZK+5Qt+jyR+B1aqwOGxv/gJrWmRF1SH8LDW56\nsACzrIJYPO0ppMpR4IlIuGMt/tY5YRW8wP2Thi4SvUZ56w3asf73WUo1EJIcb9dJ\nRYoi/Y7ZOuqs/ZzDSuv6+js4pesDLa/MaM4iipJFRxLkbQfBd5zFOmdVvePmk1He\ncN7K1BIgc/ZoasV6wqd10FdNY2wl926YALi5HWZjNH3dfn8aYnpDxToZ5B7vAKlF\nh6w9S3ULw2J0utE3KW7N4o3edlyGBnmNEbZO2DsJLhSumFARvz+OSDqFwk9wM23j\ngiWE+RFM6TUcXUlyZq0xH4Jql8h+kw1Ssf2JJItZgQKBgQDpN4BlLN4Xz3zb7jxI\nwMry7qa+aczLINmsBga7GHMvL3dnFgty+ZHMlOlvTIP8kWvWh3I+sWDpFNwG3a5m\n7kuQSIA04sNZ7wTD5/HhUxXQqPP5C6OI86L8oPhM8yrkHU4NW/yJsFJd0Br2/UUU\nWLI0dYg2ut8C5nyCiAe1cBN4/wKBgQDUJ8Cl0FTholm93LFqf4UbJyKkrMBpdKMw\ninsqocG+el8bMxqAASbjJsQ0mnfVk1pT/2V+KU/2fIOycKXWLj0sK/bnRq4pitze\nmjl0F46xP2bHdWSSCLlVLEEnIjpmM7NBCRzhLaGhWogXI+yYmHogWE9IAH25Uzoi\npO3a8jCJgQKBgQChJiXFQ5SPdWL8gYkMaJOT+84iQu8s6R0f3eYmwAVPdIgYJkZx\nAvx5FeibbI7DJiUSzvLlWSHyzOQgpmuNWlnCcCaO5KZB7YQoboxXu1aWoTg8PYuZ\n5WgZEo2gdmKLz6gQWSCOb9TqWBNZ2bYzEfrJfvFJiCTzVxpwA9j3yWLbNwKBgCMK\nDb9VES/S6I97C7JTLWC2rfoUrhK8uNcjiAQagy06eMq9Pfs2NX3+wRkPCgu0Mo78\n935GxHYpSncGM92T9XZ+LGE2Qz2JOcFqJ2MNIPwVRJxcvyd/WVy/2mLkPFD06P4s\nyyBFsRQ9J4zq2gC57jG5ZB64NguNu2RNaRtoNKwBAoGACldReSHNSecQbQWjU4YZ\nIzsUjOHdIrvo0F3LQwI0FxuxLwdgB9aHG6X3Qyk3934dwURabZptpRPo+SEGzn9r\n0FUxP/dSkeuGk0oauDE3YPbCnSk3I86mjMI69fPtvlD03bPp7wmro7bm1NKl7LP7\nDN5kFYi+vDlgenmC9dzHw+8=\n-----END PRIVATE KEY-----\n",
  "client_email": "yandex-dzen@temporal-web-372917.iam.gserviceaccount.com",
  "client_id": "111329083719587181710",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/yandex-dzen%40temporal-web-372917.iam.gserviceaccount.com"
}
sheet_id = "1kirpAEWY-bsIp7i1zlHkEj1gs2vheQH3OYLoQmCC1k4"


def get_service_sacc():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds_service = ServiceAccountCredentials.from_json_keyfile_dict(api_json, scopes=scopes).authorize(httplib2.Http())
    return build(serviceName="sheets", version="v4", http=creds_service)


def get_channel_list():
    service = get_service_sacc()
    sheet = service.spreadsheets()
    response = sheet.values().get(spreadsheetId=sheet_id, range=f"Channels!A2:B100000").execute()

    result = list()
    check = list()
    for element in response["values"]:
        if element[1] not in check:
            check.append(element[1])
            sub_result = {"channel_name": element[0], "channel_url": element[1]}
            result.append(sub_result)
    return result


def record_publication(channel_id, channel_name, publication_name, publication_type, publication_date, views,
                       end_views, percent_end_views, views_time, comments, likes, amount_publication):
    service = get_service_sacc()
    sheet = service.spreadsheets()
    today = str(date.today())
    values = [[channel_id, channel_name, publication_name,
               publication_type, str(publication_date), views, end_views,
               percent_end_views, views_time, comments, likes, today]]
    index = amount_publication + 1
    body = {"values": values}
    sheet.values().update(spreadsheetId=sheet_id, range=f"Publications!A{index}",
                          valueInputOption="RAW", body=body).execute()
    time.sleep(1)
    print(f"[INFO] Публикация {publication_name} успешно записана в Google Sheet")


if __name__ == "__main__":
    pass
