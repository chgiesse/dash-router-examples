from dash_mantine_components.theme import DEFAULT_THEME
from appshell import mantine_dark
import plotly.graph_objects as go
import plotly.io as pio
import copy


def add_figure_templates(default=None):

    """
    Create and register Plotly figure templates styled to match the Mantine default theme.

    This function generates two custom Plotly templates:
    - "mantine_light" for light mode
    - "mantine_dark" for dark mode

    Templates are registered with `plotly.io.templates`, allowing you to apply them to Plotly figures
    using the template names "mantine_light" or "mantine_dark". These templates include Mantine-inspired
    color palettes, background colors, and other layout customizations.

    Parameters:
    - default (str): The default template to apply globally. Must be either "mantine_light" or "mantine_dark".
                      If not set, the default Plotly template remains unchanged.

    Returns:
    - None: The templates are registered and optionally set as the default, but no value is returned.

    """

    colors = DEFAULT_THEME["colors"]
    font_family = DEFAULT_THEME["fontFamily"]
    # pallet generated from https://www.learnui.design/tools/data-color-picker.html#palette
    custom_colorscale = [
        "#1864ab",  # blue[9]
        "#7065b9",
        "#af61b7",
        "#e35ea5",
        "#ff6587",
        "#ff7c63",
        "#ff9e3d",
        "#fcc419",  # yellow[5]
    ]

    # Default theme configurations
    default_themes = {
        "light": {
            "colorway": [
                colors[color][6]
                for color in ["blue", "red", "green", "violet", "orange", "cyan", "pink", "yellow"]
            ],
            "paper_bgcolor":  "rgb(245, 247, 248)",  # mantine background color
            "plot_bgcolor": "rgb(245, 247, 248)",
            "gridcolor": "#dee2e6",
            "button_bg": colors["gray"][5],
            "button_active": colors["gray"][6],
            "button_text": "white"
        },
        "dark": {
            "colorway": [
                colors[color][8]
                for color in ["blue", "red", "green", "violet", "orange", "cyan", "pink", "yellow"]
            ],
            # "paper_bgcolor":  mantine_dark[7], # mantine background color
            "paper_bgcolor":  'rgb(0,0,0,0)', # mantine background color
            "plot_bgcolor":  'rgb(0,0,0,0)',
            "gridcolor": "#343a40",
            "button_bg": colors["gray"][7],
            "button_active": colors["gray"][6],
            "button_text": "white"
        }
    }

    def make_template(name):
        #Start with either a light or dark Plotly template
        base = "plotly_white" if name == "light" else "plotly_dark"
        template = copy.deepcopy(pio.templates[base])

        layout = template.layout
        theme_config = default_themes[name]

        # Apply theme settings
        layout.colorway = theme_config["colorway"]
        layout.colorscale.sequential = custom_colorscale
        layout.piecolorway = theme_config["colorway"]
        layout.paper_bgcolor = theme_config["paper_bgcolor"]
        layout.plot_bgcolor = theme_config["plot_bgcolor"]
        layout.font.family = font_family

        # Grid settings
        for axis in (layout.xaxis, layout.yaxis):
            axis.gridcolor = theme_config["gridcolor"]
            axis.gridwidth = 0.5
            axis.zerolinecolor = theme_config["gridcolor"]

        # Range selector buttons settings
        layout.xaxis.rangeselector.font.color = theme_config["button_text"]
        layout.xaxis.rangeselector.activecolor = theme_config["button_active"]
        layout.xaxis.rangeselector.bgcolor = theme_config["button_bg"]

        # Geo settings
        layout.geo.bgcolor = theme_config["plot_bgcolor"]
        layout.geo.lakecolor = theme_config["plot_bgcolor"]
        layout.geo.landcolor = theme_config["plot_bgcolor"]

        # Hover label settings
        layout.hoverlabel.font.family = font_family

        # Scatter plot settings
        template.data.scatter = (go.Scatter(marker_line_color=theme_config["plot_bgcolor"]),)
        template.data.scattergl = (go.Scattergl(marker_line_color=theme_config["plot_bgcolor"]),)

        return template


    # #register templates
    pio.templates["mantine_light"] = make_template("light")
    pio.templates["mantine_dark"] = make_template("dark")

    # set the default
    if default in ["mantine_light", "mantine_dark"]:
        pio.templates.default = default
    elif default:
        raise ValueError(f"unrecognized {default=}, allowed values are 'mantine_light' and 'mantine_dark'")

    return None


