from utilities.site.news import get_news_from_cache


def get_planetarium_news():
    news_all = get_news_from_cache()
    return news_all


def get_planetarium_contacts():
    return 'contacts'
