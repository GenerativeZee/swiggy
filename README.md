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

The frontend will be available at http://localhost:8501 in your browser.
