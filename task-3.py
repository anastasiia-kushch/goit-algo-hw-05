from pathlib import Path


with open(Path('text/article_2.txt'), 'rb', encoding='utf-8') as file:
    text = file.readlines()

# path = Path('') 