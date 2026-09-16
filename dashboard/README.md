# Smarteck Leadtracker — dashboard

`Smarteck_Leadtracker_Dashboard.html` is één bestand. Logo en data zitten erin;
alleen de webfonts komen van buiten. Openen kan met een dubbelklik, vanaf een
netwerkschijf of vanuit SharePoint — er is geen server nodig.

## Twee standen

| Stand | Wanneer | Wat kan |
| --- | --- | --- |
| **Live** | de gepubliceerde, gedeelde versie | Toevoegen, wijzigen en verwijderen; iedereen ziet elkaars wijzigingen meteen |
| **Momentopname** | dit bestand los geopend (schijf, SharePoint, zip) | Alleen lezen; toont de gegevens zoals ze uit het werkboek kwamen |

De stand staat linksonder in de zijbalk. In de live stand staan de gegevens in de
opslag van het dashboard, niet meer in het werkboek; `build_data.py` vult dan nog
wel de stappenbibliotheek, de aannames en de keuzelijsten.

Bewerkbaar zijn: leads (een nieuwe lead krijgt automatisch het volledige
stappenspoor van zijn doelgroep), contactpersonen, overeenkomsten, bronnen, en de
status van elke ontwikkelstap via een klik op de cel in de strip. Alle
keuzemenu's worden gevoed door het blad Keuzelijsten.

## Terug naar Excel

De knop **Naar Excel** in de zijbalk schrijft een werkmap met zeven bladen:
Leads, Contactpersonen, Overeenkomsten, Bronnen, Voortgang, Ontwikkelstappen en
een blad Export met de telling en de peildatum. Kolomnamen en volgorde zijn
gelijk aan de databron, datums staan als echte datum in de cel (spelregel 3), en
elk blad heeft een vastgezette kopregel plus autofilter.

De kopregel staat in de export op regel 1 en in de databron op regel 4: plak het
blok onder de kopregel van het bijbehorende blad. De export volgt de filters
niet — er gaan altijd alle leads in, zodat er nooit per ongeluk een halve set
teruggeplaatst wordt.

Het xlsx-bestand wordt in de browser zelf geschreven: `zipOpslag` en
`werkmapBytes` bouwen het zipbestand en de XML met de hand. Dat scheelt een
bibliotheek van een CDN, waardoor het dashboard ook achter een streng netwerk
blijft werken en het bestand zelfstandig blijft. Er wordt niet gecomprimeerd
(zip-methode 0); dat is geldig en Excel opent het zonder klagen.

In de gepubliceerde versie loopt het opslaan via de downloadfunctie van het
platform, die de gebruiker om bevestiging vraagt. Los geopend valt het terug op
een gewone browserdownload.

## Voortgang met datums

De stappenstrip zet niet alleen de status. Via **Datums en toelichting** in
hetzelfde menu horen bij elke ontwikkelstap ook een startdatum, een geplande en
een werkelijke einddatum, een verantwoordelijke en een toelichting — de kolommen
die het blad Voortgang wel had maar die nooit gevuld waren.

Een stap op Gereed zetten vult de werkelijke einddatum met de dag van vandaag als
die nog leeg is; terugzetten maakt hem weer leeg. Datavalidatie controleert of
elke gereedmelding een datum heeft.

Daardoor staan de ontwikkelstappen nu ook op de tijdlijn, in een tweede baan
onder de mijlpalen: aqua voor werkelijk gehaald, koper voor gepland. Dat zijn
dezelfde statuskleuren als in de strip, dus er komt geen vierde kleur bij die met
de bestaande drie zou concurreren.

## Tekens en codering

Het bestand begint met `<meta charset="utf-8">` en de bron is volledig ASCII:
euroteken, kastlijntje en de status-tekens staan als `\uXXXX` in de scriptcode,
en `build_data.py` spuit de data met `ensure_ascii=True` in. Zonder die twee
dingen viel een browser die het bestand rechtstreeks van schijf opende terug op
Windows-1252 en werden `EUR`, `-` en `e-accent` onleesbaar.

De vinkjes, kruisjes en driehoekjes in de stappenstrip zijn getekende SVG's, geen
lettertekens: die glyphs zitten niet in elke mono-letterfamilie en vielen anders
terug op een vervangend blokje.

## Indeling

Zes pagina's achter een vaste zijbalk:

| Pagina | Wat erop staat |
| --- | --- |
| Portefeuille | Kerncijfers, gateladder, verdeling per doelgroep, status, fase en herkomst |
| Leads | Vier tabbladen: alle leads, mijlpaaldata, voortgang per stap, werkstromen |
| Lead opzoeken | Eén lead voluit: kerngegevens, tijdlijn, contacten, overeenkomsten, bronnen |
| Acties | Alles wat nog een handeling vraagt, op deadline |
| Datavalidatie | De spelregels uit de Leeswijzer, regel voor regel afgevinkt |
| Leeswijzer | Werken met dit scherm |

De opzet volgt het patroon van een portefeuilledashboard: vaste zijbalk,
paginakop met een filterstrook en een verversingsstempel, een tabrij met de
kerncijfers ernaast, dichte tabellen met een totaalregel, en panelen met een
kopbalk. De filters gelden voor de vier eerste pagina's tegelijk; Datavalidatie
kijkt bewust naar de hele databron en verbergt de filterstrook.

Het visuele idioom blijft van Smarteck: geen border-radius, Space Grotesk voor
display, IBM Plex voor tekst en cijfers.

