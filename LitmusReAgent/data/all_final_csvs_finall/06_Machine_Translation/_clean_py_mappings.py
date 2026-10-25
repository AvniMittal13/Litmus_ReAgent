"""Clean .py mapping files for Machine Translation - remove Cat A and Cat B entries."""
import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

cat_a_models = [
    'Adam optimizer', 'fasttext', 'LaBSE', 'SentencePiece',
    'Various participant systems', 'Various systems',
    'various MT systems', 'various LLMs',
]

nllb_remove_langs = {'Bodo', 'Konkani', 'Bislama', 'Corsican', 'Hmong', 'Latin'}

for fname in ['06_Machine_Translation_language_models_mapping.py', 
              'reduced_06_machine_translation_language_models_mapping.py']:
    if not os.path.exists(fname):
        print(f'{fname}: NOT FOUND')
        continue
        
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove Cat A models
    for bad in cat_a_models:
        content = content.replace(f"'{bad}', ", '')
        content = content.replace(f", '{bad}'", '')
        content = content.replace(f"'{bad}'", '')
    
    # Clean up any empty lists or double commas
    content = content.replace(', , ', ', ')
    content = content.replace('[, ', '[')
    content = content.replace(', ]', ']')
    
    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{fname}: cleaned')
    else:
        print(f'{fname}: no changes')

print('Done')
