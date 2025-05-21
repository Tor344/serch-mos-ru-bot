from faker import Faker
import requests
from pathlib import Path

fake = Faker('ru_RU')


def generate_person() -> dict:
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone_number": fake.phone_number()
    }


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0"
}

PUT_TICKER1 = ("https://tickets.mos.ru/widget/api/widget/order?agent_uid={agent_uid}")

PUT_TICKER2 = ("https://tickets.mos.ru/widget/api/widget/order/payment?agent_uid={agent_uid}")

GET_INSTALL_TICKET = (
    "https://tickets.mos.ru/widget/api/widget/ticket?agent_id={agent_uid}&order_id={order_id}&ticket_id={ticket_id}")


def put_ticket1(agent_uid: str, event_id: int, performance_id: str, start_time: str, end_time, date: str, name: str,
                tariff_id: int, ticket_type_id: int) -> dict:
    person = generate_person()

    payload = {
        "client": {
            "email": person["email"],
            "name": person["name"],
            "phone_number": person["phone_number"]
        },
        "order_requests": [
            {
                "agent_uid": agent_uid,
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "items": [
                    {
                        "amount": 1,
                        "event_id": event_id,
                        "performance_id": performance_id,
                        "price": 0,
                        "tariff_id": tariff_id,
                        "ticket_type_id": ticket_type_id,
                        "visitor_cat_id": 1
                    }
                ],
                "name": name,
                "spot_id": 110
            }
        ]
    }

    # URL запроса
    url_put1 = PUT_TICKER1.format(
        agent_uid=agent_uid
    )

    response1 = requests.put(url_put1, json=payload, headers=headers)
    response1.raise_for_status()
    return response1.json()


def put_ticket2(agent_uid: str, order_id: str) -> None:
    payload2 = {
        "order_id": order_id,
        "amount": 0,
        "is_booking": False,
        "payment_type_id": 6,  # Обычно 6 = бесплатный билет
        "type_transaction": "SALE"
    }

    url_put2 = PUT_TICKER2.format(
        agent_uid=agent_uid
    )

    response2 = requests.put(url_put2, json=payload2, headers=headers)
    response2.raise_for_status()


def reg_ticket(event_id: int, agent_uid: str, performance_id: str, date: str, start_time: str, end_time: str, name,
               tariff_id: int, ticket_type_id: int):
    """Регестрирует билет"""
    response1 = put_ticket1(agent_uid, event_id, performance_id, start_time, end_time, date, name, tariff_id,
                            ticket_type_id)

    order_id = response1["id"]
    put_ticket2(agent_uid, order_id)

    ticket_id = response1["tickets"][0]["id"]

    install_r = GET_INSTALL_TICKET.format(
        agent_uid=agent_uid,
        order_id=order_id,
        ticket_id=ticket_id
    )

    ticket_data = f"{date} {start_time} {end_time} {install_r}|"
    script_dir = str(Path(__file__).parent.parent.parent)
    with open(f"{script_dir}/ticket_list.txt", "a", encoding="utf-8") as file:
        file.write(ticket_data)

