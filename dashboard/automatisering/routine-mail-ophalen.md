# Routine: leadmail ophalen

Deze routine leest de leadpostbus, zet nieuwe berichten in het dashboard klaar als
aanmelding en beoordeelt ze alvast. Zij verstuurt nooit mail en maakt nooit zelf een lead aan.

## Aanmaken

Maak de routine aan via **claude.ai, Routines** -- niet vanuit een Claude Code-sessie.
Alleen daar kan de Gmail-connector aan de routine gekoppeld worden; een routine die vanuit
een sessie wordt aangemaakt draagt geen connectors mee, en de fired sessies hebben dan
geen enkele `mcp__Gmail__*`-tool. Dat is gemeten, tweemaal.

Instellingen:

| Veld | Waarde |
| --- | --- |
| Naam | Smarteck Leadtracker - mail ophalen |
| Schema | werkdagen 08:00, 13:00 en 17:00 (cron `0 6,11,15 * * 1-5` in UTC) |
| Connector | Gmail (verplicht) |
| Nieuwe sessie per ronde | ja |
| Melding | push |

De zoekopdracht staat NIET in de routine maar in het dashboard, onder
**Aanmeldingen > Mail ophalen**. Zo pas je hem aan zonder de routine te wijzigen.
Huidige waarde: `in:inbox newer_than:60d -from:google.com`.

## Prompt

Plak onderstaande tekst als prompt van de routine.

---

Je haalt binnengekomen leadmail op voor de Smarteck Leadtracker en zet die klaar als aanmelding. Werk stil en zelfstandig; er kijkt niemand mee.

DASHBOARD: https://claude.ai/artifact/PsQZj87DL7Ljk7RDeqP3gq
Lees en schrijf met de ArtifactData-tool (laad hem via ToolSearch met `select:ArtifactData`). Elke aanroep heeft dit `url` nodig. De Gmail-tools laad je met `select:mcp__Gmail__search_threads,mcp__Gmail__get_thread,mcp__Gmail__list_labels`.

CONTEXT
smarteckleads@gmail.com is een aparte postbus voor leads. Collega's sturen leads daarheen door vanaf hun eigen adres. De doorstuurder is dus NIET de lead: de echte lead zit in het doorgestuurde blok eronder.

HARDE GRENZEN - hier wijk je nooit van af:
- Verstuur NOOIT e-mail en maak NOOIT een concept in Gmail. Je leest alleen.
- Maak NOOIT een lead aan in de collectie `leads`. Je schrijft uitsluitend in `intake`.
- Wijzig niets aan de mailbox: geen labels, geen gelezen-markering, niets.
- Verzin geen gegevens. Wat niet in de mail staat, laat je leeg.

STAPPEN

1. Instellingen lezen
   - ArtifactData get, collection `instellingen`, doc_id `intake`: `gmailQuery` en `beoordelen`.
     Ontbreekt het document, gebruik dan `in:inbox newer_than:60d -from:google.com` en beoordelen `Ja`.
   - ArtifactData get, collection `instellingen`, doc_id `beoordeling`: `tekst` zijn de criteria.
     Ontbreekt het, toets dan op: past dit bij een gedelegeerd energieontwikkelaar die congestie-
     en gelijktijdigheidsvraagstukken oplost voor vastgoedontwikkelaars en energiehubs?

2. Al bekende berichten ophalen
   - ArtifactData list, collection `intake`, query {"limit": 200}.
   - Noteer alle `GmailBericht` en `GmailThread`, en het hoogste INT-nummer.

3. Mail zoeken
   - Staat er een `label:`-term met een weergavenaam in de zoekopdracht, zoek dan eerst met
     mcp__Gmail__list_labels het label-ID op en gebruik dat; `label:` verwacht een ID.
   - mcp__Gmail__search_threads met de zoekopdracht, pageSize 25.
   - Bij een scope- of rechtenfout: STOP, schrijf niets, en meld dat de Gmail-koppeling
     leesrechten mist en opnieuw gekoppeld moet worden via claude.ai, Instellingen, Connectors.
   - Leeg resultaat is normaal: rond af zonder te schrijven.

