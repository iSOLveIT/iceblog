from locust import HttpLocust, TaskSet, task, between, TaskSequence, seq_task


class UserBehaviour(TaskSet):
    """Class containing tasks

    Arguments:
        TaskSet 
    """
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.index()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.index()

    @task
    def index(self):
        """Task that sends get and post request to the homepage
        """
        self.client.get("/")
        self.client.post("/", {"newsletter": "test1@gmail.com"})


    @task
    def category(self):
        """Task that sends get request to the each category page
        """
        self.client.get("/category/Lifestyle/?page=0")
        self.client.get("/category/Health/?page=36")
        self.client.get("/category/Tech/?page=0")
        self.client.get("/category/Entertainment/?page=0")
        self.client.get("/category/Sports/?page=0")


    @task
    def single_blog(self):
        """Task that sends get request to the a single blog page
        """
        self.client.get("/category/Lifestyle/blogpost/5eae68d06779b0be24dc4730/")

    @task
    def comment(self):
        """Task that sends comments for the a single blog
        """
        self.client.post("/category/Lifestyle/blogpost/5eae68d06779b0be24dc4730/",
                         {"name": "John Doe", "msg": "The article was written well."})

    @task
    def newsletter(self):
        """Task that sends newsletter subscription
        """
        self.client.post("/category/Lifestyle/blogpost/5eae68d06779b0be24dc4730/",
                         {"newsletter": "test100@gmail.com"})


class AdminTask(TaskSequence):
    """Class that contain task but in sequence

    Arguments:
        TaskSequence
    """
    @seq_task(1)
    def login(self):
        """The first sequence. This task emulates an admin login.
        """
        self.client.post("/admin", {"username": "USERNAME", "password": "PASSWORD"})

    @seq_task(2)
    def get_dashboard(self):
        """The second sequence. This task emulates an admin at the dashboard.
        """
        self.client.get("/admin_dashboard")

    @seq_task(3)
    def add_article(self):
        """The third sequence. This task emulates an admin adding an article.
        """
        self.client.post("/admin_dashboard/add_article", {
            "title": "The New Blog",
            "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "link": "https://images.unsplash.com/",
            "category": "Food",
            "readTime": 10
        })

    @seq_task(4)
    def delete_article(self):
        self.client.post("/admin_dashboard/delete/5eae68d06779b0be24dc4730/")


class WebsiteUser(HttpLocust):
    """Initializes the UserBehaviour class

    Arguments:
        HttpLocust
    """
    task_set = UserBehaviour
    wait_time = between(0, 0)


class AdminUser(HttpLocust):
    """Initializes the AdminTask class

    Arguments:
        HttpLocust
    """
    task_set = AdminTask
    wait_time = between(0, 0)
