import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
total = 0
for i in range(1, 6):
    f = f"05_Text_Summarization_scenario_{i}_ground_truths.json"
    data = json.load(open(f, "r", encoding="utf-8"))
    answered = sum(1 for q in data if q.get("is_answer_present") == True)
    print(f"S{i}: {answered}/{len(data)}")
    total += answered
print(f"TOTAL: {total}/300 ({total/300*100:.1f}%)")
