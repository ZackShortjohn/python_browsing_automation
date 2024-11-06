from conftestPage import CoherePage

def test_login_via_ui(browser_context, config_data):
    page = browser_context.new_page()
    cohere_page = CoherePage(page)

    #Login
    cohere_page.navigate_to_login()
    cohere_page.login(config_data["cohere_email"], config_data["cohere_password"])

    #Check user logged in successfully
    cohere_page.check_login_success()    

def test_chat_interaction(browser_context):

    page = browser_context.new_page()
    cohere_page = CoherePage(page)

    #Navigate to ChatBot
    cohere_page.navigate_to_chat()

    #Handle Popups
    cohere_page.accept_cookies()
    cohere_page.close_chat_guide_popup()  

    #Send message to ChatBot
    cohere_page.send_message("Hello AI!")
    cohere_page.wait_for_response()

    #Logout
    cohere_page.logout()

def test_file_interaction(browser_context, config_data):
    page = browser_context.new_page()
    cohere_page = CoherePage(page)

    cohere_page.navigate_to_chat()
    #Login
    cohere_page.login(config_data["cohere_email"], config_data["cohere_password"])

    #Handle Popups
    cohere_page.accept_cookies()
    cohere_page.close_chat_guide_popup()  

    #Send file to ChatBot
    file_path = "docs/Zacharias_Kontogiannis_CV.pdf"
    cohere_page.upload_file(file_path)
    cohere_page.send_message("Describe the contents of the file.")
    cohere_page.wait_for_response()

    #Logout
    cohere_page.logout()