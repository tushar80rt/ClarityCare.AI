import streamlit as st
from dotenv import load_dotenv
from therapist_agent import get_therapist_agent, search_outside_agent
from toolkits.news_toolkit_wrapper import get_wellness_news
from toolkits.arxiv_toolkit_wrapper import get_mental_health_papers

from toolkits.math_toolkit_wrapper import calculate_mood_score
import time
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

load_dotenv("api.env")

st.set_page_config(
    page_title="MindMentor.AI",
    page_icon="🧠",
    layout="wide"
)

# --- SESSION STATE ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'mood_history' not in st.session_state:
    st.session_state.mood_history = []
if 'show_resources' not in st.session_state:
    st.session_state.show_resources = False
if 'show_insights' not in st.session_state:
    st.session_state.show_insights = False

# --- HEADER ---
st.title("🌆 ClarityCare.AI")
st.caption("AI-Powered CAMEL-AI & MISTRAL AI")

# --- SIDEBAR: Profile + Mood ---
with st.sidebar:
    st.header("Your Wellness Dashboard")

    with st.expander("👤 Profile Settings", expanded=True):
        name = st.text_input("Your Name", "Friend")
        goals = st.multiselect(
            "Wellness Goals",
            ["Reduce Anxiety", "Improve Sleep", "Boost Mood", "Increase Focus", "Build Confidence", "Manage Stress"],
            ["Reduce Anxiety", "Improve Sleep"]
        )

    with st.expander("📊 Mood Tracker", expanded=True):
        mood = st.slider("Mood Today (1 = 😔, 10 = 😊)", 1, 10, 5)
        notes = st.text_area("Quick Notes", "What's affecting your mood?")

        if st.button("📂 Log Mood", use_container_width=True):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            mood_score = calculate_mood_score([mood])
            st.session_state.mood_history.append({
                "date": timestamp,
                "mood": mood,
                "score": mood_score,
                "notes": notes
            })
            st.success(f"Mood logged! 🧠 Score: {mood_score}")

# --- Mood Trends Chart ---
if st.session_state.mood_history:
    st.subheader("📈 Mood Trends")
    mood_df = pd.DataFrame(st.session_state.mood_history)
    mood_df['date'] = pd.to_datetime(mood_df['date'])
    mood_df['mood'] = pd.to_numeric(mood_df['mood'])
    mood_df = mood_df.set_index('date')['mood'].resample('D').mean().ffill()

    fig, ax = plt.subplots()
    ax.plot(mood_df.index, mood_df.values, marker='o', color='#6e8efb', linewidth=2)
    ax.fill_between(mood_df.index, mood_df.values, alpha=0.2, color='#6e8efb')
    ax.set_ylim(0, 10)
    ax.set_ylabel('Mood Score')
    ax.grid(True)
    st.pyplot(fig)

# --- Quick Actions ---
st.subheader("🚀 Quick Actions")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🧘 Meditation"):
        st.session_state.show_resources = "meditation"
with col2:
    if st.button("😌 Breathing"):
        st.session_state.show_resources = "breathing"
with col3:
    if st.button("📚 Resources"):
        st.session_state.show_resources = "resources"
with col4:
    st.session_state.show_insights = st.toggle("🧠 Insights & Support", value=st.session_state.show_insights)

# --- Chat Section ---
for chat in st.session_state.chat_history:
    if chat["sender"] == "You":
        st.chat_message("user", avatar="assets/user_avatar.png").markdown(chat["message"])
    else:
        st.chat_message("assistant", avatar="🌆").markdown(chat["message"])

user_input = st.chat_input("What's on your mind today?")
if user_input:
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        "sender": "You",
        "message": user_input,
        "time": timestamp
    })

    with st.spinner("MindMentor is thinking..."):
        agent = get_therapist_agent()

        # 🧠 Add external search info
        search_snippet = search_outside_agent(user_input)
        full_prompt = f"{user_input}\n\nBackground info from search:\n{search_snippet}"

        step = agent.step(full_prompt)
        response = step.msgs[0].content

        st.session_state.chat_history.append({
            "sender": "Therapist",
            "message": response,
            "time": timestamp
        })
    st.rerun()

# --- Right Side Section ---
if st.session_state.show_resources == "meditation":
    st.markdown("""#### 🧘 Guided Meditation
- [5-Minute](https://www.youtube.com/watch?v=inpok4MKVLM)
- [Body Scan](https://www.youtube.com/watch?v=IHjvM-BLhzU)
- [Sleep Aid](https://www.youtube.com/watch?v=aEqlQvczMJQ)
""")
elif st.session_state.show_resources == "breathing":
    st.markdown("""#### 😌 4-7-8 Breathing
1. Inhale through nose (4 sec)  
2. Hold breath (7 sec)  
3. Exhale mouth (8 sec)  
""")
    if st.button("Start 2-Min Timer"):
        with st.empty():
            for sec in range(120, -1, -1):
                mm, ss = divmod(sec, 60)
                st.markdown(f"⏳ {mm:02d}:{ss:02d}")
                time.sleep(1)
            st.success("✅ Done!")
elif st.session_state.show_resources == "resources":
    st.markdown("""#### 📚 Helpful Resources
- [Mental Health Hotlines](https://www.vandrevalafoundation.com/free-counseling)
- [Crisis Text Line](https://www.crisistextline.org/)
- [Mindfulness Guide](https://www.mindful.org/meditation/mindfulness-getting-started/)
""")
elif st.session_state.show_insights:
    st.markdown("### 🧠 Insights & Support")
    # st.markdown(f"#### ✨ Daily Affirmation\n> {generate_affirmation()}")

    news_items = get_wellness_news()
    if news_items:
        st.markdown("#### 📰 Wellness News")
        for news in news_items[:3]:
            st.markdown(f"- {news}")

    papers = get_mental_health_papers()
    if papers:
        st.markdown("#### 🔬 Latest Research")
        for paper in papers:
            if paper["entry_id"] == "#":
                st.error(paper["title"])
            else:
                st.markdown(f"- **{paper['title']}** – [Read more]({paper['entry_id']})")


st.markdown("---")
