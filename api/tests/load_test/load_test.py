from locust import HttpUser, task, between, TaskSet
import random

class FastAPILoadTest(TaskSet):
    @task(2)
    def get_all_challenges(self):
        self.client.get("/challenges/")

    @task(2)
    def get_specific_challenge(self):
        challenge_id = random.randint(5, 6)
        self.client.get(f"/challenges/{challenge_id}")

    @task(3)
    def get_user_by_id(self):
        user_id = random.randint(12, 24)
        self.client.get(f"/users/id/{user_id}")

    @task(2)
    def get_user_by_username(self):
        username = "gmail"
        self.client.get(f"/users/username/{username}")

    @task(3)
    def get_donations_by_user(self):
        user_id = 16
        self.client.get(f"/donations/user/{user_id}")

    @task(2)
    def get_friends_donations(self):
        user_id = 13
        self.client.get(f"/donations/user/{user_id}/friends")

    @task(3)
    def get_posts_by_user(self):
        user_id = 12
        self.client.get(f"/posts/user/{user_id}")

    @task(2)
    def get_friends_posts(self):
        user_id = 16
        self.client.get(f"/posts/friends/{user_id}")

    @task(2)
    def get_all_locations(self):
        self.client.get("/donations/location/all")

    @task(2)
    def get_timeslots_by_location(self):
        location_id = random.randint(1, 10)
        self.client.get(f"/donations/location/{location_id}/timeslots")


class WebsiteUser(HttpUser):
    tasks = [FastAPILoadTest]
    wait_time = between(1, 5)