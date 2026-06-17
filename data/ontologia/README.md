# Ontologia BMEN — Dados

Esta pasta contém os artefatos de dados da ontologia.

## Arquivos

- `bmen_v1.json`: estrutura inicial da ontologia (v1.0.0)
- `matriz_condicao_dominio_intervencao.csv`: matriz inicial de mapeamento condição × domínio × intervenção
- `schema.json`: JSON Schema para validação estrutural dos arquivos da ontologia
- `evidencias_fontes.json`: catálogo inicial de evidências e fontes

## Convenções

- IDs em `snake_case`
- `label` em PT-BR
- Versionamento semântico no campo `meta.version`

## Validação

Exemplo com Node.js + `ajv`:

```bash
npx ajv validate -s data/ontologia/schema.json -d data/ontologia/bmen_v1.json
```

## Evolução recomendada

1. Criar `bmen_v1_1.json` para mudanças compatíveis
2. Ligar `evidences` e `sources` diretamente às intervenções/afirmações
3. Adicionar catálogo mais amplo de sinais e avaliações
4. Incluir testes de validação no CI
