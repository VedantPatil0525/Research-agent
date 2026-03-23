import streamlit as st
import json
from agent import run_agent, generate_output
from memory import clear_memory


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="centered"
)

# ─────────────────────────────────────────────
# UI HEADER
# ─────────────────────────────────────────────

st.title("🤖 AI CEO Research Agent")
st.write("OpenClaw-style Autonomous Agent (Local • No API • phi3)")

# ─────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────

name = st.text_input("Enter Founder / CEO Name")

# ─────────────────────────────────────────────
# BUTTON ACTION
# ─────────────────────────────────────────────

if st.button("Run Agent"):

    if not name.strip():
        st.warning("Please enter a name")
    else:
        clear_memory()

        with st.spinner("🔍 Running autonomous agent..."):
            run_agent(name)
            result = generate_output(name)

        if not result:
            st.error("No data found. Try another name.")
        else:
            st.success("✅ Research Completed")

            # ─────────────────────────────
            # RESULT DISPLAY
            # ─────────────────────────────

            st.subheader("📊 Summary")
            st.write(result["Summary"])

            st.subheader("🔗 Sources")
            for src in result["Sources"]:
                st.write(src)

            # ─────────────────────────────
            # DOWNLOAD
            # ─────────────────────────────

            json_str = json.dumps(result, indent=4)

            st.download_button(
                label="⬇ Download Report",
                data=json_str,
                file_name=f"{name.replace(' ','_')}_report.json",
                mime="application/json"
            )