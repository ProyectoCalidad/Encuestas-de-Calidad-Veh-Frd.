# Panel de Resultados de Encuesta — Ford Assistance

## Archivos del repositorio (GitHub)

- `index.html` → el panel que ve el cliente (link público).
- `data.json` → los datos del panel. Se reemplaza cada mes. No tiene nombre, patente ni póliza.
- `actualizar.html` → herramienta de la entrega mensual (arma los 3 archivos).
- `logo.png`, `ford-logo.png` → logos del encabezado.
- `chart.umd.min.js` → librería de gráficos (alojada local).
- `xlsx.full.min.js` → librería para leer/escribir Excel (alojada local).

## Entrega mensual

1. Abrí `actualizar.html` **desde el link publicado** (no con doble clic). Así puede leer los demás archivos para armar el HTML.
2. Cargá la BBDD (hoja acumulada con todos los meses). Se procesa en tu navegador; no se sube a ningún lado.
3. Descargá los tres archivos:
   - `data.json` → **es el único que va a GitHub** (Add file → Upload files; confirmá que reemplaza al existente).
   - `Panel_Resultados_Ford_Assistance_AAAA-MM.html` → panel en un solo archivo, se abre sin internet.
   - `Detalle_encuestas_Ford_Assistance_AAAA-MM.xlsx` → detalle por encuesta, con nombre, patente y póliza. **No subir a GitHub.**
4. Si la herramienta muestra avisos (recuadro naranja), revisalos antes de entregar.

Los .html suelen ser bloqueados como adjunto en el correo: conviene mandarlo comprimido (.zip).

## Cómo lee la BBDD

- Las columnas se buscan **por nombre de encabezado**, no por letra: se pueden agregar o mover columnas.
- "Tipo de Problema" también se acepta como "Nombre de la Urgencia".
- Si falta una columna obligatoria, la herramienta lo informa y no genera nada.

## Reglas de normalización

- **RESPONDIO?**: texto con "NO RESPOND" → No respondió; con "PARCIAL" → Parcial; cualquier otro texto → Completa (si no lo reconoce, avisa).
- **Recomendación**: "No Recomendaría" o "Detractor" → Detractor; Promotor; Neutral.
- **Provincia** con valor 0 → se trata como vacío.
- **Modelos** agrupados por familia: Ranger, Territory, Maverick, Transit, Kuga, Everest y F-150 (incluye "FORD V8"). Un modelo nuevo queda con su nombre y la herramienta avisa. Para sumarlo a una familia, editar `FAMILIAS_MODELO` al inicio del bloque de lógica de `actualizar.html`.

## Qué calcula el panel

- Los "Ranking por…" se calculan solo sobre encuestas Completas + Parciales, y muestran únicamente %.
- Los promedios 1-5 (atención y desempeño del agente) se calculan solo sobre respuestas no vacías.
- "NPS por Modelo" lista solo modelos con al menos una recomendación respondida.
- En comentarios, "Sin categorizar" va siempre al final.

## Detalle en Excel (columnas)

Orden de Servicio · N° de Póliza · Asegurado · Patente · Fecha de Servicio · Fecha de Encuesta · Estado de Encuesta · Modelo · Versión · Provincia · Tipo de Problema · Demora (min) · Atención (1-5) · Desempeño del agente (1-5) · ¿Resolvimos su problema? · Confianza (1-5) · Recomendación · Comentario · Qué faltó para una experiencia excelente.

Sale con anchos de columna y filtro automático (sin colores).
