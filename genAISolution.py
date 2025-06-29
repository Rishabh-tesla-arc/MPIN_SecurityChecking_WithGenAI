# cspell:ignore MPIN, groq, mixtral, dotenv
from datetime import datetime
from dotenv import load_dotenv
import random
import os
from groq import Groq

# Part A - Common MPIN Check
def is_common_used_mpin(mpin: str, common_pin: set) -> bool:
    return mpin in common_pin


# Part B - Generate MPIN Variants from -
# 1. Date of Birth (self)
# 2. Date of Birth (spouse)
# 3. Anniversary Date
def generate_mpin_variants(date_str: str, pin_length: int = 4) -> set:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        day = f"{date.day:02d}"
        month = f"{date.month:02d}"
        year_full = f"{date.year}"
        year_short = year_full[-2:]

        if pin_length == 4:
            return {
                day + month,
                day + year_short,
                month + day,
                month + year_short,
                year_short + day,
                year_short + month,
            }
        elif pin_length == 6:
            return {
                day + month + year_short,
                day + year_full,
                month + day + year_short,
                month + year_full,
                year_short + day + month,
                year_short + month + day,
                year_full + day + month,
                year_full + month + day,
            }
        else:
            return set()
    except:
        return set()



# Part C - MPIN Strength Check
def check_mpin_strength(mpin: str, common_pin: set, demographic_pin: dict) -> tuple:
    reasons = []
    pin_length = len(mpin)

    # Checking if MPIN is commonly used 
    if is_common_used_mpin(mpin, common_pin):
        reasons.append("COMMONLY_USED")

    # Checking if MPIN contains any demographic information
    for key, date_str in demographic_pin.items():
        if date_str:
            generated_pins = generate_mpin_variants(date_str, pin_length)
            if mpin in generated_pins:
                reasons.append(f"DEMOGRAPHIC_{key.upper()}")

    strength = "WEAK" if reasons else "STRONG"
    return strength, reasons



# GenAI Explanation Function (Using GROQ API to explain the weakness)
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def explain_weakness(mpin: str, reasons: list, user_info: dict,tone: str = "professional") -> str:
    if not reasons:
        return f"MPIN '{mpin}' is considered STRONG because it is UNIQUE . It does not match any common or demographic pattern."


    reasons_natural = []
    if "COMMONLY_USED" in reasons:
        reasons_natural.append("It is a commonly used MPIN pattern. ")
    for r in reasons:
        if r.startswith("DEMOGRAPHIC_"):
            field = r.replace("DEMOGRAPHIC_", "").replace("_", " ").title()
            reasons_natural.append(f"It matches your {field} in a common format. ")

    reasons_text = ", and ".join(reasons_natural)

    # LLM Prompt
    prompt = f"""
The user has the MPIN '{mpin}', which has been marked WEAK due to: {', '.join(reasons)}.
Give a short, clear explanation of why it's weak and suggest 1-2 secure MPIN ideas.
Keep it under 3 sentences. Tone: professional and friendly.
Avoid repeating the MPIN too many times.
"""

    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  # Groq supported model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not generate explanation: Error my side {e}"



# Part D - Test Cases 
def run_tests():
    common_pins_4 = {f"{random.randint(0, 9999):04d}" for _ in range(500)}
    common_pins_6 = {f"{random.randint(0, 999999):06d}" for _ in range(500)}

    # Adding some common patterns to test the code
    common_pins_4.update({"0000", "1111", "1234", "1212"})
    common_pins_6.update({"000000", "123456", "121212"})

    test_cases = [
        {"mpin": "1234", "common_pin": common_pins_4, "demographics": {"dob_self": "1998-01-02", "dob_spouse": None, "anniversary": None}},
        {"mpin": "9999", "common_pin": common_pins_4, "demographics": {"dob_self": "2000-02-10", "dob_spouse": None, "anniversary": None}},
        {"mpin": "5683", "common_pin": common_pins_4, "demographics": {"dob_self": None, "dob_spouse": None, "anniversary": None}},
        {"mpin": "1212", "common_pin": common_pins_4, "demographics": {"dob_self": None, "dob_spouse": None, "anniversary": None}},
        {"mpin": "9001", "common_pin": common_pins_4, "demographics": {"dob_self": "1990-01-02", "dob_spouse": "1990-09-14", "anniversary": "2020-01-02"}},

        {"mpin": "020199", "common_pin": common_pins_6, "demographics": {"dob_self": "1999-01-02", "dob_spouse": "1999-01-02", "anniversary": "1999-01-02"}},
        {"mpin": "121212", "common_pin": common_pins_6, "demographics": {"dob_self": "2012-12-12", "dob_spouse": None, "anniversary": None}},
        {"mpin": "123456", "common_pin": common_pins_6, "demographics": {"dob_self": "1998-01-02", "dob_spouse": None, "anniversary": "2020-01-02"}},
        {"mpin": "194503", "common_pin": common_pins_6, "demographics": {"dob_self": "1998-01-02", "dob_spouse": "1998-01-02", "anniversary": "2020-01-02"}},
        {"mpin": "123456", "common_pin": common_pins_6, "demographics": {"dob_self": None, "dob_spouse": None, "anniversary": None}},
        {"mpin": "121212", "common_pin": common_pins_6, "demographics": {"dob_self": None, "dob_spouse": None, "anniversary": None}},
        {"mpin": "123456", "common_pin": common_pins_6, "demographics": {"dob_self": "1998-01-02", "dob_spouse": None, "anniversary": "2020-01-02"}},
        {"mpin": "194503", "common_pin": common_pins_6, "demographics": {"dob_self": "1988-01-02", "dob_spouse": "1998-01-02", "anniversary": "2020-01-02"}},
        {"mpin": "123456", "common_pin": common_pins_6, "demographics": {"dob_self": "1998-01-02", "dob_spouse": "1990-01-02", "anniversary": "2020-01-02"}},
        {"mpin": "194503", "common_pin": common_pins_6, "demographics": {"dob_self": "1990-01-02", "dob_spouse": "2000-01-02", "anniversary": "2020-01-02"}},
    ]

    for i, test in enumerate(test_cases):
        strength, reasons = check_mpin_strength(test["mpin"], test["common_pin"], test["demographics"])
        explanation = explain_weakness(test["mpin"], reasons, test["demographics"])
        print(f"Test {i+1}: MPIN={test['mpin']} => Strength: {strength}, Reasons: {reasons}")
        print(f"Explanation: {explanation}\n")



if __name__ == "__main__":
    run_tests()
