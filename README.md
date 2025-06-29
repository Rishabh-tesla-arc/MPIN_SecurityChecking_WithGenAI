# MPIN Strength Checker

A comprehensive tool to check the strength of your MPIN (Mobile Personal Identification Number) by analyzing common patterns, date-based variations, and personal information matches. The tool provides AI-powered explanations for weak MPINs and suggests secure alternatives.


## Features

- **Common Pattern Detection**: Identifies commonly used MPIN patterns
- **Date-based Analysis**: Checks if MPIN matches personal dates (birth date (self), birth date(spouse), anniversary)
- **AI-powered Explanations**: Provides detailed explanations using Groq API
- **Interactive Web Interface**: Simple User-friendly Streamlit application
- **Test Suite**: Predefined test cases to validate functionality


## Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional, for AI explanations):
   Create a `.env` file in the project directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```


## Usage

### Web Interface (Recommended)

Run the Streamlit application (in case streamlit is not recognized even after downloading then use the second cmd):
```bash
streamlit run app.py
python -m streamlit run app.py
```

The web interface provides two modes:
- **Interactive Input**: Enter your own MPIN and personal information
- **Run Test Cases**: Execute predefined test cases to see examples


### Command Line (If the user wants to access from CLI)

Run the test suite directly:
```bash
python genAISolution.py
```


## Function Documentation

### Core Functions in `genAISolution.py`

#### `is_common_used_mpin(mpin: str, common_pin: set) -> bool`
**Purpose**: Checks if the given MPIN exists in a set of commonly used MPINs.

**Parameters**:
- `mpin` (str): The MPIN to check
- `common_pin` (set): Set of commonly used MPINs

**Returns**: `bool` - True if MPIN is common, False otherwise




#### `generate_mpin_variants(date_str: str, pin_length: int = 4) -> set`
**Purpose**: Generates possible MPIN variants from a provided date string.

**Parameters**:
- `date_str` (str): Date in "YYYY-MM-DD" format
- `pin_length` (int): Length of MPIN (4 or 6 digits)

**Returns**: `set` - Set of possible MPIN variants

**Generated patterns for 4-digit MPINs**:
- DDMM (day + month)
- DDYY (day + year short)
- MMDD (month + day)
- MMYY (month + year short)
- YYDD (year short + day)
- YYMM (year short + month)

**Generated patterns for 6-digit MPINs**:
- DDMMYY (day + month + year short)
- DDYYYY (day + full year)
- MMDDYY (month + day + year short)
- MMYYYY (month + full year)
- YYDDMM (year short + day + month)
- YYMMDD (year short + month + day)
- YYYYDDMM (full year + day + month)
- YYYYMMDD (full year + month + day)



#### `check_mpin_strength(mpin: str, common_pin: set, demographic_pin: dict) -> tuple`
**Purpose**: Comprehensive MPIN strength analysis.

**Parameters**:
- `mpin` (str): The MPIN to analyze
- `common_pin` (set): Set of commonly used MPINs
- `demographic_pin` (dict): Dictionary with personal dates

**Returns**: `tuple` - (strength, reasons)
- `strength` (str): "WEAK" or "STRONG"
- `reasons` (list): List of reasons why MPIN is weak

**Demographic dictionary format**:
```python
{
    "dob_self": "1998-01-02",      # Your birth date
    "dob_spouse": "1995-05-15",    # Spouse's birth date
    "anniversary": "2020-06-20"    # Anniversary date
}
```



#### `explain_weakness(mpin: str, reasons: list, user_info: dict, tone: str = "professional") -> str`
**Purpose**: Generates AI-powered explanations for weak MPINs.

**Parameters**:
- `mpin` (str): The weak MPIN
- `reasons` (list): List of weakness reasons
- `user_info` (dict): User demographic information
- `tone` (str): Explanation tone ("professional", "friendly", "technical")

**Returns**: `str` - AI-generated explanation


**Requirements**: Requires GROQ_API_KEY in environment variables




#### `run_tests()`
**Purpose**: Executes predefined test cases to validate the system.

**Test Cases Include**:
- 20 Test Cases
- Common MPIN patterns
- Date-based MPINs 
- Strong MPINs 
- Various demographic combinations

**Output**: Prints test results to console

## File Structure

```
MPIN_SecurityChecking_WithGenAI/
├── app.py                 # Streamlit web interface
├── genAISolution.py       # Core MPIN analysis functions
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .env                   # Environment variables (create this and use your own API KEY)
```


## Configuration

### Environment Variables (.env file)
```
GROQ_API_KEY=your_groq_api_key_here
```

### Getting a Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for an account
3. Generate an API key
4. Add it to your `.env` file


## Security Notes

- **Local Processing**: All MPIN analysis is done locally
- **No Data Storage**: Personal information is not stored
- **Optional AI**: AI explanations require API key but are optional
- **Date Privacy**: Dates are only used for pattern matching, not stored


### User Interface View
<img width="368" alt="image" src="https://github.com/user-attachments/assets/a0785de7-0c26-4918-a87e-b5047827bb98" />
<img width="280" alt="image" src="https://github.com/user-attachments/assets/3d70daa7-c827-410a-b5e6-a43a5bcef923" />


