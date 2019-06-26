import requests
from bs4 import BeautifulSoup

def logout():
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': "PostmanRuntime/7.15.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "c5b75f78-611a-48d0-8925-3ebb4eb9c243,b603d810-f2f0-4167-9d5d-983fcccb327a",
        'Host': "intrawww.ing.puc.cl",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    actual_creds = {
    'creds': ''
    }


def get_qual_link(link):
    indice = link.find("id_curso_ic")
    id_curso = link[indice:]
    return id_curso

def rework(html):
    def wrap(to_wrap, wrap_in):
        contents = to_wrap.replace_with(wrap_in)
        wrap_in.append(contents)

    text = html
    soup = BeautifulSoup(text, "html.parser")


    for tag in soup.find_all('table', style=True):
        tag.replaceWithChildren()

    for tag in soup.find_all('table'):
        tag.attrs = {}
        new_tag = soup.new_tag("div")
        new_tag['style'] = 'display: block; overflow-x: auto;'
        wrap(tag, new_tag)


    for tag in soup.find_all('td', class_="ColorFondoResaltado"):
        new_tag = soup.new_tag("div")
        new_tag.string = tag.text
        new_tag["class"] = "asignature"
        tag.replace_with(new_tag)

    for tag in soup.find_all("td", style=True):
        if "text-align : right" in tag["style"]:
            tag["style"] = "text-align : right"
            tag.attrs["class"] = "cells others"
            if "colspan" in tag.attrs:
                del tag["colspan"] 
        else:
            del tag["style"]
            tag.attrs["class"] = "cells"

    tag = soup.find_all("tr")[1]
    children = tag.findChildren("td", recursive=False)
    for child in children:
        child.attrs["class"] = "header_table"

    for tag in soup.find_all("tr")[1:3]:
        children = tag.findChildren("td", recursive=False)
        for child in children[:3]:
            child.extract()
  
    return str(soup)


