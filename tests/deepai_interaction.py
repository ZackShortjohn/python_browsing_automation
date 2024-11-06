from deepAIPage import DeepAIPage

#Communicate with the ChatBot
def test_login_to_deepai(browser_context, config_data):
    page = browser_context.new_page()
    # page.pause()
    deepai_page = DeepAIPage(page, config_data)

    # Accept cookies before any other action
    deepai_page.accept_cookies()

    # Perform login
    deepai_page.login()
    
    #Send message
    deepai_page.send_message_to_chatbot("Hello AI!")

#Change profile picture
def test_file_interaction(browser_context, config_data):
    page = browser_context.new_page()
    deepai_page = DeepAIPage(page, config_data)

    #Upload the image
    file_path = "docs/cat.jpg"
    deepai_page.change_profile_picture(file_path)
    
    #Logout
    deepai_page.logout()