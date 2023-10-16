import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
import random
from smb_quote import SmbQuote

class AWSClient:
    def __init__(self):
        self.dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
        self.smb_quote = SmbQuote()

    def getAllItemsQuotes(self, items_per_scan=1):
        table_name = 'smb_quotes'
        exclusive_start_key = {
            'id': {'S': "211860"}
        }

        try:
            all_items = []

            while len(all_items) <= items_per_scan:
                response = self.dynamodb.scan(
                    TableName=table_name,
                    ExclusiveStartKey=exclusive_start_key,
                )

                items = response['Items']
                all_items.extend(items)

                if 'LastEvaluatedKey' in response:
                    exclusive_start_key = response['LastEvaluatedKey']
                else:
                    break

            transformed_items = []
            for item in all_items:
                transformed_item = {}
                for key, value in item.items():
                    if 'S' in value:
                        transformed_item[key] = value['S']
                    elif 'SS' in value:
                        transformed_item[key] = value['SS']
                    else:
                        transformed_item[key] = value
                transformed_items.append(transformed_item)

            df = pd.DataFrame(transformed_items)

            output_path = '/Users/steve/PycharmProjects/automation_image_generation/data/wordlists/smb_quotes.csv'
            df.to_csv(output_path, index=False)

            return transformed_items

        except NoCredentialsError:
            print("AWS credentials not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_random_quote(self):
        df = pd.read_csv('/Users/steve/PycharmProjects/automation_image_generation/data/wordlists/smb_quotes.csv')

        if df.empty:
            return None

        random_id = random.choice(df['id'].values)
        matching_rows = df[df['id'] == random_id]

        if not matching_rows.empty:
            matching_quote = matching_rows.to_dict(orient='records')[0]
            self.smb_quote.init_rows(matching_quote)
            return matching_quote
        else:
            return None


client = AWSClient()
random_quote_dict = client.get_random_quote()
smb_quote = client.smb_quote

print(f'ID: {smb_quote.id}')
print(f'Quote: {smb_quote.quote}')
print(f'Tags:{smb_quote.tags}')
print(f'Author: {smb_quote.author}')