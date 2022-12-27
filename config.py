user = "root"
password = "qnet20400"
port = 3306
host = "127.0.0.1"
db_name = "dzen"

groups = {1: "Кино", 2: "Спорт", 3: "Политика", 4: "Красота и уход", 5: "Видеоигры"}
groups_text = "\n".join([f"{key}: {groups[key]}" for key in groups.keys()])
