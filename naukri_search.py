import requests,json,ua_generator
def call_naukri(keyword: str, location: str):
    ua=ua_generator.generate()

    session=requests.Session()
    location=location.lower()
    keyword=keyword.lower()

    headers = {
        'accept': 'application/json',
        'accept-language': 'en-IN,en;q=0.9',
        'appid': '109',
        'clientid': 'd3skt0p',
        'content-type': 'application/json',
        'dnt': '1',
        'gid': 'LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE',
        'nkparam': 'UZYTLLrVnBL02V0blhg84T9LbdJCEAA/084vHsdmXa5f7qJkK5kXtmW+3UAcVz0GySaLdiD4n+mKHE1bE9bsMg==',
        'priority': 'u=1, i',
        'referer': f'https://www.naukri.com/{keyword}-jobs-in-{location}?k={keyword}&l={location}',
        'sec-ch-ua': ua.ch.brands,
        'sec-ch-ua-mobile': ua.ch.mobile,
        'sec-ch-ua-platform': ua.ch.platform,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'systemid': 'Naukri',
        'user-agent': ua.text,
    }

    params = [
        ('noOfResults', '40'),
        ('urlType', 'search_by_key_loc'),
        ('searchType', 'adv'),
        ('location', location),
        ('keyword', keyword),
        ('pageNo', '1'),
        ('k', keyword),
        ('l', location),
        ('qproductJobSource', '2'),
        ('naukriCampus', 'true'),
        ('nignbevent_src', 'jobsearchDeskGNB'),
        ('seoKey', f'{keyword}-jobs-in-{location}'),
        ('src', 'directSearch'),
        ('latLong', ''),
    ]

    response = session.get('https://www.naukri.com/jobapi/v3/search', params=params, headers=headers)
    if response.status_code==200:
        resp_json=response.json()
        json_jobs=resp_json['jobDetails']
        if json_jobs:
            jobs=''
            for i in json_jobs:
                jobs+=f'💼 {i['title']}\n🏢 {i['companyName']}\n📍 {i['placeholders'][2]['label']}\n💸 {i['placeholders'][1]['label']}\n🧪 Experience: {i['experienceText']}\n🕒 Posted: {i["footerPlaceholderLabel"]}\n🔗 [View Job & Apply](https://naukri.com{i['jdURL']})\n\n'
            # print(jobs)
            return(jobs)
        elif resp_json["noOfJobs"]==0:
            return '❌ No result found'
    elif response.status_code!=200:
        return '❌ Request Error'
    else:
        return '❌ Unknown Error'
if __name__=="__main__":
    call_naukri('QA','Delhi')