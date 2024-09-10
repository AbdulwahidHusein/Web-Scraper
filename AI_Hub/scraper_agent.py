from openai import OpenAI
import os
import data.config as config
from data import model

def extract_data(page_stats: model.PageStats, DynamicListingsContainer, form_data: model.FormData):
    # client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # system_message = """You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
    #                     from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
    #                     with no additional commentary, explanations, or extraneous information. 
    #                     You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
    #                     Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""

    # user_message = f"Extract the following information from the provided text:\nPage content:\n\n{page_stats.cleaned_html}"

    # completion = client.beta.chat.completions.parse(
    #     model=form_data.model,
    #     messages=[
    #         {"role": "system", "content": system_message},
    #         {"role": "user", "content": user_message},
    #     ],
    #     response_format=DynamicListingsContainer
    # )
    # return completion.choices[0].message.parsed
    print(page_stats.cleaned_html, "formssssssssssssssssssssssssss", page_stats.forms, "linksssssssss", page_stats.next_buttons, page_stats.prev_buttons)
    return DynamicListingsContainer
    
