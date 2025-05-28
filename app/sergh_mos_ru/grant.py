from datetime import datetime, timedelta
import time
import requests

from app.sergh_mos_ru.serch import reg_ticket

#Нужный сайт с кортами
event_id=65305
agent_uid="museum1038"

#хер пойми что
# event_id=52808
# agent_uid="museum2"
FLAG = False
GET_EVENTS_URL = (
    "https://tickets.mos.ru/widget/api/widget/getevents"
    "?event_id={event_id}"
    "&agent_uid={agent_uid}"
)


GET_PERFORMANCES_URL = (
    "https://tickets.mos.ru/widget/api/widget/events/getperformances"
    "?event_id={event_id}"
    "&agent_uid={agent_uid}"
    "&date={date}"
)


GET_PERFORMANCE_FREE_SEATS_URL = (
    "https://tickets.mos.ru/widget/api/widget/performance_free_seats"
    "?date_from={date_from}"
    "&date_to={date_to}"
    "&event_id={event_id}"
)


GET_TICKET_TARIF = ("https://tickets.mos.ru/widget/api/widget/performance/gettariffs"
                    "?performance_id={performance_id}"
                    "&agent_uid={agent_uid}")


def get_events(event_id: int, agent_uid: str) -> list[dict]:
    events_url = GET_EVENTS_URL.format(
        event_id=event_id,
        agent_uid=agent_uid,
    )

    response = requests.get(events_url)
    response.raise_for_status()

    return response.json()["data"]


def get_performances(event_id: int, agent_uid: str, date: str) -> list[dict]:
    performances_url = GET_PERFORMANCES_URL.format(
        event_id=event_id,
        agent_uid=agent_uid,
        date=date,
    )

    response = requests.get(performances_url)
    response.raise_for_status()

    return response.json()["data"]


def get_performance_free_seats(event_id: int) -> dict[str, list[dict]]:
    date_from = datetime.now()
    date_to = date_from + timedelta(days=365 * 3)

    free_seats_url = GET_PERFORMANCE_FREE_SEATS_URL.format(
        event_id=event_id,
        date_from=date_from.strftime("%Y-%m-%d"),
        date_to=date_to.strftime("%Y-%m-%d"),
    )

    response = requests.get(free_seats_url)
    response.raise_for_status()

    return response.json()


def get_ticket_tarif(performance_id: str, agent_uid: str):
    tarif_url = GET_TICKET_TARIF.format(
        performance_id=performance_id,
        agent_uid=agent_uid
    )
    response = requests.get(tarif_url)
    response.raise_for_status()
    return response.json()['data']["ticket_tariffs"][0]


def monitor_mos_ru() -> None:
    """Мониторит сайт и при появлении регистрации проходится по каждому дню и каждому мероприятию, регистрируя билет"""
    # event_id = int(input("Введите event_id: ") or "47833")
    # agent_uid = input("Введите agent_uid: ") or "museum283"

    events = get_events(event_id, agent_uid)

    if not events:
        print("Мероприятие не найдено")
        return

    event = events[0]

    end_date_str = event["end_date"]
    nearest_data = event["nearest_date"]

    if not nearest_data:
        print("Нет ближайшей даты проведения")
        return

    end_date = datetime.strptime(end_date_str.split("T")[0], "%Y-%m-%d").date()
    current_date = datetime.strptime(nearest_data.split("T")[0], "%Y-%m-%d").date()
    while current_date <= end_date:
        print(current_date.strftime("%Y-%m-%d"))  # Форматируем дату в строку

        performances = get_performances(event_id, agent_uid, current_date.strftime("%Y-%m-%d"))

        if not performances:
            print("Нет ближайшего проведения мероприятия")
            current_date += timedelta(days=1)
            continue

        name = performances[0]["name"]
        free_seats = {}

        # Тут сложность O^3 - плохо, но для демонстрации пойдет
        for performance in performances:
            for date, seats in get_performance_free_seats(event_id).items():
                for seat in seats:
                    if seat["performance_id"] != performance["id"]:
                        continue
                    if seat["free_seats_number"] < 1:
                        continue
                    try:
                        free_seats[date].append(seat)
                    except KeyError:
                        free_seats[date] = [seat]

        if not free_seats:
            print("Свободных мест нет")
            return
        FLAG = True
        for date, seats in free_seats.items():
            print(f"Ближайшие свободные места на {date}:")

            for seat in seats:
                tariff = get_ticket_tarif(seat["performance_id"], agent_uid)
                tariff_id = tariff["id"]
                ticket_type_id = tariff["ticket_type_id"]
                print(f"Perf. {seat["performance_id"]}: {seat["start_time"]} - {seat["end_time"]} , {seat["free_seats_number"]}")
                try:
                    reg_ticket(event_id, agent_uid, seat["performance_id"], nearest_data.split("T")[0], seat["start_time"],
                               seat["end_time"], name,tariff_id,ticket_type_id)
                except:
                    print("Ошибка регистрации")

            print("\n")
        current_date += timedelta(days=1)
    if FLAG:
        FLAG == False
        return True

if __name__ == "__main__":
    monitor_mos_ru()

# event_id=52808
# agent_uid=museum2
