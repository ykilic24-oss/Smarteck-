# Smarteck Leadtracker — dashboard

`Smarteck_Leadtracker_Dashboard.html` is één bestand. Logo en data zitten erin;
alleen de webfonts komen van buiten. Openen kan met een dubbelklik, vanaf een
netwerkschijf of vanuit SharePoint — er is geen server nodig.

De databron blijft het werkboek. Dit scherm leest, het schrijft niet.

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
| Gewogen pijplijn | som van *Gewogen fee* over de zichtbare leads |
| Kans op FID per gate | blad Aannames, `M1..M4 bereikt` |
| Voortgang per lead | blad Voortgang, aandeel stappen op *Gereed* |
| Gateband boven de strip | blad Ontwikkelstappen, kolom *Gate* |
| Volgende stap | eerste stap op *Loopt*, anders de eerste op *Niet gestart* |
| Signalen | de spelregels uit de Leeswijzer, per regel nagelopen |
| Mijlpaaldata | Leads, Overeenkomsten, Bronnen en Contactpersonen |
| Tijdlijn per lead | dezelfde mijlpaaldata, op een jaarschaal |

De peildatum voor verstreken deadlines staat als `VANDAAG` boven in het script.

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
