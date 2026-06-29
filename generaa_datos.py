import pandas as pd
import numpy as np

np.random.seed(42)

n = 10000

datos = pd.DataFrame({
    "ID": range(1, n + 1),
    "Edad": np.random.randint(18, 65, n),
    "Salario": np.random.randint(500, 3000, n),
    "Ciudad": np.random.choice(
        ["Quito", "Guayaquil", "Cuenca", "Loja"],
        n
    )
})

# Introducir errores
datos.loc[5, "Edad"] = np.nan
datos.loc[10, "Salario"] = np.nan
datos.loc[15, "Ciudad"] = None
datos.loc[20, "Edad"] = 150
datos.loc[25, "Salario"] = 50000

print(datos.head())

datos.to_csv("datos_practica.csv", index=False)