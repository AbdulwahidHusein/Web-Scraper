from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import setup_selenium


def detect_form(driver):
    try:
        # Try to find a form element on the page
        form = driver.find_element(By.TAG_NAME, 'form')
        if form:
            print("Form detected on the page.")
            return form
    except:
        print("No form found on the page.")
        return ""

def detect_next_button(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')] | //a[contains(text(), 'Next')]")
        if next_button:
            print("Next button detected on the page.")
            return True
    except:
        print("No 'Next' button found on the page.")
        return False

def analyze_page_structure(driver):
    form_exists = detect_form(driver)
    next_button_exists = detect_next_button(driver)

    return form_exists, next_button_exists

def get_xpath_of_element(driver, element):
    """Returns the XPath of a given WebElement."""
    return driver.execute_script(
        """
        var getPathTo = function(element) {
            if (element.id!=='')
                return 'id(\"'+element.id+'\")';
            if (element===document.body)
                return element.tagName;
            
            var ix= 0;
            var siblings= element.parentNode.childNodes;
            for (var i= 0; i<siblings.length; i++) {
                var sibling= siblings[i];
                if (sibling===element)
                    return getPathTo(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
                if (sibling.nodeType===1 && sibling.tagName===element.tagName)
                    ix++;
            }
        };
        return getPathTo(arguments[0]);
        """, element)

def fetch_html_selenium(url):
    driver = setup_selenium.setup()
    try:
        driver.get(url)
        
        buttons = driver.find_elements(By.XPATH, "//button | //input[@type='submit']")
        links = driver.find_elements(By.XPATH, "//a")

        print("Buttons:")
        for button in buttons:
            xpath = get_xpath_of_element(driver, button)
            print(f"Button text: '{button.text}', XPath: {xpath}")
        
        # Print the XPath of each link
        print("\nLinks:")
        for link in links:
            xpath = get_xpath_of_element(driver, link)
            print(f"Link text: '{link.text}', XPath: {xpath}")
        
        # Extract the HTML after analyzing the buttons and links
        html = driver.page_source
        return "html"

    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://scrapeme.live"
    html = fetch_html_selenium(url)
    print(html)