class DashboardPage:
    
    def __init__(self, page):
        self.page = page
        self.logout_link = self.page.get_by_role("link", name="Logout")

    def logout(self):
          self.logout_link.click()