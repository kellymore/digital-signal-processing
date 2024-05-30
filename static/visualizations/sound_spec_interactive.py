import plotly.graph_objects as go

# Data
categories = [
    'Earthquakes and lightning', 
    'Acoustic sound', 
    'Animal hearing', 
    'Ultrasonic cleaning', 
    'Therapeutic ultrasound', 
    'Non-destructive testing and medical ultrasound diagnostics', 
    'Acoustic microscopy', 
    'Infrasound', 
    'Human hearing range', 
    'Ultrasound'
]

low_hz = [
    0.1, 20, 40, 20000, 1000000, 2000000, 50000000, 0.01, 20, 20000
]

high_hz = [
    10, 20000, 100000, 40000, 3000000, 18000000, 1000000000, 20, 20000, 1000000000
]

fig = go.Figure()

# Add ranges
for category, low, high in zip(categories, low_hz, high_hz):
    fig.add_trace(go.Scatter(
        x=[low, high], 
        y=[category, category], 
        mode='lines+markers',
        marker=dict(size=10),
        name=category,
        line=dict(width=3)
    ))

# Update layout
fig.update_layout(
    title="Sound Spectrum Ranges",
    xaxis_title="Frequency (Hz)",
    yaxis_title="Category",
    xaxis_type="log",
    yaxis=dict(autorange="reversed"),
    height=600,
    margin=dict(l=200, r=20, t=40, b=20)
)

fig.show()
