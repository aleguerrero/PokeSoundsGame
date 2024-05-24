import os
from pydub import AudioSegment
import requests
from pydub.playback import play
import random
import subprocess

def silent_play(segment):
    """Play a segment, suppressing console output."""
    # Write the segment to a temporary file
    segment.export("temp.wav", format="wav")

    # Use ffplay to play the file, suppressing output
    FNULL = open(os.devnull, 'w')
    subprocess.call(["ffplay", "-nodisp", "-autoexit", "temp.wav"], stdout=FNULL, stderr=subprocess.STDOUT)

os.environ["PYDUB_LOGGING"] = "ERROR"

pokemon_ids = []

while len(pokemon_ids) != 5:
    pokemon_id = random.randint(1, 151)
    if pokemon_id not in pokemon_ids:
        pokemon_ids.append(pokemon_id)

pokemons_info = []

for pid in pokemon_ids:
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pid}/')
    data = response.json()
    pokemon_info = {
        "id": data['id'],
        "name": data['name'],
        "cry": data['cries']['legacy']
    }
    pokemons_info.append(pokemon_info)

selected_pokemon_index = random.randint(0, 4)

r = requests.get(pokemons_info[selected_pokemon_index]["cry"], allow_redirects=True)

open('audio.mp3', 'wb').write(r.content)

# Load audio file
audio = AudioSegment.from_file("audio.mp3")

guess = False
count = 0

while not guess and count < 3:
    silent_play(audio)
    print("Select a number from the following Pokemon:")
    option = 1
    for p in pokemons_info:
        print(f"{str(option)} - {str.upper(p['name'])}")
        option += 1

    print('What is the name of the Pokemon?')

    try:
        pokemon_number_selection = int(input())

        if pokemon_number_selection >= 1 and pokemon_number_selection <= 5:
            selected_pokemon_name = pokemons_info[pokemon_number_selection-1]['name']
            if selected_pokemon_name == pokemons_info[selected_pokemon_index]['name']:
                guess = True
                print(f"well done!! it is {str.upper(selected_pokemon_name)}")
            elif count < 2:
                print("nope, try again!")
            count += 1
        else:
            print("Please select a number between 1 and 5!")
    except:
        print("Please enter a number between 1 and 5!")

if not guess:
    print(f"The Pokemon was {str.upper(pokemons_info[selected_pokemon_index]['name'])}")