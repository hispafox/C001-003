"""
E1.2 — Explorando Tokens y Embeddings
Script que demuestra cómo los LLMs tokenizan texto y cómo funcionan
los embeddings para medir similitud semántica entre frases.

Tres partes:
  Parte 1: Tokenización paso a paso (word-level, character-level, y simulación BPE)
  Parte 2: Embeddings y similitud semántica con TF-IDF (sklearn)
  Parte 3: Visualización 2D de embeddings

Variantes opcionales documentadas en el Word:
  - tiktoken (codificación real de GPT-4): pip install tiktoken
  - sentence-transformers (embeddings neuronales): pip install sentence-transformers

Dependencias: pip install scikit-learn numpy
"""

import re
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD


# ═══════════════════════════════════════════════════════════════
# PARTE 1: TOKENIZACIÓN — De lo simple a lo sofisticado
# ═══════════════════════════════════════════════════════════════

def tokenizar_por_palabras(texto: str) -> dict:
    """Tokenización nivel 1: divide el texto por palabras y puntuación.

    Este es el método más simple. Cada palabra y signo de puntuación
    se convierte en un token. Es fácil de entender pero ineficiente:
    no maneja bien palabras desconocidas ni morfología.

    Args:
        texto: Texto a tokenizar.

    Returns:
        Diccionario con tokens, IDs y estadísticas.

    Raises:
        ValueError: Si el texto está vacío.
    """
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacío")

    tokens: list[str] = re.findall(r'\w+|[^\w\s]', texto)
    vocabulario: dict[str, int] = {}
    for token in tokens:
        if token not in vocabulario:
            vocabulario[token] = len(vocabulario)

    token_ids: list[int] = [vocabulario[t] for t in tokens]

    return {
        "metodo": "Palabras",
        "texto_original": texto,
        "tokens": tokens,
        "token_ids": token_ids,
        "num_tokens": len(tokens),
        "vocabulario_size": len(vocabulario),
        "vocabulario": vocabulario,
    }


def tokenizar_por_caracteres(texto: str) -> dict:
    """Tokenización nivel 2: cada carácter es un token.

    Vocabulario mínimo (solo caracteres únicos), pero secuencias
    muy largas. Los modelos tempranos usaban este enfoque.

    Args:
        texto: Texto a tokenizar.

    Returns:
        Diccionario con tokens, IDs y estadísticas.

    Raises:
        ValueError: Si el texto está vacío.
    """
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacío")

    tokens: list[str] = list(texto)
    vocabulario: dict[str, int] = {}
    for char in tokens:
        if char not in vocabulario:
            vocabulario[char] = len(vocabulario)

    token_ids: list[int] = [vocabulario[t] for t in tokens]

    return {
        "metodo": "Caracteres",
        "texto_original": texto,
        "tokens": tokens,
        "token_ids": token_ids,
        "num_tokens": len(tokens),
        "vocabulario_size": len(vocabulario),
        "vocabulario": vocabulario,
    }


def tokenizar_bpe_simulado(texto: str, num_merges: int = 10) -> dict:
    """Tokenización nivel 3: Simulación de Byte Pair Encoding (BPE).

    BPE es el método usado por GPT, Claude y la mayoría de LLMs modernos.
    Funciona así:
      1. Empezar con caracteres individuales
      2. Buscar el par de tokens adyacentes más frecuente
      3. Fusionar ese par en un nuevo token
      4. Repetir hasta alcanzar el tamaño de vocabulario deseado

    Args:
        texto: Texto a tokenizar.
        num_merges: Número de fusiones BPE a realizar.

    Returns:
        Diccionario con tokens, historial de merges y estadísticas.

    Raises:
        ValueError: Si el texto está vacío o num_merges < 1.
    """
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacío")
    if num_merges < 1:
        raise ValueError("num_merges debe ser al menos 1")

    palabras = texto.split()
    corpus: list[list[str]] = [list(palabra) + ["</w>"] for palabra in palabras]
    historial_merges: list[dict] = []

    for paso in range(num_merges):
        pares: Counter = Counter()
        for palabra in corpus:
            for i in range(len(palabra) - 1):
                pares[(palabra[i], palabra[i + 1])] += 1

        if not pares:
            break

        par_a_fusionar, frecuencia = pares.most_common(1)[0]
        nuevo_token = par_a_fusionar[0] + par_a_fusionar[1]

        nuevo_corpus: list[list[str]] = []
        for palabra in corpus:
            nueva_palabra: list[str] = []
            i = 0
            while i < len(palabra):
                if (i < len(palabra) - 1 and
                        palabra[i] == par_a_fusionar[0] and
                        palabra[i + 1] == par_a_fusionar[1]):
                    nueva_palabra.append(nuevo_token)
                    i += 2
                else:
                    nueva_palabra.append(palabra[i])
                    i += 1
            nuevo_corpus.append(nueva_palabra)

        historial_merges.append({
            "paso": paso + 1,
            "par_fusionado": f"{par_a_fusionar[0]} + {par_a_fusionar[1]}",
            "nuevo_token": nuevo_token,
            "frecuencia": frecuencia,
            "ejemplo_antes": " ".join(corpus[0]),
            "ejemplo_despues": " ".join(nuevo_corpus[0]),
        })
        corpus = nuevo_corpus

    todos_los_tokens: list[str] = []
    for palabra in corpus:
        todos_los_tokens.extend(palabra)

    vocabulario: dict[str, int] = {}
    for token in todos_los_tokens:
        if token not in vocabulario:
            vocabulario[token] = len(vocabulario)

    return {
        "metodo": "BPE Simulado",
        "texto_original": texto,
        "num_merges_realizados": len(historial_merges),
        "tokens": todos_los_tokens,
        "token_ids": [vocabulario[t] for t in todos_los_tokens],
        "num_tokens": len(todos_los_tokens),
        "vocabulario_size": len(vocabulario),
        "vocabulario": vocabulario,
        "historial_merges": historial_merges,
    }


