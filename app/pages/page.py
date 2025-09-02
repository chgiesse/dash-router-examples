import dash_mantine_components as dmc
from dash import html
import random


async def layout(**kwargs):
    colors = ['#FF4500', '#32CD32', '#1E90FF', '#FFD700', '#8A2BE2', '#20B2AA', '#DC143C', '#00FA9A', '#FF1493', '#00BFFF']
    anims = ['drop', "left-right", "right-left"]
    lines = []
    total = 16
    for i in range(total):
        # randomize delay and duration to increase overlap (slower, more concurrent lines)
        delay = f"{random.uniform(0,10):.2f}s"
        duration = f"{random.uniform(12,24):.2f}s"
        hoff = f"{random.uniform(20,40):.0f}px"
        color = colors[i % len(colors)]
        # Randomly choose vertical (drop) or horizontal movement
        if random.random() < 0.5:
            anim = 'drop'
            style = {
                '--anim-name': anim,
                '--delay': delay,
                '--drop-duration': duration,
                '--h-offset': hoff,
                '--color': color,
            }
            lines.append(html.Div(className='line', style=style))
        else:
            anim = random.choice(['left-right', 'right-left'])
            # choose a vertical placement for the horizontal travel
            htop = f"{random.uniform(10,90):.0f}%"
            # choose a shorter horizontal width between 4vw and 12vw
            hwidth = f"{random.uniform(4,12):.2f}vw"
            style = {
                '--anim-name': anim,
                '--delay': delay,
                '--drop-duration': duration,
                '--h-top': htop,
                '--h-width': hwidth,
                '--color': color,
            }
            # mark horizontal-moving lines with extra class for rotated styling
            lines.append(html.Div(className='line horizontal', style=style))

    return html.Div(
        className="grid-bg",
        children=[html.Div(className='lines', children=lines)],
    )
