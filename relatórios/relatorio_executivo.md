# 📊 Relatório Executivo, Análise do Mercado de Trabalho Global
**Dataset:** I2D2 / World Bank Labor Market Database  
**Período:** 1970 – 2021 | **Países:** 168 | **Observações:** 14.628 | **Variáveis:** 103  
**Projeto:** Ciências de Dados

---

## 1. Resumo Executivo

Este relatório apresenta uma análise exploratória completa do mercado de trabalho global, com base no dataset harmonizado do Banco Mundial (I2D2). A base cobre 168 países, 9 subamostras demográficas (total, gênero, faixa etária, nível educacional e zona geográfica), e mais de 50 anos de dados. Os principais achados revelam profundas desigualdades estruturais entre regiões e grupos de renda, com tendências positivas, mas desiguais, na participação feminina e na queda da informalidade.

---

## 2. Descrição do Dataset

| Dimensão | Detalhe |
|---|---|
| Tamanho | 14.628 linhas × 103 colunas |
| Granularidade | País × Ano × Subamostra |
| Subamostras | All, Male, Female, Young, Old, Low Education, High Education, Urban, Rural |
| Cobertura geográfica | 168 países, 7 regiões do Banco Mundial |
| Período | 1970 – 2021 |
| Grupos de renda | Low, Lower Middle, Upper Middle, High Income |

### Categorias de variáveis
- **Meta-dados:** país, região, renda, ano, fonte da pesquisa
- **Sociodemografia:** população por faixa etária, urbanização, dependência
- **Força de trabalho:** LFPR, desemprego, subutilização
- **Composição do emprego:** tipo (assalariado/autônomo/informal), setor, ocupação
- **Resultados:** salários (nominais, reais, PPP), horas trabalhadas, brechas de gênero
- **Educação:** escolaridade por nível, taxa de matrícula
- **Qualidade:** flags de qualidade dos dados de cada pesquisa

---

## 3. Qualidade dos Dados

- **6 variáveis** com mais de 50% de dados ausentes, principalmente indicadores de formalidade (contrato, saúde, previdência social) e dependência etária
- **70 variáveis** com cobertura superior a 70%, indicadores centrais bem preservados
- **17 variáveis** sem nenhum dado ausente, variáveis de meta-dados e estrutura

> ⚠️ A análise foi conduzida com a subamostra "All" (n=1.790), que representa os indicadores agregados por país/ano sem desagregação adicional.

---

## 4. Principais Insights

### 4.1 Participação no Mercado de Trabalho (LFPR)

- A LFPR global mediana cresceu de **~61% (1970)** para **~70% (2010)**, com leve recuo após 2015
- Países de **baixa renda** têm LFPR mais alta (77%) que os de alta renda (71%), resultado da necessidade econômica, não de oportunidade
- A LFPR **feminina** saltou de 38% para 61% entre 1970 e 2010, sinalizando um dos progressos mais significativos do período
- O recuo pós-2015 reflete envelhecimento populacional e maior taxa de inatividade voluntária em países ricos

### 4.2 Brecha de Gênero, A Maior Desigualdade Estrutural

| Região | Brecha M−F na LFPR (pp) |
|---|---|
| Oriente Médio & N. África | 52 pp |
| Sul da Ásia | 43 pp |
| América Latina | 30 pp |
| Leste Asiático | 21 pp |
| Europa & Ásia Central | 14 pp |
| América do Norte | 12 pp |
| África Subsaariana | 10 pp |

- A brecha no **Oriente Médio** é mais de 5× maior que na África Subsaariana
- A razão salarial F/M mediana global é de **0,80**, mulheres ganham 80% do salário masculino
- Países de renda média apresentam brechas salariais **maiores** que os de baixa renda, possivelmente porque o setor formal é mais amplo e mensurável naqueles

### 4.3 Informalidade, Desafio Concentrado no Sul Global

| Região | Informalidade mediana |
|---|---|
| África Subsaariana | 88% |
| Sul da Ásia | 85% |
| América Latina | 60% |
| Oriente Médio | 57% |
| Europa & Ásia Central | 47% |
| Leste Asiático | 35% |

- Países de **baixa renda**: 92% de informalidade mediana
- Países de **alta renda**: 38%, inclui trabalho autônomo de alta qualidade
- Correlação negativa significativa com educação pós-secundária: **r = −0,41** (Spearman)
- Reduzir informalidade passa, em grande medida, por ampliar acesso à educação superior

### 4.4 Desemprego, O Paradoxo dos Jovens em Países Ricos

- Taxa de desemprego jovem (15-24) é **2 a 4× maior** que a adulta em quase todas as regiões
- Países de **baixa renda**: desemprego jovem mediano de apenas 4,7%, reflexo de mercados de trabalho com pouca proteção social, onde trabalhar é necessidade imediata
- Países de **alta renda**: desemprego jovem de 19%, jovens aguardam posições adequadas ao investimento educacional feito
- A taxa de **NEET** (nem em emprego, nem em educação) é mais preocupante em países de baixa e média renda

