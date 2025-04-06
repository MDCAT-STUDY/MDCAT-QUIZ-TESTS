import streamlit as st
import datetime
import json
import os
import pandas as pd

# 1. Login/Name Input
st.title("NMDCAT AI Quiz Portal")
student_name = st.text_input("Enter your name to begin:", "")

# 2. Load Chapter list
chapters = ["Biology - Cell", "Chemistry - Bonding", "Physics - Motion"]
selected_chapter = st.selectbox("Select Chapter to Start Quiz:", chapters)

if student_name and selected_chapter:
    if st.button("Start Quiz"):
        st.session_state['start_quiz'] = True

# 3. Quiz Mode (only after start)
if st.session_state.get('start_quiz'):
    # Replace this with AI-generated questions for the selected chapter
    quiz = [
        {"question": "Where does glycolysis occur?", "options": ["A. Cytoplasm", "B. Nucleus", "C. Mitochondria", "D. Ribosome"], "answer": "A", "explanation": "Glycolysis takes place in the cytoplasm."},
        {"question": "Which bond is the strongest?", "options": ["A. Ionic", "B. Covalent", "C. Hydrogen", "D. Metallic"], "answer": "B", "explanation": "Covalent bonds are strongest due to electron sharing."}
    ]

    score = 0
    answers = []

    for i, q in enumerate(quiz):
        st.subheader(f"Q{i+1}: {q['question']}")
        selected = st.radio("Your Answer:", q['options'], key=i)
        answers.append({
            "question": q["question"],
            "selected": selected,
            "correct": selected.startswith(q["answer"]),
            "explanation": q["explanation"]
        })

    if st.button("Submit Quiz"):
        score = sum(1 for a in answers if a["correct"])
        timestamp = datetime.datetime.now().isoformat()
        result = {
            "name": student_name,
            "chapter": selected_chapter,
            "score": score,
            "total": len(quiz),
            "answers": answers,
            "timestamp": timestamp
        }

        # 4. Save to local file
        os.makedirs("results", exist_ok=True)
        filename = f"results/{student_name.replace(' ', '_')}_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)

        st.success(f"Quiz submitted! Score: {score}/{len(quiz)}")
        st.markdown("### Answer Summary:")
        for a in answers:
            st.markdown(f"- **Q:** {a['question']}  \n**Your Answer:** {a['selected']}  \n**Correct:** {'✅' if a['correct'] else '❌'}  \n**Explanation:** {a['explanation']}")
