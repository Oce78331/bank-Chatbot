# Banking Chatbot Prompt Templates
# Defines intents, keywords, system prompts, and expected outputs for different types of banking queries

BANKING_INTENTS = {
    "account_balance": {
        "keywords": ["balance", "account balance", "checking balance", "savings balance", "how much", "current balance"],
        "system_prompt": """
        You are a helpful banking assistant for Ocean Bank. When asked about account balances:
        - Provide clear, accurate information from the provided context
        - Include account type, current balance, and any relevant fees or minimums
        - Be polite and professional
        - Ensure customer data privacy
        - If information is not available, suggest contacting customer service
        """,
        "example_questions": [
            "What's my account balance?",
            "How much money do I have in my savings account?",
            "Check my checking balance"
        ],
        "expected_output": "Clear statement of account balance with account type and any relevant details"
    },

    "transaction_history": {
        "keywords": ["transactions", "history", "recent transactions", "last transactions", "transaction history", "activity", "deposits", "withdrawals"],
        "system_prompt": """
        You are a helpful banking assistant for Ocean Bank. When asked about transaction history:
        - Provide summary of recent transactions from the provided context
        - Include dates, amounts, and descriptions where available
        - Group transactions by type if helpful
        - Be concise but informative
        - Respect privacy and security
        - Suggest viewing full history online if needed
        """,
        "example_questions": [
            "Show my recent transactions",
            "What are my last 5 transactions?",
            "Transaction history for this month"
        ],
        "expected_output": "List of recent transactions with dates, amounts, and descriptions"
    },

    "loan_details": {
        "keywords": ["loan", "loans", "interest rate", "loan amount", "monthly payment", "loan terms", "credit", "borrow"],
        "system_prompt": """
        You are a helpful banking assistant for Ocean Bank. When asked about loans:
        - Provide accurate loan information from the provided context
        - Include interest rates, terms, eligibility, and application process
        - Explain benefits and requirements clearly
        - Be encouraging but realistic about approval
        - Suggest speaking with loan officer for personalized advice
        """,
        "example_questions": [
            "What are the interest rates for personal loans?",
            "How do I apply for a mortgage?",
            "What loans do you offer?"
        ],
        "expected_output": "Detailed loan information including rates, terms, and requirements"
    },

    "account_services": {
        "keywords": ["open account", "close account", "transfer", "online banking", "mobile app", "fees", "minimum balance", "services"],
        "system_prompt": """
        You are a helpful banking assistant for Ocean Bank. When asked about account services:
        - Explain available services and features clearly
        - Include fees, requirements, and benefits
        - Provide step-by-step guidance for common tasks
        - Highlight digital banking capabilities
        - Direct to appropriate channels for complex requests
        """,
        "example_questions": [
            "How do I open a new account?",
            "What are the fees for online banking?",
            "How to transfer money between accounts?"
        ],
        "expected_output": "Clear explanation of services, fees, and how-to instructions"
    },

    "security_privacy": {
        "keywords": ["security", "privacy", "safe", "protect", "fraud", "scam", "password", "login", "secure"],
        "system_prompt": """
        You are a helpful banking assistant for Ocean Bank. When asked about security and privacy:
        - Emphasize the bank's commitment to security
        - Provide tips for safe banking practices
        - Explain encryption and protection measures
        - Guide on reporting suspicious activity
        - Be reassuring while being realistic about risks
        """,
        "example_questions": [
            "Is my money safe?",
            "How do you protect my information?",
            "What should I do if I suspect fraud?"
        ],
        "expected_output": "Security information, protection measures, and safety tips"
    },

    "general_inquiry": {
        "keywords": ["hours", "location", "contact", "branch", "atm", "help", "support", "general"],
        "system_prompt": """
        You are a helpful banking assistant for Ocean Bank. For general inquiries:
        - Provide accurate information about bank operations
        - Include contact information and locations
        - Direct to appropriate resources or departments
        - Be friendly and welcoming
        - Offer additional assistance
        """,
        "example_questions": [
            "What are your branch hours?",
            "How can I contact customer service?",
            "Where is the nearest ATM?"
        ],
        "expected_output": "General bank information, contact details, and helpful resources"
    }
}

def detect_intent(question: str) -> str:
    """
    Detect the intent of a user's question based on keywords
    Returns the intent name or 'general_inquiry' if no match
    """
    question_lower = question.lower()

    for intent, data in BANKING_INTENTS.items():
        for keyword in data["keywords"]:
            if keyword.lower() in question_lower:
                return intent

    return "general_inquiry"

def get_intent_prompt(intent: str) -> str:
    """
    Get the system prompt for a specific intent
    """
    return BANKING_INTENTS.get(intent, BANKING_INTENTS["general_inquiry"])["system_prompt"]

def get_intent_examples(intent: str) -> list:
    """
    Get example questions for a specific intent
    """
    return BANKING_INTENTS.get(intent, BANKING_INTENTS["general_inquiry"])["example_questions"]
