import plotly.graph_objects as go
import numpy as np

class GroundStation:
    def __init__(self, name: str, lat: float, lon: float, coverage_radius_km: float, company: str):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.coverage_radius_km = coverage_radius_km
        self.company = company

def create_ground_stations_plot(stations: list[GroundStation], output_file: str = 'ground_stations.html'):
    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="Black",
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        projection_type="orthographic",
        showframe=False,
        showcountries=True,
        countrycolor="gray",
        lataxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5),
        lonaxis=dict(showgrid=True, gridcolor="lightgray", gridwidth=0.5),
        center=dict(lon=0, lat=0)
    )

    companies_plotted = set()

    for station in stations:
        color = company_colors.get(station.company, 'gray')
        show_in_legend = station.company not in companies_plotted

        fig.add_trace(go.Scattergeo(
            lon=[station.lon],
            lat=[station.lat],
            mode='markers',
            hovertext=[station.name],
            marker=dict(size=10, color=color),
            name=f"{station.company} Ground Station",
            showlegend=show_in_legend
        ))

        radius_deg = station.coverage_radius_km / 111
        theta = np.linspace(0, 2*np.pi, 100)
        circle_lats = station.lat + radius_deg * np.cos(theta)
        circle_lons = station.lon + radius_deg / np.cos(np.radians(station.lat)) * np.sin(theta)

        fig.add_trace(go.Scattergeo(
            lon=circle_lons,
            lat=circle_lats,
            mode='lines',
            line=dict(width=1, color=f'rgba({",".join(map(str, [int(int(color[1:3], 16)), int(color[3:5], 16), int(color[5:7], 16), 0.3]))})' if len(color) == 7 else color),
            name=f"{station.company} Coverage",
            showlegend=show_in_legend
        ))

        companies_plotted.add(station.company)

    fig.update_layout(
        title="Global Ground Stations Coverage Map",
        height=1300,
        width=1300,
        showlegend=True,
        updatemenus=[{
            'buttons': [
                {
                    'args': [{'geo.center.lon': -180, 'geo.center.lat': 0}],
                    'label': 'Pacific View',
                    'method': 'relayout'
                },
                {
                    'args': [{'geo.center.lon': -90, 'geo.center.lat': 0}],
                    'label': 'Americas View',
                    'method': 'relayout'
                },
                {
                    'args': [{'geo.center.lon': 0, 'geo.center.lat': 0}],
                    'label': 'Africa/Europe View',
                    'method': 'relayout'
                },
                {
                    'args': [{'geo.center.lon': 90, 'geo.center.lat': 0}],
                    'label': 'Asia View',
                    'method': 'relayout'
                }
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'y': 0.1
        }],
        title_x=0.5,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    fig.write_html(output_file)

if __name__ == "__main__":
    # https://docs.aws.amazon.com/ground-station/latest/ug/aws-ground-station-antenna-locations.html
    aws_stations = [
        GroundStation("Alaska 1", 64.2008, -149.4937, 1000, "AWS"),
        GroundStation("Bahrain 1", 26.0667, 50.5577, 1000, "AWS"),
        GroundStation("Cape Town 1", -33.9249, 18.4241, 1000, "AWS"),
        GroundStation("Dubbo 1", -32.2569, 148.6010, 1000, "AWS"),
        GroundStation("Hawaii 1", 20.7967, -156.3319, 1000, "AWS"),
        GroundStation("Ireland 1", 53.3331, -6.2489, 1000, "AWS"),
        GroundStation("Ohio 1", 40.4173, -82.9071, 1000, "AWS"),
        GroundStation("Oregon 1", 43.8041, -120.5542, 1000, "AWS"),
        GroundStation("Punta Arenas 1", -53.1638, -70.9171, 1000, "AWS"),
        GroundStation("Seoul 1", 37.5665, 126.9780, 1000, "AWS"),
        GroundStation("Singapore 1", 1.3521, 103.8198, 1000, "AWS"),
        GroundStation("Stockholm 1", 59.3293, 18.0686, 1000, "AWS"),
    ]

    # https://www.viasat.com/government/antenna-systems/real-time-earth/
    viasat_stations = [
        GroundStation("Accra", 5.6, -0.3, 1000, "Viasat"),
        GroundStation("Alice Springs", -23.76, 133.88, 1000, "Viasat"),
        GroundStation("Cordoba", -31.52, -64.46, 1000, "Viasat"),
        GroundStation("Fairbanks", 64.79, -147.54, 1000, "Viasat"),
        GroundStation("Guildford", 51.24, -0.62, 1000, "Viasat"),
        GroundStation("Hokkaido", 42.59, 143.45, 1000, "Viasat"),
        GroundStation("Pretoria", -25.89, 27.70, 1000, "Viasat"),
        GroundStation("Pendergrass", 34.18, -83.67, 1000, "Viasat"),
        GroundStation("Piteå", 65.33, 21.42, 1000, "Viasat"),
        GroundStation("Ushuaia", -54.50, -67.11, 1000, "Viasat"),
    ]

    # https://www.nasa.gov/technology/space-comms/near-space-network-complexes/
    commercial_stations = [
        GroundStation("KSAT Singapore", 1.3521, 103.8198, 1000, "KSAT"),
        GroundStation("KSAT Svalbard", 78.2297, 15.3975, 1000, "KSAT"),
        GroundStation("KSAT TrollSat", -72.0111, 2.5333, 1000, "KSAT"),
        GroundStation("SANSA Hartebeesthoek", -25.8897, 27.7075, 1000, "SANSA"),
        GroundStation("SSC Kiruna", 67.8557, 20.2236, 1000, "SSC"),
        GroundStation("SSC Santiago", -33.4489, -70.6693, 1000, "SSC"),
        GroundStation("SSC North Pole", 64.8037, -147.8781, 1000, "SSC"),
        GroundStation("SSC Dongara", -29.0453, 115.3494, 1000, "SSC"),
        GroundStation("SSC South Point", 19.0100, -155.6628, 1000, "SSC"),
    ]

    # https://satsearch.co/products/leafspace-leafline
    leaf_stations = [
        GroundStation("Peterborough", -32.9583, 138.8333, 1000, "Leaf"),
        GroundStation("Nangerty", -29.0000, 115.3333, 1000, "Leaf"),
        GroundStation("Absheron", 40.4500, 49.4833, 1000, "Leaf"),
        GroundStation("Kaspichan", 43.3050, 27.1500, 1000, "Leaf"),
        GroundStation("Plana", 42.4667, 23.4333, 1000, "Leaf"),
        GroundStation("Punta Arenas", -53.0333, -70.8333, 1000, "Leaf"),
        GroundStation("Santiago", -33.3500, -70.7667, 1000, "Leaf"),
        GroundStation("Blönduós", 65.6333, -20.2333, 1000, "Leaf"),
        GroundStation("Kandy", 7.2667, 80.7167, 1000, "Leaf"),
        GroundStation("Jeju", 33.3833, 126.3167, 1000, "Leaf"),
        GroundStation("Mon Loisir", -20.1333, 57.6833, 1000, "Leaf"),
        GroundStation("La Paz", 24.0833, -110.3833, 1000, "Leaf"),
        GroundStation("Awarua", -46.5167, 168.3667, 1000, "Leaf"),
        GroundStation("Santa Maria", 36.9833, -25.1333, 1000, "Leaf"),
        GroundStation("Unst", 60.7333, -0.8500, 1000, "Leaf"),
        GroundStation("Pretoria", -25.8500, 28.4500, 1000, "Leaf"),
    ]

    company_colors = {
        'AWS': 'red',
        'Viasat': 'blue',
        'KSAT': 'green',
        'SANSA': 'purple',
        'SSC': 'orange',
        'Leaf': 'cyan'
    }

    all_stations = aws_stations + viasat_stations + commercial_stations + leaf_stations
    create_ground_stations_plot(all_stations)