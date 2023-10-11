# commit_time = 2023-10-11 19:41:26.629165
from fastapi import FastAPI, HTTPException
from src.deposit_culc.router import router as router_deposit_calc
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse



app = FastAPI(
    title='Deposit calculation',
    description='Сервис для расчета депозита.'
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Введены не все данные, либо введены в неверном формате"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


app.include_router(router_deposit_calc)
