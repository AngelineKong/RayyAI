# Database Structure Documentation

## Overview

This document describes the database schema for the RayyAI financial management system. The database is built using PostgreSQL and managed with SQLAlchemy ORM.

## Entity Relationship Diagram

```
┌─────────────┐
│    user     │
│─────────────│
│ user_id (PK)│◄──────────────────────┐
│ first_name  │                       │
│ last_name   │                       │
│ email       │                       │
│ password    │                       │
│ dob         │                       │
│ gender      │                       │
│ is_deleted  │                       │
│ created     │                       │
│ updated     │                       │
└─────────────┘                       │
                                      │
┌──────────────────┐                 │
│ account          │                 │
│──────────────────│                 │
│ account_id (PK)  │─────────────────┤
│ user_id (FK)     │                 │
│ account_no       │                 │
│ account_name     │                 │
│ account_type     │                 │
│ card_id (FK)     │                 │
│ is_deleted       │                 │
└──────────────────┘                 │
         │                           │
         │                           │
         ▼                           │
┌──────────────────────────────┐   │
│ account_balance_snapshot     │   │
│──────────────────────────────│   │
│ snapshot_id (PK)             │   │
│ account_id (FK)              │   │
│ snapshot_date                │   │
│ closing_balance              │   │
│ is_deleted                   │   │
│ created                      │   │
└──────────────────────────────┘   │
                                      │
┌─────────────────────┐             │
│ income              │             │
│─────────────────────│             │
│ income_id (PK)      │             │
│ user_id (FK)        │─────────────┤
│ account_id (FK)     │             │
│ statement_id (FK)   │             │
│ amount              │             │
│ description         │             │
│ category            │             │
│ date_received       │             │
│ payer               │             │
│ department          │             │
│ project             │             │
│ reference_no        │             │
│ is_deleted          │             │
│ created             │             │
└─────────────────────┘             │
                                      │
┌─────────────────────┐             │
│ expense             │             │
│─────────────────────│             │
│ expense_id (PK)     │             │
│ user_id (FK)        │─────────────┤
│ account_id (FK)     │             │
│ statement_id (FK)   │             │
│ amount              │             │
│ tax_amount          │             │
│ tax_deductible      │             │
│ is_reimbursable     │             │
│ description         │             │
│ category            │             │
│ expense_type        │             │
│ date_spent          │             │
│ seller              │             │
│ location            │             │
│ reference_no        │             │
│ card_id (FK)        │             │
│ is_deleted          │             │
│ created             │             │
└─────────────────────┘             │
                                      │
┌─────────────────────┐             │
│ statement           │             │
│─────────────────────│             │
│ statement_id (PK)   │             │
│ user_id (FK)        │─────────────┤
│ statement_type      │             │
│ statement_url       │             │
│ period_start        │             │
│ period_end          │             │
│ credit_score        │             │
│ score_text          │             │
│ is_deleted          │             │
│ date_uploaded       │             │
└─────────────────────┘             │
                                      │
┌─────────────────────┐             │
│ ai_analysis         │             │
│─────────────────────│             │
│ analysis_id (PK)    │             │
│ user_id (FK)        │─────────────┤
│ statement_id (FK)   │             │
│ analysis_content    │             │
│ analysis_type       │             │
│ is_deleted          │             │
│ created             │             │
└─────────────────────┘             │
                                      │
┌─────────────────────────────┐     │
│ user_credit_card            │     │
│─────────────────────────────│     │
│ card_id (PK)                │◄────┤
│ user_id (FK)                │──────┘
│ card_number                 │
│ card_name                   │
│ bank_name                   │
│ card_brand                  │
│ expiry_month                │
│ expiry_year                 │
│ credit_limit                │
│ annual_fee                  │
│ next_payment_amount         │
│ next_payment_date           │
│ benefits                    │
│ current_balance             │
│ is_deleted                  │
│ created                     │
└─────────────────────────────┘
         │
         │
         ▼
┌─────────────────────────────────────────────┐
│ user_credit_card_terms_history              │
│─────────────────────────────────────────────│
│ term_history_id (PK)                        │
│ card_id (FK)                                │
│ effective_date                              │
│ interest_rate                               │
│ minimum_payment                             │
│ is_deleted                                  │
│ created                                     │
└─────────────────────────────────────────────┘

┌─────────────────────┐
│ market_credit_card  │
│─────────────────────│
│ card_id (PK)        │
│ card_name           │
│ bank_name           │
│ card_brand          │
│ annual_fee          │
│ eligibility_criteria│
│ benefits            │
│ is_deleted          │
│ created             │
│ updated             │
└─────────────────────┘

┌─────────────────────┐
│ goal                │
│─────────────────────│
│ goal_id (PK)        │
│ user_id (FK)        │──────────────┐
│ goal_name           │              │
│ description         │              │
│ category            │              │
│ priority            │              │
│ target_amount       │              │
│ current_amount      │              │
│ target_date         │              │
│ is_deleted          │              │
│ created_at          │              │
└─────────────────────┘              │
                                     │
┌─────────────────────┐              │
│ budget              │              │
│─────────────────────│              │
│ budget_id (PK)      │              │
│ user_id (FK)        │──────────────┘
│ name                │
│ limit_amount        │
│ category            │
│ period_start        │
│ period_end          │
│ alert_threshold     │
│ is_deleted          │
│ created             │
└─────────────────────┘
                                      │
┌─────────────────────────────┐      │
│ chat_conversation           │      │
│─────────────────────────────│      │
│ conversation_id (PK)        │◄─────┤
│ user_id (FK)                │──────┘
│ title                       │
│ is_deleted                  │
│ created_at                  │
│ updated_at                  │
└─────────────────────────────┘
         │
         │
         ▼
┌─────────────────────────────┐
│ chat_message                │
│─────────────────────────────│
│ message_id (PK)             │
│ conversation_id (FK)        │
│ role                        │
│ content                     │
│ metadata_json               │
│ token_count                 │
│ created_at                  │
└─────────────────────────────┘

┌─────────────────────────────┐      │
│ context_summary             │      │
│─────────────────────────────│      │
│ summary_id (PK)             │      │
│ user_id (FK)                │──────┘
│ summary_content             │
│ summary_type                │
│ data_snapshot_date          │
│ created_at                  │
│ expires_at                  │
└─────────────────────────────┘

┌─────────────────────────────┐      │
│ user_embedding_cache        │      │
│─────────────────────────────│      │
│ cache_id (PK)               │      │
│ user_id (FK)                │──────┘
│ entity_type                 │
│ entity_id                   │
│ embedding_vector            │
│ embedding_text              │
│ metadata_json               │
│ created_at                  │
└─────────────────────────────┘
```

