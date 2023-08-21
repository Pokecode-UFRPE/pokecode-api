from fastapi import FastAPI, Query

from src.PokemonRecommendation import PokemonRecommendation

app = FastAPI()


@app.get("/{pokemon_id}")
def get_recommendations(pokemon_id, quantity: int = Query(default=10, title="Quantity")):
    pokemon = PokemonRecommendation(pokemon_id, quantity)
    return pokemon.run()
