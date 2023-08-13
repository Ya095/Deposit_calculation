from fastapi import APIRouter, HTTPException
from datetime import datetime
from src.deposit_culc.schemas import DepositRequest, DepositResponse
import calendar


router = APIRouter(
    prefix='/calculations',
    tags=['Calculations'],
)


def validate_input(data: DepositRequest):
    try:
        try:
            # Проверка формата даты
            datetime.strptime(data.date, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Введите дату в формате 'дд.мм.гггг'")

        # Проверка для periods, amount и rate
        if not 1 <= data.periods <= 60:
            raise ValueError("Введите количество месяцев от 1 до 60")
        if not 10000 <= data.amount <= 3000000:
            raise ValueError("Введите сумму вклада от 10 т.р. до 3 млн.")
        if not 1 <= data.rate <= 8:
            raise ValueError("Введите процентную ставку от 1 до 8")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/calc_deposit")
def calc_deposit(data: DepositRequest):
    validate_input(data)

    # Расчет депозита
    rate = data.rate / 100
    deposit = data.amount + (data.amount * rate / 12)
    date = data.date
    response = []

    for month in range(data.periods):
        response.append(DepositResponse(date=date, amount=round(deposit, 2)))
        deposit += deposit * rate / 12

        # Увеличение даты на месяц
        date_parts = list(map(int, date.split('.')))
        year = date_parts[2]
        month = date_parts[1]

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        last_day = calendar.monthrange(year, month)[1]
        date = f'{last_day:02d}.{month:02d}.{year}'

    return {r.date: r.amount for r in response}

