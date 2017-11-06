from get_all_isbns import get_isbns
from scrape import Amazon_Scraper


U = get_isbns()
books = Amazon_Scraper(U)
books.get_all_books()
books.close_driver()

