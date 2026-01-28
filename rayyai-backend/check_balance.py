from database import SessionLocal
from services.rag_service import RAGService

db = SessionLocal()
rag = RAGService(db)
summary = rag.get_financial_summary(1)

print(f"Total Balance: RM{summary['accounts']['total_balance']:,.2f}")
print("\nAccounts:")
for acc in summary['accounts']['accounts']:
    print(f"  - {acc['account_name']}: RM{acc['balance']:,.2f}")

db.close()

