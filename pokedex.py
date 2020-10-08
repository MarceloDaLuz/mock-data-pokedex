import requests
from bs4 import BeautifulSoup
import json
import shutil
import os
import re

def main():
    URL = 'https://pokemondb.net/pokedex/national'
    r = requests.get(URL)
    if(r.status_code == 200):
        print("Success!")
        page = BeautifulSoup(r.content,'html5lib')
        title = page.find('h1').text.strip() ## title of json 
        path = ''        
        try:
            title = re.sub(r'\s+', '', title)
            title =  re.sub(r'[-()\"#/@;:<>{}`+=~|.!?,]','',title)            
            path = './pokedex/{}'.format(title)
            if os.path.isdir(path) == False:
                os.mkdir(path)
        except OSError:
            print("Erro ao criar a pasta!")
        else:
            list_of_pokemons = []        
            count_generations = 0
            for generations in page.findAll('div', attrs = {'class':'infocard-list'}):
                generations_json = {}
                ##list of pokemons on this generation
                count_generations = count_generations + 1                
                generation_title = "Geração {}".format(count_generations)                
                generations_json['generation'] = generation_title
                pokemons = []
                for pokemon in generations.findAll('div', attrs = {'class': 'infocard'}):                                    
                    pokemon_info = {}
                    # pokemon code
                    pokemon_info['code'] = pokemon.find('small').text.strip()                
                    # pokemon name
                    pokemon_info['name'] = pokemon.find('a', attrs = {'class': 'ent-name'}).text.strip()
                    # pokemon img
                    pokemon_img = pokemon.find('span', attrs = {'class': 'img-sprite'})                
                    pokemon_info['img'] =  pokemon_img['data-src']
                    # pokemon type
                    pokemon_info['type'] = {}
                    count_types = 0
                    for type_of_pokemon in pokemon.findAll('a', attrs = {'class':'itype'}):                                                            
                        pokemon_info['type'][count_types] = type_of_pokemon.text
                        count_types = count_types + 1
                    pokemons.append(pokemon_info)
                generations_json['pokemons'] = pokemons
                list_of_pokemons.append(generations_json)

            filename =  '{}/{}.json'.format(path,title)
            with open(filename,'w+',encoding='utf8') as f:
                json_string = json.dumps(list_of_pokemons,ensure_ascii=False)
                f.write(json_string)

if __name__ == "__main__":
    main()