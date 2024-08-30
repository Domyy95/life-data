import os
import random
from settings import margin
from datetime import datetime

obsidian_daily_notes_directory = "/Users/dominic/Personal/second-brain/Resources/Daily notes"
daily_notes = [f for f in os.listdir(obsidian_daily_notes_directory) if f.endswith(".md")]
current_date = datetime.now()
day_number = current_date.day

tags = {
    0: "#ideas",
    1: "#tasks",
    2: "#knowledge",
}

def extract_tag_notes(filename: str, target_tag: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    tag_exists = any(target_tag in line for line in lines)
    if not tag_exists:
        return None

    result = []
    reading = False
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            if target_tag in line:
                reading = True
            else:
                reading = False
    
        elif reading:
            result.append(line)
    
    return result


def extract_tag_from_random_file(tag: str, daily_notes: list) -> str:
    result = None
    while result == None:
        extracted_file = random.choice(daily_notes)
        file_path = os.path.join(obsidian_daily_notes_directory, extracted_file)
        result = extract_tag_notes(file_path, tag)
        
    result.insert(0, f"From {extracted_file[:-3]}:")
    return result

def random_tag_note():
    today_tag = tags[day_number % len(tags)]
    print(f"Today tag: {today_tag}")
    re =extract_tag_from_random_file(today_tag, daily_notes)
    for s in re:  
        print(s)

    print(margin)

