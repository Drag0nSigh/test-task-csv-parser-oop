<h1>Тестовое задание</h1>

***

<h2>Описание</h2>

Это скрипт для парсинга CSV-файлов с данными сотрудников. Выводит отчёты в терминал и Json файл. Отчёт группирует сотрудников по отделам, считает  у каждого заработную плату и суумирует эти данные по отделам.

***


<h2>Общая информация</h2>

**Python 3.10**


**ООП - подход**


**Покрыт тестами**


**Аннотация типов**


**Код соответсвует PEP8**



<h2>Пример запуска:</h2>

```
python main.py ../data/data1.csv --report payout_json --output test
```



***

<h2>Пример отчёта в терминале:</h2>

![image](https://github.com/user-attachments/assets/6eeaf3a2-0c99-4de5-beaa-8a896cdad675)

***

<h2>Пример отчёта JSON-файле:</h2>

```
{
    "Marketing": {
        "employees": [
            {
                "name": "Alice Johnson",
                "hours_worked": 160,
                "hourly_rate": 50,
                "payout": 8000
            }
        ],
        "total_hours": 160,
        "total_payout": 8000
    },
    "Design": {
        "employees": [
            {
                "name": "Bob Smith",
                "hours_worked": 150,
                "hourly_rate": 40,
                "payout": 6000
            },
            {
                "name": "Carol Williams",
                "hours_worked": 170,
                "hourly_rate": 60,
                "payout": 10200
            }
        ],
        "total_hours": 320,
        "total_payout": 16200
    }
}
```