---

## Tables

### 1. `user`

Core user information table.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `user_id` | serial | PRIMARY KEY | Unique identifier for each user |
| `first_name` | varchar | NOT NULL | User's first name |
| `last_name` | varchar | NOT NULL | User's last name |
| `email` | varchar | NOT NULL | User's email address (unique) |
| `password` | varchar | NOT NULL | Hashed user password |
| `dob` | date | NOT NULL | Date of birth |
| `gender` | varchar | NOT NULL | User's gender |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Account creation timestamp |
| `updated` | timestamp | NOT NULL, DEFAULT now() | Last update timestamp |

**Relationships:**
- One-to-many with `account`
- One-to-many with `income`
- One-to-many with `expense`
- One-to-many with `statement`
- One-to-many with `ai_analysis`
- One-to-many with `user_credit_card`
- One-to-many with `goal`
- One-to-many with `budget`
- One-to-many with `chat_conversation`
- One-to-many with `context_summary`
- One-to-many with `user_embedding_cache`

---

### 2. `account`

Financial accounts (savings, checking, credit cards, e-wallets, etc.).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `account_id` | serial | PRIMARY KEY | Unique identifier for each account |
| `user_id` | integer | NOT NULL, FK → user.user_id | Owner of the account |
| `account_no` | varchar | NULL | Account number |
| `account_name` | varchar | NOT NULL | Display name for the account |
| `account_type` | varchar | NOT NULL | Type: savings, checking, credit_card, investment, ewallet, cash |
| `card_id` | integer | NULL, FK → user_credit_card.card_id | Associated credit card (if applicable) |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |

