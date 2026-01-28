# AI Chat Module Setup Guide

## Overview
The AI Chat module with RAG capabilities has been fully implemented and is ready to use. All components have been created and tested.

## Completed Components

### Backend
1. ✅ Database models: `ChatConversation`, `ChatMessage`, `ContextSummary`, `UserEmbeddingCache`
2. ✅ Gemini 2.5 Pro integration service
3. ✅ PII masking service
4. ✅ Context summarization service
5. ✅ RAG service (SQL-based retrieval)
6. ✅ Action executor
7. ✅ Conversation manager
8. ✅ Chat API router with all endpoints

### Frontend
1. ✅ Chat API service methods
2. ✅ RayyAIchat component integration with backend
3. ✅ Conversation management UI
4. ✅ Markdown rendering for AI responses
5. ✅ Action execution indicators

## Setup Completed

### ✅ 1. Environment Variables
The following environment variables have been added to `.env`:
- `GEMINI_API_KEY` - Already configured
- `GEMINI_MODEL=gemini-2.0-flash-exp`
- `CONTEXT_TOKEN_LIMIT=1000000`
- `CONTEXT_SUMMARY_EXPIRY_HOURS=24`

### ✅ 2. Backend Dependencies Installed
- `google-generativeai>=0.3.0` - Installed successfully

### ✅ 3. Frontend Dependencies Installed
- `react-markdown` - Installed successfully

### ✅ 4. Database Tables Created
All new database tables have been created:
- ✅ `chat_conversation`
- ✅ `chat_message`
- ✅ `context_summary`
- ✅ `user_embedding_cache`

### 5. API Endpoints

The chat router has been added to `main.py`. Available endpoints:

- `POST /chat/conversations` - Create new conversation
- `GET /chat/conversations` - List conversations
- `GET /chat/conversations/{id}` - Get conversation details
- `DELETE /chat/conversations/{id}` - Delete conversation
- `GET /chat/conversations/{id}/messages` - Get messages
- `POST /chat/messages` - Send message (creates conversation if needed)
- `POST /chat/conversations/{id}/messages` - Send message to specific conversation
- `POST /chat/context/refresh` - Refresh financial context cache
- `POST /chat/context/summarize` - Trigger context summarization

## Features

### RAG (Retrieval-Augmented Generation)
- SQL-based retrieval of user financial data
- Context includes: accounts, transactions, budgets, goals, credit cards
- Hybrid approach ready for embeddings (optional Phase 2)

### Context Management
- Automatic conversation summarization when token limit approaches (80% threshold)
- Financial context caching (24-hour expiry)
- Incremental context updates

### PII Masking
- Credit card numbers masked (last 4 digits shown)
- Account numbers masked
- Email addresses masked
- Phone numbers masked
- SSN masked
- User's own name preserved

### Action Execution
AI can execute the following actions:
- Create/update budgets
- Create/update goals
- Categorize transactions
- Create expense/income records

Actions are parsed from LLM responses and executed automatically.

### Conversation Management
- Full conversation history persistence
- Auto-summarization for long conversations
- Token counting and limit management
- Conversation threading

## Usage

### Frontend
The RayyAIchat component is already integrated. Users can:
1. Click "Ask RayyAI" button to open chat
2. Send messages - conversations are auto-created
3. Click "New Chat" to start a new conversation
4. View markdown-formatted AI responses
5. See action execution confirmations

### Backend
The API handles:
1. Message sending with full RAG context
2. Automatic conversation creation
3. Context retrieval and formatting
4. PII masking before LLM
5. Action parsing and execution
6. Response generation and storage

## Testing

1. Start backend server:
```bash
cd rayyai-backend
uvicorn main:app --reload
```

2. Start frontend:
```bash
cd rayyai-frontend/rayyai
npm run dev
```

3. Test chat functionality:
   - Log in to the application
   - Click "Ask RayyAI" button
   - Send a message like "Show me my spending summary"
   - Verify AI response includes personalized financial data

## Notes

- Embeddings setup is optional (Phase 2 enhancement)
- The module is fully functional with SQL-based retrieval
- Streaming responses are supported but not implemented in frontend yet
- Error handling is in place but may need refinement based on usage

## Troubleshooting

### Common Issues

1. **Gemini API Error**: Ensure `GEMINI_API_KEY` is set in `.env`
2. **Database Error**: Run migrations to create new tables
3. **Frontend Error**: Install `react-markdown` package
4. **Import Error**: Ensure all services are in the `services/` directory

### Support
For issues, check:
- Backend logs for API errors
- Browser console for frontend errors
- Database connection status
- Gemini API key validity

