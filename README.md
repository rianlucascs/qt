
# Arquivos

>crqt\scr1.py

#### Visualizações, Resultados, Estratégia

- **Gráfico** - retorno estratégia X retorno ativo
- **Métricas**: Acurácia Treino, Acurácia Teste, Percentual Dias Positivo Total, Percentual Dias Positivo Teste, 
                  Dados Perdidos, Quantidade de sinais teste (venda, compra), Quantidade de sinais treino (venda, compra),
                  Quantidade de sinais total (venda, compra), Diferência (Acurácia treino - Acurácia teste),
                Média da série do retorno do modelo, Desvio padrão do retorno do modelo

# 

> crqt\scr2.py

#### Criação de dados, Estratégias

  - Gerar combinações númericas que representam variáveis (cálculos)
  - Processa essas combinações e armazena os resultados (metricas ***scr1.py*** )
  - Criação de diretórios dinâmico com base nos inputs (parametros)

# 

> crqt\scr3.py

#### Criação de dados, Volatilidade, Ativos

  - Extrai métricas de todas as ações a vista da bolsa e armazena os resultados

  - **Metricas:** Média voltatilidade diária, média amplitude das sombras,
    Média amplitude sombras (Alta, Baixa),
    Percentual dias positivos (Alta, Baixa),
    Tamanho amostra,
    Último preço,
    Média volume,
    Média volume (notação científica),
    Desvio padrão do volume,
    (Média do volume ÷ Desvio padrão do volume)

# 

> crqt\scr4.py

- Analise comportamento estratégias x preço ativo

  Não finalizado!

#

> crqt\scr5.py

#### Visualização, Filtro, Otimização

- Combina as variáveis (inputs) com todas as variáveis disponíveis em sequência
- Aplica filtro nas (metricas ***scr1.py*** ) e imprime os resultados

#

> crqt\scr6.py

#### Visualização, Risco

- Define a quantidade de contratos (lote) com base nos inputs
- **Inputs:** (Drawdrawn: maior prejuízo do modelo), (Projeção: número int que será multiplicador do drawdrawn), 
Prejuízo máximo esperado, Retorno mínimo esperado, Capital a ser alocado, Número de estratégias ativas, Último preço

-  **Cálculo do risco máximo esperado**: lote * preço * ((drawdrawn * projeção) / 100)

- **Outputs:** Lote, Prejuízo máximo esperado, Custo operacional, Média dos retonos baseada na quantidade de contratos, (Tabelas: retorno mensal e anual)

#

> crqt\scr7.py

#### Visualização, Estratégias

- **Resultados da combinção das estratégias**: Gráfico do retorno e DataFrames do retorno mensal e anual

#