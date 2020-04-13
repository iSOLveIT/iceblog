from content import app
import os


app.config['SECRET_KEY'] = os.urandom(455)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
