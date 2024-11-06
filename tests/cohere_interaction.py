from conftestPage import CoherePage

def test_login_via_ui(browser_context, config_data):
    page = browser_context.new_page()
    cohere_page = CoherePage(page)

    # Use the configuration data
    cohere_page.navigate_to_login()
    cohere_page.login(config_data["cohere_email"], config_data["cohere_password"])

    # Wait for the profile span to be visible
    profile_text = page.get_by_role("link",name="Profile")
    profile_text.wait_for(state="visible")
    assert profile_text.is_visible()

def test_chat_interaction(browser_context):

    page = browser_context.new_page()
    page.goto("https://dashboard.cohere.com/chat")

    # Check if there is a cookies popup and accept it.
    cookies = page.get_by_role("button", name="Accept All")
    try:
        cookies.wait_for(state="visible",timeout=2000)  # Wait for the cookies button to be visible
        cookies.click()
    except Exception:
        print("Cookies button not found or not visible.")

    # Check if there is a chat guide popup
    popup = page.locator("button[type='button']:has(i.icon-close)")
    try:
        popup.wait_for(state="visible", timeout=2000)  # Wait for the popup close button to be visible
        popup.click()
        # Wait for the popup to be hidden
        page.locator("div[data-component='OnboardingModal']").wait_for(state="hidden", timeout=2000)
    except Exception:
        print("Popup close button not found or not visible.")
        
    # Fill the message area
    composer_textarea = page.locator("textarea[id='composer']")
    composer_textarea.fill("Hello AI!")

    # Send the message
    send_button = page.locator("button:has(i.icon-arrow-right)")
    send_button.click()

    # Wait for the response to be displayed (dislike button appears)
    dislike_button = page.get_by_label("disapprove feedback")
    dislike_button.wait_for(state="visible")
    assert dislike_button.is_visible(), "Response should be displayed"

    # Click profile button and log out
    profile_button = page.locator("button:has(i.icon-profile)")
    profile_button.click()

    logout_button = page.get_by_role("link", name="Log out")
    logout_button.click()

    # Wait for the redirection to the login page
    page.wait_for_url("https://dashboard.cohere.com/welcome/login")
    assert page.url == "https://dashboard.cohere.com/welcome/login", "User should be redirected to the login page after logout"

def test_file_interaction(browser_context):
    page = browser_context.new_page()
    page.goto("https://dashboard.cohere.com/chat")

    # Perform login
    email_input = page.locator("input[name='email']")
    email_input.fill("zkkontogiannis@gmail.com")

    password_input = page.locator("input[name='password']")
    password_input.fill("1qaz@WSX3edc$RFV5tgb")

    submit_button = page.locator("button[type='submit']")
    submit_button.click()

    # Check if there is a cookies popup and accept it.
    cookies = page.get_by_role("button", name="Accept All")
    try:
        cookies.wait_for(state="visible",timeout=2000)  # Wait for the cookies button to be visible
        cookies.click()
    except Exception:
        print("Cookies button not found or not visible.")

    # Check if there is a chat guide popup
    popup = page.locator("button[type='button']:has(i.icon-close)")
    try:
        popup.wait_for(state="visible", timeout=2000)  # Wait for the popup close button to be visible
        popup.click()
        # Wait for the popup to be hidden
        page.locator("div[data-component='OnboardingModal']").wait_for(state="hidden", timeout=2000)
    except Exception:
        print("Popup close button not found or not visible.")

    #Upload File to the ChatBot
    file_path = "docs/Zacharias_Kontogiannis_CV.pdf"

    with page.expect_file_chooser() as fc_info:
        page.locator("button:has(i.icon-clip)").click() 
    file_chooser = fc_info.value
    file_chooser.set_files(file_path)

    #Check File was uploaded successfully
    attached_file_icon = page.locator("div:nth-child(5) > div > div > .icon-outline")
    attached_file_icon.wait_for(state="visible")
    assert attached_file_icon.is_visible(), "File upload failed."

    #Write Message to the ChatBot
    write_message = page.locator("textarea[id='composer']")
    write_message.fill("Describe the contents of the file.")

    #Send Message
    send_button = page.locator("button:has(i.icon-arrow-right)")
    send_button.click()

    # Wait for the response to be displayed
    dislike_button = page.get_by_label("disapprove feedback")
    dislike_button.wait_for(state="visible")
    assert dislike_button.is_visible(), "Response should be displayed"

    # Click profile button and log out
    profile_button = page.locator("button:has(i.icon-profile)")
    profile_button.click()

    logout_button = page.get_by_role("link", name="Log out")
    logout_button.click()

    # Wait for the redirection to the login page
    page.wait_for_url("https://dashboard.cohere.com/welcome/login")
    assert page.url == "https://dashboard.cohere.com/welcome/login", "User should be redirected to the login page after logout"