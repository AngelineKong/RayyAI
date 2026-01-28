# RAG System Explanation & Testing Guide

## 📁 The 3 Files Explained

### 1. `insert_mock_transactions.py`
**Purpose:** Legacy script for inserting basic transaction data
- **What it does:** Inserts simple income and expense transactions
- **Data created:** Only transactions (no accounts, budgets, goals, or credit cards)
- **Use case:** Basic testing, but **outdated** - use `chatMockData.py` instead
- **Status:** ⚠️ Legacy - kept for reference

### 2. `chatMockData.py` ⭐ **USE THIS ONE**
**Purpose:** Comprehensive mock data generator for RAG testing
- **What it creates:**
  - ✅ User account (if doesn't exist)
  - ✅ 5 different account types (Savings, Current, Investment, Cash, E-Wallet)
  - ✅ 2 credit cards with balances
  - ✅ Income transactions (last 90 days)
  - ✅ Expense transactions (needs & wants, last 90 days)
  - ✅ 4 active budgets with status tracking
  - ✅ 4 financial goals with progress
- **How to run:**
  ```bash
  cd C:\Users\Angeline\rayyai-backend
  .\venv\Scripts\python.exe chatMockData.py
  ```
- **When to use:** Before testing RAG - ensures you have realistic financial data

### 3. `test_rag.py` ⭐ **TEST WITH THIS**
**Purpose:** Comprehensive test suite for RAG service
- **What it tests:**
  - ✅ Account retrieval
  - ✅ Transaction retrieval (income & expenses)
  - ✅ Spending summary calculations
  - ✅ Budget status tracking
  - ✅ Goals progress tracking
  - ✅ Credit card information
  - ✅ Financial summary generation
  - ✅ Context formatting for LLM
- **How to run:**
  ```bash
  cd C:\Users\Angeline\rayyai-backend
  .\venv\Scripts\python.exe test_rag.py
  ```
- **When to use:** After creating mock data, to verify RAG is working correctly

---

## 🔄 How Your RAG System Works

### What is RAG?
**RAG = Retrieval-Augmented Generation**

Instead of the AI responding from general knowledge, RAG:
1. **Retrieves** your actual financial data from the database
2. **Formats** it into readable context
3. **Augments** the AI's response with your real data
4. **Generates** personalized, accurate answers

### RAG Flow Diagram

```
User asks: "What's my current balance?"
         ↓
┌─────────────────────────────────────────┐
│  Chat Endpoint (/chat/message)          │
│  - Receives user message                │
│  - Authenticates user                   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  RAG Service (rag_service.py)          │
│  Step 1: RETRIEVE Data                  │
│  - get_user_accounts()                  │
│  - get_recent_transactions()             │
│  - get_spending_summary()               │
│  - get_budgets_status()                 │
│  - get_goals_status()                   │
│  - get_credit_cards()                   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  RAG Service                            │
│  Step 2: AGGREGATE                      │
│  - get_financial_summary()              │
│  Combines all data into one structure   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  RAG Service                            │
│  Step 3: FORMAT                         │
│  - format_context_for_llm()              │
│  Converts data to text like:             │
│  "=== ACCOUNTS ===                      │
│   Total Balance: $15,080.00             │
│   - Main Savings: $26,310.00            │
│   ..."                                   │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  PII Masking Service                    │
│  - mask_financial_context()             │
│  Removes sensitive info for logging    │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  Context Summarizer                     │
│  - get_or_generate_summary()            │
│  Creates cached summary for efficiency  │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│  Gemini AI Service                      │
│  - Receives:                            │
│    • User's question                    │
│    • Formatted financial context        │
│    • Conversation history               │
│    • System instructions                 │
│  - Generates personalized response      │
└─────────────────────────────────────────┘
         ↓
User receives: "Your current balance is $15,080.00
                across 5 accounts. Your Main Savings
                Account has $26,310.00..."
```

### Key Components

#### 1. **RAG Service** (`services/rag_service.py`)
The core data retrieval engine:

```python
class RAGService:
    # Retrieves accounts with balances
    def get_user_accounts(user_id) -> List[Dict]
    
    # Gets recent transactions (90 days)
    def get_recent_transactions(user_id, days=90) -> Dict
    
    # Calculates spending by category
    def get_spending_summary(user_id, days=30) -> Dict
    
    # Gets active budgets with status
    def get_budgets_status(user_id) -> List[Dict]
    
    # Gets goals with progress
    def get_goals_status(user_id) -> List[Dict]
    
    # Gets credit cards with utilization
    def get_credit_cards(user_id) -> List[Dict]
    
    # Combines everything
    def get_financial_summary(user_id) -> Dict
    
    # Formats for LLM
    def format_context_for_llm(financial_data) -> str
```

#### 2. **Chat Router** (`routers/chat.py`)
Orchestrates the RAG flow:

```python
@router.post("/chat/message")
async def send_message():
    # 1. Get user's financial data via RAG
    financial_data = rag_service.get_financial_summary(user_id)
    
    # 2. Format it for the LLM
    financial_context_text = rag_service.format_context_for_llm(financial_data)
    
    # 3. Send to Gemini AI with context
    response = await gemini_service.generate_response(
        user_message=message,
        financial_context=financial_context_text,
        conversation_history=conv_context
    )
    
    # 4. Return personalized answer
    return response
```

#### 3. **Context Formatting**
The RAG service formats data like this:

```
=== ACCOUNTS ===
Total Balance: $15,080.00
Number of Accounts: 5
- Main Savings Account (savings): $26,310.00
- Current Account (current): $-1,650.00
...

=== RECENT TRANSACTIONS (Last 90 Days) ===
Income: $29,000.00 (10 transactions)
Expenses: $13,920.00 (32 transactions)
Net Flow: $15,080.00

=== SPENDING BY CATEGORY (Last 30 Days) ===
Total Spending: $5,120.00
- Shopping: $1,300.00
- Groceries: $700.00
...
```

This formatted text is sent to the AI, so it knows your actual financial situation!

---

## 🧪 How to Test Your RAG System

### Step 1: Create Mock Data
```bash
cd C:\Users\Angeline\rayyai-backend
.\venv\Scripts\python.exe chatMockData.py
```

**Expected output:**
```
[OK] User: Angel M
[OK] Accounts: 5
[OK] Credit Cards: 2
[OK] Transactions: 21
[OK] Budgets: 4
[OK] Goals: 4
[SUCCESS] Mock data created successfully!
```

### Step 2: Test RAG Service
```bash
.\venv\Scripts\python.exe test_rag.py
```

**What it tests:**
- ✅ All 8 data retrieval functions
- ✅ Context formatting
- ✅ Data completeness
- ✅ Validation checks

**Expected output:**
```
[PASS] Accounts retrieved successfully
[PASS] Transactions retrieved successfully
[PASS] Context formatting works
[PASS] Context contains 6/6 expected sections
[PASS] Financial summary contains all required keys

Checks Passed: 5/5
[SUCCESS] All RAG tests passed!
```

### Step 3: Test in Chat Interface

1. **Start Backend:**
   ```bash
   cd C:\Users\Angeline\rayyai-backend
   .\venv\Scripts\activate
   uvicorn main:app --reload
   ```

2. **Start Frontend:**
   ```bash
   cd C:\Users\Angeline\rayyai-frontend\rayyai
   npm run dev
   ```

3. **Login** as User ID 1 (the mock data user)

4. **Open Chat** and test these queries:

   **Account Queries:**
   - "What's my current balance?"
   - "Show me all my accounts"
   - "How much do I have in my savings account?"

   **Transaction Queries:**
   - "What did I spend this month?"
   - "Show me my recent income"
   - "What's my biggest expense category?"

   **Budget Queries:**
   - "Am I over budget in any category?"
   - "How am I doing on my groceries budget?"
   - "Which budgets are near their limit?"

   **Goal Queries:**
   - "How am I doing on my financial goals?"
   - "What's my progress on the emergency fund?"
   - "How much more do I need for my vacation goal?"

   **Analysis Queries:**
   - "Analyze my spending patterns"
   - "What's my needs vs wants breakdown?"
   - "Give me financial advice based on my data"

### Step 4: Verify RAG is Working

**Good signs:**
- ✅ AI mentions specific amounts from your data
- ✅ AI references your actual accounts, budgets, goals
- ✅ AI provides accurate calculations
- ✅ AI gives personalized advice based on your spending

**Bad signs:**
- ❌ AI gives generic answers
- ❌ AI doesn't mention your specific data
- ❌ AI says "I don't have access to your data"
- ❌ Numbers don't match your database

---

## 🔍 Debugging RAG Issues

### Check if data exists:
```bash
python -c "from database import SessionLocal; from models import Income, Expense; db = SessionLocal(); print(f'Income: {db.query(Income).filter(Income.user_id == 1).count()}'); print(f'Expense: {db.query(Expense).filter(Expense.user_id == 1).count()}'); db.close()"
```

### Check RAG retrieval:
```bash
.\venv\Scripts\python.exe test_rag.py
```

### Check chat endpoint:
- Open browser DevTools (F12)
- Go to Network tab
- Send a chat message
- Check the `/chat/message` request
- Look at the response - it should include your financial data in the context

### Common Issues:

1. **No data in response:**
   - Verify user_id matches (should be 1)
   - Check database has data
   - Verify authentication token

2. **Wrong data:**
   - Check user_id in token matches data owner
   - Verify data wasn't deleted
   - Check database connection

3. **AI doesn't use data:**
   - Check context is being sent (look at request payload)
   - Verify context formatting is correct
   - Check Gemini API is receiving context

---

## 📊 RAG Data Flow Summary

```
Database (PostgreSQL)
    ↓
RAG Service (Retrieves)
    ↓
Financial Summary (Aggregates)
    ↓
Context Formatter (Converts to text)
    ↓
PII Masker (Removes sensitive data)
    ↓
Context Summarizer (Caches for efficiency)
    ↓
Gemini AI (Generates response)
    ↓
User (Receives personalized answer)
```

---

## 🎯 Quick Test Checklist

- [ ] Run `chatMockData.py` - Data created successfully
- [ ] Run `test_rag.py` - All tests pass (5/5)
- [ ] Backend running on port 8000
- [ ] Frontend running
- [ ] Logged in as User ID 1
- [ ] Chat interface opens
- [ ] Ask "What's my balance?" - Gets specific amount
- [ ] Ask "Am I over budget?" - Mentions specific budgets
- [ ] Ask "How are my goals?" - Shows actual progress

If all checkboxes are ✅, your RAG system is working perfectly! 🎉

