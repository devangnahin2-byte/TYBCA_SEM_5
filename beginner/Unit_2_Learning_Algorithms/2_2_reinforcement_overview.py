import streamlit as st

st.set_page_config(page_title="Reinforcement Learning Intro", page_icon="🤖")

st.title("Reinforcement Learning in Education")
st.header("How Agents Learn by Doing")

st.markdown("""
Unlike supervised learning where we give the model answers, in RL, an **Agent** learns to achieve a **Goal** in an **Environment** by performing **Actions** and receiving **Rewards** or **Penalties**.

Imagine building an AI agent that creates the best possible study timetable for a student.

1. **Environment:** The student's available time and subjects.
2. **Agent:** Our AI timetable creator.
3. **Action:** Assigning a subject to a time slot.
4. **Reward (+1):** Agent assigned a subject when the student is most awake.
5. **Penalty (-1):** Agent assigned heavy math at midnight.

""")

st.info("Over many tries, the agent learns the 'policy' (rules) that get the highest total reward, ending up with the perfect personalized timetable!")

if st.button("Simulate Learning Step"):
    import random
    action = random.choice(["Math at 10 AM", "Physics at 1 AM", "Break time after lunch"])
    
    if "1 AM" in action:
        st.error(f"Action: '{action}'. Reward: -5 (Student is asleep!)")
    elif "Break" in action:
        st.success(f"Action: '{action}'. Reward: +2 (A much needed rest!)")
    else:
        st.success(f"Action: '{action}'. Reward: +3 (Good time to study!)")

st.divider()
with st.expander("💻 View Source Code"):
    with open(__file__, "r", encoding="utf-8") as f:
        st.code(f.read(), language="python")