### 4.5 Transformação Estrutural, Saída da Agricultura

- Queda consistente do emprego agrícola: de ~50% global em 1970 para ~25% em 2020
- Em países de **baixa renda**: 67% do emprego ainda está na agricultura
- Em países de **alta renda**: apenas 4%, com amplo domínio de serviços (>70%)
- A velocidade dessa transição é um dos principais determinantes do desenvolvimento econômico

### 4.6 Correlações Estruturais Relevantes (Spearman)

| Par de Variáveis | r |
|---|---|
| Agricultura × Informalidade | +0,72 |
| Serviços × Educação Pós-Sec. | +0,68 |
| Edu. Pós-Sec. × Informalidade | −0,41 |
| Edu. Pós-Sec. × LFPR Feminina | +0,27 |
| Brecha Salarial F/M × LFPR Fem. | −0,18 |

---

## 5. Perguntas de Negócio Respondidas

1. **Quais regiões têm maior exclusão feminina do mercado de trabalho?** → Oriente Médio e Sul da Ásia
2. **Existe correlação entre educação e informalidade?** → Sim, r = −0,41; mais educação = menos informalidade
3. **A brecha salarial de gênero está diminuindo?** → Lentamente, especialmente nos países de alta renda
4. **O que diferencia o mercado de trabalho de países pobres e ricos?** → Informalidade, composição setorial e acesso à proteção social
5. **Quando jovens são mais vulneráveis ao desemprego?** → Em países de alta renda, paradoxalmente

---

## 6. Metodologia

- **Linguagem:** Python 3.12
- **Bibliotecas:** pandas, numpy, matplotlib, seaborn, scipy
- **Estratégia de análise:** Subamostra "All" como base; subamostras Male/Female para análises de gênero
- **Período de referência:** Todos os anos disponíveis (1970–2021)
- **Estatísticas centrais:** Mediana preferida à média para robustez a outliers
- **Correlações:** Spearman (dados não-normais confirmados por skewness > 1 em várias variáveis)

---

## 7. Limitações

- **Cobertura temporal desigual:** países de alta renda têm mais observações (5.040) vs. baixa renda (1.172)
- **Representatividade:** algumas pesquisas usam metodologias distintas entre países
- **Variáveis com alta ausência:** informality-related e proteção social têm cobertura limitada nos anos 1970–1990
- **Salários nominais:** não comparáveis diretamente entre países sem ajuste PPP (variável real disponível, mas com 40% de ausência)
- **Subnotificação:** dados de países em conflito ou com capacidade estatística limitada podem subestimar indicadores negativos

---

## 8. Recomendações

1. **Foco na inclusão feminina** em MEA e SAS: políticas de licença parental, creches e educação feminina têm os maiores retornos esperados em termos de LFPR
2. **Combate à informalidade** via expansão educacional e formalização gradual: a correlação com educação pós-secundária é a mais acionável
3. **Programas para jovens** em países de alta renda: o paradoxo do alto desemprego jovem em economias ricas demanda políticas ativas de inserção
4. **Monitoramento da transição agrícola** em países de baixa renda: velocidade e qualidade dos empregos criados nos setores industrial e de serviços é determinante
5. **Análise de sobrevivência** (Kaplan-Meier): próximo passo natural para medir tempo de transição entre empregos formais e informais

---

## 9. Próximos Passos

- [ ] Modelagem preditiva de informalidade com Random Forest + SHAP values
- [ ] Análise de cluster de países por perfil de mercado de trabalho (K-Means)
- [ ] Análise de convergência: países que mais avançaram em 20 anos
- [ ] Dashboard interativo em Power BI ou Tableau
- [ ] Integração com dados de PIB per capita e Gini (Banco Mundial API)
- [ ] Análise de impacto da pandemia COVID-19 (2020-2021)

---

## 10. Estrutura do Projeto GitHub

```
labor-market-global-eda/
│
├── data/
│   ├── raw/                        # Dataset original (.xlsx)
│   └── processed/                  # Dataset limpo (.parquet)
│
├── notebooks/
│   ├── 01_eda_labor_market.py      # EDA completa (este script)
│   ├── 02_feature_engineering.py  # Engenharia de features
│   └── 03_modeling.py             # Modelagem ML
│
├── reports/
│   ├── relatorio_executivo.md      # Este relatório
│   └── figures/                    # 8 gráficos gerados
│
├── requirements.txt
└── README.md
```

---

*Relatório gerado automaticamente pela pipeline de EDA. Análise realizada com dados públicos do Banco Mundial (I2D2 Database).*
