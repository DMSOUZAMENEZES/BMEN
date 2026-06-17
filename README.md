# BMEN — Base de Modelagem do Espectro Neurodesenvolvimento

> Ontologia clinica para avaliacao e diagnostico diferencial em neurodesenvolvimento infantil.
> Desenvolvida para a clinica da Dra. Sinara.

---

## Estrutura do Repositorio

```
BMEN/
├── ontology/           # Ontologias por condicao clinica (DSM-5)
│   ├── tea.json        # Transtorno do Espectro Autista
│   ├── tdah.json       # Transtorno do Deficit de Atencao e Hiperatividade
│   ├── linguagem.json  # Transtornos de Linguagem e Comunicacao
│   └── ansiedade.json  # Transtornos de Ansiedade
│
├── concepts.json       # Dicionario Mestre de Conceitos Clinicos
├── aliases.json        # Aliases por conceito (como cuidadores descrevem)
│
├── evidence/           # Instrumentos de avaliacao e evidencias clinicas
├── differentials/      # Guias de diagnostico diferencial
├── docs/               # Documentacao e guias de contribuicao
└── schemas/            # JSON Schemas para validacao dos dados
```

---

## Filosofia

**Primeiro o ativo intelectual, depois a tecnologia.**

Esta base segue uma abordagem em fases:

- **Fase 1 (atual)** — Arquivos JSON no GitHub. Versionamento facil, revisao pela Dra. Sinara, sem custo, editavel por IA.
- **Fase 2** — Migracao para Supabase quando a ontologia estiver madura (TEA, TDAH, Linguagem, Sensorial, Ansiedade completos).
- **Fase 3** — BMEN Studio: interface para busca semantica de conceitos e aliases.
- **Fase 4** — Vetorizacao: embeddings + pgvector + busca semantica.

---

## Como funciona

Cada **conceito clinico** tem:

- Um **ID unico** no formato `CONDICAO_CRITERIO_DOMINIO_NUM`
- Um **peso** de 1 a 10 (especificidade diagnostica)
- **Aliases** — as formas como cuidadores, professores e pacientes descrevem o mesmo comportamento

**Exemplo:**

```json
{
  "concept": "contato_visual_reduzido",
  "condition": "TEA",
  "criterion": "A2",
  "weight": 10,
  "aliases": [
    "evita olhar nos olhos",
    "contato visual inconsistente",
    "olhar fugaz"
  ]
}
```

---

## Condicoes mapeadas

| Condicao | Criterios | Status |
|----------|-----------|--------|
| TEA | A1, A2, A3, B1, B2, B3, B4 | Em progresso |
| TDAH | A1 (Desatencao), A2 (Hiperatividade) | Em progresso |
| Linguagem | Expressivo, Receptivo, Pragmatico | Em progresso |
| Ansiedade | Separacao, Social, Generalizada | Em progresso |

---

## Contribuindo

Veja [docs/GUIA_DE_CONTRIBUICAO.md](docs/GUIA_DE_CONTRIBUICAO.md) para o processo completo.

Todos os novos conceitos requerem revisao da Dra. Sinara antes do merge.

---

*A BMEN sera muito mais valiosa do que qualquer GPT, fluxo ou aplicacao construida sobre ela.*
*E ela que se torna a propriedade intelectual do projeto.*
