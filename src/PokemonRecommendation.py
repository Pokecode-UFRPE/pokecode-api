from pathlib import Path
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, OneHotEncoder


class PokemonRecommendation:

    def __init__(self, compare_to: int, similar: int = 5):
        current_path = Path(__file__).resolve().parent.parent
        file_path = current_path / "data" / "pokemon.parquet"
        self.pokemon_df = pd.read_parquet(file_path)
        selected_columns = ['typing', 'hp', 'speed', 'height', 'weight', 'shape', 'primary_color']
        pokemon_features = self.pokemon_df[selected_columns].copy()

        encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        encoded_columns = pd.DataFrame(encoder.fit_transform(pokemon_features[['typing', 'shape', 'primary_color']]))
        encoded_columns.columns = encoder.get_feature_names_out(['typing', 'shape', 'primary_color'])
        pokemon_features = pd.concat([pokemon_features, encoded_columns], axis=1)
        pokemon_features.drop(columns=['typing', 'shape', 'primary_color'], inplace=True)
        scaler = StandardScaler()
        pokemon_features[['hp', 'speed', 'height', 'weight']] = scaler.fit_transform(
            pokemon_features[['hp', 'speed', 'height', 'weight']])

        self.k_neighbors = similar
        self.knn_model = NearestNeighbors(n_neighbors=self.k_neighbors, metric='euclidean')
        self.knn_model.fit(pokemon_features)

        self.distances, self.indices = self.knn_model.kneighbors(
            pokemon_features.iloc[int(compare_to)].values.reshape(1, -1))

    def run(self):
        pokemon = []
        for i in range(1, self.k_neighbors):
            pokemon.append(str(self.pokemon_df.loc[self.indices[0][i], 'pokedex_number']))
        return pokemon
