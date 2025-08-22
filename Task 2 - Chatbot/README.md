# Task 2 - Financial Analysis Chatbot

This folder contains a prototype chatbot that answers predefined financial queries based on the analyzed SEC 10-K data.

## Contents

- **financial_chatbot.py** - Main chatbot implementation with:
  - Command-line interactive mode
  - Optional Flask web interface
  - 5 predefined financial queries
  
- **chatbot_documentation.md** - Complete documentation of the chatbot

- **test_chatbot.py** - Test script to validate chatbot functionality

- **financial_data_sample.csv** - Financial data used by the chatbot

## Available Queries

The chatbot can answer these questions:
1. "What is the total revenue?"
2. "How has net income changed over the last year?"
3. "What are the profit margins?"
4. "Which company has the highest revenue?"
5. "How is the financial health of the companies?"

## Usage

### Command-Line Mode
```bash
python financial_chatbot.py
# Choose option 1
```

### Web Interface Mode (requires Flask)
```bash
pip install flask
python financial_chatbot.py
# Choose option 2
# Open http://localhost:5000
```

### Run Tests
```bash
python test_chatbot.py
```