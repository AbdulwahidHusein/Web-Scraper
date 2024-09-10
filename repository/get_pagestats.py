from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data import model

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

def detect_forms(driver):
    try:
        # Find all form elements on the page
        forms = driver.find_elements(By.TAG_NAME, 'form')
        return [{'xpath': get_xpath_of_element(driver, form), 'text': form.text} for form in forms]
    except Exception as e:
        print(f"An error occurred while detecting forms: {e}")
        return []

def detect_next_buttons(driver):
    try:
        # Find all 'Next' buttons (by text or common navigation classes/IDs)
        next_buttons = driver.find_elements(By.XPATH, """
            //button[contains(text(), 'Next')] | 
            //a[contains(text(), 'Next')] |
            //button[contains(@aria-label, 'Next')] | 
            //a[contains(@aria-label, 'Next')] |
            //a[contains(@class, 'next')] | 
            //button[contains(@class, 'next')] |
            //a[contains(@href, 'next')] |
            //a[contains(@class, 'pagination-next')] |
            //a[contains(text(), '>')] |
            //a[contains(text(), '›')] |
            //a[contains(text(), '→')]
        """)
        
        return [{'xpath': get_xpath_of_element(driver, button), 'text': button.text} for button in next_buttons]
    except Exception as e:
        print(f"An error occurred while detecting 'Next' buttons: {e}")
        return []

def detect_prev_buttons(driver):
    try:
        # Find all 'Previous' buttons (by text, common navigation classes/IDs, and symbols)
        prev_buttons = driver.find_elements(By.XPATH, """
            //button[contains(text(), 'Previous')] | 
            //a[contains(text(), 'Previous')] |
            //button[contains(@aria-label, 'Previous')] | 
            //a[contains(@aria-label, 'Previous')] |
            //a[contains(@class, 'prev')] | 
            //button[contains(@class, 'prev')] |
            //a[contains(@href, 'prev')] |
            //a[contains(@class, 'pagination-prev')] |
            //a[contains(text(), '<')] |
            //a[contains(text(), '‹')] |
            //a[contains(text(), '←')]
        """)
        
        return [{'xpath': get_xpath_of_element(driver, button), 'text': button.text} for button in prev_buttons]
    except Exception as e:
        print(f"An error occurred while detecting 'Previous' buttons: {e}")
        return []



def page_stats(driver) -> model.PageStats:
    forms = detect_forms(driver)
    next_buttons = detect_next_buttons(driver)
    prev_buttons = detect_prev_buttons(driver)

    pagestats = model.PageStats(html=driver.page_source, forms=forms, next_buttons=next_buttons, prev_buttons=prev_buttons)
    return pagestats


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



# def fetch_html_selenium(url):
#     driver = setup_selenium.setup()
#     try:
#         driver.get(url)
#         #wait
#         driver.implicitly_wait(10)

#         # print("Buttons:")
#         # for button in buttons:
#         #     xpath = get_xpath_of_element(driver, button)
#         #     print(f"Button text: '{button.text}', XPath: {xpath}")
        
#         # Print the XPath of each link
#         # print("\nLinks:")
#         # for link in links:
#         #     xpath = get_xpath_of_element(driver, link)
#         #     print(f"Link text: '{link.text}', XPath: {xpath}")
        
#         # Extract the HTML after analyzing the buttons and links
#         html = driver.page_source
#         return html

#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     url = "https://scrapeme.live"
#     html = fetch_html_selenium(url)
#     print(html)