
import time
from celery_app import app



@app.task
def add(x, y):
    print(f"  [Worker] Adding {x} + {y} ...")
    time.sleep(3)           
    result = x + y
    print(f"  [Worker] Done! {x} + {y} = {result}")
    return result


@app.task
def send_email(to_address, subject):
    print(f"  [Worker] Sending email to {to_address} ...")
    time.sleep(5)          
    msg = f"Email sent to {to_address} | Subject: '{subject}'"
    print(f"  [Worker] {msg}")
    return msg


@app.task
def risky_task(number):
    print(f"  [Worker] Risky task executed with number={number}")
    time.sleep(1)
    if number < 0:
        raise ValueError(f"Negative numbers are not allowed: {number}")
    return f"Safe! Number was {number}"
