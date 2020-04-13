from .views import IndexEndpoint, AboutEndpoint, CategoryEndpoint, ContactEndpoint, SingleEndpoint
from content import app


# Route for index
app.add_url_rule('/', view_func=IndexEndpoint.as_view("index"))

# Route for about
app.add_url_rule('/about', view_func=AboutEndpoint.as_view("about"))

# Route for contact
app.add_url_rule('/contact', view_func=ContactEndpoint.as_view("contact"))

# Route for blog category
app.add_url_rule('/category', view_func=CategoryEndpoint.as_view("category"))

# Route for single blog
app.add_url_rule('/blogpost', view_func=SingleEndpoint.as_view("blogpost"))