vizro_dark = {
  "layout": {
    "annotationdefaults": {
      "font": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.8784313725)"
      },
      "showarrow": False
    },
    "bargroupgap": 0.1,
    "coloraxis": {
      "autocolorscale": False,
      "colorbar": {
        "outlinewidth": 0,
        "showticklabels": True,
        "thickness": 20,
        "tickfont": {
          "size": 14,
          "color": "rgba(255, 255, 255, 0.6)"
        },
        "ticklabelposition": "outside",
        "ticklen": 8,
        "ticks": "outside",
        "tickwidth": 1,
        "title": {
          "font": {
            "size": 14,
            "color": "rgba(255, 255, 255, 0.6)"
          }
        },
        "tickcolor": "rgba(255, 255, 255, 0.3019607843)"
      }
    },
    "colorscale": {
      "diverging": [
        [0.0, "#7e000c"],
        [0.05555555555555555, "#9d1021"],
        [0.1111111111111111, "#bc1f37"],
        [0.16666666666666666, "#db2f4c"],
        [0.2222222222222222, "#ea536b"],
        [0.2777777777777778, "#f67486"],
        [0.3333333333333333, "#fe94a0"],
        [0.3888888888888889, "#fbb6be"],
        [0.4444444444444444, "#f8d6da"],
        [0.5, "#E6E8EA"],
        [0.5555555555555556, "#afe7f9"],
        [0.6111111111111112, "#5bd6fe"],
        [0.6666666666666666, "#3bbef1"],
        [0.7222222222222222, "#24a6e1"],
        [0.7777777777777778, "#0d8ed1"],
        [0.8333333333333334, "#0077bd"],
        [0.8888888888888888, "#0061a4"],
        [0.9444444444444444, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequential": [
        [0.0, "#afe7f9"],
        [0.125, "#5bd6fe"],
        [0.25, "#3bbef1"],
        [0.375, "#24a6e1"],
        [0.5, "#0d8ed1"],
        [0.625, "#0077bd"],
        [0.75, "#0061a4"],
        [0.875, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequentialminus": [
        [0.0, "#7e000c"],
        [0.125, "#9d1021"],
        [0.25, "#bc1f37"],
        [0.375, "#db2f4c"],
        [0.5, "#ea536b"],
        [0.625, "#f67486"],
        [0.75, "#fe94a0"],
        [0.875, "#fbb6be"],
        [1.0, "#f8d6da"]
      ]
    },
    "colorway": [
      "#00b4ff",
      "#ff9222",
      "#3949ab",
      "#ff5267",
      "#08bdba",
      "#fdc935",
      "#689f38",
      "#976fd1",
      "#f781bf",
      "#52733e"
    ],
    "font": {
      "family": "Inter, sans-serif, Arial",
      "size": 14,
      "color": "rgba(255, 255, 255, 0.8784313725)"
    },
    "legend": {
      "bgcolor": "rgba(0, 0, 0, 0)",
      "font": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.8784313725)"
      },
      "orientation": "h",
      "title": {
        "font": {
          "size": 14,
          "color": "rgba(255, 255, 255, 0.8784313725)"
        }
      },
      "y": -0.2
    },
    "map": {
      "style": "carto-darkmatter"
    },
    "margin": {
      "autoexpand": True,
      "b": 64,
      "l": 80,
      "pad": 0,
      "r": 24,
      "t": 64
    },
    "modebar": {
      "activecolor": "darkgrey",
      "bgcolor": "rgba(0, 0, 0, 0)",
      "color": "dimgrey"
    },
    "showlegend": True,
    "title": {
      "font": {
        "size": 20,
        "color": "rgba(255, 255, 255, 0.8784313725)"
      },
      "pad": {
        "b": 0,
        "l": 24,
        "r": 24,
        "t": 24
      },
      "x": 0,
      "xanchor": "left",
      "xref": "container",
      "y": 1,
      "yanchor": "top",
      "yref": "container"
    },
    "uniformtext": {
      "minsize": 12,
      "mode": "hide"
    },
    "xaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": True,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(255, 255, 255, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
      "linecolor": "rgba(255, 255, 255, 0.3019607843)",
      "tickcolor": "rgba(255, 255, 255, 0.3019607843)"
    },
    "yaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": False,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(255, 255, 255, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(255, 255, 255, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
      "linecolor": "rgba(255, 255, 255, 0.3019607843)",
      "tickcolor": "rgba(255, 255, 255, 0.3019607843)"
    },
    "geo": {
      "bgcolor": "#141721",
      "lakecolor": "#141721",
      "landcolor": "#141721"
    },
    "paper_bgcolor": "#141721",
    "plot_bgcolor": "#141721",
    "polar": {
      "angularaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      },
      "bgcolor": "#141721",
      "radialaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      }
    },
    "ternary": {
      "aaxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      },
      "baxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      },
      "bgcolor": "#141721",
      "caxis": {
        "gridcolor": "rgba(255, 255, 255, 0.1019607843)",
        "linecolor": "rgba(255, 255, 255, 0.3019607843)"
      }
    }
  },
  "data": {
    "bar": [
      {
        "marker": {
          "line": {
            "color": "#141721"
          }
        },
        "type": "bar"
      }
    ],
    "waterfall": [
      {
        "connector": {
          "line": {
            "color": "rgba(255, 255, 255, 0.3019607843)",
            "width": 1
          }
        },
        "decreasing": {
          "marker": {
            "color": "#ff9222"
          }
        },
        "increasing": {
          "marker": {
            "color": "#00b4ff"
          }
        },
        "textfont": {
          "color": "rgba(255, 255, 255, 0.8784313725)"
        },
        "textposition": "outside",
        "totals": {
          "marker": {
            "color": "grey"
          }
        },
        "type": "waterfall"
      }
    ]
  }
}

