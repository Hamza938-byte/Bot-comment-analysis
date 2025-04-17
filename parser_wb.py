from core.config import BASE_URL
from core.scraping.page_loader import PageLoader
from core.scraping.review_extractor import ReviewExtractor
from core.utils.CSV_saver import CSVSaver
from core.utils.webdriver import WebDriverManager


"""   Реализация парсера WB.   """


def Parser_WB(product_ids):
    all_reviews = []
    driver = WebDriverManager.create_webdriver()
    page_loader = PageLoader(driver)
    page_loader.load_page(f"{BASE_URL}{product_ids}/detail.aspx")
    page_loader.accept_cookies()
    product_name = ReviewExtractor.get_product_name(driver)

    if page_loader.open_reviews_section():
        page_loader.scroll_to_load_reviews()
        all_reviews.extend(
            ReviewExtractor.extract_reviews(driver, product_ids, product_name)
        )
    driver.quit()

    CSVSaver.save_to_CSV(all_reviews, product_ids)
    return f'wb_reviews_{product_ids}.csv'