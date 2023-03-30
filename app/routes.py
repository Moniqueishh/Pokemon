
from app import app

from flask import render_template, request, url_for, redirect
from flask_login import current_user, login_required

from .auth.forms import pSearch, LoginForm
from .models import User, Pokemon
import requests, json
from flask_bootstrap import Bootstrap


@app.route('/')
def homePage():
    return render_template('index.html')

@app.route("/search", methods=["GET", "POST"])
def searchPage():
    form = pSearch()
    Pokemon.query.limit(5)
    if request.method == "POST":
        if form.validate():
            pokemonName = form.pokemonName.data
            print(pokemonName)
            # return redirect(url_for("homePage"))
            
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemonName}'
            response = requests.get(url)
            if response.ok:
                my_dict = response.json()
                pokemon_dict = {}
                pokemon_dict["Name"] = my_dict["name"]
                pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
                pokemon_dict["Base XP"] = my_dict["base_experience"]
                pokemon_dict["Front Shiny"] = my_dict["sprites"]["front_shiny"]
                pokemon_dict["Base ATK"] = my_dict["stats"][1]["base_stat"]
                pokemon_dict["Base HP"] = my_dict["stats"][0]["base_stat"]
                pokemon_dict["Base DEF"] = my_dict["stats"][2]["base_stat"]

                # poke = Pokemon(pokemon_dict = {})


                return render_template("search_results.html", form = form, pokemon_dict = pokemon_dict)


            else:
                return "The pokemon you're looking for does not exist."

    return render_template("search.html", form = form)

@app.route('/catch')
@login_required
def catch(poke_id):
    poke = Pokemon.query.get(poke_id)
    if poke:
        current_user.catch(poke)
        poke.caught_poke.counts(5)
    else:
        pass

    return render_template('search.html')

# @app.route('/catch/<int:poke_id>)
# @login_required
# def catchPokemon(poke_id):
#         poke = Pokemon.query.get(poke_id)
#         if poke:
#             current_user.catch(poke)
#             poke.caught = True
#             poke.caught_poke.count(5)
#         else:
#             pass
#     return redirect(url_for("catchPoke")
