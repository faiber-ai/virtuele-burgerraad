# Virtuele Burgerraad

## Project Overview

This is a fork of Karpathy's LLM Council, adapted for the Dutch market. Instead of multiple LLM models debating, we simulate 15 Dutch citizen personas reacting to proposed legislation ("wetsvoorstellen"). The goal is to stress-test policies for "menselijke maat" — making the human impact of policy visible.

## Goal

A demo/brand-building tool for Faiber.ai. Not a real product. Should be visually compelling enough to screenshot/record for LinkedIn. When a journalist or citizen pastes text from a new bill (e.g., the new rental law) into the app, they don't get a dry report—they get a "digital demonstration" of virtual citizens on their screen. That screenshot is what people will share.

## Architecture

**Keep from original LLM Council:**
- FastAPI backend structure
- React/Vite frontend
- OpenRouter integration
- 3-stage deliberation flow

**Modify for Virtuele Burgerraad:**
- Stage 1: 15 personas (same model, different system prompts) react to input text
- Stage 2: Personas read each other's reactions and respond ("Anja reageert op Sjoerd")
- Stage 3: "Nationale Ombudsman" AI synthesizes all concerns into a report

### The 4-Stage Flow

**Stage 1 - Eerste Reacties (Individual Reactions)**
- All 15 personas read the policy text simultaneously (parallel API calls)
- Each answers: "Wat betekent dit voor jouw portemonnee en jouw dagelijks leven?"
- Each response gets a sentiment score (-1 to 1) for avatar coloring
- Output: 15 individual reactions with sentiment

**Stage 2 - Coalitievorming (Coalition Formation)**
- AI analyzes Stage 1 reactions and clusters personas into 3-4 coalitions
- Coalitions are **dynamic per policy topic**, not fixed demographics
- Examples of how coalitions shift:
  - Huurwet: Renters (Anja, Fatima, Youssef) vs Property owners (Sjoerd, Marieke)
  - Digitalisering: Digitally excluded (Willem, Henk) vs Digital natives (Ahmed, Bram)
  - Stikstofbeleid: Rural (Johan, Sjoerd) vs Urban (Lisa, Priya)
- Each coalition gets a name and shared position statement
- AI selects a spokesperson per coalition (most affected persona)
- Output: Coalition definitions, member lists, spokespersons, position statements

**Stage 3 - Coalitiedebatten (Coalition Debates)**
- AI picks 2 coalition matchups with highest tension
- Each debate: 3 exchanges per side (6 messages total per debate)
- Format: **Spokesperson + Interjections**
  - Spokesperson leads the argument for their coalition
  - Other coalition members add short interjections ("Precies!", "En vergeet niet dat...", "Zeg dat!")
  - Creates visual activity: multiple avatars light up during debate
- Example debate flow:
  ```
  Sjoerd (spokesperson): "Wij betalen de rekening voor dit soort regelingen..."
    → Marieke: "Precies!" | Johan: "👏"
  Fatima (spokesperson): "Jij hebt tenminste een vast contract en een koophuis."
    → Dennis: "Zeg dat!" | Anja: "Inderdaad"
  Sjoerd: "Dat heb ik zelf opgebouwd, met 20 jaar hard werken."
    → Marieke: "Zonder subsidie!"
  Fatima: "Ik werk ook hard. Drie diensten per week, en toch kom ik niet rond."
    → Claudia: "Dit herken ik zo"
  ...
  ```
- Output: 2 structured debates with spokesperson turns + interjection arrays

**Stage 4 - Ombudsman Rapport (Synthesis)**
- "Nationale Ombudsman" AI reads everything: individual reactions, coalitions, debates
- Produces final report:
  - Overall "Menselijke Maat" score (traffic light: red/orange/green)
  - Biggest pain points by coalition
  - Which groups are hit hardest
  - Key unresolved tensions from debates
  - Recommendations for policy adjustment
- Output: Structured report suitable for scorecard visualization

## The 15 Personas