def comparar_metodos(texto: str, num_merges: int = 15) -> list[dict]:
    """Compara los tres métodos de tokenización sobre el mismo texto.

    Args:
        texto: Texto a tokenizar con cada método.
        num_merges: Número de merges para BPE.

    Returns:
        Lista con resumen de cada método.
    """
    metodos = [
        tokenizar_por_palabras(texto),
        tokenizar_por_caracteres(texto),
        tokenizar_bpe_simulado(texto, num_merges),
    ]
    return [{
        "metodo": m["metodo"],
        "num_tokens": m["num_tokens"],
        "vocabulario_size": m["vocabulario_size"],
        "primeros_5_tokens": m["tokens"][:5],
        "ratio_chars_token": round(len(texto) / m["num_tokens"], 2),
    } for m in metodos]


# ═══════════════════════════════════════════════════════════════
# PARTE 2: EMBEDDINGS CON TF-IDF
# ═══════════════════════════════════════════════════════════════

def calcular_similitud(frases: list[str]) -> dict:
    """Calcula embeddings TF-IDF y similitud coseno entre frases.

    TF-IDF convierte texto en vectores numéricos donde cada dimensión
    representa la importancia de un término en el documento relativo
    al corpus. La similitud coseno mide el ángulo entre vectores:
    1.0 = idénticos, 0.0 = sin relación.

    Args:
        frases: Lista de frases a comparar (mínimo 2).

    Returns:
        Diccionario con vectores, matriz de similitud y pares ordenados.

    Raises:
        ValueError: Si hay menos de 2 frases.
    """
    if len(frases) < 2:
        raise ValueError("Se necesitan al menos 2 frases para comparar")

    vectorizer = TfidfVectorizer(lowercase=True, max_features=1000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(frases)
    sim_matrix = cosine_similarity(tfidf_matrix)

    pares: list[dict] = []
    for i in range(len(frases)):
        for j in range(i + 1, len(frases)):
            pares.append({
                "indice_a": i, "indice_b": j,
                "frase_a": frases[i], "frase_b": frases[j],
                "similitud": round(float(sim_matrix[i][j]), 4),
            })
    pares.sort(key=lambda x: x["similitud"], reverse=True)

    feature_names = vectorizer.get_feature_names_out()
    top_palabras: list[list[str]] = []
    for i in range(len(frases)):
        row = tfidf_matrix[i].toarray()[0]
        top_indices = row.argsort()[-5:][::-1]
        top_palabras.append([feature_names[idx] for idx in top_indices if row[idx] > 0])

    return {
        "frases": frases,
        "dimensiones": tfidf_matrix.shape,
        "vocabulario_size": len(vectorizer.vocabulary_),
        "matriz_similitud": sim_matrix.round(4).tolist(),
        "pares": pares,
        "top_palabras_por_frase": top_palabras,
    }


# ═══════════════════════════════════════════════════════════════
# PARTE 3: VISUALIZACIÓN 2D
# ═══════════════════════════════════════════════════════════════

def visualizar_embeddings_2d(frases: list[str]) -> dict:
    """Reduce embeddings TF-IDF a 2D con SVD para visualización.

    Args:
        frases: Lista de frases a representar en 2D.

    Returns:
        Diccionario con coordenadas 2D y varianza explicada.
    """
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(frases)

    n_components = min(2, tfidf_matrix.shape[1])
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    coords = svd.fit_transform(tfidf_matrix)

    puntos: list[dict] = []
    for i, frase in enumerate(frases):
        etiqueta = frase[:45] + ("..." if len(frase) > 45 else "")
        puntos.append({
            "frase": etiqueta,
            "x": round(float(coords[i][0]), 4),
            "y": round(float(coords[i][1]), 4) if n_components > 1 else 0.0,
        })

    return {
        "varianza_explicada": [round(float(v), 4) for v in svd.explained_variance_ratio_],
        "puntos": puntos,
    }


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── DEMO 1: Tokenización por palabras ──
    print("=" * 70)
    print("PARTE 1a: TOKENIZACIÓN POR PALABRAS")
    print("=" * 70)

    texto_demo = "La inteligencia artificial generativa está transformando la programación."
    rp = tokenizar_por_palabras(texto_demo)

    print(f"\nTexto: \"{texto_demo}\"")
    print(f"Tokens ({rp['num_tokens']}): {rp['tokens']}")
    print(f"IDs:    {rp['token_ids']}")
    print(f"Vocabulario ({rp['vocabulario_size']} tokens únicos)")

    # ── DEMO 2: Tokenización por caracteres ──
    print("\n" + "=" * 70)
    print("PARTE 1b: TOKENIZACIÓN POR CARACTERES")
    print("=" * 70)

    rc = tokenizar_por_caracteres(texto_demo)
    print(f"\nTexto: \"{texto_demo}\"")
    print(f"Tokens ({rc['num_tokens']}): {rc['tokens'][:20]}...")
    print(f"Vocabulario ({rc['vocabulario_size']} caracteres únicos)")

    # ── DEMO 3: BPE simulado ──
    print("\n" + "=" * 70)
    print("PARTE 1c: BYTE PAIR ENCODING (BPE) — SIMULACIÓN PASO A PASO")
    print("=" * 70)

    texto_bpe = "la programación de inteligencia artificial es la nueva programación"
    rb = tokenizar_bpe_simulado(texto_bpe, num_merges=12)

    print(f"\nTexto: \"{texto_bpe}\"")
    print(f"\nProceso BPE — {rb['num_merges_realizados']} fusiones:")
    print(f"{'Paso':>4}  {'Par fusionado':<20} {'Nuevo token':<15} {'Freq':>4}")
    print("-" * 50)
    for m in rb["historial_merges"]:
        print(f"{m['paso']:>4}  {m['par_fusionado']:<20} {m['nuevo_token']:<15} {m['frecuencia']:>4}")

    print(f"\nTokens finales ({rb['num_tokens']}): {rb['tokens']}")

    # ── DEMO 4: Comparativa ──
    print("\n" + "=" * 70)
    print("PARTE 1d: COMPARATIVA DE MÉTODOS")
    print("=" * 70)

    texto_comp = "La inteligencia artificial y la programación están transformando el mundo de la tecnología"
    comp = comparar_metodos(texto_comp, num_merges=15)

    print(f"\nTexto ({len(texto_comp)} chars): \"{texto_comp}\"\n")
    print(f"{'Método':<15} {'Tokens':>8} {'Vocab':>8} {'Ratio':>8}  {'Primeros 5'}")
    print("-" * 75)
    for m in comp:
        print(f"{m['metodo']:<15} {m['num_tokens']:>8} {m['vocabulario_size']:>8} {m['ratio_chars_token']:>8}  {m['primeros_5_tokens']}")

    print("\n  → BPE logra el equilibrio óptimo entre vocabulario y longitud de secuencia.")
    print("    Por eso GPT, Claude y la mayoría de LLMs usan variantes de BPE.")

    # ── DEMO 5: Embeddings ──
    print("\n" + "=" * 70)
    print("PARTE 2: EMBEDDINGS Y SIMILITUD SEMÁNTICA (TF-IDF)")
    print("=" * 70)

    frases_demo = [
        "Python es un lenguaje de programación muy popular",
        "Python es uno de los lenguajes más usados en el mundo",
        "Me gusta programar en Python y JavaScript",
        "El clima de Madrid es cálido en verano",
        "La temperatura en verano en Madrid es alta",
        "Los gatos son animales domésticos independientes",
    ]

    print("\nFrases:")
    for i, f in enumerate(frases_demo):
        print(f"  [{i}] {f}")

    sr = calcular_similitud(frases_demo)

    print(f"\nDimensiones del espacio vectorial: {sr['dimensiones']}")
    print(f"\nPalabras más representativas por frase:")
    for i, (f, p) in enumerate(zip(frases_demo, sr["top_palabras_por_frase"])):
        print(f"  [{i}] {', '.join(p[:4])}")

    print(f"\nMatriz de similitud:")
    print("      " + "".join(f"  [{i}]  " for i in range(len(frases_demo))))
    for i, row in enumerate(sr["matriz_similitud"]):
        print(f"  [{i}] " + "".join(f" {v:.3f} " for v in row))

    print("\nTop 5 pares más similares:")
    for par in sr["pares"][:5]:
        barra = "█" * int(par["similitud"] * 30)
        print(f"  {par['similitud']:.4f} {barra}")
        print(f"         [{par['indice_a']}] ↔ [{par['indice_b']}]")

    # ── DEMO 6: Visualización 2D ──
    print("\n" + "=" * 70)
    print("PARTE 3: VISUALIZACIÓN 2D DE EMBEDDINGS")
    print("=" * 70)

    viz = visualizar_embeddings_2d(frases_demo)
    print(f"\nVarianza explicada: {viz['varianza_explicada']}")
    print("\nCoordenadas 2D:")
    for p in viz["puntos"]:
        print(f"  ({p['x']:>7.4f}, {p['y']:>7.4f})  {p['frase']}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("TESTS:")
    print("=" * 70)

    # Test 1
    r = tokenizar_por_palabras("Hola mundo")
    assert r["tokens"] == ["Hola", "mundo"] and r["num_tokens"] == 2
    print("  [PASS] Test 1: Tokenización por palabras básica")

    # Test 2
    r = tokenizar_por_palabras("¡Hola, mundo!")
    assert "Hola" in r["tokens"] and "," in r["tokens"]
    print("  [PASS] Test 2: Puntuación separada como tokens")

    # Test 3
    r = tokenizar_por_caracteres("ABC")
    assert r["tokens"] == ["A", "B", "C"] and r["vocabulario_size"] == 3
    print("  [PASS] Test 3: Tokenización por caracteres")

    # Test 4
    r = tokenizar_bpe_simulado("ab ab ab cd", num_merges=1)
    assert "a" in r["historial_merges"][0]["par_fusionado"]
    print("  [PASS] Test 4: BPE fusiona par más frecuente primero")

    # Test 5
    r1 = tokenizar_bpe_simulado("la la la programación", num_merges=1)
    r5 = tokenizar_bpe_simulado("la la la programación", num_merges=5)
    assert r5["num_tokens"] <= r1["num_tokens"]
    print("  [PASS] Test 5: Más merges BPE = menos tokens")

    # Test 6
    for fn in [tokenizar_por_palabras, tokenizar_por_caracteres, tokenizar_bpe_simulado]:
        try:
            fn("")
            assert False
        except ValueError:
            pass
    print("  [PASS] Test 6: ValueError con texto vacío (3 métodos)")

    # Test 7
    comp = comparar_metodos("Hola mundo de la IA")
    assert len(comp) == 3
    print("  [PASS] Test 7: Comparativa devuelve 3 métodos")

    # Test 8
    sim = calcular_similitud(["Python es genial", "Python es genial", "El mar es azul"])
    assert sim["matriz_similitud"][0][1] == 1.0
    print("  [PASS] Test 8: Frases idénticas → similitud 1.0")

    # Test 9
    sim = calcular_similitud([
        "Python es un lenguaje de programación",
        "Java es un lenguaje de programación",
        "Los gatos duermen mucho",
    ])
    assert sim["matriz_similitud"][0][1] > sim["matriz_similitud"][0][2]
    print("  [PASS] Test 9: Frases relacionadas > frases sin relación")

    # Test 10
    try:
        calcular_similitud(["solo una"])
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 10: ValueError con menos de 2 frases")

    # Test 11
    viz = visualizar_embeddings_2d(["Frase uno", "Frase dos", "Frase tres"])
    assert len(viz["puntos"]) == 3 and all("x" in p and "y" in p for p in viz["puntos"])
    print("  [PASS] Test 11: Visualización 2D genera coordenadas válidas")

    # Test 12
    sim = calcular_similitud(["Python es genial para IA", "Java es bueno para web"])
    assert all(len(tp) > 0 for tp in sim["top_palabras_por_frase"])
    print("  [PASS] Test 12: Top palabras por frase no vacío")

    print("\n  Todos los tests pasaron correctamente.")