**Relationships:**
- Many-to-one with `user`
- Many-to-one with `user_credit_card` (optional)
- One-to-many with `account_balance_snapshot`
- One-to-many with `income`
- One-to-many with `expense`

---

### 3. `account_balance_snapshot`

Historical snapshots of account balances.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `snapshot_id` | serial | PRIMARY KEY | Unique snapshot identifier |
| `account_id` | integer | NOT NULL, FK → account.account_id | Account being snapshotted |
| `snapshot_date` | date | NOT NULL | Date of the snapshot |
| `closing_balance` | double precision | NOT NULL | Balance at end of day |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Snapshot creation timestamp |

**Relationships:**
- Many-to-one with `account`

---

### 4. `income`

Income transactions and records.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `income_id` | serial | PRIMARY KEY | Unique income record identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | User who received income |
| `account_id` | integer | NOT NULL, FK → account.account_id | Account receiving the income |
| `statement_id` | integer | NULL, FK → statement.statement_id | Source statement (if imported) |
| `amount` | double precision | NOT NULL | Income amount |
| `description` | varchar | NULL | Description of income source |
| `category` | varchar | NOT NULL | Income category (e.g., Salary, Freelance, Investment) |
| `date_received` | date | NOT NULL | Date income was received |
| `payer` | varchar | NOT NULL | Name of the payer |
| `department` | varchar | NULL | Department (if applicable) |
| `project` | varchar | NULL | Project name (if applicable) |
| `reference_no` | varchar | NULL | Transaction reference number |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Record creation timestamp |

**Relationships:**
- Many-to-one with `user`
- Many-to-one with `account`
- Many-to-one with `statement` (optional)

---

### 5. `expense`

Expense transactions and records.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `expense_id` | serial | PRIMARY KEY | Unique expense record identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | User who made the expense |
| `account_id` | integer | NOT NULL, FK → account.account_id | Account used for payment |
| `statement_id` | integer | NULL, FK → statement.statement_id | Source statement (if imported) |
| `amount` | double precision | NOT NULL | Expense amount |
| `tax_amount` | double precision | NULL | Tax portion of the amount |
| `tax_deductible` | boolean | NULL | Whether tax is deductible |
| `is_reimbursable` | boolean | NULL | Whether expense is reimbursable |
| `description` | varchar | NOT NULL | Description of expense |
| `category` | varchar | NOT NULL | Expense category (e.g., Food & Dining, Transportation) |
| `expense_type` | varchar | NULL | Type: "needs" or "wants" |
| `date_spent` | date | NOT NULL | Date expense occurred |
| `seller` | varchar | NOT NULL | Merchant/seller name |
| `location` | varchar | NULL | Location of purchase |
| `reference_no` | varchar | NULL | Receipt or reference number |
| `card_id` | integer | NULL, FK → user_credit_card.card_id | Credit card for debt payment |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Record creation timestamp |

**Relationships:**
- Many-to-one with `user`
- Many-to-one with `account`
- Many-to-one with `statement` (optional)
- Many-to-one with `user_credit_card` (optional)

**Constraints:**
- `expense_type` must be "needs", "wants", or NULL

---

### 6. `statement`

