# Gets Contacts from Facebook Ads for a Facebook Page

A simple script to retrieve contact information from advertisements posted by a certain Facebook page.

**No authorization is required.**

The script can find the internal page ID from its link (which does not match the visible account number), retrieves advertisements through the Facebook Ads Library API, and collects unique email addresses, phone numbers, and website links.

## Example

Inputs are taken from the study [The Sad Fate of Small Facebook Audiences: Mexico](https://www.digitalmethods.net/Dmi/WinterSchool2024FBaudiencesMexico
).

```sh
$ python3 test.py
Internal Facebook ID of the page (company ID) is 116812033038668
Unique email adressses of ads are: marca@noticaribepeninsular.com.mx, noticaribe2018@gmail.com
Unique phone numbers of ads are: +525583686255, +529984287875
Unique websites of ads are: https://noticaribepeninsular.com.mx/, https://facebook.com/NoticaribeInfo
```