import os
import json
import re
from striprtf.striprtf import rtf_to_text

def parse_rtf_to_json(rtf_path, json_path):
    print(f"Starting to parse {rtf_path}")
    # Mapping from RTF filename abbreviations to full book names
    book_name_map = {
        "Ge": "Gênesis", "Ex": "Êxodo", "Le": "Levítico", "Nu": "Números", "De": "Deuteronômio",
        "Jos": "Josué", "Jg": "Juízes", "Ru": "Rute", "1Sa": "1 Samuel", "2Sa": "2 Samuel",
        "1Ki": "1 Reis", "2Ki": "2 Reis", "1Ch": "1 Crônicas", "2Ch": "2 Crônicas", "Ezr": "Esdras",
        "Ne": "Neemias", "Es": "Ester", "Job": "Jó", "Ps": "Salmos", "Pr": "Provérbios",
        "Ec": "Eclesiastes", "Ca": "Cântico de Salomão", "Isa": "Isaías", "Jer": "Jeremias",
        "La": "Lamentações", "Eze": "Ezequiel", "Da": "Daniel", "Ho": "Oseias", "Joe": "Joel",
        "Am": "Amós", "Ob": "Obadias", "Jon": "Jonas", "Mic": "Miqueias", "Na": "Naum",
        "Hab": "Habacuque", "Zep": "Sofonias", "Hag": "Ageu", "Zec": "Zacarias", "Mal": "Malaquias",
        "Mt": "Mateus", "Mr": "Marcos", "Lu": "Lucas", "Joh": "João", "Ac": "Atos",
        "Ro": "Romanos", "1Co": "1 Coríntios", "2Co": "2 Coríntios", "Ga": "Gálatas", "Eph": "Efésios",
        "Php": "Filipenses", "Col": "Colossenses", "1Th": "1 Tessalonicenses", "2Th": "2 Tessalonicenses",
        "1Ti": "1 Timóteo", "2Ti": "2 Timóteo", "Tit": "Tito", "Phm": "Filemom", "Heb": "Hebreus",
        "Jas": "Tiago", "1Pe": "1 Pedro", "2Pe": "2 Pedro", "1Jo": "1 João", "2Jo": "2 João",
        "3Jo": "3 João", "Jude": "Judas", "Re": "Apocalipse"
    }

    with open(rtf_path, 'r', encoding='latin-1') as f:
        rtf_content = f.read()

    print("  Converting RTF to text...")
    text_content = rtf_to_text(rtf_content, errors="ignore")

    lines = text_content.split('\n')

    bible_book = {}
    current_chapter = None

    chapter_regex = re.compile(r'Capítulo (\d+)')
    verse_regex = re.compile(r'^(\d+)\s(.+)')

    print("  Parsing lines...")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        chapter_match = chapter_regex.search(line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            bible_book[current_chapter] = {}
            continue

        if current_chapter:
            verse_match = verse_regex.match(line)
            if verse_match:
                verse_number = verse_match.group(1)
                verse_text = verse_match.group(2).strip()
                bible_book[current_chapter][verse_number] = verse_text

    # Get the book abbreviation from the filename
    abbr = os.path.basename(rtf_path).split('_')[2]

    # Save to JSON using the abbreviation
    json_filename = os.path.join(json_path, f'{abbr.lower()}.json')

    if os.path.exists(json_filename):
        print(f"  Skipping {json_filename}, already exists.")
        return

    print(f"  Saving to {json_filename}...")
    with open(json_filename, 'w', encoding='utf-8') as jf:
        json.dump(bible_book, jf, ensure_ascii=False, indent=4)
    print(f"Finished parsing {rtf_path}")

if __name__ == '__main__':
    rtf_dir = 'bible'
    json_dir = 'bible_json'

    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    for filename in sorted(os.listdir(rtf_dir), reverse=True):
        if filename.endswith('.rtf'):
            rtf_filepath = os.path.join(rtf_dir, filename)
            parse_rtf_to_json(rtf_filepath, json_dir)

    print('Done.')
