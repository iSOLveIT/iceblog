from locust import HttpLocust, TaskSet, task, between, TaskSequence, seq_task

'''
class UserBehaviour(TaskSet):
    # def on_start(self):
    #     """ on_start is called when a Locust start before any task is scheduled """
    #     self.index()
    #
    # def on_stop(self):
    #     """ on_stop is called when the TaskSet is stopping """
    #     self.index()

    # def login(self):
    #     self.client.post("/admin", {"username":"iSOLveIT20", "password":"gigantic"})
    #
    # # def logout(self):
    # #     self.client.post("/logout", {"username":"ellen_key", "password":"education"})

    @task
    def index(self):
        self.client.get("/")

    @task
    def category(self):
        self.client.get("/category/Lifestyle/")

    @task
    def single_blog(self):
        self.client.get("/category/Lifestyle/blogpost/5eae68d06779b0be24dc4730/")

    # @task
    # def comment(self):
    #     self.client.post("/category/Lifestyle/blogpost/5eae68d06779b0be24dc4730/",
    #                      {"name":"iSOLveIT20", "msg":"Great"})


# class AdminTask(TaskSequence):
#     @seq_task(1)
#     def login(self):
#         self.client.post("/admin", {"username":"iSOLveIT20", "password":"gigantic"})
#
#     @seq_task(2)
#     def get_dashboard(self):
#         self.client.get("/admin_dashboard")
#
#     @seq_task(3)
#     def delete_article(self):
#         self.client.post("/admin_dashboard/delete/5eae6826e1f72f5b3583e6c7/")
'''


class UserBehaviour(TaskSet):
    @task
    def index(self):
        self.client.get("/ishort")


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(0, 0)
