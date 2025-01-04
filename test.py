import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import unittest
import HtmlTestRunner
from datetime import datetime

class SimpleSeleniumTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        
    def test_01_wait_types(self):
        """Test different types of waits"""
        self.driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")
        
        start_button = self.driver.find_element(By.CSS_SELECTOR, "#start button")
        start_button.click()
        
        wait = WebDriverWait(self.driver, 10)
        finish_text = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#finish h4"))
        )
        
        fluent_wait = WebDriverWait(
            self.driver,
            timeout=10,
            poll_frequency=0.5
        )
        
        self.assertEqual(finish_text.text, "Hello World!")
        
    def test_02_action_class(self):
        """Test ActionChains functionality"""
        self.driver.get("https://the-internet.herokuapp.com/hovers")
        
        image = self.driver.find_element(By.CSS_SELECTOR, ".figure")
        
        actions = ActionChains(self.driver)
        actions.move_to_element(image).perform()
        
        caption = self.driver.find_element(By.CSS_SELECTOR, ".figcaption h5")
        self.assertTrue(caption.is_displayed())
        
    def test_03_select_class(self):
        """Test Select class functionality"""
        self.driver.get("https://the-internet.herokuapp.com/dropdown")
        
        dropdown = Select(self.driver.find_element(By.ID, "dropdown"))

        dropdown.select_by_index(1)
        time.sleep(1)
        
        dropdown.select_by_value("2")
        time.sleep(1)
        
        dropdown.select_by_visible_text("Option 1")
        
        selected_option = dropdown.first_selected_option
        self.assertEqual(selected_option.text, "Option 1")
        
    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    test_dir = "test_reports"
    report_file = f"TestReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleSeleniumTest)
    
    runner = HtmlTestRunner.HTMLTestRunner(
        output=test_dir,
        report_name=report_file,
        report_title="Simple Selenium Test Report",
        descriptions="Test cases for different Selenium WebDriver features"
    )
    
    try:
        runner.run(suite)
    except AttributeError as e:
        unittest.TextTestRunner(verbosity=2).run(suite)