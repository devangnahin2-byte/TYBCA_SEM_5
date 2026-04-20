import streamlit as st
import numpy as np
import time

st.title("Unit 2.2: Reinforcement Learning Overview")
st.markdown("### Q-Learning Simple Grid Navigation")

st.write("Reinforcement learning involves an agent learning to make decisions by performing actions in an environment to maximize cumulative reward.")

grid_size = 5
goal_state = (4, 4)
st.write(f"**Environment:** {grid_size}x{grid_size} Grid. **Goal:** Bottom-right corner.")

st.info("Because RL training loops can be intensive, here we demonstrate a simple visual flow of an agent exploring a grid.")

start = st.button("Simulate Random Agent Run")

if start:
    grid = np.zeros((grid_size, grid_size))
    agent_pos = [0, 0]
    
    chart_placeholder = st.empty()
    steps = 0
    max_steps = 30
    
    while tuple(agent_pos) != goal_state and steps < max_steps:
        viz_grid = np.copy(grid)
        viz_grid[agent_pos[0], agent_pos[1]] = 1 # Agent
        viz_grid[goal_state[0], goal_state[1]] = 2 # Goal
        
        st.write(f"Step: {steps}")
        chart_placeholder.dataframe(viz_grid)
        
        action = np.random.choice(['U', 'D', 'L', 'R'])
        
        if action == 'U' and agent_pos[0] > 0: agent_pos[0] -= 1
        elif action == 'D' and agent_pos[0] < grid_size - 1: agent_pos[0] += 1
        elif action == 'L' and agent_pos[1] > 0: agent_pos[1] -= 1
        elif action == 'R' and agent_pos[1] < grid_size - 1: agent_pos[1] += 1
        
        steps += 1
        time.sleep(0.2)
        
    if tuple(agent_pos) == goal_state:
        st.success(f"Agent reached the goal in {steps} steps!")
    else:
        st.error("Agent failed to reach the goal within the step limit.")

st.markdown("""
**Key Concepts to Remember:**
- **State ($S$)**: The current situation of the agent (e.g., its coordinates on the grid).
- **Action ($A$)**: What the agent chooses to do.
- **Reward ($R$)**: Feedback from the environment (e.g., +10 for Goal, -1 for each step).
- **Policy ($\pi$)**: The strategy the agent uses to decide actions based on states.
""")


st.markdown("---")
st.markdown("### 🎓 Student Learning Section")
with st.expander("👨‍💻 View Source Code \n\n*Analyze the exact code running this page*"):
    import os
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as f:
        code_content = f.read()
        clean_code = code_content.split("# --- Educational Enhancements ---")[0]
        st.code(clean_code, language="python")

st.info("💡 **Challenge for Students:** Try modifying parameters in the sidebar or inputs to observe how the data and charts respond instantly. This is the power of reactive programming in Streamlit!")
