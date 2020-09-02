# Local modules
import os

# User-defined modules
from content import app


# Configure Secret Key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if __name__ == "__main__":
    app.run(threaded=True)
