# All environment variables go here: paths to datasets/models/logs etc...

TEST_VARIABLE = 'hi'

COMPANY_NAMES = ['Amazon', 'Apple', 'Bank of America', 'BASF', 'Blackrock', 'Boeing', 'Chevron', 'Cisco',
                 'Exxon Mobile', 'Facebook', 'Ford', 'General Motors', 'Google', 'Honeywell', 'JetBlue',
                 'Johnson Johnson', 'JP Morgan', 'Mastercard', 'Mc Donalds', 'Microsoft', 'Morgan Stanley', 'Oracle',
                 'PepsiCo', 'Samsung', 'Siemens', 'TD Bank', 'Unilever', 'Visa', 'Walt Disney', 'Wells Fargo']

SYNONYMS = {
    'Amazon': ['AMZN'],
    'Apple': ['AAPL', 'iPhone'],
    'Bank of America': ['BankofAmerica', '$BAC'],
    'BASF': ['BFFAF'],
    'Blackrock': ['BLK'],
    'Boeing': ['$BA'],
    'Chevron': ['CVX', 'Texaco', 'Caltex'],
    'Cisco': ['CSCO'],
    'Exxon Mobile': ['Exxon', 'Exxonmobil', 'XOM'],
    'Facebook': ['FB', 'Oculus'],
    'Ford': [],
    'General Motors': ['GM'],
    'Google': ['Alphabet', 'GOOGL', 'Android'],
    'Honeywell': ['$HON'],
    'JetBlue': ['JBLU'],
    'Johnson Johnson': ['JNJ', 'Johnson & Johnson'],
    'JP Morgan': ['JPM', 'JP Morgan Chase', 'JPMorgan'],
    'Mastercard': ['$MA'],
    'Mc Donalds': ["Mc Donald's", 'Macces', 'Maccies', '$MCD', 'Maccy D', 'Maccas'],
    'Microsoft': ['MSFT'],
    'Morgan Stanley': ['$MS', 'Morganstanley'],
    'Oracle': ['$ORC'],
    'PepsiCo': ['Pepsi', '$PEP'],
    'Samsung': ['SSNLF'],
    'Siemens': ['SMAWF', 'SMEGF', 'SIEGY'],
    'TD Bank': ['$TD'],
    'Unilever': ['UNLYF', '$UL', 'Persil', 'Ben&Jerrys', 'Benjerrys', 'Benandjerrys'],
    'Visa': ['$V'],
    'Walt Disney': ['Disney', '$DIS'],
    'Wells Fargo': ['WFC']
}

COMPANY_SPECIFIC_ACTIONS = {
    'Amazon': ['climate pledge', 'pledge fund'],
    'Apple': ['supply chain', 'carbon footprint'],
    'Bank of America': ['green bond'],
    'BASF': ['palm oil'],
    'Boeing': ['hazardous', 'waste', 'water use'],
    'Chevron': ['human rights', 'racial'],
    'Cisco': ['plastic'],
    'Exxon Mobile': ['methane', 'flaring', 'emissions'],
    'Facebook': ['solar', 'wind power', 'wind project'],
    'Ford': ['water', 'gender'],
    'General Motors': ['habitat', 'wildlife', 'energy use'],
    'Honeywell': ['manufacturing site'],
    'JP Morgan': ['global workforce'],
    'JetBlue': ['fuel'],
    'Johnson Johnson': ['health'],
    'Mastercard': ['pandemic'],
    'Mc Donalds': ['vegetarian', 'vegan', 'recycle'],
    'Microsoft': ['water', 'circular economy'],
    'Morgan Stanley': ['plastic', 'women', 'green bond'],
    'Oracle': ['renewable energy', 'recycling', 'reuse'],
    'PepsiCo': ['commodities'],
    'Samsung': ['female'],
    'Siemens': ['environment', 'efficiency'],
    'TD Bank': ['emission'],
    'Unilever': ['forest'],
    'Visa': ['renewable electricity', 'green bond'],
    'Walt Disney': ['diverse', 'diversity', 'energy'],
    'Wells Fargo': ['development']
}

GENERAL_TOPCIS = {
    "methane": ["flaring"],
    "biodiversity": ["habitat", "wildlife"],
    "plastic": ["recycling", "recycle", "reuse"],
    "air travel": ["flying"]
}

KEYWORDS = {
    "carbon": ["coal", "greenhouse gas"],
    "sustainability": ["environment", "ecological", "sustainable", "sustainably"],
    "climate pledge fund": [],
    "the climate pledge": [],
    "global warming": ["climate change", "global climate change"],
    "fully-electric delivery": ["fully-electric delivery", "electric delivery", "e-mobility", "emobility"],
    "net zero carbon": ["net-zero", "net zero", "carbon-neutral", "carbon neutral", "carbonneutral", "carbon free", "emission free"],
    "protect forests": ["forestation", "reforestation", "afforestation", "save forest", "protect forest"],
    "reduce carbon emission": ["become carbon neutral", "reduce greenhouse gas", "cut down emission", "reduction of greenhouse", "reduction of emission", "carbon emission", "greenhouse gas"],
    "renewable energy": ["wind energy", "solar"],
}

DATA_PATH = "P:/Programming/Python/TUM.ai Makeathon/data"

TWITTER_ARCHIVE_DATASET_PATH = f"{DATA_PATH}/Twitter Archive Dataset"

LABELED_TWITTER_DATASET_PATH = f"{DATA_PATH}/Twitter Dataset Labeled"
LABELED_COMPANY_SUSTAINABILITY_PATH = f"{LABELED_TWITTER_DATASET_PATH}/Company + Sustainability"
LABELED_COMPANY_ACTION_PATH = f"{LABELED_TWITTER_DATASET_PATH}/Company + ACTION"
LABELED_KEYWORDS_PATH = f"{LABELED_TWITTER_DATASET_PATH}/KEYWORD"
