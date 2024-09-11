from selenium.webdriver.common.by import By
from data import model, format_data

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


def get_forms(driver):
    forms = driver.find_elements(By.TAG_NAME, 'form')
    return [{'xpath': get_xpath_of_element(driver, form), 'text': form.text} for form in forms]

# def detect_buttons_and_links(driver):
#     """Detect all buttons and links on the page."""
#     try:
#         buttons = driver.find_elements(By.TAG_NAME, 'button')
#         links = driver.find_elements(By.TAG_NAME, 'a')
#         all_elements = buttons + links
        
#         return [{'xpath': get_xpath_of_element(driver, element), 'text': element.text} for element in all_elements]
#     except Exception as e:
#         print(f"An error occurred while detecting buttons and links: {e}")
#         return []\
from selenium.webdriver.common.by import By
import re

def detect_pagination_elements(driver):
    """Detect all potential pagination buttons and links on the page."""
    pagination_keywords = ['next', 'previous', 'prev', 'pagination', 'older', 'newer', 'page', '>>', '<<']
    pagination_href_pattern = re.compile(r'[\?&]page=\d+', re.IGNORECASE)  # Matches '?page=2' or '&page=2'
    
    try:
        # Get all buttons and links
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        links = driver.find_elements(By.TAG_NAME, 'a')
        all_elements = buttons + links
        
        pagination_elements = []
        
        # Check for pagination-related elements based on text, attributes, and href
        for element in all_elements:
            element_text = element.text.lower().strip()
            element_class = element.get_attribute('class') or ''
            element_aria_label = element.get_attribute('aria-label') or ''
            element_title = element.get_attribute('title') or ''
            element_href = element.get_attribute('href') or ''
            
            # Check if the element contains any pagination-related keyword
            if (any(keyword in element_text for keyword in pagination_keywords) or
               any(keyword in element_class for keyword in pagination_keywords) or
               any(keyword in element_aria_label for keyword in pagination_keywords) or
               any(keyword in element_title for keyword in pagination_keywords) or
               pagination_href_pattern.search(element_href)):  # Check for pagination pattern in href
                pagination_elements.append({
                    'xpath': get_xpath_of_element(driver, element),
                    'text': element.text,
                    'href': element_href if element_href else None,  # Include href if it's a link
                    'class': element_class
                })
        
        return pagination_elements

    except Exception as e:
        print(f"An error occurred while detecting pagination elements: {e}")
        return []


def page_stats(driver) -> model.PageStats:
    all_buttons_and_links = detect_pagination_elements(driver)
    forms = get_forms(driver)
    html = driver.page_source
    cleaned = format_data.clean_html(html)
    redeable_html = format_data.html_to_markdown_with_readability(cleaned)
    pagestats = model.PageStats(
        html=redeable_html, 
        forms=forms, 
        buttons_and_links=all_buttons_and_links
    )
    
    return pagestats

# Assuming fetch_html_selenium is defined as before
#if __name__ == "__main__":
#    url = "https://scrapeme.live"
#    html = fetch_html_selenium(url)
#    print(html)