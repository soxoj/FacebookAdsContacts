from FacebookAdsLibrary.main import FacebookAdsLibrary

if __name__ == '__main__':
    fb = FacebookAdsLibrary()

    page_id = fb.get_page_id_by_url('https://www.facebook.com/NoticaribeInfo')
    print(f'Internal Facebook ID of the page (company ID) is {page_id}')

    ads = fb.get_ads(str(int(page_id))).get('Ads')

    emails = set()
    phones = set()
    websites = set()

    for a in ads:
        if a["Email"]:
            emails.add(a["Email"])

        if a["Phone"]:
            phones.add(a["Phone"])

        if a["Website"]:
            websites.add(a["Website"])

    print(f'Unique email adressses of ads are: {", ".join(emails)}')
    print(f'Unique phone numbers of ads are: {", ".join(phones)}')
    print(f'Unique websites of ads are: {", ".join(websites)}')