| # | Naam | Leeftijd | Profiel | Kernzorg |
|---|------|----------|---------|----------|
| 1 | Anja | 48 | Alleenstaande moeder, parttime schoonmaak, Enschede | "Elke brief van de Belastingdienst is stress" |
| 2 | Bram | 31 | ZZP'er, grafisch ontwerper, Amsterdam | "Ik val overal tussen wal en schip" |
| 3 | Henk | 67 | Gepensioneerd elektricien, Drenthe | "De zorgpremie vreet m'n koopkracht op" |
| 4 | Ingrid | 64 | Mantelzorger, vrouw van Henk | "Er wordt altijd van je verwacht dat je het zelf oplost" |
| 5 | Youssef | 24 | Starter, HBO bedrijfskunde, Utrecht, €30k studieschuld | "Ik kan nergens een huis krijgen" |
| 6 | Sjoerd | 44 | Middenmanager logistiek, Vinex-wijk Houten | "Wij betalen alles, krijgen niks" |
| 7 | Fatima | 52 | Verpleegkundige, Rotterdam-Zuid, sociale huur | "Ik werk me kapot en kan de huur amper betalen" |
| 8 | Johan | 58 | Melkveehouder, Friesland, 80 koeien | "Den Haag snapt niet hoe een boerenbedrijf werkt" |
| 9 | Lisa | 29 | Basisschoolleraar, Nijmegen | "De werkdruk is onhoudbaar" |
| 10 | Willem | 73 | Weduwnaar, alleen AOW, Tilburg, beperkt digitaal | "Alles moet online, maar ik kan dat niet" |
| 11 | Priya | 35 | Kennismigrant, developer bij ASML, Eindhoven | "De 30%-regeling is cruciaal voor ons" |
| 12 | Dennis | 38 | Flexwerker magazijn via uitzendbureau, Venlo | "Ik weet nooit of ik volgende maand nog werk heb" |
| 13 | Marieke | 41 | MKB-ondernemer, kapsalon met 3 werknemers, Zwolle | "De administratielast is niet te doen" |
| 14 | Ahmed | 19 | MBO-student installatietechniek, Den Haag | "Ik maak me zorgen of ik straks genoeg ga verdienen" |
| 15 | Claudia | 55 | Thuiszorg, particuliere huur Haarlem, zoon met beperking | "Het systeem is niet gemaakt voor uitzonderingen" |

These personas represent Dutch archetypes covering current pain points: housing market, benefits/toeslagen, healthcare costs, flex work, self-employment, caregiving, farming, education, digital exclusion, knowledge migration, SME administration burden, and youth prospects.

## Frontend Requirements & Visual Design

The UI should NOT be a standard chat interface. It should be a dashboard that communicates emotion and impact directly.

### Visual Elements to Implement

**1. Human Heatmap (Stage 1 replacement)**
- Replace standard tabs with visual persona avatars (AI-generated realistic Dutch citizen photos)
- Status rings/glow around each avatar based on sentiment:
  - Red pulsing: "Grote paniek/onuitvoerbaar" (major panic/unworkable)
  - Orange: "Zorgen/complex" (worried/complex)
  - Green: "Positief/kansrijk" (positive/promising)
- Click avatar to expand their specific "bezwaarschrift" (objection)

**2. Impact Slider (sidebar)**
- "Vóór vs. Na" visualization
- Portemonnee-check: Visual barometer showing disposable income changes per persona
- Stress-meter: Gauge that increases as policy text complexity grows (measured by LLM based on B1 language level)

**3. Battle Arena (Stage 2)**
- Connection lines between avatars showing who "attacks" or "supports" whose arguments
- Sentiment bubbles: Speech bubbles with exclamations like "Ho even!" or "Dit klopt niet voor ZZP'ers" appearing above avatars during deliberation

**4. Nationale Ombudsman Scorekaart (Stage 3)**
- Traffic light system: Large visual header with final "Menselijke Maat" score
- "Grootste Pijnpunt" graphic: Word cloud or chart showing which group is hardest hit
- Downloadable infographic: Button to export analysis as shareable infographic

### General UI Requirements
- Dutch UI text throughout
- Clean, modern look suitable for LinkedIn screenshots
- Animations: `pulse` for red warnings, `slide-in` for citizen reactions

## Tech Decisions

- Use same model for all personas (e.g., `claude-sonnet-4-20250514` via OpenRouter)
- System prompts define persona personality, background, and perspective
- Keep OpenRouter as LLM provider
- Backend runs on **port 8001** (not 8000)
- Frontend runs on **port 5173** (Vite default)

### Backend Structure

**`config.py`**
- `PERSONAS` list with persona definitions (name, age, profile, core concern, system prompt)
- `PERSONA_MODEL` - model used for all personas (e.g., claude-sonnet-4-20250514)
- `OMBUDSMAN_MODEL` - model for Stage 4 synthesis
- Uses `OPENROUTER_API_KEY` from `.env`

**`burgerraad.py`** (main deliberation logic)
- `stage1_eerste_reacties(policy_text)`:
  - Query same model 15x in parallel with different persona system prompts
  - Each response includes sentiment_score (-1 to 1)
  - Returns: list of {persona, reaction, sentiment_score}

- `stage2_coalitievorming(stage1_results)`:
  - AI analyzes all reactions and clusters into 3-4 coalitions
  - Determines coalition names, members, spokespersons
  - Generates position statement per coalition
  - Returns: list of coalition objects

- `stage3_coalitiedebatten(stage1_results, coalitions)`:
  - AI picks 2 highest-tension coalition matchups
  - Generates 3 exchanges per side (6 messages per debate)
  - Each exchange includes spokesperson message + interjections
  - Returns: list of 2 debate objects

