from splinter import Browser

class Task:
    def __init__(self, user):
        self.topic_url = "https://forum.lowyat.net/topic/"
        self.owner = user

    def add(self, url):
        post_id = self.process_id(url)

        if post_id and self.get_post_owner(post_id) == self.owner:
            print("Verified success, will bump {}{} for {}!".format(self.topic_url, post_id, self.owner))
        else:
            print("unable to process url {}".format(url))

    def process_id(self, url):
        post_id = 0

        if "lowyat.net/topic" in url:
            post_id = url.split(".lowyat.net/topic/")[1].split("/")[0]

        return post_id

    def get_post_owner(self, post_id):
        with Browser('firefox', headless=True) as browser:
            url = "{}{}".format(self.topic_url, post_id)
            print("visit {}".format(url))
            browser.visit(url)

            return browser.find_by_css(".normalname a").first["text"]


if __name__ == "__main__":
    job = Task("ACHARR")
    status = job.add("https://forum.lowyat.net/topic/4503006/+20")


