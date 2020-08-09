from content import app
import os


# Configure Secret Key
app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY'))

if __name__ == "__main__":
    app.run(threaded=True)