Uploaded financial statements and documents.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `statement_id` | serial | PRIMARY KEY | Unique statement identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | Owner of the statement |
| `statement_type` | varchar | NOT NULL | Type: CTOS, CCRIS, bank, credit_card, ewallet, receipt |
| `statement_url` | varchar | NOT NULL | URL/path to the uploaded statement |
| `period_start` | date | NULL | Statement period start date |
| `period_end` | date | NULL | Statement period end date |
| `credit_score` | integer | NULL | Credit score (if applicable) |
| `score_text` | varchar | NULL | Credit score description |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `date_uploaded` | timestamp | NOT NULL, DEFAULT now() | Upload timestamp |

**Relationships:**
- Many-to-one with `user`
- One-to-many with `income`
- One-to-many with `expense`
- One-to-many with `ai_analysis`

---

### 7. `ai_analysis`

AI-powered financial analysis and insights.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `analysis_id` | serial | PRIMARY KEY | Unique analysis identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | User receiving the analysis |
| `statement_id` | integer | NULL, FK → statement.statement_id | Associated statement (if applicable) |
| `analysis_content` | json | NOT NULL | Analysis data (JSON format) |
| `analysis_type` | varchar | NOT NULL | Type of analysis performed |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Analysis creation timestamp |

**Relationships:**
- Many-to-one with `user`
- Many-to-one with `statement` (optional)

**Analysis Types:**
- Financial health metrics
- Card analytics
- Cash flow forecast
- Goal completion forecast
- Debt strategy
- Card recommendation
- Cashback alerts
- Goal alignment
- Goal contribution recommendation
- Spending analysis
- Budget recommendation
- Anomaly detection

---

### 8. `user_credit_card`

User's personal credit cards.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `card_id` | serial | PRIMARY KEY | Unique card identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | Card owner |
| `card_number` | varchar | NOT NULL | Card number |
| `card_name` | varchar | NOT NULL | Display name |
| `bank_name` | varchar | NOT NULL | Issuing bank |
| `card_brand` | varchar | NOT NULL | Brand: Visa, MasterCard, etc. |
| `expiry_month` | integer | NOT NULL | Expiry month (1-12) |
| `expiry_year` | integer | NOT NULL | Expiry year |
| `credit_limit` | double precision | NOT NULL | Credit limit |
| `annual_fee` | double precision | NOT NULL | Annual fee |
| `next_payment_amount` | double precision | NULL | Next payment due |
| `next_payment_date` | date | NULL | Next payment date |
| `benefits` | json | NOT NULL | Card benefits (JSON) |
| `current_balance` | double precision | NOT NULL | Current outstanding balance |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Card creation timestamp |

**Relationships:**
- Many-to-one with `user`
- One-to-many with `account` (as linked account)
- One-to-many with `expense` (as debt payments)
- One-to-many with `user_credit_card_terms_history`

---

### 9. `user_credit_card_terms_history`

Historical tracking of credit card terms changes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `term_history_id` | serial | PRIMARY KEY | Unique history record identifier |
| `card_id` | integer | NOT NULL, FK → user_credit_card.card_id | Associated card |
| `effective_date` | date | NOT NULL | Date terms became effective |
| `interest_rate` | double precision | NOT NULL | Interest rate |
| `minimum_payment` | double precision | NULL | Minimum payment amount |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Record creation timestamp |

**Relationships:**
- Many-to-one with `user_credit_card`

---

### 10. `market_credit_card`

Available credit cards in the market for recommendations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `card_id` | serial | PRIMARY KEY | Unique card identifier |
| `card_name` | varchar | NOT NULL | Card name |
| `bank_name` | varchar | NOT NULL | Issuing bank |
| `card_brand` | varchar | NOT NULL | Brand: Visa, MasterCard, etc. |
| `annual_fee` | double precision | NOT NULL | Annual fee |
| `eligibility_criteria` | json | NOT NULL | Eligibility requirements (JSON) |
| `benefits` | json | NOT NULL | Card benefits (JSON) |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Record creation timestamp |
| `updated` | timestamp | NOT NULL, DEFAULT now() | Last update timestamp |

**Relationships:**
- None (reference table)

---

### 11. `goal`

