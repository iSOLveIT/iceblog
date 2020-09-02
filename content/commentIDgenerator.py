# Local modules
import random

# User-defined modules
from content import mongo

# Third-party modules


# Create Mongodb connection
articles = mongo.get_collection(name='articles')


def random_string():
    """Generate a random string of letters and digits """
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Creates a list and then joins the elements in the list into a string
    unique_str = ''.join(random.sample(s, 7))
    return unique_str


def comments_id():
    generated_str = random_string()
    # Search the database to find if the comments_id already exist
    search = articles.find_one({
        "comments": {'$elemMatch': {'commentId': generated_str}}
    })

    if search is not None:
        # If comment_id already exist, re-run the function
        return comments_id()
    return generated_str
