"""Count predictive vs QnA questions per task-scenario pair."""
import json
from pathlib import Path

def main():
    # Use the root-level generated_questions folder
    generated_dir = Path(__file__).parent.parent / 'generated_questions'
    
    results = []
    for f in sorted(generated_dir.glob('*.json')):
        data = json.load(open(f))
        task = data['task']
        scenario = f.stem.split('_scenario')[1]
        
        # Use the explicit question_type field
        predictive = sum(1 for q in data['questions'] if q.get('question_type', '').lower() == 'predictive')
        qna = sum(1 for q in data['questions'] if q.get('question_type', '').lower() == 'qna')
        
        results.append((task, scenario, predictive, qna, len(data['questions'])))
    
    # Print header
    print(f"{'Task':<28} {'Scen':<5} {'Pred':<6} {'QnA':<6} {'Total':<6}")
    print('-' * 55)
    
    # Print results
    current_task = None
    for task, scen, pred, qna, total in results:
        if current_task and current_task != task:
            print()  # Add blank line between tasks
        current_task = task
        print(f"{task:<28} {scen:<5} {pred:<6} {qna:<6} {total:<6}")
    
    # Summary
    print('\n' + '=' * 55)
    total_pred = sum(r[2] for r in results)
    total_qna = sum(r[3] for r in results)
    total_all = sum(r[4] for r in results)
    print(f"{'TOTAL':<28} {'':<5} {total_pred:<6} {total_qna:<6} {total_all:<6}")

if __name__ == '__main__':
    main()
