

# from tst.a import app
from uvicorn import run
from app import app

# uvicorn main:app --host 0.0.0.0 --port 80 --reload

# 6770171831:AAGbiNkmQCbEsgCEJOzdBnO-3luh74bTCgM

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=80)