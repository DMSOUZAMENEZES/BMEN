# Guia de Contribuicao - BMEN

## Como adicionar um novo Conceito

### Passo 1: Identificar o conceito clinico

Defina o comportamento observavel que voce quer modelar. O conceito deve ser:
- Observavel por clinico, cuidador ou professor
- Mapeavel a um criterio diagnostico especifico
- Descrito em linguagem clinica precisa

### Passo 2: Criar o ID do conceito

Use a convencao: `{CONDICAO}_{CRITERIO}_{DOMINIO}_{NUMERO}`

Exemplos:
- `TEA_A1_SOC_001` - TEA, criterio A1, dominio social, primeiro conceito
- `TDAH_A1_DES_003` - TDAH, criterio A1, desatencao, terceiro conceito

### Passo 3: Adicionar em concepts.json

```json
{
  "id": "TEA_A1_SOC_001",
  "concept": "nome_do_conceito_em_snake_case",
  "label": "Nome Legivel do Conceito",
  "condition": "TEA",
  "criterion": "A1",
  "domain": "social",
  "weight": 10,
  "description": "Descricao clinica clara e objetiva",
  "age_relevant": "todos",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

### Passo 4: Adicionar aliases em aliases.json

```json
{
  "concept": "nome_do_conceito_em_snake_case",
  "condition": "TEA",
  "criterion": "A1",
  "aliases": [
    "expressao como cuidador descreveria",
    "outra forma de dizer o mesmo",
    "frase que pode aparecer na queixa"
  ]
}
```

### Passo 5: Vincular ao criterio na ontologia

No arquivo `ontology/{condicao}.json`, adicione o ID do conceito no array `concepts` do criterio correspondente.

---

## Convencoes de nomenclatura

| Campo | Convencao | Exemplo |
|-------|-----------|---------|
| concept | snake_case | `contato_visual_reduzido` |
| label | Title Case | `Contato Visual Reduzido` |
| condition | MAIUSCULAS | `TEA`, `TDAH` |
| criterion | Letra maiuscula + numero | `A1`, `B2` |

---

## Pesos dos conceitos (weight)

| Peso | Significado |
|------|-------------|
| 10 | Criterio patognomonico |
| 8-9 | Alta especificidade |
| 5-7 | Contribui para o quadro |
| 1-4 | Inespecifico, contexto dependente |

---

## Revisao pela Dra. Sinara

Todos os novos conceitos devem ser revisados pela Dra. Sinara antes do merge.
Abra uma Issue no GitHub descrevendo o conceito clinico e aguarde aprovacao.
