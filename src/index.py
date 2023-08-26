from fastapi import FastAPI, Query
import uvicorn
from PokemonRecommendation import PokemonRecommendation

app = FastAPI()


@app.get("/{pokemon_id}")
def get_recommendations(pokemon_id, quantity: int = Query(default=10, title="Quantity")):
    pokemon = PokemonRecommendation(pokemon_id, quantity)
    return pokemon.run()


if __name__ == "__main__":
    port = 3001  # Defina a porta desejada
    host = "0.0.0.0"  # Isso permite acesso de qualquer IP na mesma rede
    uvicorn.run(app, host=host, port=port)
