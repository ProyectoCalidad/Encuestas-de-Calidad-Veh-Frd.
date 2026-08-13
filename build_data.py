"""
Convierte el Excel de BBDD (BBDD_Vehículo.xlsx) al archivo data.json
que usa el dashboard (index.html).

Uso:
    python3 build_data.py "BBDD_Vehículo.xlsx" data.json

Las columnas se toman por POSICIÓN (letra de Excel), no por nombre exacto,
porque algunos encabezados traen saltos de línea/emojis que son frágiles
para matchear por texto. Si el Excel cambia el orden de columnas, hay que
actualizar el diccionario COL_LETTERS de abajo.
"""
import sys
import json
import pandas as pd

# Letra de Excel -> nombre interno.
COL_LETTERS = {
    'B': 'mes',
    'G': 'avgAtencion',       # 1-5, nivel de satisfacción contacto con agente
    'H': 'comentario',        # texto libre "qué hicimos bien / en qué mejorar"
    'I': 'avgAgente',         # 1-5, satisfacción desempeño del agente
    'M': 'mejora',            # texto libre "qué faltó para experiencia excelente"
    'N': 'modelo',
    'P': 'tipoProblema',
    'Q': 'tipoMovil',
    'R': 'provincia',
    'T': 'satAtencion',
    'U': 'satAgente',
    'V': 'confianza',
    'W': 'recomendacion',
    'X': 'categoriaComentario',
    'Y': 'categoriaMejora',
    'J': 'resuelto',
    'Z': 'respondio',
    'AA': 'tramoDemora',
    'AB': 'tramoKm',
}


def col_idx(letter):
    """'A'->0, 'B'->1, ..., 'Z'->25, 'AA'->26, 'AB'->27"""
    n = 0
    for ch in letter:
        n = n * 26 + (ord(ch) - ord('A') + 1)
    return n - 1


def main(src, dst):
    df = pd.read_excel(src, header=0)
    n_cols_needed = max(col_idx(l) for l in COL_LETTERS) + 1
    if df.shape[1] < n_cols_needed:
        raise SystemExit(f"El Excel tiene {df.shape[1]} columnas, se esperaban al menos {n_cols_needed}.")

    out = pd.DataFrame()
    for letter, name in COL_LETTERS.items():
        out[name] = df.iloc[:, col_idx(letter)]

    # "¿Resolvimos su problema y/o consulta?" a veces trae texto libre
    # (ej. "A medias, el chofer no contaba con..."). Se normaliza a Si/No/Parcial.
    def norm_resuelto(v):
        if pd.isna(v):
            return None
        s = str(v).strip().lower()
        if s.startswith('si'):
            return 'Si'
        if s.startswith('no') and not s.startswith('no info'):
            return 'No'
        if s.startswith('a medias'):
            return 'Parcial'
        return 'Otro'
    out['resuelto'] = out['resuelto'].apply(norm_resuelto)

    # Mes -> "YYYY-MM"
    out['mes'] = pd.to_datetime(out['mes']).dt.strftime('%Y-%m')

    # Promedios numéricos: se dejan como número o None (nunca 0 por vacío)
    for c in ['avgAtencion', 'avgAgente']:
        out[c] = pd.to_numeric(out[c], errors='coerce')
        out[c] = out[c].where(out[c].notna(), None)

    # Limpieza de strings
    text_cols = ['modelo', 'provincia', 'tipoProblema', 'tipoMovil', 'tramoDemora', 'tramoKm',
                 'satAtencion', 'satAgente', 'confianza', 'recomendacion',
                 'respondio', 'comentario', 'mejora', 'categoriaComentario', 'categoriaMejora']
    for c in text_cols:
        out[c] = out[c].astype(str).str.strip()

    records = out.to_dict(orient='records')

    # Saneo final: cualquier variante de vacío -> None real (json.dump -> null, no NaN)
    EMPTY = {'nan', 'none', ''}
    for rec in records:
        for k, v in rec.items():
            if v is None:
                continue
            if isinstance(v, float) and v != v:  # NaN
                rec[k] = None
            elif isinstance(v, str) and v.strip().lower() in EMPTY:
                rec[k] = None

    with open(dst, 'w', encoding='utf-8') as f:
        json.dump({
            'generatedAt': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
            'records': records,
        }, f, ensure_ascii=False, indent=0)

    print(f"OK: {len(records)} registros escritos en {dst}")


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'BBDD_Vehículo.xlsx'
    dst = sys.argv[2] if len(sys.argv) > 2 else 'data.json'
    main(src, dst)
