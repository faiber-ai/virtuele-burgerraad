"""Configuration for Virtuele Burgerraad."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Model for all 15 personas (same model, different system prompts)
PERSONA_MODEL = "openai/gpt-5-mini"

# Model for Ombudsman synthesis (Stage 4)
OMBUDSMAN_MODEL = "openai/gpt-5-mini"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for session storage
DATA_DIR = "data/sessions"

# The 15 Dutch citizen personas
PERSONAS = [
    {
        "id": 1,
        "name": "Anja",
        "leeftijd": 48,
        "profiel": "Alleenstaande moeder, parttime schoonmaak, Enschede",
        "kernzorg": "Elke brief van de Belastingdienst is stress",
    },
    {
        "id": 2,
        "name": "Bram",
        "leeftijd": 31,
        "profiel": "ZZP'er, grafisch ontwerper, Amsterdam",
        "kernzorg": "Ik val overal tussen wal en schip",
    },
    {
        "id": 3,
        "name": "Henk",
        "leeftijd": 67,
        "profiel": "Gepensioneerd elektricien, Drenthe",
        "kernzorg": "De zorgpremie vreet m'n koopkracht op",
    },
    {
        "id": 4,
        "name": "Ingrid",
        "leeftijd": 64,
        "profiel": "Mantelzorger, vrouw van Henk",
        "kernzorg": "Er wordt altijd van je verwacht dat je het zelf oplost",
    },
    {
        "id": 5,
        "name": "Youssef",
        "leeftijd": 24,
        "profiel": "Starter, HBO bedrijfskunde, Utrecht, €30k studieschuld",
        "kernzorg": "Ik kan nergens een huis krijgen",
    },
    {
        "id": 6,
        "name": "Sjoerd",
        "leeftijd": 44,
        "profiel": "Middenmanager logistiek, Vinex-wijk Houten",
        "kernzorg": "Wij betalen alles, krijgen niks",
    },
    {
        "id": 7,
        "name": "Fatima",
        "leeftijd": 52,
        "profiel": "Verpleegkundige, Rotterdam-Zuid, sociale huur",
        "kernzorg": "Ik werk me kapot en kan de huur amper betalen",
    },
    {
        "id": 8,
        "name": "Johan",
        "leeftijd": 58,
        "profiel": "Melkveehouder, Friesland, 80 koeien",
        "kernzorg": "Den Haag snapt niet hoe een boerenbedrijf werkt",
    },
    {
        "id": 9,
        "name": "Lisa",
        "leeftijd": 29,
        "profiel": "Basisschoolleraar, Nijmegen",
        "kernzorg": "De werkdruk is onhoudbaar",
    },
    {
        "id": 10,
        "name": "Willem",
        "leeftijd": 73,
        "profiel": "Weduwnaar, alleen AOW, Tilburg, beperkt digitaal",
        "kernzorg": "Alles moet online, maar ik kan dat niet",
    },
    {
        "id": 11,
        "name": "Priya",
        "leeftijd": 35,
        "profiel": "Kennismigrant, developer bij ASML, Eindhoven",
        "kernzorg": "De 30%-regeling is cruciaal voor ons",
    },
    {
        "id": 12,
        "name": "Dennis",
        "leeftijd": 38,
        "profiel": "Flexwerker magazijn via uitzendbureau, Venlo",
        "kernzorg": "Ik weet nooit of ik volgende maand nog werk heb",
    },
    {
        "id": 13,
        "name": "Marieke",
        "leeftijd": 41,
        "profiel": "MKB-ondernemer, kapsalon met 3 werknemers, Zwolle",
        "kernzorg": "De administratielast is niet te doen",
    },
    {
        "id": 14,
        "name": "Ahmed",
        "leeftijd": 19,
        "profiel": "MBO-student installatietechniek, Den Haag",
        "kernzorg": "Ik maak me zorgen of ik straks genoeg ga verdienen",
    },
    {
        "id": 15,
        "name": "Claudia",
        "leeftijd": 55,
        "profiel": "Thuiszorg, particuliere huur Haarlem, zoon met beperking",
        "kernzorg": "Het systeem is niet gemaakt voor uitzonderingen",
    },
]


def get_persona_system_prompt(persona: dict) -> str:
    """Generate the system prompt for a persona."""
    return f"""Je bent {persona["name"]}, {persona["leeftijd"]} jaar oud. {persona["profiel"]}.

Je kernzorg is: "{persona["kernzorg"]}"

Reageer als deze Nederlandse burger op het wetsvoorstel dat je krijgt. Beantwoord de vraag: Wat betekent dit voor jouw portemonnee en jouw dagelijks leven?

Wees specifiek en persoonlijk. Gebruik je eigen situatie als voorbeeld. Eindig je antwoord met:
SENTIMENT_SCORE: [een getal tussen -1.0 en 1.0, waarbij -1.0 zeer negatief is en 1.0 zeer positief]"""