vizro_light = {
  "layout": {
    "annotationdefaults": {
      "font": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.8784313725)"
      },
      "showarrow": False
    },
    "bargroupgap": 0.1,
    "coloraxis": {
      "autocolorscale": False,
      "colorbar": {
        "outlinewidth": 0,
        "showticklabels": True,
        "thickness": 20,
        "tickfont": {
          "size": 14,
          "color": "rgba(20, 23, 33, 0.6)"
        },
        "ticklabelposition": "outside",
        "ticklen": 8,
        "ticks": "outside",
        "tickwidth": 1,
        "title": {
          "font": {
            "size": 14,
            "color": "rgba(20, 23, 33, 0.6)"
          }
        },
        "tickcolor": "rgba(20, 23, 33, 0.3019607843)"
      }
    },
    "colorscale": {
      "diverging": [
        [0.0, "#7e000c"],
        [0.05555555555555555, "#9d1021"],
        [0.1111111111111111, "#bc1f37"],
        [0.16666666666666666, "#db2f4c"],
        [0.2222222222222222, "#ea536b"],
        [0.2777777777777778, "#f67486"],
        [0.3333333333333333, "#fe94a0"],
        [0.3888888888888889, "#fbb6be"],
        [0.4444444444444444, "#f8d6da"],
        [0.5, "#E6E8EA"],
        [0.5555555555555556, "#afe7f9"],
        [0.6111111111111112, "#5bd6fe"],
        [0.6666666666666666, "#3bbef1"],
        [0.7222222222222222, "#24a6e1"],
        [0.7777777777777778, "#0d8ed1"],
        [0.8333333333333334, "#0077bd"],
        [0.8888888888888888, "#0061a4"],
        [0.9444444444444444, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequential": [
        [0.0, "#afe7f9"],
        [0.125, "#5bd6fe"],
        [0.25, "#3bbef1"],
        [0.375, "#24a6e1"],
        [0.5, "#0d8ed1"],
        [0.625, "#0077bd"],
        [0.75, "#0061a4"],
        [0.875, "#004c8c"],
        [1.0, "#003875"]
      ],
      "sequentialminus": [
        [0.0, "#7e000c"],
        [0.125, "#9d1021"],
        [0.25, "#bc1f37"],
        [0.375, "#db2f4c"],
        [0.5, "#ea536b"],
        [0.625, "#f67486"],
        [0.75, "#fe94a0"],
        [0.875, "#fbb6be"],
        [1.0, "#f8d6da"]
      ]
    },
    "colorway": [
      "#00b4ff",
      "#ff9222",
      "#3949ab",
      "#ff5267",
      "#08bdba",
      "#fdc935",
      "#689f38",
      "#976fd1",
      "#f781bf",
      "#52733e"
    ],
    "font": {
      "family": "Inter, sans-serif, Arial",
      "size": 14,
      "color": "rgba(20, 23, 33, 0.8784313725)"
    },
    "legend": {
      "bgcolor": "rgba(0, 0, 0, 0)",
      "font": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.8784313725)"
      },
      "orientation": "h",
      "title": {
        "font": {
          "size": 14,
          "color": "rgba(20, 23, 33, 0.8784313725)"
        }
      },
      "y": -0.2
    },
    "map": {
      "style": "carto-darkmatter"
    },
    "margin": {
      "autoexpand": True,
      "b": 64,
      "l": 80,
      "pad": 0,
      "r": 24,
      "t": 64
    },
    "modebar": {
      "activecolor": "darkgrey",
      "bgcolor": "rgba(0, 0, 0, 0)",
      "color": "dimgrey"
    },
    "showlegend": True,
    "title": {
      "font": {
        "size": 20,
        "color": "rgba(20, 23, 33, 0.8784313725)"
      },
      "pad": {
        "b": 0,
        "l": 24,
        "r": 24,
        "t": 24
      },
      "x": 0,
      "xanchor": "left",
      "xref": "container",
      "y": 1,
      "yanchor": "top",
      "yref": "container"
    },
    "uniformtext": {
      "minsize": 12,
      "mode": "hide"
    },
    "xaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": True,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(20, 23, 33, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
      "linecolor": "rgba(20, 23, 33, 0.3019607843)",
      "tickcolor": "rgba(20, 23, 33, 0.3019607843)"
    },
    "yaxis": {
      "automargin": True,
      "layer": "below traces",
      "linewidth": 1,
      "showline": False,
      "showticklabels": True,
      "tickfont": {
        "size": 14,
        "color": "rgba(20, 23, 33, 0.6)"
      },
      "ticklabelposition": "outside",
      "ticklen": 8,
      "ticks": "outside",
      "tickwidth": 1,
      "title": {
        "font": {
          "size": 16,
          "color": "rgba(20, 23, 33, 0.8784313725)"
        },
        "standoff": 8
      },
      "visible": True,
      "zeroline": False,
      "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
      "linecolor": "rgba(20, 23, 33, 0.3019607843)",
      "tickcolor": "rgba(20, 23, 33, 0.3019607843)"
    },
    "geo": {
      "bgcolor": "white",
      "lakecolor": "white",
      "landcolor": "white"
    },
    "paper_bgcolor": "white",
    "plot_bgcolor": "white",
    "polar": {
      "angularaxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      },
      "bgcolor": "white",
      "radialaxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      }
    },
    "ternary": {
      "aaxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      },
      "baxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      },
      "bgcolor": "white",
      "caxis": {
        "gridcolor": "rgba(20, 23, 33, 0.1019607843)",
        "linecolor": "rgba(20, 23, 33, 0.3019607843)"
      }
    }
  },
  "data": {
    "bar": [
      {
        "marker": {
          "line": {
            "color": "white"
          }
        },
        "type": "bar"
      }
    ],
    "waterfall": [
      {
        "connector": {
          "line": {
            "color": "rgba(20, 23, 33, 0.3019607843)",
            "width": 1
          }
        },
        "decreasing": {
          "marker": {
            "color": "#ff9222"
          }
        },
        "increasing": {
          "marker": {
            "color": "#00b4ff"
          }
        },
        "textfont": {
          "color": "rgba(20, 23, 33, 0.8784313725)"
        },
        "textposition": "outside",
        "totals": {
          "marker": {
            "color": "grey"
          }
        },
        "type": "waterfall"
      }
    ]
  }
}

def apply_vizro_theme():
    pio.templates['plotly_dark'] = vizro_dark
    pio.templates['plotly'] = vizro_light
