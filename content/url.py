from .user_views import *
from content import app
from .admin_views import *

# USER ROUTES
# Route for index
app.add_url_rule('/', view_func=IndexEndpoint.as_view("index"))

# Route for about
app.add_url_rule('/about', view_func=AboutEndpoint.as_view("about"))

# Route for contact
app.add_url_rule('/contact', view_func=ContactEndpoint.as_view("contact"))

# Route for blog category
app.add_url_rule('/category', view_func=CategoryEndpoint.as_view("category"))

# Route for single blog
app.add_url_rule('/blogpost/<string:blog_id>/',
                 view_func=SingleEndpoint.as_view("blogpost"))

# Route for likes
app.add_url_rule('/likes', view_func=LikesEndpoint.as_view("likes"))


# ADMIN ROUTES
# Route for admin_login
app.add_url_rule('/login', view_func=AdminLoginEndpoint.as_view("login"))

# Route for callback_handler
app.add_url_rule('/callback', view_func=CallbackHandler.as_view("callback_handling"))

# Route for admin dashboard
app.add_url_rule('/admin_dashboard', view_func=AdminDashboardEndpoint.as_view("dashboard"))

# Route for registering new user
app.add_url_rule('/admin_dashboard/create_user', view_func=RegisterUserEndpoint.as_view("sign_up"))

# Route for admin dashboard
app.add_url_rule('/admin_dashboard/profile', view_func=AdminProfileEndpoint.as_view("profile"))

# Route for admin logout
app.add_url_rule('/admin_dashboard/logout', view_func=AdminLogoutEndpoint.as_view("logout"))

# Route for add article
app.add_url_rule('/admin_dashboard/add_article',
                 view_func=AddArticleEndpoint.as_view("addarticle"))

# Route for edit article
app.add_url_rule('/admin_dashboard/edit_article/<string:blog_id>/',
                 view_func=EditArticleEndpoint.as_view("editarticle"))

# Route for delete article
app.add_url_rule('/admin_dashboard/delete/<string:blog_id>/',
                 view_func=DeleteArticleEndpoint.as_view("deletearticle"))

# Route for comment status
app.add_url_rule('/admin_dashboard/comments',
                 view_func=CommentStatusEndpoint.as_view("comments"))

# Route for comment approval
app.add_url_rule('/admin_dashboard/commentsapproval',
                 view_func=CommentApprovalEndpoint.as_view("commentsapproval"))

