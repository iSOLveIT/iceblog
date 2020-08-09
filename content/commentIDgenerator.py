from content import mongo
import random

# Create Mongodb connection
articles = mongo.get_collection(name='articles')


def random_string():
    """Generate a random string of letters and digits """
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Creates a list and then joins the elements in the list into a string
    comment_id = ''.join(random.sample(s, 7))
    # Search the database to find if the comments_id already exist
    search = articles.find_one({
        "comments": {'$elemMatch': {'commentId': comment_id}}
    })

    if search is not None:
        # If comment_id already exist, re-run the function
        return random_string()
    # function returns comment_id
    return comment_id
