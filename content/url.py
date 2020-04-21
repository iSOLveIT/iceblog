from .user_views import IndexEndpoint, AboutEndpoint, CategoryEndpoint, ContactEndpoint, SingleEndpoint
from content import app
from .admin_views import *


# Route for index
app.add_url_rule('/', view_func=IndexEndpoint.as_view("index"))

# Route for about
app.add_url_rule('/about', view_func=AboutEndpoint.as_view("about"))

# Route for contact
app.add_url_rule('/contact', view_func=ContactEndpoint.as_view("contact"))

# Route for blog category
app.add_url_rule('/category/<string:category>/', view_func=CategoryEndpoint.as_view("category"))

# Route for single blog
app.add_url_rule('/category/<string:category>/blogpost/<string:blog_id>/', view_func=SingleEndpoint.as_view("blogpost"))


# ADMIN ROUTES
# Route for admin_login
app.add_url_rule('/admin', view_func=AdminLoginEndpoint.as_view("admin"))

# Route for admin dashboard
app.add_url_rule('/admin_dashboard', view_func=AdminEndpoint.as_view("dashboard"))

# Route for add article
app.add_url_rule('/admin_dashboard/add_article',
                 view_func=AddArticleEndpoint.as_view("addarticle"))

# Route for edit article
app.add_url_rule('/admin_dashboard/edit_article/<string:blog_id>/',
                 view_func=EditArticleEndpoint.as_view("editarticle"))

# Route for delete article
app.add_url_rule('/admin_dashboard/delete/<string:blog_id>/',
                 view_func=DeleteArticleEndpoint.as_view("deletearticle"))

# Route for admin logout
app.add_url_rule('/admin_dashboard/logout', view_func=AdminLogoutEndpoint.as_view("logout"))
