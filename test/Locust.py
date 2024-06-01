from locust import HttpUser, TaskSet, task, between
from random import choice


class UserBehavior(TaskSet):
    def on_start(self):
        """Called when a Locust user starts before any task is scheduled."""
        self.open_homepage()

    @task(1)
    def open_homepage(self):
        """Simulate opening the homepage."""
        self.client.get("/")

    @task(2)
    def search_route(self):
        """Simulate searching for a route."""
        start_station = choice(["Qianwan", "Buxin", "Hanling"])  # Replace with actual station names
        end_station = choice(["Guanlan", "Luohu", "Bantian"])  # Replace with actual station names
        self.client.get(f"/search_route?start_station={start_station}&end_station={end_station}")

    @task(3)
    def search_bus(self):
        """Simulate searching for a bus."""
        station_name = choice(["Qianwan", "Luohu", "Bantian"])  # Replace with actual station names
        self.client.get(f"/search_bus/{station_name}")

    @task(4)
    def search_out(self):
        """Simulate searching for an exit."""
        station_name = choice(["Qianwan", "Luohu", "Bantian"])  # Replace with actual station names
        self.client.get(f"/search_out/{station_name}")

    @task(5)
    def board_card(self):
        """Simulate boarding a card."""
        data = {
            "user_id": "881000497",  # Replace with actual user ID
            "start_station": "Qianwan",  # Replace with actual station name
            "carriage_type": 1  # Replace with actual carriage type
        }
        self.client.post("/board_card", json=data)

    @task(6)
    def exit_card(self):
        """Simulate exiting a card."""
        data = {
            "user_id": "881000497",  # Replace with actual user ID
            "start_station": "Qianwan",  # Replace with actual start station name
            "end_station": "Luohu"  # Replace with actual end station name
        }
        self.client.post("/exit_card", json=data)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(20, 30)  # Simulate a user waiting between 1 and 5 seconds between tasks
