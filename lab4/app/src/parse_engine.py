import time

from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Item, Category


class Parser:
    def __init__(self):
        self.driver = self._init_driver()
        self.base_url = "https://ricewear.com"

    def _init_driver(self) -> webdriver.Chrome:
        options = Options()
        options.add_argument('--headless')
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        return webdriver.Chrome(options=options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def navigate_to_catalog(self):
        self.driver.get(self.base_url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "каталог"))
        ).click()

    def get_available_categories(self) -> List[str]:
        self.navigate_to_catalog()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-store-parts-switcher"))
        )
        return [cat.text for cat in self.driver.find_elements(By.CLASS_NAME, "js-store-parts-switcher")]

    def select_category(self, category_name: str):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-store-parts-switcher"))
        )
        categories = self.driver.find_elements(By.CLASS_NAME, "js-store-parts-switcher")
        for category in categories:
            if category.text == category_name:
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable(category)
                ).click()
                return
        raise ValueError(f"Категория {category_name} не найдена")

    def _handle_popup(self):
        try:
            popup = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.t-popup.t-popup_show"))
            )
            close_btn = popup.find_element(By.CSS_SELECTOR, "button.t-popup__block-close-button")
            self.driver.execute_script("arguments[0].click();", close_btn)
        except:
            pass

    def _load_all_pages(self):
        while True:
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                load_more = WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "js-store-load-more-btn"))
                )
                self.driver.execute_script("arguments[0].click();", load_more)
                time.sleep(0.5)
            except:
                break

    @staticmethod
    def category_has_items(category_name: str) -> bool:
        """Проверяет существование категории и наличие в ней товаров"""
        category = Category.query.filter_by(name=category_name).first()
        return category and len(category.items) > 0


    def parse_category(self, category_name: str) -> Dict[int, Dict]:
        if self.category_has_items(category_name):
            print(f"Категория {category_name} уже существует в БД, пропускаем парсинг")
            return {}
        try:
            self.navigate_to_catalog()
            self.select_category(category_name)
            self._load_all_pages()
            
            category = self._get_or_create_category(category_name)
            items = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".t-item [href]"))
            )

            result = {}
            for elem in items:
                try:
                    self._handle_popup()
                    item_data = self._extract_item_data(elem)
                    item = self._process_item(item_data, category)
                    result[item.id] = item.as_dict()
                except Exception as e:
                    print(f"Ошибка обработки элемента: {str(e)}")
                    continue

            return result
        finally:
            db.session.commit()

    def _extract_item_data(self, elem) -> Dict:
        WebDriverWait(self.driver, 10).until(EC.visibility_of(elem))
        return {
            'name': elem.find_element(By.CLASS_NAME, "t-name").text,
            'price': int(elem.find_element(By.CLASS_NAME, "t-store__card__price-value").text.replace(' ', '')),
            'old_price': self._get_old_price(elem),
            'currency': elem.find_element(By.CLASS_NAME, "t-store__card__price-currency").text,
            'href': elem.get_attribute("href")
        }

    def _get_old_price(self, elem):
        try:
            return int(elem.find_element(By.CLASS_NAME, "js-store-prod-price-old-val").text.replace(' ', ''))
        except:
            return None

    def _get_or_create_category(self, name: str) -> Category:
        category = Category.query.filter_by(name=name).first()
        if not category:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
        return category

    def _process_item(self, item_data: Dict, category: Category) -> Item:
        existing = Item.query.filter_by(href=item_data['href']).first()
        if existing:
            if category not in existing.categories:
                existing.categories.append(category)
                db.session.merge(existing)
            return existing

        new_item = Item(**item_data)
        new_item.categories.append(category)
        db.session.add(new_item)
        return new_item

    @staticmethod
    def get_items_by_category(category_name: str) -> List[Dict]:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            return []
        return [item.as_dict() for item in category.items]
    