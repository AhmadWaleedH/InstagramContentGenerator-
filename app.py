from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain


apikey = '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'

os.environ['OPENAI_API_KEY'] = apikey

llm = OpenAI(temperature=0.9) 
# title_template = PromptTemplate(
#     input_variables = ['text'], 
#     template='Generate 10 instagram hashtags based on the following text\n{text}'
# )

# script_template = PromptTemplate(
#     input_variables = ['text'], 
#     template='write a youtube video script based on this title. TITLE: {title}'
# )

def generate_ig_content(text):
    prompt = 'generate ig hashtag, location tag, caption and suggestion from the following text\n' + text
    print(llm(prompt))
    response = llm(prompt)
    return response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract relevant data and generate captions, hashtags, and location pins
    captions = []
    ig_content = generate_ig_content(soup.text)
    captions=ig_content
    
    return render_template('result.html', captions=captions)

if __name__ == '__main__':
    app.run()