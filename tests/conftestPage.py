class CoherePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://dashboard.cohere.com/welcome/login"  # This could also come from config
        self.email_input_selector = "input[name='email']"
        self.password_input_selector = "input[name='password']"
        self.login_button_selector = "button[type='submit']"

    def navigate_to_login(self):
        self.page.goto(self.url)

    def login(self, email, password):
        self.page.fill(self.email_input_selector, email)
        self.page.fill(self.password_input_selector, password)
        self.page.click(self.login_button_selector)

