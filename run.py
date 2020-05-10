from content import app
import os


app.config['SECRET_KEY'] = os.urandom(255)

if __name__ == "__main__":
    app.run(port="4080", debug=True, threaded=True)
