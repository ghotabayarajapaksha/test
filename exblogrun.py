import requests
from bs4 import BeautifulSoup
import feedwithgpt as bloody
import time
import feedparser

# image and post upload to exblog.jp

def upload_image(img_url,imgCookies):
    cookies = imgCookies
    
    headers = {
        'authority': 'userconf.exblog.jp',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://userconf.exblog.jp',
        'referer': 'https://userconf.exblog.jp/image/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    imgname = img_url.split('/')[-1]
    image_content = requests.get(img_url).content

    data = {
        'filename[]': (imgname, image_content, 'image/jpeg'),
    }

    response = requests.post('https://userconf.exblog.jp/api/image/upload/', cookies=cookies, headers=headers, files=data)

    getimgurl = requests.get('https://userconf.exblog.jp/image/', cookies=cookies, headers=headers)
    soup = BeautifulSoup(getimgurl.content, 'html.parser')

    selector = '#imageContainer > ul > li:nth-child(1) > a'

    # Find the element with the specified selector and get its href attribute
    link = soup.select_one(selector)
    if link:
        href = link.get('href')
        print(href)
        return href
    else:
        print("image not found.")

def getImgDatenTime(img_url):
    imgUrl = img_url
    filename = imgUrl.split("/")[-1]
    fileM = imgUrl.split("/")[-2]
    fileH = imgUrl.split("/")[-3]
    fileY = imgUrl.split("/")[-4]
    filedate = (f"{fileY}/{fileH}/{fileM}/")

    return filedate,filename

def postup(postdata,img_url,postcookies ,imgCookies):

    cookies = postcookies
    url = 'https://userconf.exblog.jp/entry/?'
    text = postdata["content"]

    #upload image image to exblog.jp
    imgUrl = upload_image(img_url,imgCookies)

    #get image date time and name from uploaded image
    ImgDatenTime = getImgDatenTime(imgUrl)
    filedate = ImgDatenTime[0]
    filename = ImgDatenTime[1]

    payload = {
        'subject': postdata["subject"],
        'cgiid': "2",
        'tags[1]': postdata["tag1"],
        'tags[2]': postdata["tag2"],
        'tags[3]': postdata["tag3"],
        'content': f'[#IMAGE|{filename}|{filedate}|mid|640|427#]<font style="vertical-align: inherit;"><font style="vertical-align: inherit;">{text}</font></font>',
        'moresubject': 'More',
        'morecontent': '',
        'send_timeline': '1',
        'b_hatena': '1',
        'send_ping': '1',
        'thumbnail_url': postdata["thumbnail_url"],
        'pstflag': '1',
        'openflag': '1',
        '_submit': 'Release',
        'preview': 'post',
        '_qf__form': '',
        '_token': 'ec004cf8202d37193dc158a9d1a167a6dc281696',
        'moreflag': '',
        'cgname': postdata["cgname"],
        'rdate': '',
        'blogThemeSerial': '',
        'htmlflag': '1',
        'eid': 'e0446349',
        'draftid': '5039256'
    }

    response = requests.post(url, data=payload, cookies=cookies)

    # Print the response status code
    print(response.status_code)

def main():
    # get feed from bloody-disgusting.com and generate content
    url = "https://bloody-disgusting.com/feed/"

    postcookies = {
                'xbg_s': 'pfs5o2j7k1ic05nkviigheam67',
                'universe_aid': 'd4d2b554-ac1a-4e0e-be2e-2958b451c76c',
                'sk': 'f8511dfa864d8f9a514441803101cf7c',
                'sharedid': '3fd3edc7-344b-4b86-8807-9eb356837049',
                'lvllt': '1705148664',
                'lvlct': '1705148664',
                'exblogTicket': 'IRLSrcwhmG-Fu6DrX9w-sthQvXHnxY6SwNBoE-YReJov6XnitXJ8ydFB_vdiv-xLTKad1KSV90iminJKOpS7uhdyF2Waqm05DOxi3QnYRdPfRbfwUpWY7WocQqFj1sFzECwa9slVFXFesv4IZBIDVpf0xaqifwaOKzjoZk5xXwk3fTAOOWfsx7ZKaML4fUH7J9mDH2JNjcMF86VUEcVe_u7WrN0nYQL67oK_fduAi5Y%3D',
                '_gid': 'GA1.2.1116694935.1705140299',
                '_gcl_au': '1.1.1542887535.1705140299',
                '_ga_SK7DRSBW10': 'GS1.1.1705148656.2.1.1705148703.13.0.0',
                '_ga': 'GA1.1.1226393098.1705140299',
                '__utmz': '29310824.1705140299.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
                '__utmt': '1',
                '__utmc': '29310824',
                '__utmb': '29310824.5.10.1705148656',
                '__utma': '29310824.1226393098.1705140299.1705140299.1705148656.2',
                '__ursgen': '0000103.016036099063',
                'UID': '9244EEBEBD537E05',
                'TIX': '102SC9OUStJZjI1azJpTmJzWVAvQ3Jjd09NTkw0NTFGVGQ1YlJ6QndHcCtGN1BkNFV0V3dSTTFMMDBYaUZYNGZqTmVsMGZvWW44OU1jakxDZlpsai9iM1BORGwyUkFGS3c0WUFpMWVJNms5SUdGb3pFU0N5bmt5UmVRTTBsc0h6c0Y2RTkzOXl2MWRseW1NaEtwcllaSUVENmNZQnQrK2tSSUNTRFJnRnN3TXhKYXZVNWRtMU1ha2FxK2dtM1B4bmhwczhYYW1waDNmTjU3WW9rRU4xVEx4eUJacDJXakhoT2sybFFXVDBoZDN2dFdjRXpCOGhuQVZlSWpYYWk3RzVkM1oxcjRaKzkxZjMrQzRvcnhwTDMvQUcwaVhIYldKU0tLVTl1c2pkeVIvclBuM2UxclhmSVZhM0pwTXZkc0EzZkFaUExBRWFXMDJ6ZnZ1cjFTVDQ2QXBxUVFqTVVnQ3A5U2xPNE9Yek1hVHlpd25idTdwNkZEbHk4NUpUSk1GcmNFdXNMdGlzcmdieDQ9'
            }

    imgCookies = {
                '__utmz': '29310824.1705140299.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
                '_gid': 'GA1.2.1116694935.1705140299',
                '_gcl_au': '1.1.1542887535.1705140299',
                'sharedid': '3fd3edc7-344b-4b86-8807-9eb356837049',
                'TIX': '102SC9OUStJZjI1azJpTmJzWVAvQ3Jjd09NTkw0NTFGVGQ1YlJ6QndHcCtGN1BkNFV0V3dSTTFMMDBYaUZYNGZqTmVsMGZvWW44OU1jakxDZlpsai9iM1BORGwyUkFGS3c0WUFpMWVJNms5SUdGb3pFU0N5bmt5UmVRTTBsc0h6c0Y2RTkzOXl2MWRseW1NaEtwcllaSUVENmNZQnQrK2tSSUNTRFJnRnN3TXhKYXZVNWRtMU1ha2FxK2dtM1B4bmhwczhYYW1waDNmTjU3WW9rRU4xVEx4eUJacDJXakhoT2sybFFXVDBoZDN2dFdjRXpCOGhuQVZlSWpYYWk3RzVkM1oxcjRaKzkxZjMrQzRvcnhwTDMvQUcwaVhIYldKU0tLVTl1c2pkeVIvclBuM2UxclhmSVZhM0pwTXZkc0EzZkFaUExBRWFXMDJ6ZnZ1cjFTVDQ2QXBxUVFqTVVnQ3A5U2xPNE9Yek1hVHlpd25idTdwNkZEbHk4NUpUSk1GcmNFdXNMdGlzcmdieDQ9',
                'UID': '9244EEBEBD537E05',
                'vsturis': 'http%3A%2F%2Fhellhere.exblog.jp%2F',
                'xbg_s': '7u6059psdl2q55f9etjovbrqf7',
                'exblogTicket': 'IRLSrcwhmG-Fu6DrX9w-sthQvXHnxY6SwNBoE-YReJov6XnitXJ8ydFB_vdiv-xLTKad1KSV90iminJKOpS7uhdyF2Waqm05DOxi3QnYRdPfRbfwUpWY7WocQqFj1sFzECwa9slVFXFesv4IZBIDVpf0xaqifwaOKzjoZk5xXwkrpZtGgIKSD_xhJ-K-wbSxDVlrFzm-9CB2QNEgc9dVqJTTHAKNiP8gQLOrIFJ8rOE%3D',
                'sk': '042e26e26e62f0c117943fae3dcc3295',
                '__utma': '29310824.1226393098.1705140299.1705226645.1705241971.6',
                '__utmc': '29310824',
                '__utmt': '1',
                'lvllt': '1705241979',
                'lvlct': '1705241979',
                '__utmb': '29310824.9.10.1705241971',
                '_ga_SK7DRSBW10': 'GS1.1.1705241558.6.1.1705242245.4.0.0',
                '_ga': 'GA1.1.1226393098.1705140299',
            }

    # refresh feed every 10 minutes
    Ptitle = "" # Previous title

    while True:
            
            Ltitle = bloody.feedValue(url,"title")
                
            # Update the local feed data only if there's new data
            if Ltitle != Ptitle:
                Ptitle = Ltitle
                bd = bloody.getFeed(url)
                    # Wait for a while before checking the feed again
    
                subject =  bd["title"]
                tag1 = (bd["tags1"])
                tag2 = (bd["tags2"])
                tag3 = (bd["tags3"])
                content = (bd["content"])
                img_url = (bd["imageSrc"])
                cgname = (bd["category"])

                    # local image (if use need to chage upload_image > payload > data) "rb"
                    # img_url = './Upscales.ai_1704795163725.jpeg'

                postdata = {
                    "subject": subject,
                    "tag1": tag1,
                    "tag2": tag2,
                    "tag3": tag3,
                    "content": content,
                    "thumbnail_url": img_url,
                    "cgname": cgname
                    }

                postup(postdata,img_url,postcookies,imgCookies)

                print("New data added to the feed")
            else:
                print("No updates to the feed")

            time.sleep(600)

if __name__ == '__main__':
    main()