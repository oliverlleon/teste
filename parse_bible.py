from rtf_converter import rtf_to_txt
import re
import json
import os

def parse_bible_text(text_content):
    bible_data = {}
    current_chapter = None
    last_verse = None

    # Regex to find chapter titles, e.g., "Capítulo 1" or "Salmo 1"
    chapter_regex = re.compile(r'^(?:Capítulo|Salmo)\s+(\d+)', re.IGNORECASE)
    # Regex to find a verse number at the start of a line
    verse_regex = re.compile(r'^(\d+)\s+(.*)')

    for line in text_content.splitlines():
        line = line.strip()
        if not line:
            continue

        chapter_match = chapter_regex.match(line)
        if chapter_match:
            current_chapter = chapter_match.group(1)
            if current_chapter not in bible_data:
                bible_data[current_chapter] = {}
            last_verse = None # Reset last verse when a new chapter starts
            continue

        if current_chapter:
            verse_match = verse_regex.match(line)
            if verse_match:
                verse_num = verse_match.group(1)
                verse_text = verse_match.group(2).strip()
                bible_data[current_chapter][verse_num] = verse_text
                last_verse = verse_num
            elif last_verse and line: # This is a continuation of the previous verse
                bible_data[current_chapter][last_verse] += " " + line

    return bible_data

def main():
    """
    Main function to parse all Bible RTF files.
    """
    bible_dir = "bible"
    output_dir = "bible_json"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    book_mapping = {
        "01_Ge_T": "ge", "02_Ex_T": "ex", "03_Le_T": "le", "04_Nu_T": "nu",
        "05_De_T": "de", "06_Jos_T": "jos", "07_Jz_T": "jz", "08_Ru_T": "ru",
        "09_1Sa_T": "1sa", "10_2Sa_T": "2sa", "11_1Rs_T": "1rs", "12_2Rs_T": "2rs",
        "13_1Cr_T": "1cr", "14_2Cr_T": "2cr", "15_Esd_T": "esd", "16_Ne_T": "ne",
        "17_Est_T": "est", "18_Job_T": "job", "19_Ps_T": "sal", "20_Pr_T": "pr",
        "21_Ec_T": "ec", "22_Ca_T": "ca", "23_Is_T": "is", "24_Je_T": "je",
        "25_Lm_T": "lm", "26_Ez_T": "ez", "27_Da_T": "da", "28_Os_T": "os",
        "29_Jl_T": "jl", "30_Am_T": "am", "31_Ob_T": "ob", "32_Jn_T": "jn",
        "33_Mq_T": "mq", "34_Na_T": "na", "35_Hab_T": "hab", "36_Zf_T": "zf",
        "37_Ag_T": "ag", "38_Zc_T": "zc", "39_Ml_T": "ml", "40_Mt_T": "mt",
        "41_Mr_T": "mr", "42_Lu_T": "lu", "43_Jo_T": "jo", "44_At_T": "at",
        "45_Ro_T": "ro", "46_1Co_T": "1co", "47_2Co_T": "2co", "48_Gá_T": "ga",
        "49_Ef_T": "ef", "50_Fl_T": "flp", "51_Col_T": "col", "52_1Te_T": "1te",
        "53_2Te_T": "2te", "54_1Ti_T": "1ti", "55_2Ti_T": "2ti", "56_Tit_T": "tit",
        "57_Flm_T": "fm", "58_He_T": "he", "59_Tg_T": "tg", "60_1Pe_T": "1pe",
        "61_2Pe_T": "2pe", "62_1Jo_T": "1jo", "63_2Jo_T": "2jo", "64_3Jo_T": "3jo",
        "65_Jd_T": "jd", "66_Re_T": "re"
    }

    folder_path = bible_dir

    if not os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' was not found. Exiting.")
        return

    for rtf_file in os.listdir(folder_path):
        if rtf_file.endswith(".rtf"):
            book_abbr = None
            for key, value in book_mapping.items():
                if key in rtf_file:
                    book_abbr = value
                    break

            if book_abbr:
                print(f"Processing {rtf_file} as {book_abbr}")
                try:
                    rtf_path = os.path.join(folder_path, rtf_file)
                    with open(rtf_path, 'r', encoding='latin1') as f:
                        rtf_content = f.read()

                    text_content = rtf_to_txt(rtf_content)

                    json_data = parse_bible_text(text_content)

                    json_filename = f"{book_abbr}.json"
                    output_path = os.path.join(output_dir, json_filename)
                    with open(output_path, 'w', encoding='utf8') as jf:
                        json.dump(json_data, jf, ensure_ascii=False, indent=2)
                    print(f"File {json_filename} saved successfully.")

                except Exception as e:
                    print(f"Error processing file {rtf_file}: {e}")

if __name__ == "__main__":
    main()
