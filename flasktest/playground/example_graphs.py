import pandas as pd
import plotly.express as px
import plotly.offline

df_example = pd.read_csv("../static/data/api/pubg/df_hambinooo_solo_fpp.csv")
color = "rgb(20,27,37)"

kills = px.bar(
    data_frame=df_example, # which df  to use
    x="Season", # which column for the x-axis
    y="Kills_g", # which column for the y-axis
    title="Kills per game vs season | hambinooo solo-fpp", # set graph title
)
kills.update_traces(marker_color=color,
                  marker_line_width=None, opacity=None)
kills.update_layout(
    xaxis_title="Season",
    yaxis_title="Kills per game",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Josefin Sans",
        size=17,
        color=color,
    ),
)
kills.write_image("flasktest/static/images/data/pubg/example_kills.png", scale=2)

damage = px.bar(
    data_frame=df_example, # which df  to use
    x="Season", # which column for the x-axis
    y="Damage_g", # which column for the y-axis
    title="Damage per game vs season | hambinooo solo-fpp", # set graph title
)
damage.update_traces(marker_color=color,
                  marker_line_width=None, opacity=None)
damage.update_layout(
    xaxis_title="Season",
    yaxis_title="Damage per game",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Josefin Sans",
        size=17,
        color=color,
    ),
)
damage.write_image("flasktest/static/images/data/pubg/example_damage.png", scale=2)

distance = px.bar(
    data_frame=df_example, # which df  to use
    x="Season", # which column for the x-axis
    y="Distance_g", # which column for the y-axis
    title="Distance per game vs season | hambinooo solo-fpp", # set graph title
)
distance.update_traces(marker_color=color,
                  marker_line_width=None, opacity=None)
distance.update_layout(
    xaxis_title="Season",
    yaxis_title="Distance per game",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Josefin Sans",
        size=17,
        color=color,
    ),
)
distance.write_image("flasktest/static/images/data/pubg/example_distance.png", scale=2)