Financial goals and savings targets.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `goal_id` | serial | PRIMARY KEY | Unique goal identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | Goal owner |
| `goal_name` | varchar | NOT NULL | Goal name |
| `description` | varchar | NOT NULL | Goal description |
| `category` | varchar | NOT NULL | Category: Emergency Fund, Vacation, Car Purchase, Home Down Payment, Education, Retirement, Investment, Other |
| `priority` | varchar | NOT NULL | Priority: low, medium, high |
| `target_amount` | double precision | NOT NULL | Target amount |
| `current_amount` | double precision | NOT NULL | Current progress |
| `target_date` | date | NULL | Target completion date |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Goal creation timestamp |

**Relationships:**
- Many-to-one with `user`

**Goal Categories:**
- Emergency Fund
- Vacation
- Car Purchase
- Home Down Payment
- Education
- Retirement
- Investment
- Other

**Goal Priorities:**
- low
- medium
- high

---

### 12. `budget`

Budget plans and spending limits.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `budget_id` | serial | PRIMARY KEY | Unique budget identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | Budget owner |
| `name` | varchar | NOT NULL | Budget name |
| `limit_amount` | double precision | NOT NULL | Spending limit |
| `category` | varchar | NOT NULL | Budget category |
| `period_start` | date | NOT NULL | Budget period start |
| `period_end` | date | NOT NULL | Budget period end |
| `alert_threshold` | double precision | NOT NULL | Alert threshold (0-100%) |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created` | timestamp | NOT NULL, DEFAULT now() | Budget creation timestamp |

**Relationships:**
- Many-to-one with `user`

**Budget Categories:**
- Housing
- Food
- Transportation
- Entertainment
- Utilities
- Shopping
- Health & Fitness
- Travel
- Education
- Others

**Budget Periods:**
- weekly
- monthly
- quarterly
- yearly

---

### 13. `chat_conversation`

Chat conversation metadata and context management.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `conversation_id` | serial | PRIMARY KEY | Unique conversation identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | Conversation owner |
| `title` | varchar | NULL | Conversation title (auto-generated from first message) |
| `is_deleted` | boolean | NOT NULL | Soft delete flag |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Creation timestamp |
| `updated_at` | timestamp | NOT NULL, DEFAULT now() | Last update timestamp |

**Relationships:**
- Many-to-one with `user`
- One-to-many with `chat_message`

---

### 14. `chat_message`

Individual messages in chat conversations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `message_id` | serial | PRIMARY KEY | Unique message identifier |
| `conversation_id` | integer | NOT NULL, FK → chat_conversation.conversation_id | Parent conversation |
| `role` | varchar | NOT NULL | Message role: "user" or "assistant" |
| `content` | text | NOT NULL | Message content |
| `metadata_json` | json | NULL | Structured metadata (actions, token counts) |
| `token_count` | integer | NULL | Token count for this message |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Message timestamp |

**Relationships:**
- Many-to-one with `chat_conversation`

---

### 15. `context_summary`

Cached financial summaries for efficient context management.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `summary_id` | serial | PRIMARY KEY | Unique summary identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | Summary owner |
| `summary_content` | text | NOT NULL | Summary content (JSON or text) |
| `summary_type` | varchar | NOT NULL | Type: "financial_snapshot", "conversation_summary" |
| `data_snapshot_date` | date | NOT NULL | Date when data was captured |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Creation timestamp |
| `expires_at` | timestamp | NULL | Expiration timestamp |

**Relationships:**
- Many-to-one with `user`

**Summary Types:**
- `financial_snapshot` - Comprehensive financial state
- `conversation_summary` - Summarized conversation history

---

### 16. `user_embedding_cache`

Embedding vectors for semantic search (Phase 2 enhancement).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `cache_id` | serial | PRIMARY KEY | Unique cache identifier |
| `user_id` | integer | NOT NULL, FK → user.user_id | Owner of the embedding |
| `entity_type` | varchar | NOT NULL | Type: "transaction", "goal", "budget", etc. |
| `entity_id` | integer | NOT NULL | ID of the entity |
| `embedding_vector` | array(float) | NULL | Vector embedding (for pgvector) |
| `embedding_text` | text | NOT NULL | Text that was embedded |
| `metadata_json` | json | NULL | Additional metadata |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Creation timestamp |

**Relationships:**
- Many-to-one with `user`

**Entity Types:**
- transaction
- goal
- budget
- account
- income
- expense

---

## Database Connection

The database connection is configured in `database.py`:

```python
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

