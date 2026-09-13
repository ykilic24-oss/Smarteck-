#!/usr/bin/env python3
"""Leest de Excel-databron en schrijft de JSON die het dashboard inleest.

Gebruik:
    python3 dashboard/tools/build_data.py Smarteck_Leadtracker_Databron.xlsx

Schrijft dashboard/data/leadtracker.json en injecteert diezelfde JSON tussen de
markers DATA-START / DATA-END in dashboard/Smarteck_Leadtracker_Dashboard.html,
zodat het dashboard een los bestand blijft dat zonder server opent.

Gekoppeld wordt op kolomnaam, niet op kolompositie -- spelregel 5 uit de
Leeswijzer. Een hernoemde kolom valt hier om, niet stil in de browser.
"""

import datetime as _dt
import json
import pathlib
import sys

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "dashboard" / "data" / "leadtracker.json"
OUT_HTML = ROOT / "dashboard" / "Smarteck_Leadtracker_Dashboard.html"

# Blad -> rij waarop de kolomkoppen staan. De bladen hebben een titel- en een
# toelichtingsregel boven de tabel.
SHEETS = {
    "Leads": 4,
    "Contactpersonen": 4,
    "Overeenkomsten": 4,
    "Bronnen": 4,
    "Voortgang": 4,
    "Ontwikkelstappen": 4,
}


def clean(value):
    if value is None:
        return ""
    if isinstance(value, (_dt.datetime, _dt.date)):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        return value.strip()
    return value


def read_table(ws, header_row):
    headers = [clean(c.value) for c in ws[header_row]]
    rows = []
    for excel_row in ws.iter_rows(min_row=header_row + 1):
        record = {}
        for header, cell in zip(headers, excel_row):
            if header:
                record[header] = clean(cell.value)
        # Een regel telt alleen mee als de eerste kolom (het ID) gevuld is.
        if record.get(headers[0]):
            rows.append(record)
    return rows


def read_aannames(ws):
    """Het blad Aannames is een label/waarde-lijst, geen tabel."""
    pairs = {}
    for row in ws.iter_rows(values_only=True):
        cells = [clean(c) for c in row]
        label = cells[0] if cells else ""
        if not isinstance(label, str) or not label:
            continue
        waarden = [c for c in cells[1:] if c != ""]
        if waarden:
            pairs[label] = waarden
    return pairs


def main():
    if len(sys.argv) < 2:
        sys.exit("gebruik: build_data.py <pad naar databron.xlsx>")
    src = pathlib.Path(sys.argv[1])
    wb = openpyxl.load_workbook(src, data_only=True)

    data = {name: read_table(wb[name], row) for name, row in SHEETS.items()}
    data["Aannames"] = read_aannames(wb["Aannames"])
    data["_bron"] = {
        "bestand": src.name,
        "gelezen_op": _dt.date.today().isoformat(),
    }

    payload = json.dumps(data, ensure_ascii=False, indent=1)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(payload + "\n", encoding="utf-8")
    print(f"geschreven: {OUT_JSON.relative_to(ROOT)}")
    for name in SHEETS:
        print(f"  {name}: {len(data[name])} regels")

    if OUT_HTML.exists():
        html = OUT_HTML.read_text(encoding="utf-8")
        start, end = "/* DATA-START */", "/* DATA-END */"
        if start in html and end in html:
            head = html.split(start)[0]
            tail = html.split(end)[1]
            OUT_HTML.write_text(
                f"{head}{start}\nconst DATA = {payload};\n{end}{tail}",
                encoding="utf-8",
            )
            print(f"bijgewerkt: {OUT_HTML.relative_to(ROOT)}")
        else:
            print("let op: markers DATA-START/DATA-END niet gevonden in de html")


if __name__ == "__main__":
    main()
