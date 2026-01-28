# AI Tools Guide - Budget and Credit Card Management

## Overview
RayyAI now has enhanced capabilities to manage budgets and credit cards through natural conversation with a confirmation-based flow.

## Gemini MCP Database Host

The Gemini agent can reach the backend databases via the Model Context Protocol host that is mounted inside FastAPI.

- Endpoint: `http://localhost:8000/mcp` (Streamable HTTP transport)
- Server name: `RayyAI Database MCP`
- Authentication: none (local development). Secure this endpoint before exposing it publicly.

### Available Tools

#### Postgres
- `postgres_query` – SELECT with optional column list, filters, limit/offset, ordering
- `postgres_insert` – INSERT row(s) with optional `returning` columns
- `postgres_update` – UPDATE filtered rows with required `values`
- `postgres_delete` – DELETE filtered rows with optional `returning`

Guardrails:
- Only tables registered in SQLAlchemy metadata are accessible.
- Column names are validated against the table schema.
- Filters require explicit operators; bulk updates/deletes must include at least one filter.

#### MongoDB
- `mongo_find` – Find documents with projection, pagination, and sort
- `mongo_insert` – Insert one or many documents
- `mongo_update` – Update one or many documents using `$set`
- `mongo_delete` – Delete one or many documents

Guardrails:
- Collection access is restricted to existing collections in the configured database.
- Filters and update payloads reject keys beginning with `$` to block operator injection.
- Empty filters are disallowed for write/delete operations.

### Usage Pattern

1. Gemini issues a tool call with the appropriate argument schema (see tool descriptions above).
2. The MCP host validates the payload and executes the database action.
3. Results are serialized (dates → ISO 8601, decimals → float, ObjectIds → string) before being returned to Gemini.

### Configuration Notes

- Environment variables:
  - `MONGODB_ATLAS_CLUSTER_URI`
  - `MONGODB_DB_NAME` (or include the DB in the URI)
- Requirements: `mcp==1.21.0`, `pymongo==4.8.0`
- The MCP server starts automatically when FastAPI boots via `services.mcp_host.mount_mcp(app)`.

## Available Tools

### Budget Management

#### Create Budget
**User request:** "Set a budget for groceries", "Create a $500 monthly dining budget"

**AI flow:**
1. Suggests the action with details
2. Asks for confirmation
3. Executes after user confirms

**Required parameters:**
- name: Budget name
- limit_amount: Budget limit
- category: Expense category
- period_start: Start date (YYYY-MM-DD)
- period_end: End date (YYYY-MM-DD)
- alert_threshold: Optional, default 0.8 (80%)

**Example:**
```
User: "Set a $500 monthly groceries budget"
AI: "I can create a monthly groceries budget of $500 for November 2025 (2025-11-01 to 2025-11-30). You'll get alerts when you reach 80% of the limit. Would you like me to proceed?"
User: "Yes"
AI: "Perfect! I've created your groceries budget. ✅"
```

#### Update Budget
**User request:** "Update my groceries budget to $600", "Change my dining budget limit"

**Required parameters:**
- budget_id: Budget to update
- Plus any fields to update (name, limit_amount, category, etc.)

#### Delete Budget
**User request:** "Delete my entertainment budget", "Remove the shopping budget"

**Required parameters:**
- budget_id: Budget to delete

### Credit Card Management

#### Add Credit Card
**User request:** "Add my credit card", "Register my Visa card"

**AI flow:**
1. Asks for required information
2. Confirms the details
3. Adds the card after user confirms

**Required parameters:**
- card_name: Card name (e.g., "Chase Sapphire Preferred")
- bank_name: Bank name
- card_brand: Visa/Mastercard/Amex/etc
- credit_limit: Credit limit
- current_balance: Current balance

**Optional parameters:**
- card_number: Masked card number
- annual_fee: Annual fee
- expiry_month: Expiry month (1-12)
- expiry_year: Expiry year (YYYY)
- next_payment_amount: Next payment amount
- next_payment_date: Next payment date (YYYY-MM-DD)
- benefits: JSON object with benefits info

**Example:**
```
User: "Add my credit card"
AI: "I'd be happy to add your credit card! I'll need:
- Card name (e.g., 'Chase Sapphire')
- Bank name
- Card brand (Visa/Mastercard/Amex)
- Credit limit
- Current balance

Please provide these details."

User: "Chase Freedom, Chase Bank, Visa, $10,000 limit, $2,500 balance"
AI: "Got it! I'll add:
- Card: Chase Freedom (Visa)
- Bank: Chase Bank
- Limit: $10,000
- Balance: $2,500
- Utilization: 25%

Shall I add this card?"

User: "Yes"
AI: "Done! Your Chase Freedom card has been added. ✅"
```

