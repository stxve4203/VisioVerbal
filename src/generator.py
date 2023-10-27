import string

import openai
import json
import random
from VisioVerbal.text_helpers.text_formatter import text_formatter
import os
import sys


"""
CONFIG 
"""

WORDLIST_JSON_PATH = 'VisioVerbal/data/wordlists/wordlists.json'



class TextGenerator():
    def __init__(self, api_key):

        self.api_key = api_key
        self.client = openai
        self.client.api_key = self.api_key

# Generate Phrase
    def generate_phrase(self):

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(os.path.dirname(__file__))
        data_file_path = os.path.join(base_path, 'data', 'wordlists', 'wordlists.json')

        try:
            with open(WORDLIST_JSON_PATH) as json_file:
                data = json.load(json_file)

        except FileNotFoundError:
            print(f"Error: The file '{data_file_path}' was not found.")

        num_prompts = 10
        random_prompts = []

        for _ in range(num_prompts):
            random_noun = random.choice(data["nouns"])
            random_adjective = random.choice(data["adjectives"])
            random_verb = random.choice(data["verbs"])
            random_phrase = random.choice(data["phrases"])

            random_prompt = f"{random_adjective} {random_noun} {random_verb} {random_phrase}"
            random_prompts.append(random_prompt)

        # Print the list of random prompts
        for prompt in random_prompts:
            return prompt


    def generate_custom_text(self, text, temperature=0.2):
        try:
            response = self.client.ChatCompletion.create(
                model='gpt-4',
                message=[
                    {'role': 'user',
                     'content': text
                    }
                ],
                temperature=temperature
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return str(e)


# Generate title
    def generate_title(self, prompt, temperature=0.2):
        try:
            response = self.client.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {'role': 'user',
                     'content': f'Generate a title for {prompt}'
                    }
                ],
                temperature=temperature
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return str(e)

    def generate_description(self, prompt, temperature=0.2):
        try:
            response = self.client.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {'role': 'user',
                     'content': f'Generate description for {prompt}, max length 250 words.'
                     }
                ],
                temperature=temperature
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return str(e)


# Generate Tags
    def generate_tags(self, prompt, temperature=0.2):
        try:
            response = self.client.ChatCompletion.create(
                model='gpt-4',
                messages=[
                    {'role': 'user',
                     'content': f'Generate 10 unique tags for {prompt}, without the 1., 2., 3., 4. ... and seperated with , .'}
                ],
                temperature=temperature
            )
            tags = response['choices'][0]['message']['content']
            return tags

        except Exception as e:
            return str(e)


# Generate Image Text
    def generate_image_text(self):
        prompt = self.generate_phrase()
        title = self.generate_title(prompt)
        description = self.generate_description(prompt)
        tags_list = []

        for i in range(1):
            tag = self.generate_tags(prompt)
            tags_list.append(tag)

        # Clean Strings
        cleaned_title = title.replace('\\', "")
        cleaned_description = description.replace('\\', "")

        # Format Strings
        formatted_description = text_formatter.limit_words_per_line(cleaned_description, max_words_per_line=20)

        image_data = {
                'Phrase': prompt,
                'Title': cleaned_title,
                'Description': formatted_description,
                'Tags': tags_list
        }

        file_name = f'{image_data["Phrase"]}' + '.json'

        file_path = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/recent_text_files"
        file_path = os.path.join(file_path, file_name)

        with open(file_path, 'w') as json_file:
            json.dump(image_data, json_file)

            # Return the generated data
        return image_data