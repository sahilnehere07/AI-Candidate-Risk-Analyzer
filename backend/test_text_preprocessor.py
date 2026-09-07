from services.text_preprocessor import clean_text


text = """
John Doe


Software Engineer


I built a scalable web application.

AI


Python


FastAPI
"""


cleaned = clean_text(text)

print("CLEANED TEXT:")
print(cleaned)