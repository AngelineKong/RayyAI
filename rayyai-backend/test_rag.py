"""
Test script for RAG (Retrieval-Augmented Generation) Service
Tests data retrieval, formatting, and context generation for financial data.
"""
from database import SessionLocal
from services.rag_service import RAGService
from models import User
import json

def test_rag_service(user_id=1):
    """Test RAG service data retrieval and formatting"""
    
    print("=" * 70)
    print("RAG Service Test")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # Verify user exists
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            print(f"\n[ERROR] User with ID {user_id} not found!")
            return False
        
        print(f"\n[OK] Testing with user: {user.first_name} {user.last_name} (ID: {user.user_id})")
        
        # Initialize RAG service
        rag_service = RAGService(db)
        
        print("\n" + "=" * 70)
        print("1. TESTING ACCOUNT RETRIEVAL")
        print("=" * 70)
        
        accounts = rag_service.get_user_accounts(user_id)
        print(f"\n[RESULT] Retrieved {len(accounts)} accounts")
        
        if len(accounts) == 0:
            print("[WARNING] No accounts found - RAG will have limited context")
        else:
            print("\n[ACCOUNTS]")
            for acc in accounts:
                print(f"  - {acc['account_name']} ({acc['account_type']}): RM{acc['balance']:,.2f}")
        
        print("\n" + "=" * 70)
        print("2. TESTING TRANSACTION RETRIEVAL")
        print("=" * 70)
        
        transactions = rag_service.get_recent_transactions(user_id, days=90, limit=100)
        income_count = len(transactions.get("income", []))
        expense_count = len(transactions.get("expense", []))
        
        print(f"\n[RESULT] Retrieved {income_count} income transactions and {expense_count} expense transactions")
        
        if income_count > 0:
            print(f"\n[INCOME SAMPLE] (showing first 3)")
            for inc in transactions["income"][:3]:
                print(f"  - RM{inc['amount']:,.2f} from {inc['payer']} ({inc['category']}) on {inc['date_received']}")
        
        if expense_count > 0:
            print(f"\n[EXPENSE SAMPLE] (showing first 3)")
            for exp in transactions["expense"][:3]:
                print(f"  - RM{exp['amount']:,.2f} to {exp['seller']} ({exp['category']}, {exp.get('expense_type', 'N/A')}) on {exp['date_spent']}")
        
        print("\n" + "=" * 70)
        print("3. TESTING SPENDING SUMMARY")
        print("=" * 70)
        
        spending_summary = rag_service.get_spending_summary(user_id, days=30)
        print(f"\n[RESULT] Total spending (last 30 days): RM{spending_summary.get('total_spending', 0):,.2f}")
        
        if spending_summary.get('by_category'):
            print(f"\n[SPENDING BY CATEGORY]")
            for category, amount in sorted(
                spending_summary['by_category'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]:
                print(f"  - {category}: RM{amount:,.2f}")
        
        if spending_summary.get('needs_vs_wants'):
            print(f"\n[NEEDS VS WANTS]")
            for exp_type, amount in spending_summary['needs_vs_wants'].items():
                print(f"  - {exp_type}: RM{amount:,.2f}")
        
        print("\n" + "=" * 70)
        print("4. TESTING BUDGET STATUS")
        print("=" * 70)
        
        budgets = rag_service.get_budgets_status(user_id)
        print(f"\n[RESULT] Retrieved {len(budgets)} active budgets")
        
        if len(budgets) == 0:
            print("[WARNING] No active budgets found")
        else:
            print("\n[BUDGETS]")
            for budget in budgets:
                status = "OVER BUDGET" if budget["is_over_budget"] else (
                    "NEAR LIMIT" if budget["is_near_limit"] else "OK"
                )
                print(f"  - {budget['name']} ({budget['category']}): "
                      f"RM{budget['spent_amount']:,.2f} / RM{budget['limit_amount']:,.2f} "
                      f"({budget['percentage_used']:.1f}%) - {status}")
        
        print("\n" + "=" * 70)
        print("5. TESTING GOALS STATUS")
        print("=" * 70)
        
        goals = rag_service.get_goals_status(user_id)
        print(f"\n[RESULT] Retrieved {len(goals)} goals")
        
        if len(goals) == 0:
            print("[WARNING] No goals found")
        else:
            print("\n[GOALS]")
            for goal in goals:
                status = "COMPLETED" if goal["is_completed"] else "IN PROGRESS"
                print(f"  - {goal['goal_name']} ({goal['category']}): "
                      f"RM{goal['current_amount']:,.2f} / RM{goal['target_amount']:,.2f} "
                      f"({goal['progress_percentage']:.1f}%) - {status}")
                if goal.get("target_date"):
                    print(f"    Target: {goal['target_date']} ({goal.get('days_remaining', 0)} days remaining)")
        
        print("\n" + "=" * 70)
        print("6. TESTING CREDIT CARDS")
        print("=" * 70)
        
        credit_cards = rag_service.get_credit_cards(user_id)
        print(f"\n[RESULT] Retrieved {len(credit_cards)} credit cards")
        
        if len(credit_cards) == 0:
            print("[WARNING] No credit cards found")
        else:
            print("\n[CREDIT CARDS]")
            for card in credit_cards:
                print(f"  - {card['card_name']} ({card['bank_name']}): "
                      f"RM{card['current_balance']:,.2f} / RM{card['credit_limit']:,.2f} "
                      f"({card['utilization_percentage']:.1f}% utilization)")
                if card.get("next_payment_date"):
                    print(f"    Next Payment: RM{card['next_payment_amount']:,.2f} on {card['next_payment_date']}")
        
        print("\n" + "=" * 70)
        print("7. TESTING FINANCIAL SUMMARY (COMPREHENSIVE)")
        print("=" * 70)
        
        financial_summary = rag_service.get_financial_summary(user_id)
        
        print(f"\n[SUMMARY STATISTICS]")
        print(f"  Accounts: {financial_summary['accounts']['total_count']} "
              f"(Total Balance: RM{financial_summary['accounts']['total_balance']:,.2f})")
        print(f"  Transactions (90d): {financial_summary['transactions']['recent_income']} income, "
              f"{financial_summary['transactions']['recent_expenses']} expenses")
        print(f"  Net Flow (90d): RM{financial_summary['transactions']['net_flow_90d']:,.2f}")
        print(f"  Budgets: {financial_summary['budgets']['active_count']} active "
              f"({financial_summary['budgets']['over_budget_count']} over budget)")
        print(f"  Goals: {financial_summary['goals']['total_count']} total "
              f"({financial_summary['goals']['completed_count']} completed)")
        print(f"  Credit Cards: {financial_summary['credit_cards']['total_count']} "
              f"({financial_summary['credit_cards']['total_utilization']:.1f}% total utilization)")
        
        print("\n" + "=" * 70)
        print("8. TESTING CONTEXT FORMATTING FOR LLM")
        print("=" * 70)
        
        formatted_context = rag_service.format_context_for_llm(financial_summary)
        
        print(f"\n[FORMATTED CONTEXT LENGTH] {len(formatted_context)} characters")
        print(f"\n[FORMATTED CONTEXT PREVIEW] (first 500 characters)")
        print("-" * 70)
        print(formatted_context[:500])
        print("...")
        print("-" * 70)
        
        print("\n[FORMATTED CONTEXT FULL]")
        print("=" * 70)
        print(formatted_context)
        print("=" * 70)
        
        # Validation checks
        print("\n" + "=" * 70)
        print("VALIDATION CHECKS")
        print("=" * 70)
        
        checks_passed = 0
        checks_total = 0
        
        # Check 1: Accounts exist
        checks_total += 1
        if len(accounts) > 0:
            print("[PASS] Accounts retrieved successfully")
            checks_passed += 1
        else:
            print("[FAIL] No accounts found")
        
        # Check 2: Transactions exist
        checks_total += 1
        if income_count > 0 or expense_count > 0:
            print("[PASS] Transactions retrieved successfully")
            checks_passed += 1
        else:
            print("[FAIL] No transactions found")
        
        # Check 3: Context formatted
        checks_total += 1
        if len(formatted_context) > 100:
            print("[PASS] Context formatting works")
            checks_passed += 1
        else:
            print("[FAIL] Context formatting too short or empty")
        
        # Check 4: Context contains expected sections
        checks_total += 1
        expected_sections = ["ACCOUNTS", "TRANSACTIONS", "SPENDING", "BUDGETS", "GOALS", "CREDIT CARDS"]
        sections_found = sum(1 for section in expected_sections if section in formatted_context)
        if sections_found >= 3:  # At least 3 sections should be present
            print(f"[PASS] Context contains {sections_found}/{len(expected_sections)} expected sections")
            checks_passed += 1
        else:
            print(f"[FAIL] Context missing expected sections (found {sections_found}/{len(expected_sections)})")
        
        # Check 5: Financial summary complete
        checks_total += 1
        required_keys = ["accounts", "transactions", "spending_summary", "budgets", "goals", "credit_cards"]
        keys_present = sum(1 for key in required_keys if key in financial_summary)
        if keys_present == len(required_keys):
            print("[PASS] Financial summary contains all required keys")
            checks_passed += 1
        else:
            print(f"[FAIL] Financial summary missing keys (found {keys_present}/{len(required_keys)})")
        
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Checks Passed: {checks_passed}/{checks_total}")
        
        if checks_passed == checks_total:
            print("\n[SUCCESS] All RAG tests passed!")
            return True
        else:
            print(f"\n[WARNING] {checks_total - checks_passed} test(s) failed. Review the output above.")
            return False
        
    except Exception as e:
        print(f"\n[ERROR] Error during RAG testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("\nStarting RAG Service Test...\n")
    success = test_rag_service(user_id=1)
    
    if success:
        print("\n[SUCCESS] RAG service is ready for use!")
    else:
        print("\n[WARNING] Please review the errors above and fix any issues.")
    
    print("\n" + "=" * 70)

