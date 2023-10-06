from django.urls.resolvers import RegexPattern,RoutePattern
from web import urls

def get_urls():
    url_list = []
    for url in urls.urlpatterns:
        url_list.append(url.pattern._regex) if isinstance(url.pattern, RegexPattern) else url_list.append(url.pattern._route)
    print(url_list)
    return url_list


get_urls()
