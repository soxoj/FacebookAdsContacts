import re
import json
import requests
from pprint import pprint


class FacebookAdsLibrary:
    def __init__(self):
        self.reqs = requests.Session()
        self.reqs.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
        self.create_session()

    def get_page_id_by_url(self, url):
        response = self.reqs.get(url).text
        page_id = re.search(r',\\\"page_id\\\":\\\"(\d+)\\\"', response)
        if page_id:
            return page_id.groups(0)[0]

        return None

    def create_session(self):
        params = {
            'active_status': 'all',
            'ad_type': 'all',
            'country': 'ALL',
            'search_type': 'page',
            'media_type': 'all',
        }

        response = requests.get('https://www.facebook.com/ads/library/', params=params)
        html = response.text
        self.update_cookies(html)
        self.data = self.get_request_data(html)
        self.session_id = self.get_session_id(html)

    def update_cookies(self, html):
        cookies = eval(html.split("_js_datr")[1].split(",")[1])
        cookies = {
            'datr': cookies
        }
        self.reqs.cookies.update(cookies)

    def refresh_session(self) -> None:
        """Refreshes the session by closing the current session and creating a new one using new sessionId and Requests Data."""
        self.reqs.close()
        self.reqs = requests.Session()
        self.create_session()

    def get_session_id(self, html):
        return eval(html.split("sessionId")[1].split(":")[1].split(",")[0])

    def get_request_data(self, html):
        dic = json.loads(html.split("{(new ServerJS()).handle(")[1].split(");")[0])
        big_list = dic["define"]
        for lst in big_list:
            if lst[0] == "LSD":
                Lsd = lst[2]["token"]
            elif lst[0] == "WebConnectionClassServerGuess":
                ccg = lst[2]["connectionClass"]
            elif lst[0] == "SiteData":
                dic1 = lst[2]
                data = {
                    '__hs': dic1["haste_session"],
                    '__rev': dic1["__spin_r"],
                    '__hsi': dic1["hsi"],
                    '__spin_r': dic1["__spin_r"],
                    '__spin_b': dic1["__spin_b"],
                    '__spin_t': dic1["__spin_t"],
                }
        data.update({
            '__user': '0',
            '__a': '1',
            '__csr': '',
            'lsd': Lsd,
            '__ccg': ccg,
        })
        return data 

    def get_company_id(self, companyName: str) -> str | None:
        search_company_url = f'https://www.facebook.com/ads/library/async/search_typeahead/?ad_type=all&country=ALL&is_mobile=true&q={companyName}&session_id={self.session_id}'

        scu_headers = {
            'Authority': 'www.facebook.com',
            'Method': 'POST',
            'Path': f'/ads/library/async/search_typeahead/?ad_type=all&country=ALL&is_mobile=true&q={companyName}&session_id={self.session_id}',
            'Scheme': 'https',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en,sl-SI;q=0.9,sl;q=0.8',
            'Content-Length': '610',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.facebook.com',
            'Referer': 'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&media_type=all',
            'Save-Data': 'on',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'X-ASBD-ID': '198387',
            'X-FB-LSD': 'zbcoPxeWkHXBwgt1gf3Y8D',
        }

        response = self.reqs.post(search_company_url, headers=scu_headers, data=self.data).text
        payload = json.loads(response.replace("for (;;);", ""))
        try:
            return payload['payload']['pageResults'][0]['id']
        except Exception:
            return None

    def get_payload(self, company_id: str) -> dict:
        search_ads_url = f'https://www.facebook.com/ads/library/async/search_ads/?session_id={self.session_id}&count=30&active_status=all&ad_type=all&countries[0]=ALL&view_all_page_id={company_id}&media_type=all&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page'

        headers = {
            "Authority": "www.facebook.com",
            "Method": "POST",
            "Path": f"/ads/library/async/search_ads/?session_id={self.session_id}&count=30&active_status=all&ad_type=all&countries[0]=ALL&view_all_page_id={company_id}&media_type=all&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page",
            "Scheme": "https",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en,sl-SI;q=0.9,sl;q=0.8",
            "Content-Length": "571",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.facebook.com",
            "Referer": f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id={company_id}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all",
            'Save-Data': 'on',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'X-ASBD-ID': '198387',
            'X-FB-LSD': 'zbcoPxeWkHXBwgt1gf3Y8D',
        }
        response = self.reqs.post(search_ads_url, headers=headers, data=self.data)
        response.encoding = "utf-8"
        response = response.text.replace('for (;;);{"__ar":1,', "{")
        try:
            return json.loads(response)
        except Exception:
            return None

    def get_page_data(self, payload: dict, company_id: str) -> dict | None:
        page_link = f"https://facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id={company_id}&search_type=page&media_type=all"
        try:
            payload['payload']['results'][0][0]['snapshot']['link_url']
        except Exception:
            has_active_ads = False
            return None
        has_active_ads = True
        total_ads = payload["payload"]["totalCount"]
        return {
            "Page Link": page_link,
            "Has Active Ads": has_active_ads,
            "Total Ads": total_ads,
            "Ads": []
        }

    def get_title(self, snapshot, cards) -> str:
        ad_title = snapshot['title'] if (snapshot['title']) else None

        if (not ad_title or "{{product" in ad_title) and cards:
            ad_title = cards[0]['title']

        if snapshot.get('body', {}).get('markup', {}).get('__html'):
            ad_title = snapshot['body']['markup']['__html'][:50] + '...' 

        return ad_title
        #ad_title = re.sub(r"\{\{.*?\}\}", "", ad_title)

    def get_body(self, snapshot, cards) -> str:
        ad_body = snapshot['body']['markup']['__html']
        ad_body = ad_body.replace("<br />", "\n")
        if ad_body == "&#123;&#123;product.brand&#125;&#125;" or "{{product" in ad_body or ad_body is None:
            ad_body = cards[0]['body']
        return ad_body
        #ad_body = re.sub(r"\{\{.*?\}\}", "", ad_body)

    def get_image(self, snapshot, cards) -> dict:
        ad_image = img[0] if (img := snapshot['images']) else {"original_image_url": None, "resized_image_url": None}
        if not (any(ad_image.values())) and (cards):
            ad_image = {
                "original Image Url": cards[0]['original_image_url'],
                "Resized Image Url": cards[0]['resized_image_url'],
            }
        return ad_image
        #ad_image = re.sub(r"\{\{.*?\}\}", "", ad_image)

    def get_video(self, snapshot, cards) -> dict:
        ad_video = vid[0] if (vid := snapshot['videos']) else {"video_hd_url": None, "video_sd_url": None, "video_preview_image_url": None}
        if not (any(ad_video.values())) and (cards):
            ad_video = {
                    "Hd Url": cards[0]['video_hd_url'] if (cards[0]['video_hd_url'] != 'null') else None,
                    "Sd Url": cards[0]['video_sd_url'] if (cards[0]['video_sd_url'] != 'null') else None,
                    "Preview Image Url": cards[0]['video_preview_image_url'] if (cards[0]['video_preview_image_url'] != 'null') else None,
            }
        return ad_video

    def get_caption_cta_type(self, snapshot, cards) -> tuple:
        ad_caption = snapshot['caption']
        ad_cta_type = snapshot['cta_type']

        if ad_caption is None or "{{product" in ad_caption:
            ad_caption = cards[0]['caption']
        if ad_cta_type is None or "{{product" in ad_cta_type:
            ad_cta_type = cards[0]['cta_type']

        return ad_caption, ad_cta_type
        #ad_cta_type = re.sub(r"\{\{.*?\}\}", "", ad_cta_type)
        #ad_caption = re.sub(r"\{\{.*?\}\}", "", ad_caption)

    def parse_payload(self, data: list) -> dict:
        snapshot = data[0]['snapshot']
        cards = snapshot['cards']
        fev_info = data[0]['fevInfo']

        ad_url = snapshot['link_url']
        if ad_url:
            ad_url = re.sub(r"\{\{.*?\}\}", "", ad_url)
        elif snapshot.get('adArchiveID'):
            ad_url = f'https://www.facebook.com/ads/library/?id={snapshot["adArchiveID"]}'
        else:
            ad_url = "unknown"

        ad_image = self.get_image(snapshot, cards)
        ad_video = self.get_video(snapshot, cards)

        ad_title = self.get_title(snapshot, cards)
        ad_body = self.get_body(snapshot, cards)

        # ad_caption, ad_cta_type = self.get_caption_cta_type(snapshot, cards)
        ad_format = snapshot["display_format"]

        return {
                "Ad Link": ad_url,
                "Ad Format": ad_format,
                "Ad Title": ad_title,
                "Ad Body": ad_body,
                "Ad Image": ad_image,
                "Ad Video": ad_video,
                "Email": fev_info.get('email'),
                "Phone": fev_info.get('phone'),
                "Website": fev_info.get('website'),
                "Address": fev_info.get('address'),
                # "Ad Caption": ad_caption,
                # "Ad CTA Type": ad_cta_type
            }

    def get_ads(self, company_id: str) -> dict | None:
        payload = self.get_payload(company_id)
        if not payload:
            return None

        ads = self.get_page_data(payload, company_id)
        if ads is None:
            return None

        for data in payload['payload']['results']:
            ads['Ads'].append(self.parse_payload(data))

        return ads

    def __del__(self):
        self.reqs.close()

if __name__ == '__main__':
    fb = FacebookAdsLibrary()
    keyword = "Google"
    page_id = fb.get_company_id(keyword)
    pprint(fb.get_ads(page_id))