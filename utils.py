from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату"""
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").astimezone().date()
        except ValueError:
            print(
                "Неверный формат даты. Убедитесь, что введённая дата соответствует формату ГГГГ-ММ-ДД."
            )
