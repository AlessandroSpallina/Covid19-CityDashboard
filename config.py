import dash_html_components as html

CITY_NAME = "Villarosa"
LOGO_PATH = "logo.png"  # defined from assets directory
DATASET_RAW_CSV_URL = "https://raw.githubusercontent.com/ComuneDiVillarosa/Covid-19/main/dataset.csv"
DATASET_HUMAN_CSV_URL = "https://github.com/ComuneDiVillarosa/Covid-19/blob/main/dataset.csv"

MAYOR_NAME = "Il Sindaco Informa"
MAYOR_LINK = "https://www.facebook.com/fascianasindaco"

DASHBOARD_DESCRIPTION = [
    html.P('''Raccolta dati Covid-19 Comune di Villarosa (EN).'''),
    html.P('''Questo sito ha l'intento di fornire ai cittadini la possibilità di conoscere l'attuale situazione 
        relativa al covid-19 nel territorio.'''),
    html.P('''Dati raccolti ed estrapolati dal Comune di Villarosa in concomitanza ai dati comunicati dall'Azienda 
        Sanitaria Provinciale di Enna. '''),
    html.A("Iscriviti al canale telegram per il bollettino giornaliero!",
           href="https://t.me/covid19villarosa", target="_blank"),
]

DASHBOARD_FOOTER = [
    '''Dataset a questo ''',
    html.A("link", href=DATASET_HUMAN_CSV_URL, target="_blank"),
    '''. Idea: ''',
    html.A("Gianluca Spallina", href="http://t.me/Giasball", target="_blank"),
    '''. Sviluppo: ''',
    html.A("Alessandro Spallina", href="https://github.com/AlessandroSpallina", target="_blank"),
    '''.'''
]