# BMEN

Base de conhecimento inicial do projeto **BMEN**.

## Fase 1 (v1.0)

Ontologia inicial com foco em:

- TEA
- TDAH
- Linguagem
- Ansiedade
- Sensorial

## Estrutura inicial

- `docs/` — documentação do projeto
- `data/` — dados e recursos
- `src/` — código-fonte

## Próximos passos

1. Definir esquema da ontologia
2. Adicionar fontes e referências
3. Versionar datasets iniciais
4. Implementar validações básicas

## Validação de dados da ontologia

```bash
python3 /home/runner/work/BMEN/BMEN/src/validate_ontology.py
```

O comando valida:

- estrutura e campos obrigatórios dos datasets JSON
- formato de identificadores e versão semântica
- referências cruzadas entre entidades, evidências e fontes
- consistência da matriz CSV e do manifesto de datasets
