# __animeyt_dl__
Funciones para descarga desde [animeyt](www.animeyt.tv).

## Uso
### Busqueda(search)
Retorna una lista de resultados como diccionarios
```python
resultados = animeyt_dl.search("dragon ball z")
```

### Descarga(download_anime_from_dict)
Descarga una serie, recibe como parametro un resultado de busqueda y opcionalmente el numero de capitulo a partir del cual descargar, si no se especifica descarga la serie completa
```python
resultados = animeyt_dl.search("fullmetal alchemist")
##descarga la serie completa
animeyt_dl.download_anime_from_dict(resultados[0])
resultados2 = animeyt_dl.search("dragon ball z")
##descarga la serie a partir del capitulo 194 incluido
animeyt_dl.download_anime_from_dict(resultados2[0], 194)
```
