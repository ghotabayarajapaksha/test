from openai import OpenAI
import feedparser
from bs4 import BeautifulSoup
import requests
import time

client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)


def genarateContent(client,content):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f"""As an AI language model, I'm tasked with generating a SEO-friendly article. The article will be based on the following content. The article should adhere to the following guidelines:
            - Length: The article should be comprehensive and detailed, with a minimum word count of 600 words and not exceeding 1200 words.
            - Formatting: The article should utilize HTML formatting. This includes the use of 'div', 'strong', 'italic', and 'bold' tags to enhance readability and structure.
            - Content: The article should focus solely on the provided content. It should not contain any credits, social links, or disclaimers.
            Please provide the content you'd like me to expand upon. here is the content inside the brackets: {content}""",
        }
            ],
        model="gpt-3.5-turbo",
        )
    return (chat_completion.choices[0].message.content)
    


def getPostImgnCategory(postLink):
    response = requests.get(postLink)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        image_element = soup.select_one("#mvp-post-feat-img > img")
        ctegory_element = soup.select_one("#mvp-post-head > h3 > a > span")
        category = (ctegory_element.text)

        # Check if the element is found
        if image_element:
            src = image_element.get("src")
            # print("Image Source:", src)
            return src,category
        else:
            print("Image element not found with the specified selector.")

def feedValue(url,key):
    feed = feedparser.parse(url)
    value = (feed['entries'][0][key])
    return value

def getFeed(url):

    feed = feedparser.parse(url)
    

    # title
    # title = (feed['entries'][0]['title'])
    title = feedValue(url,"title")

    # tags
    tags1 = (feedValue(url,"tags")[0]["term"])
    tags2 = (feedValue(url,"tags")[1]["term"])
    tags3 = (feedValue(url,"tags")[2]["term"])

    # content
    html_content = (feedValue(url,"content")[0]["value"])
    soup = BeautifulSoup(html_content, "html.parser")
    content = soup.get_text()

    article = genarateContent(client,content)

    # get image and category from post
    postLink = feedValue(url,"link")
    PostImgnCategory = getPostImgnCategory(postLink)
    imageSrc = PostImgnCategory[0]
    category = PostImgnCategory[1]
    return {
        "title":title,
        "tags1":tags1,
        "tags2":tags2,
        "tags3":tags3,
        "content":article,
        "imageSrc":imageSrc,
        "category":category
    
    }


