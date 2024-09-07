from datetime import datetime
from repository.get_html import fetch_html_selenium
from data import model
from AI_Hub.scraper_agent import extract_data
from data import format_data

def perform_scrape(form_data: model.FormData) -> model.FinalResult:
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_html = fetch_html_selenium(form_data.url)
        
        markdown = format_data.html_to_markdown_with_readability(raw_html)
        # save_raw_data(markdown, timestamp)
        # print("config, ", config.FormData, config.FormData.fields, config.FormData.url)
        DynamicListingModel = model.create_dynamic_listing_model(form_data.fields)
  
        DynamicListingsContainer = model.create_listings_container_model(DynamicListingModel)
        formatted_data = extract_data(markdown, DynamicListingsContainer, form_data)

        df = format_data.get_data_frame(formatted_data)
        
    
        
        result = model.FinalResult(df=df, markdown=markdown, timestamp=timestamp)


        return result
    except Exception as e:
        print(e)
        raise Exception(e)

if __name__ == "__main__":
    from data.config import form_data
    print(perform_scrape())