import datetime

import requests

from app.sergh_mos_ru.serch import reg_ticket

GET_EVENTS_URL = (
    "https://tickets.mos.ru/widget/api/widget/getevents"
    "?event_id={event_id}"
    "&agent_uid={agent_uid}"
)
GET_DATA_END_URL = ("https://tickets.mos.ru/widget/api/widget/performance/gettariffs"
                    "?performance_id={performance_id}"
                    "&agent_uid={agent_uid}")


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
    date_from = datetime.datetime.now()
    date_to = date_from + datetime.timedelta(days=365 * 3)

    free_seats_url = GET_PERFORMANCE_FREE_SEATS_URL.format(
        event_id=event_id,
        date_from=date_from.strftime("%Y-%m-%d"),
        date_to=date_to.strftime("%Y-%m-%d"),
    )

    response = requests.get(free_seats_url)
    response.raise_for_status()

    return response.json()


def main():
    event_id = int(input("Введите event_id: ") or "47833")
    agent_uid = input("Введите agent_uid: ") or "museum283"

    events = get_events(event_id, agent_uid)

    if not events:
        print("Мероприятие не найдено")
        return

    event = events[0]

    nearest_data = event["nearest_date"]

    if not nearest_data:
        print("Нет ближайшей даты проведения")
        return

    performances = get_performances(event_id, agent_uid, nearest_data.split("T")[0])

    if not performances:
        print("Нет ближайшего проведения мероприятия")
        return
    name = performances[0]["name"]
    free_seats = {}

    # Тут сложность O^3 - плохо, но для демонстрации пойдет
    for performance in performances:
        for date, seats in get_performance_free_seats(event_id).items():
            for seat in seats:
                if seat["performance_id"] != performance["id"]:
                    continue

                try:
                    free_seats[date].append(seat)
                except KeyError:
                    free_seats[date] = [seat]

    if not free_seats:
        print("Свободных мест нет")
        return

    for date, seats in free_seats.items():
        print(f"Ближайшие свободные места на {date}:")

        for seat in seats:
            print(f"Perf. {seat["performance_id"]}: {seat["start_time"]} - {seat["end_time"]}")
            # reg_ticket(event_id, agent_uid, seat["performance_id"],nearest_data.split("T")[0],seat["start_time"],seat["end_time"],name)
            break
        print("\n")


if __name__ == "__main__":
    main()

# museum1037
# 65432
#event_id=7813
# &agent_uid=museum151
#event_id=64511
# agent_uid=museum223