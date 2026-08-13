# Panel de Satisfacción — Ford Assistance

## Qué incluye

- `index.html` → el panel que ve el cliente (público, sin login).
- `data.json` → los datos que alimentan el panel (generado a partir de tu Excel).
- `actualizar.html` → herramienta para generar el `data.json` nuevo cada mes, sin instalar nada.
- `logo.png` → logo de Cardinal Assistance, en el encabezado.
- `ford-logo.png` → logo de Ford, en el encabezado.
- `chart.umd.min.js` → librería de gráficos, alojada localmente (no depende de internet externo).
- `xlsx.full.min.js` → librería que usa `actualizar.html` para leer el Excel, también local.
- `build_data.py` → alternativa por línea de comandos (Python) para generar `data.json`, opcional.

El panel **no tiene backend ni base de datos**: es un archivo HTML que lee `data.json`
al abrirse. Por eso hay que resubir `data.json` cada vez que haya datos nuevos.

## 1. Publicarlo (una sola vez)

La forma más simple y gratuita es **GitHub Pages**:

1. Creá una cuenta en [github.com](https://github.com) si no tenés una.
2. Creá un repositorio nuevo (puede ser público), por ejemplo `panel-ford-assistance`.
3. Subí los 7 archivos (todos menos `build_data.py`, que es opcional) a la raíz del repositorio.
4. Andá a **Settings → Pages**, en "Source" elegí la rama `main` y carpeta `/ (root)`. Guardar.
5. En un minuto te da un link tipo `https://tu-usuario.github.io/panel-ford-assistance/` — ese es el que compartís con el cliente. No necesita cuenta ni login para abrirlo.

## 2. Actualizarlo cada mes

1. Abrí `actualizar.html` en tu navegador (doble clic, no necesita internet ni instalar nada) — tiene que estar guardado en la misma carpeta que `xlsx.full.min.js`.
2. Arrastrá ahí el Excel de BBDD del mes (mismo formato que siempre).
3. Descargá el `data.json` que te genera.
4. Reemplazá el archivo `data.json` en tu repositorio/hosting por este nuevo (mismo nombre).
5. Listo — el link del panel ya muestra los datos actualizados. No hay que tocar ningún otro archivo.

En GitHub, reemplazar el archivo es: "Add file" → "Upload files" → arrastrar el `data.json`
nuevo (te pregunta si reemplazar el existente, confirmar que sí) → Commit changes.

## 3. Qué muestra el panel

**5 indicadores clave (KPI):**
- Resolución del Problema (% "Sí")
- Satisfacción de Atención (promedio 1-5 de la columna G + % equivalente, y debajo el desglose por categoría)
- Satisfacción con Desempeño del Agente (promedio 1-5 de la columna I + % equivalente, y desglose)
- Confianza en Ford (% "Confío")
- Nivel de Respuesta (% de casos con encuesta respondida, total o parcial)

**8 gráficos:**
1. Nivel de Recomendación (NPS + cantidad y % por Promotor/Neutral/Detractor)
2. NPS por Modelo (% por modelo, 100% apilado, con etiquetas)
3. Ranking por Modelo (%, con etiquetas)
4. Ranking por Provincia (cantidad de casos)
5. Ranking por Tipo de Problema (%, con etiquetas)
6. Ranking por Tiempo de Arribo (cantidad, por tramo de demora)
7. Ranking por Tipo de Servicio (%, tipo de móvil asignado, con etiquetas)
8. Ranking por Kilometraje (%, con etiquetas)

**Comentarios de clientes (al pie, debajo de los gráficos):**
- Comentarios de la encuesta, agrupados por categoría (columna X), mostrando el texto de la columna H.
- Sugerencias de mejora, agrupadas por categoría (columna Y), mostrando el texto de la columna M.
- Ambos respetan los filtros de arriba (si filtrás por mes, se actualizan solos).

**Filtros (arriba, en el encabezado):** Mes, Modelo, Provincia — combinables entre sí,
afectan a los KPIs, los 8 gráficos y los comentarios a la vez.

**Modo claro/oscuro:** botón ☀️/🌙 arriba a la derecha. La preferencia queda guardada
en el navegador para la próxima visita.

## Notas

- La columna "¿Resolvimos su problema?" a veces trae texto libre (ej. "A medias, ...");
  el conversor lo normaliza automáticamente a Si / No / Parcial.
- Los promedios de satisfacción (G, I) solo se calculan sobre encuestas respondidas —
  nunca se promedia sobre celdas vacías.
- Los colores combinan la paleta de Cardinal (verde azulado, naranja, rosa) para las
  categorías de datos, con el azul institucional de Ford en el encabezado y los gráficos
  principales.
- Todas las librerías externas (gráficos, lectura de Excel) están alojadas localmente
  dentro del repositorio, no dependen de conexión a servicios externos — así se evita el
  problema de la red corporativa bloqueando esos dominios.
