from playwright.sync_api import Page
from conftest import config_data

class DeepAIPage:
    def __init__(self, page: Page,config: config_data):
        self.page = page
        self.url = config["deepai_url"]
        self.profile_url = config["deepai_profile_url"]
        self.email = config["deepai_email"]
        self.password =config["deepai_password"]

    def accept_cookies(self):
        self.page.goto(self.url)
        iframe = self.page.frame_locator("iframe[title='SP Consent Message']")
        accept_button = iframe.locator("button[title='Accept']")
        accept_button.wait_for(state='visible')
        accept_button.click()

    def login(self):
        self.page.locator("#headerLoginButton").click()
        login_panel = self.page.locator("button.button.login-with-email")
        login_panel.wait_for(state="visible")
        login_panel.click()

        self.page.locator("input#user-email").fill(self.email)
        self.page.locator("input#user-password").fill(self.password)
        self.page.locator("button#login-via-email-id").click()

        # Wait for the login modal to be hidden
        self.page.locator("#login-modal").wait_for(state="hidden")

    def send_message_to_chatbot(self, message: str):
        #Send message to the ChatBot
        write_message = self.page.get_by_placeholder("Hey! I'm a smart AI chatbot.")
        write_message.fill(message)

        send_button = self.page.get_by_role("button",name="Start Chatting")
        send_button.click()

        #Wait for the ChatBot to respond
        copy_button = self.page.get_by_role("button",name="Copy")
        copy_button.wait_for(state="visible")
        #Check that the response is visible
        assert copy_button.is_visible(), "ChatBot should answer!"

    def change_profile_picture(self,file_path: str):
        self.page.goto(self.profile_url)

        with self.page.expect_file_chooser() as fc_info:
            self.page.get_by_text("Choose an image").click() 
        file_chooser = fc_info.value
        file_chooser.set_files(file_path)

        #Update the profile
        update_profile_button = self.page.get_by_text("Update Profile")
        update_profile_button.click()

        #Wait for update confirmation
        confirmation_text = self.page.get_by_text("Great success! Your profile")
        confirmation_text.wait_for(state="visible")
        assert confirmation_text.is_visible()

    def logout(self):
        #Log out
        profile_button = self.page.locator("#dropMenuButton")
        profile_button.click()

        logout_button = self.page.get_by_role("button",name="Logout")
        logout_button.click()

        #Confirm user logged out
        self.page.wait_for_url(self.url)
        assert self.page.url == self.url, "User should be redirected to the login page after logout"