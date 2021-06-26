import dash
import dash_bootstrap_components as dbc
import dash_html_components as html


layout = dbc.Container(
    [
        html.H1("Analysis part is Under Development.."),
        html.Div(
            [
                html.H3("Curial points for trading", style={"color": "orange"}),
                html.Li(
                    "Start Slow and Steady.. gain Experience", style={"color": "orange"}
                ),
                html.Li(
                    "keep regular check on the News.. follow news websites",
                    style={"color": "orange"},
                ),
                html.Li(
                    "Read analysis suggestion of experts", style={"color": "orange"}
                ),
                html.Li("Be Patient", style={"color": "orange"}),
                html.Li(
                    "Learn more about investment Source", style={"color": "orange"}
                ),
            ]
        ),
        html.Footer(
            html.H3(html.Center(" Time Is Money ", style={"color": "lightgreen"}))
        ),
    ]
)
