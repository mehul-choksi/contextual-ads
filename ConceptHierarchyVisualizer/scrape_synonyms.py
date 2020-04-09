import pprint
from googleapiclient.discovery import build


class SearchScraper:
    def __init__(self):
        self.cx = "017904673884379667699:ewclq3iogbe"
        self.key = "AIzaSyB5JjU-bb44bx5G8OlY9qUMG3Gfs_LUePQ"

        self.service = build("customsearch", "v1",
                  developerKey=self.key)

    def get_search_results(self, query, start=0):
        res = self.service.cse().list(
            q=query,
            cx=self.cx,
            start= start
          ).execute()

        return res

    def get_search_results_links(self, query):
        res = self.get_search_results(query)
        print()
        total_search_items = int(res.get('queries').get('request')[0].get('totalResults'))

        print("Searches : ",total_search_items)

        links = list()

        i = 1
        while i<30 and i<total_search_items:
            res = self.get_search_results(query,i)
            item_list = res.get('items')

            for item in item_list:
                links.append(item.get('link'))

            i += 10

        return links


        def get_search_results_links(self, query):
            res = self.get_search_results(query)
            print()
            total_search_items = int(res.get('queries').get('request')[0].get('totalResults'))

            print("Searches : ",total_search_items)

            links = list()

            i = 1
            while i<30 and i<total_search_items:
                res = self.get_search_results(query,i)
                item_list = res.get('items')

                for item in item_list:
                    links.append(item.get('link'))

                i += 10

            return links

def main():
    searchScraper = SearchScraper()
    searchScraper.get_search_results_links('blog about Skin Stickers Laptop Accessories')

if __name__ == '__main__':
  main()