**Configuration:**
- Connection pooling with 12 connections
- Max overflow of 20 connections
- Pool timeout of 30 seconds
- Pool recycle of 1000 seconds

---

## Soft Delete Pattern

All tables implement soft delete using the `is_deleted` boolean flag. This allows for:
- Data retention for audit purposes
- Recovery of accidentally deleted records
- Historical reporting

**Best Practices:**
- Default all queries to filter `is_deleted = FALSE`
- Use `is_deleted = TRUE` instead of hard deletes
- Maintain referential integrity even after soft deletion

---

## Enumerations

### Account Types
- `savings` - Savings account
- `checking` - Checking account
- `credit_card` - Credit card account
- `investment` - Investment account
- `ewallet` - Electronic wallet
- `cash` - Cash account

### Statement Types
- `CTOS` - CTOS credit report
- `CCRIS` - Central Credit Reference Information System
- `bank` - Bank statement
- `credit_card` - Credit card statement
- `ewallet` - E-wallet statement
- `receipt` - Receipt

### Expense Types
- `needs` - Essential expenses
- `wants` - Non-essential expenses

### Goal Categories
- Emergency Fund
- Vacation
- Car Purchase
- Home Down Payment
- Education
- Retirement
- Investment
- Other

### Goal Priorities
- low
- medium
- high

### Budget Categories
- Housing
- Food
- Transportation
- Entertainment
- Utilities
- Shopping
- Health & Fitness
- Travel
- Education
- Others

### Budget Periods
- weekly
- monthly
- quarterly
- yearly

---

## Foreign Key Relationships Summary

| Child Table | Parent Table | Foreign Key | Relationship |
|-------------|--------------|-------------|--------------|
| `account` | `user` | `user_id` | Many-to-One |
| `account` | `user_credit_card` | `card_id` | Many-to-One (optional) |
| `account_balance_snapshot` | `account` | `account_id` | Many-to-One |
| `income` | `user` | `user_id` | Many-to-One |
| `income` | `account` | `account_id` | Many-to-One |
| `income` | `statement` | `statement_id` | Many-to-One (optional) |
| `expense` | `user` | `user_id` | Many-to-One |
| `expense` | `account` | `account_id` | Many-to-One |
| `expense` | `statement` | `statement_id` | Many-to-One (optional) |
| `expense` | `user_credit_card` | `card_id` | Many-to-One (optional) |
| `statement` | `user` | `user_id` | Many-to-One |
| `ai_analysis` | `user` | `user_id` | Many-to-One |
| `ai_analysis` | `statement` | `statement_id` | Many-to-One (optional) |
| `user_credit_card` | `user` | `user_id` | Many-to-One |
| `user_credit_card_terms_history` | `user_credit_card` | `card_id` | Many-to-One |
| `goal` | `user` | `user_id` | Many-to-One |
| `budget` | `user` | `user_id` | Many-to-One |
| `chat_conversation` | `user` | `user_id` | Many-to-One |
| `chat_message` | `chat_conversation` | `conversation_id` | Many-to-One |
| `context_summary` | `user` | `user_id` | Many-to-One |
| `user_embedding_cache` | `user` | `user_id` | Many-to-One |

---

## Indexes

The following indexes are automatically created by SQLAlchemy:

