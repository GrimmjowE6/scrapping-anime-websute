import json
from bs4 import BeautifulSoup
import requests
import re



with open('animeLinks.json', 'r') as f:
    animeLinksFromJson = json.load(f)


animeDataList=[]
c=0
err=0
print(c,"/",len(animeLinksFromJson))
      
for animeLinkFromJson in animeLinksFromJson:
    try:
        
        igenre=0
        genres=[]

        url = animeLinkFromJson
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")


        #get the name
        getName = soup.find('h1', {'class': "anime-details-title"})
        name=getName.string
        
        #get the  genres
        getAnimeGenres = soup.find('ul', {'class': "anime-genres"})
        getAnimeGenres= getAnimeGenres.find_all("a")
        for i  in getAnimeGenres:
            genres.append(getAnimeGenres[igenre].string)
            igenre+=1


        #get poster image link
        getPosterImgLink = soup.find('div', {'class': "anime-thumbnail"})
        getPosterImgLink= getPosterImgLink.find("img")
        posterImgLink = getPosterImgLink["src"]


        #get story 
        getStory = soup.find('p', {'class': "anime-story"})
        story=getStory.string

        #get anime info
        getAnimeInfo = soup.find_all('div', {'class': "col-md-6 col-sm-12"})

        #get type
        type=getAnimeInfo[0]('a')[0].string
        type = type.split(":", 1)[-1]
        type=re.sub("\s", "", type)

        #get date
        date = getAnimeInfo[1].text
        date=int(re.sub("\D", "", date))

        #get condition
        condition=getAnimeInfo[2]('a')[0].string
        condition = condition.split(":", 1)[-1]
        condition=re.sub("\s", "", condition)


        #get episod's number
        epNum = getAnimeInfo[3].text
        epNum=re.sub("\D", "", epNum)
        


        #get season
        season=getAnimeInfo[5]('a')[0].string
        season = season.split(":", 1)[-1]
        season=re.sub("\s", "", season)


        

        #get source
        source = getAnimeInfo[6].text
        source = source.split(":", 1)[-1]
        source=re.sub("\s", "", source)
        

        #get epesodes cart info 
        getCartsInfo = soup.find_all('div', {'class': "episodes-card-container"})
        
        
        if getCartsInfo:
        # get cart image link
            cartImgLink = getCartsInfo[0].find("img")["src"]
        else:
            continue

        epNum=1
        episodeNumber=[]

        for cartInfo in getCartsInfo:
            #get link of episode
            getEpLink = cartInfo.find('a')
            #server array will be removes every time
            servers=[]
            #connect to the episode page
            epRequest = requests.get(getEpLink["href"])
            soupEp = BeautifulSoup(epRequest.content, "html.parser").body
            #get servers links
            getServers=soupEp.find("ul",{"id":"episode-servers"})
            getServerLinks=getServers.find_all("a")
            for link in getServerLinks:
                if(link.string == "yonaplay - multi" or link.string =="streamsb" or link.string=="uqload" or link.string=="vidbom" or link.string=="vidia"):
                    continue
                else:
                    servers.append({link.string : link["data-ep-url"]})
            episodeNumber.append({epNum : servers})
            epNum+=1
        #jm3 kolchi hna 9bl matjm3o f array wa7d
        animeData={
            "name":name,
            "genre":genres,
            "poster":posterImgLink,
            "story":story,
            "type":type,
            "date":date,
            "condition":condition,
            "ep_number":epNum,
            "season":season,
            "cart_image":cartImgLink,
            "source":source,
            "ep_links":[episodeNumber]
        }

        animeDataList.append(animeData)

        c+=1
        print(c,"/",len(animeLinksFromJson)-err)
        
    except Exception as e:
        err += 1
        with open("error.txt", "w") as errorFile:
            errorFile.write(f"error {err} = {animeLinkFromJson}\n")
        continue





with open("animeData.json", "w", encoding="utf-8") as file:
    # write the JSON data to the file with ensure_ascii set to False
    json.dump(animeDataList, file, ensure_ascii=False)


print("fin")