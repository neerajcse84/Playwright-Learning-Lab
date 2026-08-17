class LoginPage:
     
     def __init__(self, page):
        self.page = page
        self.username = self.page.get_by_placeholder("Username")
        self.password = self.page.get_by_placeholder("Password")
        self.login_button = self.page.get_by_role("button", name="Login")
       

     def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    