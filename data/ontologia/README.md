# Ontologia BMEN — Dados

Esta pasta contém os artefatos de dados da ontologia.

## Arquivos

- `bmen_v1.json`: estrutura inicial da ontologia (v1.0.0)
- `matriz_condicao_dominio_intervencao.csv`: matriz inicial de mapeamento condição × domínio × intervenção
- `schema.json`: JSON Schema versionável para a ontologia principal (classes, propriedades, IDs, namespaces e relações)
- `evidencias_fontes.json`: catálogo inicial de evidências e fontes
- `evidencias_fontes.schema.json`: JSON Schema para catálogo de evidências e fontes
- `datasets_manifest.json`: manifesto versionado dos datasets iniciais

## Convenções

- IDs em `snake_case`
- `label` em PT-BR
- Versionamento semântico no campo `meta.version`

## Validação

Validação automatizada (sem dependências externas):

```bash
python3 /home/runner/work/BMEN/BMEN/src/validate_ontology.py
```

Essa validação cobre:

1. Estrutura/formato dos datasets
2. Identificadores obrigatórios e padrão de IDs
3. Referências para entidades existentes
4. Consistência mínima entre JSON, CSV e manifesto

## Como contribuir com novas versões

1. Atualize o dataset alvo (`bmen_v1.json`, `evidencias_fontes.json` ou `matriz_condicao_dominio_intervencao.csv`)
2. Se houver mudança estrutural, atualize o schema correspondente
3. Atualize `datasets_manifest.json` com versão e metadados
4. Execute `python3 /home/runner/work/BMEN/BMEN/src/validate_ontology.py`
5. Submeta o PR incluindo fontes/referências para novos conceitos e relações

## Evolução recomendada

1. Criar `bmen_v1_1.json` para mudanças compatíveis
2. Ligar `evidences` e `sources` diretamente às intervenções/afirmações
3. Adicionar catálogo mais amplo de sinais e avaliações
4. Incluir testes de validação no CI
