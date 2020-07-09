from content import mongo
import random


# Create Mongodb connection
articles = mongo.get_collection(name='articles')

def random_string():
    """Generate a random string of letters and digits """
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # Generating a Random String including letters and digits"

    comment_id = ''.join(random.sample(s, 7))
    search = articles.find_one({
        "comments": { '$elemMatch': { 'commentId': comment_id } }
     })

    if search is not None:
        return random_string()
    return comment_id