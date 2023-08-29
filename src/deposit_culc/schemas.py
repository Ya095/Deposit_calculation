from pydantic import BaseModel, Field


class DepositRequest(BaseModel):
    date: str = Field(description='Дата заявки', examples=['31.01.2021'])
    periods: int = Field(description='Количество месяцев по вкладу', examples=[3])
    amount: int = Field(description='Сумма вклада', examples=[10000])
    rate: float = Field(description='Процент по вкладу', examples=[6])


class DepositResponse(BaseModel):
    date: str
    amount: float
