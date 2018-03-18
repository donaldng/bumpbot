from splinter import Browser
import time

class BumpBot:

    def __init__(self, username):
        self.premium = True
        self.base_url = "https://forum.lowyat.net"
        self.topic_url = "https://forum.lowyat.net/topic/"
        self.loaded = []
        self.username = username
        self.posts = [4524211, 4524212]
        self.session = []

        with Browser('firefox', headless=False) as self.browser:
            
            self.visit(self.base_url)
            self.login()
            
            if self.logged_in():
                self.bumping()
                self.logout()

    def logged_in(self):
        return self.browser.is_text_present(self.username)

    def visit(self, url):
        print("visit {}".format(url))
        self.browser.visit(url)

    def login(self):
        
        self.browser.fill('UserName', self.username)
        self.browser.fill('PassWord', 'pascodep')

        print("Login with username {} and password *****".format(self.username))

        button = self.browser.find_by_css('.button')
        button.click()
        print("We in!")

    def logout(self):
        logout_link = self.browser.find_by_text('Log out')
        logout_link.click()
        print("Logout!")

    def scrollDown(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    
    def bumping(self):
        for post in self.posts:
            self.visit("{}{}".format(self.topic_url, post))
            self.scrollDown()
            self.browser.fill('Post', 'bump!')
            submit_button = self.browser.find_by_name('submit')
            # submit_button.click()
            print("Submit!")
            time.sleep(3)        

if __name__ == "__main__":
    BumpBot("donduck")