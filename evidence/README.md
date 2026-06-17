# Evidence

Pasta para armazenar evidencias clinicas e instrumentos de avaliacao que embasam os conceitos da BMEN.

## Estrutura

Cada arquivo JSON nesta pasta representa um instrumento ou conjunto de evidencias:

- `ados2.json` - Autism Diagnostic Observation Schedule, 2nd Edition
- `m-chat.json` - Modified Checklist for Autism in Toddlers
- `snap-iv.json` - Swanson, Nolan and Pelham Rating Scale (TDAH)
- `conners.json` - Escalas de Conners para TDAH
- `preschool-language.json` - Escalas de avaliacao de linguagem

## Formato

```json
{
  "id": "INSTRUMENTO_001",
  "name": "Nome do Instrumento",
  "type": "observational|interview|rating_scale|neuropsychological",
  "conditions": ["TEA", "TDAH"],
  "age_range": { "min": 2, "max": 16 },
  "items": [],
  "references": []
}
```
