from dotenv import load_dotenv
from openai import OpenAI
import os

# Load the API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

# Define placeholder values
company_name = "CNC Anwendungstechnik Miroslav Pop"
language_source = "German"
language_target = "English"

company_description = f'''
"CNC Anwendungstechnik Miroslav Pop" ist spezialisiert auf qualitativ hochwertige und einzigartige Produkte. Fräsen und schneiden von fast allen Materialien und Sägen, Bohren, Stanzen, Schweißen und Schleifen.
'''

product_description = f'''
Unser Unternehmen "CNC Anwendungstechnik Miroslav Pop" bietet eine Vielzahl an Fertigungsmöglichkeiten an. Wir können Holz und andere Materialien sägen, ablängen und verbinden, indem wir sie schweißen, löten oder verkleben. 
Wir können auch Trennungen durchführen und verschiedene Werkzeuge verwenden, wie zum Beispiel Fräsen, Bohren und Kanten anleimen. 
Unsere Messgeräte (z.B. "SuperMässung 5000 Delüxe") ermöglichen eine Genauigkeit von 0,001 mm.
Wir können auch 3D-Bearbeitungen durchführen und Materialien mit Laserschneiden oder Plasmaschneiden bearbeiten.
'''

# Multi-line comment with placeholders
system_role = f'''
You are a helpful translator for a B2B e-commerce platform. Your task is to translate the following text while adhering to the following rules:

1. Make the translation sound as natural as possible.
2. Pay attention to nuance.
3. Never translate terms that are enclosed in double straight quotation marks ("), even if the terms contain words that could be translated.  For example, if the original text contains "Hutversand Qualität", the translation must contain "Hutversand Qualität".
4. You MUST NEVER translate any occurances of the <company_name> passed by the user.
5. You MUST only use double straight quotation marks (") for quotations.
'''

user_role = f"""
<company_name>
{company_name}
</company_name>
<company_description>
{company_description}
</company_description>
<product_description>
{product_description}
</product_description>
Translate the text from {language_source} to {language_target} while following ALL rules above.
Use JSON format with the keys "company_description", and "product_description".
"""

# print(user_role)
# exit()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": system_role},
        {"role": "user", "content": user_role}
    ]
)

print(response.choices[0].message.content)
