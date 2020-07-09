from content import app
import os


app.config['SECRET_KEY'] = os.urandom(75)

if __name__ == "__main__":
    app.run(port="6080", debug=True, threaded=True)