### Primary Keys (Auto-indexed)
- `user.user_id`
- `account.account_id`
- `account_balance_snapshot.snapshot_id`
- `income.income_id`
- `expense.expense_id`
- `statement.statement_id`
- `ai_analysis.analysis_id`
- `user_credit_card.card_id`
- `user_credit_card_terms_history.term_history_id`
- `market_credit_card.card_id`
- `goal.goal_id`
- `budget.budget_id`
- `chat_conversation.conversation_id`
- `chat_message.message_id`
- `context_summary.summary_id`
- `user_embedding_cache.cache_id`

### Foreign Key Indexes
- `account.user_id`
- `account.card_id`
- `account_balance_snapshot.account_id`
- `income.user_id`
- `income.account_id`
- `income.statement_id`
- `expense.user_id`
- `expense.account_id`
- `expense.statement_id`
- `expense.card_id`
- `statement.user_id`
- `ai_analysis.user_id`
- `ai_analysis.statement_id`
- `user_credit_card.user_id`
- `user_credit_card_terms_history.card_id`
- `goal.user_id`
- `budget.user_id`
- `chat_conversation.user_id`
- `chat_message.conversation_id`
- `context_summary.user_id`
- `user_embedding_cache.user_id`

### Additional Indexes
- `user.email` (unique index)

---

## API Integration

The database is accessed through FastAPI routers in the `routers/` directory:

- `auth.py` - Authentication and user management
- `users.py` - User profile operations
- `accounts.py` - Account management
- `transactions.py` - Income and expense transactions
- `statements.py` - Statement uploads and processing
- `cards.py` - Credit card management
- `goals.py` - Financial goal tracking
- `budgets.py` - Budget management
- `rayyai.py` - AI-powered financial insights
- `chat.py` - AI chat with RAG capabilities
- `utils.py` - Utility functions

---

## Maintenance Notes

### Backup Strategy
- Regular automated backups recommended
- Retention policy: 30 days daily, 12 months monthly
- Consider point-in-time recovery for production

### Performance Optimization
- Monitor query performance with EXPLAIN ANALYZE
- Add composite indexes for common filter combinations
- Consider partitioning for high-volume tables (statements, transactions)
- Regular VACUUM and ANALYZE operations

### Security Considerations
- Passwords are hashed before storage
- All queries should use parameterized statements
- Implement rate limiting on API endpoints
- Regular security audits recommended

---

## Migration History

Database schema changes are managed through Alembic migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Revision Log

- **v1.0 - Initial Schema**: Created comprehensive database structure with all core entities
- **v1.1 - Soft Delete**: Implemented `is_deleted` flag across all tables
- **v1.2 - Credit Cards**: Added user credit cards and market credit cards tables
- **v1.3 - Goals & Budgets**: Added financial goals and budget tracking
- **v1.4 - AI Analysis**: Added AI-powered financial analysis storage
- **v1.5 - Balance Snapshots**: Added account balance history tracking
- **v2.0 - Chat Module**: Added AI chat with RAG capabilities, context summarization, and conversation management

## Future Enhancements

Potential areas for database expansion:

1. **Notifications Table**: Track user notifications and alerts
2. **Categories Table**: Dynamic category management
3. **Recurring Transactions**: Store recurring income/expense patterns
4. **Investment Tracking**: Add investment portfolios and holdings
5. **Tax Tracking**: Enhanced tax categorization and reporting
6. **Multi-Currency Support**: Exchange rates and currency conversion
7. **Audit Log**: Comprehensive change tracking
8. **Data Exports**: CSV/PDF export job tracking
9. **Collaboration**: Shared accounts and budgets
10. **Billing**: Subscription and payment tracking
11. **Embedding Search**: Full semantic search integration (Phase 2)
12. **Chat Analytics**: Track conversation metrics and AI performance

---

## Contact

For questions about the database structure, please refer to:
- Backend repository: `rayyai-backend`
- Database configuration: `database.py`
- SQLAlchemy models: `models.py`
- API schemas: `schemas.py`

---

*Last Updated: $(date)*
*Schema Version: 1.0*

