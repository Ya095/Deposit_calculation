from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)

# Тест ошибки на ввод не верного типа данных
def test_deposit_culc_wrong_input_data_type():
    request_data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 'data'
    }

    expected_response = {"error": "Ошибка валидации данных. Проверьте, что вводите данные в верном формате"}

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 400
    assert response.json() == expected_response


# Тесты изменения даты (февраль и смена года)
def test_deposit_culc_with_february():
    request_data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }

    expected_response = {
        "31.01.2021": 10050,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75
    }

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 200
    assert response.json() == expected_response


def test_deposit_culc_with_change_year():
    request_data = {
        "date": "20.10.2021",
        "periods": 5,
        "amount": 10000,
        "rate": 6
    }

    expected_response = {
        "20.10.2021": 10050,
        "30.11.2021": 10100.25,
        "31.12.2021": 10150.75,
        "31.01.2022": 10201.51,
        "28.02.2022": 10252.51
    }

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 200
    assert response.json() == expected_response


# Тесты ввода не верных значений
def test_deposit_culc_invalid_input_date():
    request_data = {
        "date": "31.01.",
        "periods": 3,
        "amount": 50000,
        "rate": 7
    }

    expected_response = {"error": "Введите дату в формате 'дд.мм.гггг'"}

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 400
    assert response.json() == expected_response


def test_deposit_culc_invalid_input_periods():
    request_data = {
        "date": "31.01.2021",
        "periods": 61,
        "amount": 50000,
        "rate": 4
    }

    expected_response = {"error": "Введите количество месяцев от 1 до 60"}

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 400
    assert response.json() == expected_response


def test_deposit_culc_invalid_input_amount():
    request_data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 5000,
        "rate": 3
    }

    expected_response = {"error": "Введите сумму вклада от 10 т.р. до 3 млн."}

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 400
    assert response.json() == expected_response


def test_deposit_culc_invalid_input_rate():
    request_data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 50000,
        "rate": 9
    }

    expected_response = {"error": "Введите процентную ставку от 1 до 8"}

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 400
    assert response.json() == expected_response


# Тесты крайних состояний (min)
def test_deposit_culc_extreme_states_min_for_all_data():
    request_data = {
        "date": "31.01.2021",
        "periods": 1,
        "amount": 10000,
        "rate": 1
    }

    expected_response = {
        "31.01.2021": 10008.33
    }

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 200
    assert response.json() == expected_response


# Тесты крайних состояний (max)
def test_deposit_culc_extreme_states_max_for_all_data():
    request_data = {
        "date": "31.01.2021",
        "periods": 60,
        "amount": 3000000,
        "rate": 8
    }

    expected_response = {
        "31.01.2021": 3020000,
        "28.02.2021": 3040133.33,
        "31.03.2021": 3060400.89,
        "30.04.2021": 3080803.56,
        "31.05.2021": 3101342.25,
        "30.06.2021": 3122017.87,
        "31.07.2021": 3142831.32,
        "31.08.2021": 3163783.53,
        "30.09.2021": 3184875.42,
        "31.10.2021": 3206107.92,
        "30.11.2021": 3227481.97,
        "31.12.2021": 3248998.52,
        "31.01.2022": 3270658.51,
        "28.02.2022": 3292462.9,
        "31.03.2022": 3314412.65,
        "30.04.2022": 3336508.74,
        "31.05.2022": 3358752.13,
        "30.06.2022": 3381143.81,
        "31.07.2022": 3403684.77,
        "31.08.2022": 3426376,
        "30.09.2022": 3449218.51,
        "31.10.2022": 3472213.3,
        "30.11.2022": 3495361.39,
        "31.12.2022": 3518663.8,
        "31.01.2023": 3542121.55,
        "28.02.2023": 3565735.7,
        "31.03.2023": 3589507.27,
        "30.04.2023": 3613437.32,
        "31.05.2023": 3637526.9,
        "30.06.2023": 3661777.08,
        "31.07.2023": 3686188.93,
        "31.08.2023": 3710763.52,
        "30.09.2023": 3735501.94,
        "31.10.2023": 3760405.29,
        "30.11.2023": 3785474.66,
        "31.12.2023": 3810711.15,
        "31.01.2024": 3836115.9,
        "29.02.2024": 3861690,
        "31.03.2024": 3887434.6,
        "30.04.2024": 3913350.83,
        "31.05.2024": 3939439.84,
        "30.06.2024": 3965702.77,
        "31.07.2024": 3992140.79,
        "31.08.2024": 4018755.06,
        "30.09.2024": 4045546.76,
        "31.10.2024": 4072517.07,
        "30.11.2024": 4099667.19,
        "31.12.2024": 4126998.3,
        "31.01.2025": 4154511.62,
        "28.02.2025": 4182208.37,
        "31.03.2025": 4210089.76,
        "30.04.2025": 4238157.02,
        "31.05.2025": 4266411.4,
        "30.06.2025": 4294854.14,
        "31.07.2025": 4323486.51,
        "31.08.2025": 4352309.75,
        "30.09.2025": 4381325.15,
        "31.10.2025": 4410533.98,
        "30.11.2025": 4439937.54,
        "31.12.2025": 4469537.12
    }

    response = client.post("/calculations/calc_deposit", json=request_data)

    assert response.status_code == 200
    assert response.json() == expected_response
