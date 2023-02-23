from bs4 import BeautifulSoup
import requests
import prettify



#for i  in range(43):
url=f"https://witanime.com/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A/page/1/"
result=requests.get(url)
doc=BeautifulSoup(result.text,"html.parser")
print(doc.prettify()) 

def get_Urls():
    for i in range(44):
        url=f"https://witanime.com/%D9%82%D8%A7%D8%A6%D9%85%D8%A9-%D8%A7%D9%84%D8%A7%D9%86%D9%85%D9%8A/page/{i}/"
        r=requests.get(url)
        soup=BeautifulSoup(r.content,"html.parser")
        bookName=soup.find_all('div',{'class':"hover ehover6"})
        for i in bookName:
            linko=i.find('a')
            link=linko['href']
            with open('urls.txt','a') as f:
                f.write(f'{{link}}\n')

get_Urls()


