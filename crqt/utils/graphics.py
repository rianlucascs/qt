import plotly.graph_objects as go

class Graphic:

    def __init__(self, data, x='Date', y=['adj_close', 'retorno_modelo']):
        self.data = data
        self.x = x
        self.y = y
    
    def update_layout(self, fig):
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            ),
            yaxis=dict(
                title=self.y[0],
                titlefont=dict(color="#1f77b4"),
                tickfont=dict(color="#1f77b4")
            ),
            yaxis2=dict(
                title=self.y[1],
                titlefont=dict(color="#ff7f0e"),
                tickfont=dict(color="#ff7f0e"),
                overlaying='y',
                side='right'
            ),
            showlegend=True
        )
    
    def scale(self):
        fig = go.Figure()
        
        # Adicionando a primeira série no primeiro eixo y (esquerdo)
        fig.add_trace(go.Scatter(x=self.data[self.x], y=self.data[self.y[0]], mode='lines', name=self.y[0]))
        
        # fig.add_trace(go.Scatter(x=self.data[self.x], y=self.data[self.y[2]], mode='lines', name=self.y[2]))
        
        # Adicionando a segunda série no segundo eixo y (direito)
        fig.add_trace(go.Scatter(x=self.data[self.x], y=self.data[self.y[1]], mode='lines', name=self.y[1], yaxis='y2'))

        self.update_layout(fig)
        fig.show()