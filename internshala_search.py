import requests,json,ua_generator
from bs4 import BeautifulSoup
def call_intern(keyword: str, location: str):
    ua=ua_generator.generate()
    session=requests.Session()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,it;q=0.6',
        'dnt': '1',
        'priority': 'u=0, i',
        'referer': 'https://internshala.com/',
        'sec-ch-ua': ua.ch.brands,
        'sec-ch-ua-mobile': ua.ch.mobile,
        'sec-ch-ua-platform': ua.ch.platform,
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.text,
    }

    response = session.get(f'https://internshala.com/internships/keywords-{keyword}-in-{location.lower()}/', headers=headers)
    if response.status_code==200:
        res_html=response.text
        # print(response.url)
        soup=BeautifulSoup(res_html,'html.parser')

        jobs=''
        if soup.find_all("div",class_="view_detail_button"):
            jb=soup.find_all("div",class_="view_detail_button")
        
            for card in jb:
                title = card.find("a", class_="job-title-href").get_text(strip=True) if card.find("a", class_="job-title-href") else 'N/A'
                company = card.find("p", class_="company-name").get_text(strip=True) if card.find("p", class_="company-name") else 'N/A'
                stipend = card.find("span", class_="stipend").get_text(strip=True) if card.find("span", class_="stipend") else 'N/A'
                location = card.find("div", class_="row-1-item locations").get_text(strip=True) if card.find("div", class_="row-1-item locations") else 'N/A'
                link = "https://internshala.com" + card.find("a", class_="job-title-href")['href'] if card.find("a", class_="job-title-href") else 'N/A'
                duration_div_list = card.find_all('div',class_="row-1-item")
                duration = duration_div_list[2].find("span").get_text(strip=True) if duration_div_list[2].find("span") else 'N/A'
                posted = card.find("div", class_="detail-row-2").find('span').get_text(strip=True) if card.find("div", class_="detail-row-2") and card.find("div", class_="detail-row-2").find('span') else 'N/A'


                
                jobs+=f"💼 {title}\n🏢 {company}\n📍 {location}\n💸 {stipend}\n⏳ Duration: {duration}\n🕒 Posted: {posted}\n🔗 [View Job & Apply]({link})\n\n"
            print(jobs)
            # return jobs
        elif not soup.find_all("div",class_="view_detail_button"):
            return '❌ No result found'
        else:
            return '❌ Unknown Error'
    elif response.status_code!=200:
        return '❌ Request Error'
if __name__=="__main__":
    call_intern('python development', 'mumbai')