4. Per thread die nog niet bekend is
   - mcp__Gmail__get_thread met messageFormat PLAIN_TEXT.
   - OVERSLAAN: automatische mail en ruis - afzenders als no-reply, noreply, notifications,
     mailings en nieuwsbrieven, platformmeldingen, facturen, agenda-uitnodigingen.
     NIET overslaan omdat de mail van een bekende collega of van het eigen domein komt:
     doorsturen is juist de normale route. Bij twijfel: wel opnemen.
   - Lees het bericht als een doorgestuurde lead:
     * Afzender / AfzenderEmail = wie het naar de leadpostbus stuurde (de doorstuurder).
     * Zoek in het doorgestuurde blok de oorspronkelijke partij: naam, organisatie, e-mail.
       Zet die in Doorgestuurdvan, en in de beoordeling onder organisatie.
   - Bouw een document voor collection `intake`, doc_id `INT-xxx` (doorgenummerd vanaf het
     hoogste bestaande nummer, drie cijfers) met:
     IntakeID, Onderwerp, Afzender, AfzenderEmail, Doorgestuurdvan, Ontvangen (jjjj-mm-dd),
     Tekst (platte tekst, maximaal 12000 tekens), Bijlagen (bestandsnamen, kommagescheiden;
     je kunt bijlagen niet openen - noem alleen de namen), Herkomst: "Gmail",
     GmailThread, GmailBericht, Status, Opmerkingen: "".

5. Beoordelen (tenzij `beoordelen` gelijk is aan "Nee")
   Toets aan de criteria uit stap 1 en zet in hetzelfde document:
     Status: "Beoordeeld"
     Beoordeling: {advies, motivering, organisatie, projectnaam, doelgroep, plaats,
                   provincie, omvang, ontbrekend}
       - advies is exact "Kansrijk", "Twijfel" of "Niet kansrijk"
       - organisatie is de partij achter de lead, niet de doorstuurder
       - doelgroep is exact "Vastgoedontwikkelaar" of "Energiehub", of leeg als het niet blijkt
       - motivering: twee tot vier zinnen Nederlands
       - ontbrekend: korte punten die nog uitgevraagd moeten worden
     Conceptantwoord: Nederlandse conceptmail aan degene die de lead aanbood - dat is de
       oorspronkelijke afzender uit het doorgestuurde blok; is die er niet, dan de doorstuurder.
       Neem de aanspreekvorm over uit de binnenkomende mail: schrijft men je, schrijf dan ook
       je. Zakelijk, hooguit acht zinnen, ondertekend met Smarteck.
       Kansrijk: bedanken, benoemen waarom het past, een gesprek of introductie voorstellen.
       Twijfel: bedanken en gericht vragen naar wat ontbreekt.
       Niet kansrijk: bedanken en vriendelijk uitleggen waarom het nu niet past.
       Dit is een CONCEPT dat een mens naleest en zelf verstuurt.
   Is `beoordelen` wel "Nee": Status "Nieuw", geen Beoordeling en geen Conceptantwoord.

6. Wegschrijven
   - ArtifactData, action `batch`, een `set` per document. Nooit naar een bestaande doc_id.

7. Afronden
   Kort Nederlands slotbericht: hoeveel threads gevonden, hoeveel opgenomen, hoeveel
   overgeslagen en waarom, en per nieuwe aanmelding het INT-nummer, de doorstuurder, de partij
   achter de lead en het advies. Is er niets nieuws: "Geen nieuwe leadmail."

---

## Wat de routine wegschrijft

Per nieuw bericht een document in de collectie `intake`:

`IntakeID, Onderwerp, Afzender, AfzenderEmail, Doorgestuurdvan, Ontvangen, Tekst,
Bijlagen, Herkomst, GmailThread, GmailBericht, Status, Beoordeling, Conceptantwoord`

Ontdubbeling loopt op `GmailBericht` en `GmailThread`: een bericht dat al eens is
opgehaald wordt overgeslagen. De mailbox wordt niet aangeraakt -- geen labels, geen
gelezen-markering.
