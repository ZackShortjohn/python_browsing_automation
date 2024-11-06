from playwright.sync_api import Page
from conftest import config_data

class CoherePage:
    def __init__(self, page: Page,config: config_data):
        self.page = page
        self.loginUrl = config["cohere_url"]
        self.chatUrl =  config["cohere_chat_url"]
        self.email = config["cohere_email"]
        self.password = config["cohere_password"]

    def navigate_to_login(self):
        self.page.goto(self.loginUrl)

    def navigate_to_chat(self):
        self.page.goto(self.chatUrl)

    def login(self):
        self.page.locator("input[name='email']").fill(self.email)
        self.page.locator("input[name='password']").fill(self.password)
        self.page.locator("button[type='submit']").click()

    def check_login_success(self):
        # Wait for the profile span to be visible
        profile_text = self.page.get_by_role("link",name="Profile")
        profile_text.wait_for(state="visible")
        assert profile_text.is_visible()

    def accept_cookies(self):
        # Check if there is a cookies popup and accept it.
        cookies = self.page.get_by_role("button", name="Accept All")
        try:
            cookies.wait_for(state="visible",timeout=5000)  # Wait for the cookies button to be visible
            cookies.click()
        except Exception:
            print("Cookies button not found or not visible.")

    def close_chat_guide_popup(self):
        # Check if there is a chat guide popup
        popup = self.page.locator("button[type='button']:has(i.icon-close)")
        try:
            popup.wait_for(state="visible", timeout=5000)  # Wait for the popup close button to be visible
            popup.click()
            # Wait for the popup to be hidden
            self.page.locator("div[data-component='OnboardingModal']").wait_for(state="hidden", timeout=2000)
        except Exception:
            print("Popup close button not found or not visible.")

    def send_message(self, message: str):
        # Fill the message area
        composer_textarea = self.page.locator("textarea[id='composer']")
        composer_textarea.fill(message)

        # Send the message
        send_button = self.page.locator("button:has(i.icon-arrow-right)")
        send_button.click()

    def wait_for_response(self):
        # Wait for the response to be displayed (dislike button appears)
        dislike_button = self.page.get_by_label("disapprove feedback")
        dislike_button.wait_for(state="visible")
        assert dislike_button.is_visible(), "Response should be displayed"

    def upload_file(self, file_path: str):
        #Upload File to the ChatBot
        with self.page.expect_file_chooser() as fc_info:
            self.page.locator("button:has(i.icon-clip)").click() 
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)

        #Check File was uploaded successfully
        attached_file_icon = self.page.locator("div:nth-child(5) > div > div > .icon-outline")
        attached_file_icon.wait_for(state="visible")
        assert attached_file_icon.is_visible(), "File upload failed."

    def logout(self):
        # Click profile button and log out
        profile_button = self.page.locator("button:has(i.icon-profile)")
        profile_button.click()
        logout_button = self.page.get_by_role("link", name="Log out")
        logout_button.click()

        # Wait for the redirection to the login page
        self.page.wait_for_url("https://dashboard.cohere.com/welcome/login")
        assert self.page.url == "https://dashboard.cohere.com/welcome/login", "User should be redirected to the login page after logout"