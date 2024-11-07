import os
import time
import requests
from openai import OpenAI
from PIL import Image
from io import BytesIO
from config.config import OPENAI_API_KEY

def article_image():
    # https://www.datacamp.com/tutorial/a-comprehensive-guide-to-the-dall-e-3-api
    # start time of function
    start_time = time.time()

    # working directory
    cwd = str(os.getcwd())

    client = OpenAI(api_key=OPENAI_API_KEY)

    # ------------------------------------GETTING SUMMARY FOR DALLE PROMPT------------------------------------
    # opening aritcle text
    with open('article_text.txt', 'r') as file:
        # Wczytywanie całej zawartości pliku
        article = file.read()

    prompt = f"""
    Podsumuj po polsku artykuł z znajdujący się w potrójnym cudzysłowiu. Odpowiedź ma mieć maksymalnie 500 znaków.
    '''{article}'''
    """

    def get_response(prompt):
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # lub inny dostępny model
            messages=[
                {"role": "system", "content": "Jesteś osobą poszerzającą wiedzę o AI, która dzieli się swoimi przemyśleniami na portalu LinkedIn w formie podsumowań arykułów, które przeczytała."},
                {"role": "user", "content": prompt}
            ],
            # max_tokens=20,
            temperature=0.25
        )
        return response.choices[0].message.content

    text_response = get_response(prompt)

    print("RESPONSE:\n", text_response)

    # ------------------------------------GETTING IMAGE FROM DALLE------------------------------------

    prompt_dalle = f"""
    W potrójnym cudzysłowiu znajduje się podsumowanie treści artykułu. Na podstawie podsumowania stwórz obraz, który będzie nawiązywał do treści artykułu i dobrze go zobrazuje odbiorcom na platformie LinkedIn.
    '''{text_response}'''
    """

    print("PROMPT DALLE:", prompt_dalle)

    def get_image_from_DALL_E_3_API(prompt_dalle):

        image_dimension = "1024x1024"
        image_quality = "standard"
        model = "dall-e-3"
        nb_final_image = 1

        response = client.images.generate(
            model=model,
            prompt=prompt_dalle,
            size=image_dimension,
            quality=image_quality,
            n=nb_final_image,
        )

        image_url = response.data[0].url

        print(image_url)
        print(response.data[0])

        # Pobierz obraz z URL
        image_response = requests.get(image_url)

        # Sprawdź, czy pobieranie obrazu się powiodło
        if image_response.status_code == 200:
            # Otwórz obraz za pomocą PIL i zapisz go jako plik
            image = Image.open(BytesIO(image_response.content))
            image.save("post_image.png")
            print("Obraz został zapisany jako 'generated_image.png'")
        else:
            print("Błąd podczas pobierania obrazu")

    get_image_from_DALL_E_3_API(prompt_dalle)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time)
    print('finish')

if __name__ == "__main__":
    article_image()

