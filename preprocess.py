import os
import sys
import re
import shutil

renames = {
    "king-knut": "King Knut",
    "ta'ahsu": "Ta'ahsu",
    "andoryx-lukather": "Andoryx Lukather"
}

character_names = {
    "Luvon",
    "Hulnir",
    "Geo",
    "Hasselhoff",
    "Kella",
    "Sashka",
    # Turner's Table
    "Fen",
    "Heimer",
    "Grizz",
    "Sixela"
}

name_prefix=r"(?<![\[>\*])"
name_suffix=r"(?=[\. ])"

def update_links(post_file_path, character_mapping):
    with open(post_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    updated = False

    for character_name, character_file in character_mapping.items():
        #print("MATCHING: ", character_name)
        name = renames[character_name]
        # Use a case-insensitive regular expression to find references to the character
        # TODO: make this into a real pattern match.
        regex_pattern = re.compile(name_prefix + re.escape(name) + name_suffix, re.IGNORECASE)
        for m in regex_pattern.finditer(content):
            #print("MATCH: ", content[m.start() - 5:m.end()+5])
            updated=True
        # content = regex_pattern.sub(f'[{{% link {character_file} %}}]', content)

    # Now match characters that don't have a file
    for name in character_names:
        #print("MATCHING: ", name)
        regex_pattern = name_prefix + re.escape(name) + name_suffix
        #print(regex_pattern)
        for m in re.finditer(regex_pattern, content):
            #print("MATCH: ", content[m.start() - 5:m.end()+5])
            updated=True
        content = re.sub(regex_pattern, f"**{name}**", content)

    # Create a backup of the original file in the tmp directory
    backup_dir = os.path.join(os.getcwd(), 'tmp')
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(post_file_path, os.path.join(backup_dir, os.path.basename(post_file_path)))

    with open(post_file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return updated

def main():
    posts_directory = "_posts"
    characters_directory = "_characters"

    character_mapping = {}

    # Create a mapping of character names to their corresponding markdown files
    for character_file_name in os.listdir(characters_directory):
        if character_file_name.endswith(".md"):
            character_name = os.path.splitext(character_file_name)[0]
            character_mapping[character_name] = os.path.join(characters_directory, character_file_name)

    #print(character_mapping)

    # Update links in each post file
    for post_file_name in os.listdir(posts_directory):
        #print(post_file_name)
        if post_file_name.endswith(".md"):
            post_file_path = os.path.join(posts_directory, post_file_name)
            updated = update_links(post_file_path, character_mapping)
            if updated:
                #print(f'Links updated in {post_file_name}')
                sys.stdout.write(post_file_path + " ")

if __name__ == "__main__":
    main()