#### Update Credit Card
**User request:** "Update my Visa balance to $3,000", "Change my credit card limit"

**Required parameters:**
- card_id: Card to update
- Plus any fields to update

#### Remove Credit Card
**User request:** "Remove my old Mastercard", "Delete my Visa card"

**Required parameters:**
- card_id: Card to delete

### Credit Card Analytics

#### Analyze Utilization
**User request:** "What's my credit card utilization?", "How much credit am I using?"

**Parameters:**
- card_id: Optional (if omitted, analyzes all cards)

**Returns:**
- Utilization percentages
- Available credit
- Balances and limits
- Payment due dates
- Recommendations

**Example:**
```
User: "What's my credit card utilization?"
AI: "Let me check your credit usage... 💳

## Credit Card Overview

- **Total Utilization:** 26.2%
- **Total Balance:** $21,000
- **Total Limit:** $80,000
- **Available Credit:** $59,000

## Individual Cards

1. **Harimau 2 Card** (Harimau Bank)
   - Balance: $12,500 / $50,000
   - Utilization: 25.0% ✅
   - Next Payment: $2,500 on 2025-11-21

2. **Sotong Enrich** (Sotong Bank)
   - Balance: $8,500 / $30,000
   - Utilization: 28.3% ✅
   - Next Payment: $1,700 on 2025-11-28

## Recommendations

- Your utilization is excellent (under 30%)
- Keep balances low for optimal credit score
- Upcoming payments: $4,200 total this month"
```

## Confirmation Flow

### How It Works

1. **User requests action**: "Create a budget", "Add credit card"
2. **AI suggests**: Details what it will do
3. **AI asks**: "Would you like me to proceed?"
4. **User confirms**: "Yes", "Proceed", "Confirm", "Go ahead"
5. **AI executes**: Performs the action and confirms success

### No Confirmation Needed

These requests don't need confirmation (read-only):
- "What's my credit utilization?"
- "Show me my budgets"
- "Am I over budget?"
- "When are my credit card payments due?"

## Action Format (Internal)

Actions are wrapped in `<action>` tags with JSON format:

```xml
<action>
{
  "action": "create_budget",
  "parameters": {
    "name": "Monthly Groceries",
    "limit_amount": 500,
    "category": "Groceries",
    "period_start": "2025-11-01",
    "period_end": "2025-11-30",
    "alert_threshold": 0.8
  }
}
</action>
```

**Note**: Action blocks are never shown to users - they're internal commands.

## Complete Action List

### Budget Actions
- `create_budget`: Create new budget
- `update_budget`: Update existing budget
- `delete_budget`: Delete budget (soft delete)

### Credit Card Actions
- `create_credit_card`: Add new credit card
- `update_credit_card`: Update credit card details
- `delete_credit_card`: Remove credit card (soft delete)
- `analyze_credit_utilization`: Analyze credit usage

### Goal Actions
- `create_goal`: Create financial goal
- `update_goal`: Update existing goal

### Transaction Actions
- `categorize_transaction`: Update transaction category
- `create_expense`: Create expense record
- `create_income`: Create income record

## Testing the Tools

### Test Budget CRUD
```
1. Create: "Set a $500 monthly groceries budget"
2. Update: "Update my groceries budget to $600"
3. Delete: "Delete my entertainment budget"
```

### Test Credit Card CRUD
```
1. Add: "Add my Visa card with $10,000 limit and $2,500 balance"
2. Update: "Update my Visa card balance to $3,000"
3. Remove: "Remove my old Mastercard"
```

### Test Analytics
```
1. "What's my credit card utilization?"
2. "Am I over budget anywhere?"
3. "When are my credit card payments due?"
4. "Show me my budget status"
```

### Test Confirmation Flow
```
User: "Create a $300 dining budget"
AI: "I can create a monthly dining budget of $300. Would you like me to proceed?"
User: "No, make it $400 instead"
AI: "Sure! I can create a monthly dining budget of $400. Shall I proceed?"
User: "Yes"
AI: "Done! Your dining budget of $400 has been created."
```

## Error Handling

The AI will handle errors gracefully:
- Missing required information → Asks for it
- Invalid data → Explains the issue
- Budget/card not found → Provides alternatives
- Duplicate entries → Suggests updating instead

## Best Practices

1. **Be specific**: "Add my Chase Visa" is better than "Add card"
2. **Provide details**: Include amounts, dates, names when creating
3. **Confirm carefully**: Review details before confirming
4. **Use natural language**: The AI understands conversational requests
5. **Ask follow-ups**: "Show me the budget I just created"

