

# from tst.a import app
from uvicorn import run
from app import app

# uvicorn main:app --host 0.0.0.0 --port 80 --reload

if __name__ == "__main__":
    # run(app, host="0.0.0.0", port=8080)
    run(app, host="192.168.3.39", port=8927)