- `stage4_ombudsman_rapport(stage1_results, coalitions, debates)`:
  - Ombudsman AI synthesizes everything
  - Returns: report with score, pain points, recommendations

**`openrouter.py`**
- Async model queries via OpenRouter
- Parallel execution with `asyncio.gather()`
- Graceful degradation on failures

**`storage.py`**
- JSON-based session storage in `data/sessions/`
- Each session: {id, created_at, policy_text, stage1, stage2, stage3, stage4}

### Frontend Structure

**Components to create:**

`PersonaAvatar.jsx`
- Avatar image with sentiment ring/glow (red/orange/green)
- Name label below
- Click to expand reaction
- Pulse animation when speaking in debate

`Stage1View.jsx` - Eerste Reacties
- Grid of all 15 PersonaAvatars
- Sentiment colors visible at a glance
- Click avatar → modal/panel with full reaction

`Stage2View.jsx` - Coalitievorming
- Animated transition: avatars slide into coalition clusters
- Coalition name labels ("De Kwetsbaren", "Hardwerkende Middenklasse")
- Spokesperson highlighted (larger avatar or crown icon)
- Position statement displayed per coalition

`Stage3View.jsx` - Coalitiedebatten
- Split screen or spotlight view for 2 debating spokespersons
- Speech bubbles for main arguments
- Interjection bubbles floating from coalition members
- Visual indicator of which coalition is "winning" (optional)

`Stage4View.jsx` - Ombudsman Rapport
- Traffic light score (large, prominent)
- "Grootste Pijnpunten" section
- "Hardst Geraakt" coalition highlight
- Recommendations list
- Export/share button for infographic

**Styling:**
- Primary colors: Dutch government-inspired but modern (think Rijksoverheid.nl meets startup)
- Sentiment colors: Red (#e74c3c), Orange (#f39c12), Green (#27ae60)
- Avatar ring animations in CSS (pulse, glow)
- Smooth transitions between stages

## Data Flow

```
User pastes wetsvoorstel text
    ↓
Stage 1: Eerste Reacties
    15 parallel queries (same model, 15 persona system prompts)
    → Returns: [{persona, reaction, sentiment_score}, ...]
    ↓
Stage 2: Coalitievorming
    AI analyzes reactions, clusters into 3-4 coalitions
    → Returns: [{
        name: "De Kwetsbaren",
        members: ["Anja", "Willem", "Dennis", "Claudia"],
        spokesperson: "Anja",
        position: "Deze wet vergroot de onzekerheid..."
    }, ...]
    ↓
Stage 3: Coalitiedebatten
    AI picks 2 high-tension matchups
    2 debates × 6 messages each, with interjections
    → Returns: [{
        coalition_a: "Hardwerkende Middenklasse",
        coalition_b: "De Kwetsbaren",
        spokesperson_a: "Sjoerd",
        spokesperson_b: "Fatima",
        exchanges: [{
            speaker: "Sjoerd",
            message: "Wij betalen de rekening...",
            interjections: [{persona: "Marieke", text: "Precies!"}]
        }, ...]
    }, ...]
    ↓
Stage 4: Ombudsman Rapport
    Synthesis of all previous stages
    → Returns: {
        score: "orange",  // red/orange/green
        summary: "...",
        hardest_hit: ["De Kwetsbaren", "Starters"],
        pain_points: [...],
        unresolved_tensions: [...],
        recommendations: [...]
    }
    ↓
Frontend: Render as visual dashboard
    - Avatar grid with sentiment colors
    - Coalition clusters with connecting lines
    - Debate view with spotlight + interjection bubbles
    - Scorecard with traffic light and pain points
```

## Out of Scope

- User authentication
- Database persistence (JSON files fine)
- Mobile optimization
- Production hardening
- Real policy impact calculations (this is illustrative, not authoritative)

## Why This Can Go Viral

1. **Emotion Visualization**: Not just text, but an "Emotional Barometer" per persona
2. **The "Stress-test" Button**: Users upload policy text, see reactions within 60 seconds
3. **The Mirror Function**: AI shows where policy helps one citizen but hurts another—exposing "system errors" like the toeslagenaffaire

## Development Notes

### Running the Project
```bash
# Backend (from project root)
python -m backend.main

# Frontend (from frontend directory)
npm run dev
```

### Important Gotchas
1. Always run backend as `python -m backend.main` from project root (relative imports)
2. CORS must allow localhost:5173 and localhost:3000
3. All ReactMarkdown must be wrapped in `.markdown-content` class

### Language
- All user-facing text: Dutch
- Code comments and documentation: English
- Variable/function names: English

## Credits

- Original LLM Council concept: Andrej Karpathy
- Virtuele Burgerraad adaptation: Faiber.ai