## Bijwerken

```
python3 dashboard/tools/build_data.py dashboard/data/Smarteck_Leadtracker_Databron.xlsx
```

Het script leest de bladen Leads, Contactpersonen, Overeenkomsten, Bronnen,
Voortgang en Ontwikkelstappen plus de aannames, schrijft `data/leadtracker.json`
en zet diezelfde JSON tussen de markers `DATA-START` / `DATA-END` in de html.

Gekoppeld wordt op **kolomnaam**, niet op kolompositie — spelregel 5 uit de
Leeswijzer. Een hernoemde kolom valt daardoor zichtbaar om in het script, en
niet stilletjes in de browser.

## Wat het dashboard afleidt

Niets uit het blad Overzicht wordt overgenomen; alle tellingen worden opnieuw
berekend uit de invoerbladen, zodat ze meebewegen met de filters.

| Op het scherm | Waar het vandaan komt |
| --- | --- |
| Gewogen pijplijn | berekend, zie hieronder |
| Kans op FID per gate | blad Aannames, `M1..M4 bereikt` |
| Voortgang per lead | blad Voortgang, aandeel stappen op *Gereed* |
| Gateband boven de strip | blad Ontwikkelstappen, kolom *Gate* |
| Volgende stap | eerste stap op *Loopt*, anders de eerste op *Niet gestart* |
| Signalen | de spelregels uit de Leeswijzer, per regel nagelopen |
| Mijlpaaldata | Leads, Overeenkomsten, Bronnen en Contactpersonen |
| Tijdlijn per lead | mijlpaaldata plus de stapdatums, op een jaarschaal |
| Laatste stap gereed | hoogste werkelijke einddatum van een gereede stap |
| Volgende stap gepland | laagste geplande datum van een niet-gereede stap |

De peildatum voor verstreken deadlines is de dag van openen.

### Feemodel

Slaagkans en gewogen fee zijn niet los in te vullen; ze volgen uit de gate en de
verwachte fee. De initiatiefee is verdiend zodra M1 bereikt is en elk gate-aandeel
zodra die gate bereikt is; wat daarna nog komt telt mee maal de kans op FID van de
bereikte gate:

```
ontwikkelfee = fee - initiatiefee
verdiend     = initiatiefee + som van de aandelen tot en met de bereikte gate
resterend    = som van de aandelen na de bereikte gate
gewogen fee  = verdiend + resterend * kans(bereikte gate)
```

Dit model is afgeleid uit het blad Aannames en getoetst aan beide regels van het
werkboek: 555.000 op M2 geeft 332.400 en 250.000 op M1 geeft 70.000 — allebei
exact de waarde die het werkboek zelf noemt. Toets het bij twijfel tegen
`Smarteck_Engine2_Feemodel.xlsx`; de staffel, de gateverdeling en de kansen komen
alle uit het blad Aannames, dus een wijziging daar werkt meteen door.

Het blad Voortgang heeft geen enkele datum ingevuld — geen startdatum, geen
geplande en geen werkelijke einddatum. Daarom staan de ontwikkelstappen niet op
de tijdlijn en is er geen doorlooptijd te berekenen; de mijlpaaldata komen uit de
bladen die wél datums dragen. Datavalidatie meldt dit als openstaand punt.

## Merk

Alle tokens komen uit `design/README.md` — dezelfde `:root` als de website.
Geen border-radius, Space Grotesk voor display, IBM Plex Sans voor lopende
tekst, IBM Plex Mono voor labels en cijfers.

Twee contrastpunten die in `design/README.md` als bevinding staan, zijn hier
meteen goed gezet: op navy wordt `--zink-lt` gebruikt en niet `--zink` (2,78:1),
en koperkleurige tekst op een licht vlak staat op `--koper-dk` (6,5:1) in plaats
van `--koper` (3,9:1).

### Statuspalet — nieuw

De huisstijl had nog geen statuskleuren. Deze vijf zijn toegevoegd en gevalideerd
op onderscheidbaarheid, ook bij kleurenblindheid:

| Status | Licht | Donker | Teken |
| --- | --- | --- | --- |
| Gereed | `#1D8F91` (aqua) | `#4FB3B4` | ✓ |
| Loopt | `#BE612E` (koper) | `#E8A882` | ▸ |
| Geblokkeerd | `#8C1D4E` | `#E84E6B` | ✕ |
| Niet gestart | `#E7E2D8` | `#16354A` | — |
| Niet van toepassing | `#EFECE6` | `#13293A` | – |

Geblokkeerd is bewust *niet* de rode `#C0392B` uit het diagram op de homepage:
die ligt op ΔE 7,9 van koper en is daarmee zelfs met normaal kleurenzicht
nauwelijks van *Loopt* te onderscheiden. `#8C1D4E` ligt op ΔE 20,0.

Aqua en koper liggen bij protanopie op ΔE 7,8 — bruikbaar, maar alleen mét een
tweede drager. Vandaar dat elke cel naast de kleur een eigen teken draagt, elke
legenda-ingang een tekstlabel heeft en elke cel zijn status voluit in de tooltip
noemt. Kleur is nergens de enige drager van betekenis.

## Toegankelijkheid

Licht en donker zijn apart ontworpen, inclusief de niet-gestempelde
systeemstand. De stappenstrip is met het toetsenbord te doorlopen; elke cel
heeft een `aria-label` met stapnummer, naam en status, en de voortgangsbalk
heeft een tekstueel equivalent.
