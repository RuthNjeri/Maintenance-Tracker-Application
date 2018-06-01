#run.py
<<<<<<< HEAD
from app import app
=======


from app import create_app

app = create_app('development')
>>>>>>> 2ddb97ca05298ac7af2558e95407c1ec86a0dfb5

if __name__ == '__main__':
    app.run()