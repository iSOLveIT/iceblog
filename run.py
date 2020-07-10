from content import app
import os


app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY'))

if __name__ == "__main__":
    app.run(threaded=True)
