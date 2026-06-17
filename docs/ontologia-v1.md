# Ontologia BMEN v1.0 — Fase 1

## Objetivo

Definir uma ontologia inicial para organizar conhecimento sobre neurodesenvolvimento e saúde mental em contexto educacional/clínico, com foco em:

- TEA
- TDAH
- Linguagem
- Ansiedade
- Sensorial

## Escopo desta versão

Esta versão (v1.0) prioriza:

1. Estrutura conceitual mínima e consistente
2. Relações principais entre conceitos
3. Campos para evidências e fontes
4. Base para expansão incremental (v1.1+)

## Modelo conceitual (alto nível)

### Entidades principais

- `Condition` (Condição)
- `Domain` (Domínio funcional)
- `Profile` (Perfil individual)
- `Sign` (Sinal observado)
- `Intervention` (Intervenção)
- `Assessment` (Avaliação)
- `Outcome` (Desfecho)
- `Evidence` (Evidência)
- `Source` (Fonte)

### Domínios funcionais (Fase 1)

- Comunicação/Linguagem
- Atenção/Funções executivas
- Regulação emocional
- Processamento sensorial
- Interação social

## Classes iniciais

### 1) Condition

Representa uma condição clínica ou constructo-alvo.

Campos recomendados:

- `id` (string, único)
- `label` (string)
- `aliases` (string[])
- `description` (string)
- `category` (ex.: neurodesenvolvimento, ansiedade)
- `severity_levels` (string[] opcional)
- `references` (Source[])

Instâncias base:

- `TEA`
- `TDAH`
- `TranstornoAnsiedade`

---

### 2) Domain

Representa áreas funcionais impactadas.

Campos:

- `id`
- `label`
- `description`

Instâncias base:

- `Linguagem`
- `AtencaoExecutivo`
- `RegulacaoEmocional`
- `Sensorial`
- `InteracaoSocial`

---

### 3) Sign

Sinal observável/relatável, não necessariamente diagnóstico isolado.

Campos:

- `id`
- `label`
- `description`
- `observable_in` (contextos)
- `related_domains` (Domain[])

Exemplos:

- hipersensibilidade_a_som
- dificuldade_manutencao_foco
- ecolalia
- inquietacao_motora
- evitacao_social

---

### 4) Assessment

Instrumento/procedimento de avaliação.

Campos:

- `id`
- `label`
- `type` (triagem, clínica, observacional)
- `target_domains` (Domain[])
- `age_range` (opcional)
- `references`

---

### 5) Intervention

Ação ou estratégia de suporte/intervenção.

Campos:

- `id`
- `label`
- `type` (educacional, terapêutica, ambiental)
- `target_domains`
- `indications` (Condition[]/Sign[])
- `contraindications` (opcional)
- `expected_outcomes` (Outcome[])
- `references`

---

### 6) Profile

Representa o perfil individual longitudinal.

Campos:

- `id`
- `age`
- `context` (escola, clínica, casa)
- `conditions` (Condition[])
- `signs` (Sign[])
- `assessments` (Assessment[])
- `interventions` (Intervention[])
- `outcomes` (Outcome[])
- `updated_at`

---

### 7) Outcome

Desfecho mensurável ou qualitativo.

Campos:

- `id`
- `label`
- `metric_type` (quantitativo/qualitativo)
- `measurement_window`
- `value`
- `interpretation`

---

### 8) Evidence e Source

Evidência conectada a afirmações/estratégias.

`Evidence`:

- `id`
- `statement`
- `level` (baixo, moderado, alto)
- `sources` (Source[])

`Source`:

- `id`
- `title`
- `authors`
- `year`
- `url_or_doi`
- `notes`

## Relações principais

- `Condition affects Domain`
- `Condition associated_with Sign`
- `Assessment evaluates Domain`
- `Intervention targets Domain`
- `Intervention indicated_for Condition/Sign`
- `Intervention produces Outcome`
- `Evidence supports Intervention/Statement`
- `Profile has Condition/Sign/Assessment/Intervention/Outcome`

## Regras de modelagem (v1.0)

1. IDs em `snake_case`, estáveis e únicos.
2. `label` em PT-BR; aliases opcionais em EN.
3. Toda intervenção deve ter ao menos 1 domínio-alvo.
4. Toda afirmação técnica deve apontar para pelo menos 1 fonte (quando disponível).
5. Evitar inferências diagnósticas automáticas sem avaliação formal.

## Exemplo de fluxo

1. Registrar sinais observados no `Profile`
2. Associar domínios impactados
3. Selecionar avaliações pertinentes
4. Definir intervenções por domínio
5. Monitorar desfechos em janela temporal
6. Revisar plano com base em evidências

## Governança e versão

- Versão atual: `1.0.0`
- Tipo de evolução:
  - PATCH: correções textuais/metadata
  - MINOR: novos conceitos/relacionamentos compatíveis
  - MAJOR: mudanças incompatíveis no esquema

## Próximas entregas (v1.1)

- Matriz condição × domínio × intervenção
- Vocabulário controlado de sinais
- Templates de avaliação por faixa etária
- SHACL/JSON Schema para validação automática
