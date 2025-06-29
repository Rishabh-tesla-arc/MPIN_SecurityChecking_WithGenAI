import streamlit as st
from datetime import datetime
import random
from dotenv import load_dotenv
import os
from groq import Groq


load_dotenv()

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except:
    client = None


from genAISolution import check_mpin_strength, explain_weakness, run_tests

# Page config
st.set_page_config(page_title="MPIN Strength Checker", page_icon="🔐")

st.title("MPIN Strength Checker")

# Mode selection
mode = st.radio("Choose mode:", ["Interactive Input", "Run Test Cases (Default Declared Test Cases in the Code)"])

if mode == "Interactive Input":
    mpin = st.text_input("Enter your MPIN (4 or 6 digits)", placeholder="e.g., 1234")

    # Date inputs
    st.subheader("Personal Information (Optional)")
    col1, col2 = st.columns(2)

    with col1:
        dob_self = st.date_input("Your Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.now())
        dob_spouse = st.date_input("Spouse's Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.now())

    with col2:
        anniversary = st.date_input("Anniversary Date", min_value=datetime(1900, 1, 1), max_value=datetime(2024, 12, 31))

    # dates to string format
    def date_to_string(date_obj):
        if date_obj:
            return date_obj.strftime("%Y-%m-%d")
        return None


    # Check button
    if st.button("Check MPIN Strength"):
        if mpin:
            if len(mpin) in [4, 6] and mpin.isdigit():
                # Get common pins (same logic in genAISolution.py)
                common_pins_4 = {f"{random.randint(0, 9999):04d}" for _ in range(500)}
                common_pins_6 = {f"{random.randint(0, 999999):06d}" for _ in range(500)}

                # Adding some common patterns to test the code
                common_pins_4.update({"0000", "1111", "1234", "1212"})
                common_pins_6.update({"000000", "123456", "121212"})

                common_pins = common_pins_4 if len(mpin) == 4 else common_pins_6
                
                
                # Preparing demographics
                demographics = {
                    "dob_self": date_to_string(dob_self),
                    "dob_spouse": date_to_string(dob_spouse),
                    "anniversary": date_to_string(anniversary)
                }
                
                # Checking strength (same logic in genAISolution.py)
                strength, reasons = check_mpin_strength(mpin, common_pins, demographics)
                
                # Displaying results
                st.subheader("Results")
                
                if strength == "WEAK":
                    st.error(f"Strength: WEAK")
                else:
                    st.success(f"Strength: STRONG")
                
                if reasons:
                    st.write("Issues found:")
                    for reason in reasons:
                        st.write(f"- {reason}")
                
                # AI Explanation
                if client:
                    with st.spinner("Generating AI explanation..."):
                        explanation = explain_weakness(mpin, reasons, demographics)
                        st.write("AI Explanation:")
                        st.info(explanation)
                else:
                    st.warning("AI explanations unavailable. Please set GROQ_API_KEY in your .env file.")
                
            else:
                st.error("Please enter a valid 4 or 6 digit MPIN")
        else:
            st.warning("Please enter an MPIN to check")


else:  # Run Test Cases mode (Default Declared Test Cases in the Code)
    st.subheader("Test Cases Results")
    
    if st.button("Run Test Cases"):
        # Capturing the output from run_tests
        import io
        import sys
        
        # Redirecting stdout to capture print statements
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            run_tests()
            output = new_stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        
        # Displaying the test results
        st.text_area("Test Results:", output, height=400)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>🔐 Secure your digital life with strong MPINs</div>",
    unsafe_allow_html=True
) 
