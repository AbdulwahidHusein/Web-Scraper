from datetime import datetime
from data import model
from AI_Hub.scraper_agent import setup, perform_agent_scrapping, dynamic_container
from data import format_data

from repository import setup_selenium, get_pagestats

# driver = setup_selenium.setup()



def perform_scrape(form_data: model.FormData) -> model.FinalResult:
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # raw_html = fetch_html_selenium(form_data.url)
        
        # driver.get(form_data.url)
        # pagestats = get_pagestats.page_stats(driver)
        
        # markdown = format_data.html_to_markdown_with_readability(pagestats.html)
        # save_raw_data(markdown, timestamp)
        # print("config, ", config.FormData, config.FormData.fields, config.FormData.url)
        DynamicListingModel = model.create_dynamic_listing_model(form_data.fields)
        
        # pagestats.driver = driver
        # pagestats.cleaned_html = markdown
  
        DynamicListingsContainer = model.create_listings_container_model(DynamicListingModel)
        # formatted_data = extract_data(pagestats, DynamicListingsContainer, form_data)
        
        setup(DynamicListingsContainer, form_data)
        
        perform_agent_scrapping()

        df = format_data.get_data_frame(dynamic_container)
        
    
        
        result = model.FinalResult(df=df, markdown="markdown", timestamp=timestamp)


        return result
    except Exception as e:
        print(e)
        raise Exception(e)

if __name__ == "__main__":
    from data.config import form_data
    print(perform_scrape())