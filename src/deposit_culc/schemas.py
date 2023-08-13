from pydantic import BaseModel, Field


class DepositRequest(BaseModel):
    date: str = Field(default=' ', description='Дата заявки', examples=['31.01.2021'])
    periods: int = Field(default=0, description='Количество месяцев по вкладу', examples=[3])
    amount: int = Field(default=0, description='Сумма вклада', examples=[10000])
    rate: float = Field(default=0, description='Процент по вкладу', examples=[6])


class DepositResponse(BaseModel):
    date: str
    amount: float

