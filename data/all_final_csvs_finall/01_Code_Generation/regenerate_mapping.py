"""Script to regenerate language_models_mapping.py from CSV data."""
import csv
import re
from collections import defaultdict

# Read CSV and build mapping
language_models = defaultdict(set)

with open('combined_01_code_generation.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        languages_str = row.get('Languages', '')
        models_str = row.get('Models', '')
        
        # Parse languages - handle parenthetical notes
        languages_str = re.sub(r'\([^)]*\)', '', languages_str)
        languages = [l.strip() for l in languages_str.split(',') if l.strip()]
        
        # Parse models - clean up various formats
        models_raw = re.sub(r'\s*\([^)]*\)', '', models_str)
        models = [m.strip() for m in re.split(r',\s*', models_raw) if m.strip()]
        
        for lang in languages:
            if any(skip in lang.lower() for skip in ['total', 'programming', 'code']):
                continue
            for model in models:
                if model:
                    language_models[lang].add(model)

sorted_mapping = {k: sorted(v) for k, v in sorted(language_models.items())}

# Build content
lines = []
lines.append('"""')
lines.append('Language to Models Mapping for 01_Code_Generation')
lines.append('Generated from combined CSV data')
lines.append(f'Total languages: {len(sorted_mapping)}')
lines.append('"""')
lines.append('')
lines.append('from collections import Counter')
lines.append('')
lines.append('# Language to Models Mapping')
lines.append('# Format: language: [list of models benchmarked on this language]')
lines.append('')
lines.append('LANGUAGE_MODELS_MAPPING = {')

for lang, models in sorted_mapping.items():
    lines.append(f'    "{lang}": {models},')

lines.append('}')
lines.append('')
lines.append('# Statistics')
lines.append('TOTAL_LANGUAGES = len(LANGUAGE_MODELS_MAPPING)')
lines.append('TOTAL_UNIQUE_MODELS = len(set(model for models in LANGUAGE_MODELS_MAPPING.values() for model in models))')
lines.append('')
lines.append('')
lines.append('def get_models_for_language(language):')
lines.append('    """Get all models benchmarked for a specific language."""')
lines.append('    return LANGUAGE_MODELS_MAPPING.get(language, [])')
lines.append('')
lines.append('')
lines.append('def get_languages_for_model(model):')
lines.append('    """Get all languages that a specific model has been benchmarked on."""')
lines.append('    return [lang for lang, models in LANGUAGE_MODELS_MAPPING.items() if model in models]')
lines.append('')
lines.append('')
lines.append('def get_all_languages():')
lines.append('    """Get all available languages."""')
lines.append('    return list(LANGUAGE_MODELS_MAPPING.keys())')
lines.append('')
lines.append('')
lines.append('def get_all_models():')
lines.append('    """Get all unique models."""')
lines.append('    all_models = set()')
lines.append('    for models in LANGUAGE_MODELS_MAPPING.values():')
lines.append('        if isinstance(models, list):')
lines.append('            all_models.update(models)')
lines.append('    return sorted(all_models)')
lines.append('')
lines.append('')
lines.append('def get_language_statistics():')
lines.append('    """Get statistics about each language\'s model coverage."""')
lines.append('    stats = {}')
lines.append('    for language, models in LANGUAGE_MODELS_MAPPING.items():')
lines.append('        if isinstance(models, list):')
lines.append('            model_list = models')
lines.append('        else:')
lines.append('            model_list = [models] if models else []')
lines.append('        stats[language] = {')
lines.append('            \'model_count\': len(model_list),')
lines.append('            \'models\': sorted(model_list)')
lines.append('        }')
lines.append('    return stats')
lines.append('')
lines.append('')
lines.append('def get_model_statistics():')
lines.append('    """Get detailed statistics about model coverage."""')
lines.append('    model_counter = Counter()')
lines.append('    for models in LANGUAGE_MODELS_MAPPING.values():')
lines.append('        if isinstance(models, list):')
lines.append('            for model in models:')
lines.append('                model_counter[model] += 1')
lines.append('        else:')
lines.append('            model_counter[models] += 1')
lines.append('    return dict(model_counter.most_common())')
lines.append('')
lines.append('')
lines.append('def print_summary():')
lines.append('    """Print a summary of the mapping."""')
lines.append('    print(f"Task: 01_Code_Generation")')
lines.append('    print(f"Total Languages: {TOTAL_LANGUAGES}")')
lines.append('    print(f"Total Unique Models: {TOTAL_UNIQUE_MODELS}")')
lines.append('')
lines.append('')
lines.append('if __name__ == "__main__":')
lines.append('    print_summary()')

with open('01_Code_Generation_language_models_mapping.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'Generated mapping with {len(sorted_mapping)} languages')
print(f'Languages: {list(sorted_mapping.keys())}')
