# Personal Assistant Bot

A fuzzy input to structured JSON converter that categorizes user requests, extracts key entities, and provides follow-up questions when needed.

## Features

- Categorizes user requests into intent categories (dining, travel, gifting, etc.)
- Extracts key entities (date, time, location, etc.)
- Provides confidence scores for categorization
- Suggests follow-up questions for missing information
- Web search capability for non-standard requests

## Setup Instructions

### Prerequisites

- Python 3.10.7 or higher

### Installation

1. Clone the repository:

   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in .env:
   - add api_key
   - add model_name

## Running the Application

### Backend Service

- Run the backend API:

```bash
python main.py
```

### Frontend Interface

- Run the Streamlit frontend:

```bash
cd streamlit
streamlit run app.py
```

## Usage Examples

#### Example Input:

- "Need a sunset-view table for two tonight; gluten-free menu a must"

#### Example Output:

- ````json{
    "intent_category": "dining_reservation",
    "key_entities": "```json{
      "party_size": 2,
      "date": "tonight",
      "table_preference": "sunset-view",
      "dietary_restrictions": "gluten-free"
    }```",
    "confidence_score": "1",
    "follow_up_questions": "[
      "Which restaurant would you like to make a reservation for?",
      "What time would you like the reservation to be tonight?"
    ]"
  }
  ````

## 🔍 Test Cases

Sample inputs and their outputs are available in:
[`sample_input_output/sample.txt`] and can view screen shots for the same.
