
# Scripts

> **crqt\scr1.py**

#### Visualizações, Resultados, Estratégia

- **Gráfico** - retorno estratégia X retorno ativo
- **Métricas**: Acurácia Treino, Acurácia Teste, Percentual Dias Positivo Total, Percentual Dias Positivo Teste, 
                  Dados Perdidos, Quantidade de sinais teste (venda, compra), Quantidade de sinais treino (venda, compra),
                  Quantidade de sinais total (venda, compra), Diferência (Acurácia treino - Acurácia teste),
                Média da série do retorno do modelo, Desvio padrão do retorno do modelo

# 

> **crqt\scr2.py**

#### Criação de dados, Estratégias

  - Gerar combinações númericas que representam variáveis (cálculos)
  - Processa essas combinações e armazena os resultados (metricas ***scr1.py*** )
  - Criação de diretórios dinâmico com base nos inputs (parametros)

# 

> **crqt\scr3.py**

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

> **crqt\scr4.py**

- Analise comportamento estratégias x preço ativo

  Não finalizado!

#

> **crqt\scr5.py**

#### Visualização, Filtro, Otimização

- Combina as variáveis (inputs) com todas as variáveis disponíveis em sequência
- Aplica filtro nas (metricas ***scr1.py*** ) e imprime os resultados

#

> **crqt\scr6.py**

#### Visualização, Risco

- Define a quantidade de contratos (lote) com base nos inputs
- **Inputs:** (Drawdrawn: maior prejuízo do modelo), (Projeção: número int que será multiplicador do drawdrawn), 
Prejuízo máximo esperado, Retorno mínimo esperado, Capital a ser alocado, Número de estratégias ativas, Último preço

-  **Cálculo do risco máximo esperado**: lote * preço * ((drawdrawn * projeção) / 100)

- **Outputs:** Lote, Prejuízo máximo esperado, Custo operacional, Média dos retonos baseada na quantidade de contratos, (Tabelas: retorno mensal e anual)

#

> **crqt\scr7.py**

#### Visualização, Estratégias

- **Resultados da combinção das estratégias**: Gráfico do retorno e DataFrames do retorno mensal e anual

#

### **Observações**: 

1° 

O acesso a cada variável é dado pelo número contido no nome da função

**Exemplo de feature**

    def feature157(m, t=5):
        W = lambda x, t=5: x.rolling(t).sum()
        Q = lambda x, t=5: x.rolling(t).std()
        R = lambda x, t=5: x.rolling(t).max()
        T = lambda x, t=5: x.rolling(t).min()
        E = lambda x, t=5: x.rolling(t).mean()
        Z = lambda x: ((W(m, 18) ** 3) / (Q(m, 8) ** 2))
        X = lambda x: (Z(m) + W(Z(m).shift(1), 13))
        C = lambda x: (R(X(m), 11) - X(m)) + (T(X(m), 3) - X(m))
        V = lambda x: m / abs(W(m * 2) - C(m))
        B = lambda x: (E(x, 13).diff() - x * Q(V(x))) / (1-V(x))
        N = lambda x: B(x) / (1 - abs(B(x) - (B(x) / X(x))))
        M = lambda x: x / abs(N(x) - (N(x) - W(N(x), 2)))
        return M(m)
- m = série do retorno do ativo
- t = parâmetro inicial das médias
- data[f157] = feature157(data['serie_retorno'])
