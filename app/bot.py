from utils.instagrapi_utils import login_user

class InstagramBot:
    def __init__(self):
        self.client = None

    def login(self):
        self.client = login_user()

if __name__ == "__main__":
    # Replace 'your_username' and 'your_password' with your actual credentials
    bot = InstagramBot()
    bot.login()