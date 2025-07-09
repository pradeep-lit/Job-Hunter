import requests,json,ua_generator
from datetime import datetime
def call_remotive(keyword: str, company: str=''):
    ua=ua_generator.generate()

    session=requests.Session()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-IN,en;q=0.9',
        'dnt': '1',
        'priority': 'u=0, i',
        'sec-ch-ua': ua.ch.brands,
        'sec-ch-ua-arch': ua.ch.architecture,
        'sec-ch-ua-bitness': ua.ch.bitness,
        'sec-ch-ua-full-version': ua.ch.get_browser_version(),
        'sec-ch-ua-full-version-list': ua.ch.brands_full_version_list,
        'sec-ch-ua-mobile': ua.ch.mobile,
        'sec-ch-ua-model': ua.ch.model,
        'sec-ch-ua-platform': ua.ch.platform,
        'sec-ch-ua-platform-version': ua.ch.platform_version,
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': ua.text,
    }

    params = {
        'search': keyword.lower(),
        'company_name' : company.lower(),
        'limit' : '40'
    }
    return_string=''
    response = session.get('https://remotive.com/api/remote-jobs', params=params,headers=headers)
    
    if response.status_code==200:
        rjson=response.json()
        if rjson['jobs']:
            jobs=rjson['jobs']
            for i in jobs:
                dt=datetime.fromisoformat(i['publication_date'])
                time=dt.strftime('%d %b %Y, %I:%M %p')
                return_string+=f"💼 {i['title']}\n🏢 {i['company_name']}\n📍 {i['candidate_required_location']}\n💸 {'N/A' if i['salary']=='' else i['salary']}\n🕒 Posted: {time}\n🔗 [View Job & Apply]({i['url']})\n\n"
            return return_string
            # print(return_string)
        elif rjson['job-count']==0: 
            return '❌ No result found'
    elif response.status_code!=200:
        return '❌ Request Error'
if __name__=='__main__':
    call_remotive('Software Developer')