import openai
import json
import random
from Helpers import text_formatter
import os

class TextGenerator():
    def __init__(self, api_key):

        self.api_key = api_key
        self.client = openai
        self.client.api_key = self.api_key

# Generate Phrase
    def generate_phrase(self):

        with open('../data/wordlists/wordlists.json') as json_file:
            data = json.load(json_file)

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
            print(prompt)
            return prompt


# Generate title
    def generate_title(self, prompt, temperature=0.2):
        try:
            response = self.client.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': f'Generate a title for {prompt}'}
                ],
                temperature=temperature
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return str(e)

    def generate_description(self, prompt, temperature=0.2):
        try:
            response = self.client.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': f'Generate description for {prompt}'}
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
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': f'Generate 10 unique tags for {prompt}, without the counting numbers.'}
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
                'Title': cleaned_title,
                'Description': formatted_description,
                'Tags': tags_list
        }

        with open('generated_texts.txt', 'a') as file:
            file.write(f"Title: {image_data['Title']}\n")
            file.write("-" * 100 + "\n")
            file.write(f"Description: {image_data['Description']}\n")
            file.write("-" * 100 + "\n")
            file.write("Tags:\n")
            for tag in image_data['Tags']:
                file.write(f"{tag}\n")
            file.write("-" * 100 + "\n")

            # Return the generated data
        return image_data


