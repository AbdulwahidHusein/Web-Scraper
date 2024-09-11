from openai import OpenAI
from langchain_openai import ChatOpenAI

import os
from data import model
from repository import get_pagestats, setup_selenium

from langchain.tools import tool

os.environ.setdefault("OPENAI_API_KEY", os.getenv('OPENAI_API_KEY'))

driver = setup_selenium.setup()

container = None
page_stats = None
form_data = None

def setup(DynamicListingsContainer, form_datal: model.FormData):
    global driver, container, page_stats, form_data
    container = DynamicListingsContainer
    form_data = form_datal
    try:
        driver.get(form_data.url)
        page_stats = get_pagestats.page_stats(driver)
    except Exception as e:
        print(e)



from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

global dynamic_container

@tool
def add_data(html_content) -> str:
    """
    parses and adds the data from the current page to the results list
    Args:
        html_content: the html content of the current page
    returns: status message
    """
    global dynamic_container
    try:
        
        client = OpenAI()

        system_message = """You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
                            from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
                            with no additional commentary, explanations, or extraneous information. 
                            You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                            Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""

        user_message = f"Extract the following information from the provided text:\nPage content:\n\n{html_content}"

        completion = client.beta.chat.completions.parse(
            model=form_data.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            response_format=DynamicListingsContainer
        )
        result =  completion.choices[0].message.parsed
        if dynamic_container is None:
            dynamic_container = DynamicListingsContainer(listings=[])
        
        dynamic_container.listings.extend(result.listings)
        return "Data added successfully."
    except Exception as e:
        return f"Error: {e}"


@tool
def ClickLink(xpath) -> str:
    """
    Clicks a link specified by the given XPath.

    Args:
        xpath: The XPath string of the link to click.

    Returns:
        str: A message indicating the result of the click action.
    """
    global driver  # Use the global driver

    try:
        # Find the link using the provided XPath
        link_element = driver.find_element(By.XPATH, xpath)
        link_element.click()  # Click the link
        return "Link clicked successfully."
    except NoSuchElementException:
        return "Error: Link not found."
    except Exception as e:
        return f"An error occurred while clicking the link: {e}"

@tool
def wait(seconds) -> None:
    """waits for a given number of seconds
    Args: seconds (int)
    """
    driver.implicitly_wait(seconds)
    return None
    
@tool
def get_page_data() -> model.PageStats:
    """returns the statistics of the driver
    it contains the html, forms, buttons and links of the curent driver
    Args:None
    Returns:model.PageStats
    """
    global driver
    return get_pagestats.page_stats(driver)


from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a intellegent web scraper who analyses the page and extracts relevant data you can fill forms, click on links and extract data from the current page(driver) using your tools available 
             you always use get page data tool before extracting the page and also you can click buttons fill forms using your tools after clicking links or filling forms you have to wait for a while usoing your waiting tool until the page loads.
             after you get the current page data you can extract a data from the current page using add data tool or you can click relevant links from the given page data even if you belive more data can be found by clicking links you can click the link to extract further""",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)




def perform_agent_scrapping():
    global driver, container, page_stats, form_data
    model = ChatOpenAI(model = form_data.model)
    
    tools = [ClickLink, wait, get_page_data, add_data]
    
    agent = create_tool_calling_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor.invoke({"input": "start your job"})




if __name__ == "__main__":
    form_data = model.FormData(model="gpt-4o-mini", fields=["name", "price"], url="https://scrapeme.live/shop/page/2/", query="")
    
    DynamicListingModel = model.create_dynamic_listing_model(form_data.fields)
    DynamicListingsContainer = model.create_listings_container_model(DynamicListingModel)
    
    setup(DynamicListingsContainer, form_data)
    
    result = perform_agent_scrapping()
    print(dynamic_container)