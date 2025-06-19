# from elevenlabs.conversational_ai.conversation import ClientTools
# from langchain_community.tools import DuckDuckGoSearchRun
# import os


# SAVE_DIR = "D:/MyAIConversations"  # Customize this path as needed
# os.makedirs(SAVE_DIR, exist_ok=True)  # Create if doesn't exist


# def searchWeb(parameters):
#     query = parameters.get("query")
#     results = DuckDuckGoSearchRun(query=query)
#     return results

# def save_to_text(parameters):
#     filename = parameters.get("filename")
#     data =parameters.get("data")

#     safe_filename = os.path.basename(filename)

#     full_path = os.path.join(SAVE_DIR, safe_filename)

#     formatted_data = f"{data}"

#     with open(full_path,"a", encoding="utf-8") as file:
#         file.write(formatted_data + "\n") 




# client_tools = ClientTools()
# client_tools.register("searchWeb",searchWeb)
# client_tools.register("saveToTxt",save_to_text)

import os
import openai
import requests

from dotenv import load_dotenv
from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun
from PIL import Image
from io import BytesIO

SAVE_DIR = "D:/MyAIConversations"
os.makedirs(SAVE_DIR, exist_ok=True)

def searchWeb(parameters):
    query = parameters.get("query")
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.run(query)
    return results

def save_to_text(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")

    safe_filename = os.path.basename(filename)
    full_path = os.path.join(SAVE_DIR, safe_filename)

    with open(full_path, "a", encoding="utf-8") as file:
        file.write(f"{data}\n")


def create_html_file(parameters):
    filename = parameters.get("filename")
    data = parameters.get("data")
    title = parameters.get("title")

    formatted_html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1.0">
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <div>{data}</div>
        </body>
        </html>
        """
    safe_filename = os.path.basename(filename)
    full_path = os.path.join(SAVE_DIR, safe_filename)
    with open(full_path, "w", encoding="utf-8") as file:
        file.write(formatted_html)


def generate_image(parameters):
    prompt = parameters.get("prompt")
    filename = parameters.get("filename")
    size = parameters.get("size", "1024x1024")
    save_dir = parameters.get("save_dir", "generate_images")

    os.makedirs(save_dir,exist_ok=True)
    filepath = os.path.join(save_dir,filename)

    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response= openai.OpenAI()

    response = openai.images.generate(
        prompt=prompt,
        model="dall-e-3",
        n=1,
        size=size,
        quality="standard"
    )

    image_url = response['data'][0].url
    print(f"Image URL: {image_url}")

    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image.save(filepath)

client_tools = ClientTools()
client_tools.register("searchWeb", searchWeb)
client_tools.register("saveToTxt", save_to_text)
client_tools.register("createHtmlFile",create_html_file)
client_tools.register("generateImage",generate_image)
