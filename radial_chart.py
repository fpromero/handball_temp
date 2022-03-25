import plotly.graph_objects as go
def plot_radial_chart(df, categories, name="Player"):
  fig = go.Figure()
  for i, row in df.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=row[categories].values,
        theta=categories,
        #fill='toself',
        name= row[name]
    ))
 
 
  fig.update_layout(
    polar=dict(
      radialaxis=dict(
        visible=True,
      )),
    showlegend=True
  )
  fig.show()
