from fastapi import APIRouter, HTTPException
from datetime import datetime
from src.deposit_culc.schemas import DepositRequest, DepositResponse
from consts import *
import calendar


router = APIRouter(
    prefix='/calculations',
    tags=['Calculations'],
)


def validate_input(data: DepositRequest):
    try:
        datetime.strptime(data.date, "%d.%m.%Y")

        if not min_months_count <= data.periods <= max_months_count:
            raise ValueError("Введите количество месяцев от 1 до 60")
        if not min_deposit_count <= data.amount <= max_deposit_count:
            raise ValueError("Введите сумму вклада от 10 т.р. до 3 млн.")
        if not min_deposit_sum <= data.rate <= max_deposit_sum:
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

