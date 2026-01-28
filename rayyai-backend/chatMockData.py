"""
Comprehensive Mock Data Script for RAG Testing
Creates realistic financial data including accounts, transactions, budgets, goals, and credit cards.
"""
from database import SessionLocal
from models import (
    User, Account, Income, Expense, Budget, Goal, UserCreditCard,
    AccountBalanceSnapshot
)
from datetime import date, datetime, timedelta
from passlib.context import CryptContext
from routers.utils import calculate_account_balance
import random

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_mock_user(db, user_id=1):
    """Create or get a test user"""
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        user = User(
            user_id=user_id,
            first_name="John",
            last_name="Doe",
            email="test@example.com",
            password=hash_password("testpassword123"),
            dob=date(1990, 5, 15),
            gender="Male",
            is_deleted=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"[CREATED] User: {user.first_name} {user.last_name} (ID: {user.user_id})")
    else:
        print(f"[EXISTS] User: {user.first_name} {user.last_name} (ID: {user.user_id})")
    
    return user

def create_mock_accounts(db, user_id):
    """Create diverse accounts for testing"""
    accounts_data = [
        {"name": "Main Savings Account", "type": "savings", "subtype": "Islamic Savings", "account_no": "SAV-001"},
        {"name": "Current Account", "type": "current", "subtype": None, "account_no": "CUR-001"},
        {"name": "Investment Account", "type": "investment", "subtype": "Stocks Portfolio", "account_no": "INV-001"},
        {"name": "Cash Wallet", "type": "cash", "subtype": None, "account_no": None},
        {"name": "E-Wallet", "type": "ewallet", "subtype": "GrabPay", "account_no": "EW-001"},
    ]
    
    accounts = {}
    for acc_data in accounts_data:
        existing = db.query(Account).filter(
            Account.user_id == user_id,
            Account.account_name == acc_data["name"],
            Account.is_deleted == False
        ).first()
        
        if existing:
            accounts[acc_data["name"]] = existing
            print(f"[EXISTS] Account: {acc_data['name']} (ID: {existing.account_id})")
        else:
            account = Account(
                user_id=user_id,
                account_name=acc_data["name"],
                account_type=acc_data["type"],
                account_subtype=acc_data["subtype"],
                account_no=acc_data["account_no"],
                is_deleted=False
            )
            db.add(account)
            db.flush()
            accounts[acc_data["name"]] = account
            print(f"[CREATED] Account: {acc_data['name']} (ID: {account.account_id})")
    
    db.commit()
    return accounts

def create_mock_credit_cards(db, user_id):
    """Create mock credit cards"""
    cards_data = [
        {
            "card_name": "Harimau 2 Card",
            "bank_name": "Harimau Bank",
            "card_brand": "Visa",
            "credit_limit": 50000.0,
            "current_balance": 12500.0,
            "annual_fee": 160.0,
            "expiry_month": 12,
            "expiry_year": 2028,
            "next_payment_amount": 2500.0,
            "next_payment_date": date.today() + timedelta(days=15),
            "benefits": {"cashback": "5%", "rewards": "Miles"}
        },
        {
            "card_name": "Sotong Enrich",
            "bank_name": "Sotong Bank",
            "card_brand": "Mastercard",
            "credit_limit": 30000.0,
            "current_balance": 8500.0,
            "annual_fee": 200.0,
            "expiry_month": 8,
            "expiry_year": 2027,
            "next_payment_amount": 1700.0,
            "next_payment_date": date.today() + timedelta(days=22),
            "benefits": {"miles": "3x Enrich miles", "bonus": "10,000 bonus miles"}
        },
    ]
    
    cards = {}
    for card_data in cards_data:
        existing = db.query(UserCreditCard).filter(
            UserCreditCard.user_id == user_id,
            UserCreditCard.card_name == card_data["card_name"],
            UserCreditCard.is_deleted == False
        ).first()
        
        if existing:
            cards[card_data["card_name"]] = existing
            print(f"[EXISTS] Credit Card: {card_data['card_name']} (ID: {existing.card_id})")
        else:
            card = UserCreditCard(
                user_id=user_id,
                card_number=f"****-****-****-{random.randint(1000, 9999)}",
                card_name=card_data["card_name"],
                bank_name=card_data["bank_name"],
                card_brand=card_data["card_brand"],
                credit_limit=card_data["credit_limit"],
                current_balance=card_data["current_balance"],
                annual_fee=card_data["annual_fee"],
                expiry_month=card_data["expiry_month"],
                expiry_year=card_data["expiry_year"],
                next_payment_amount=card_data["next_payment_amount"],
                next_payment_date=card_data["next_payment_date"],
                benefits=card_data["benefits"],
                is_deleted=False
            )
            db.add(card)
            db.flush()
            cards[card_data["card_name"]] = card
            print(f"[CREATED] Credit Card: {card_data['card_name']} (ID: {card.card_id})")
    
    db.commit()
    return cards

def create_mock_transactions(db, user_id, accounts):
    """Create diverse transactions for the past 90 days with daily granularity"""
    today = date.today()
    
    # Income transactions
    income_transactions = [
        {"date": today - timedelta(days=0), "amount": 500.0, "category": "Freelance", "description": "Client Payment", "payer": "Startup XYZ"},
        {"date": today - timedelta(days=1), "amount": 350.0, "category": "Freelance", "description": "Consulting Session", "payer": "Tech Startup"},
        {"date": today - timedelta(days=5), "amount": 5500.0, "category": "Salary", "description": "Monthly Salary", "payer": "ABC Corp"},
        {"date": today - timedelta(days=15), "amount": 1200.0, "category": "Freelance", "description": "Web Development Project", "payer": "Tech Solutions Inc"},
        {"date": today - timedelta(days=35), "amount": 5500.0, "category": "Salary", "description": "Monthly Salary", "payer": "ABC Corp"},
        {"date": today - timedelta(days=45), "amount": 800.0, "category": "Investment Returns", "description": "Dividend Payment", "payer": "Investment Fund"},
        {"date": today - timedelta(days=65), "amount": 5500.0, "category": "Salary", "description": "Monthly Salary", "payer": "ABC Corp"},
    ]
    
    # Expense transactions - needs (daily essentials)
    expense_needs = [
        # Today
        {"date": today, "amount": 45.0, "category": "Food & Dining", "description": "Lunch", "seller": "Mamak Restaurant", "expense_type": "needs"},
        {"date": today, "amount": 25.0, "category": "Transportation", "description": "Grab to Office", "seller": "Grab", "expense_type": "needs"},
        # Yesterday
        {"date": today - timedelta(days=1), "amount": 35.0, "category": "Food & Dining", "description": "Breakfast & Lunch", "seller": "Local Cafe", "expense_type": "needs"},
        {"date": today - timedelta(days=1), "amount": 60.0, "category": "Groceries", "description": "Fresh Produce", "seller": "Wet Market", "expense_type": "needs"},
        {"date": today - timedelta(days=1), "amount": 30.0, "category": "Transportation", "description": "Fuel", "seller": "Petronas", "expense_type": "needs"},
        # 2 days ago
        {"date": today - timedelta(days=2), "amount": 50.0, "category": "Food & Dining", "description": "Family Dinner", "seller": "Chinese Restaurant", "expense_type": "needs"},
        {"date": today - timedelta(days=2), "amount": 20.0, "category": "Transportation", "description": "Parking Fee", "seller": "Parking Mall", "expense_type": "needs"},
        # 3 days ago
        {"date": today - timedelta(days=3), "amount": 250.0, "category": "Utilities", "description": "Electricity Bill", "seller": "TNB", "expense_type": "needs"},
        {"date": today - timedelta(days=3), "amount": 40.0, "category": "Food & Dining", "description": "Lunch Meeting", "seller": "Cafe", "expense_type": "needs"},
        # 4 days ago
        {"date": today - timedelta(days=4), "amount": 120.0, "category": "Groceries", "description": "Weekly Groceries", "seller": "Giant Supermarket", "expense_type": "needs"},
        {"date": today - timedelta(days=4), "amount": 35.0, "category": "Transportation", "description": "MRT Top-up", "seller": "MRT Station", "expense_type": "needs"},
        # 5 days ago
        {"date": today - timedelta(days=5), "amount": 45.0, "category": "Food & Dining", "description": "Lunch & Dinner", "seller": "Food Court", "expense_type": "needs"},
        {"date": today - timedelta(days=5), "amount": 80.0, "category": "Utilities", "description": "Water Bill", "seller": "SYABAS", "expense_type": "needs"},
        # 6 days ago
        {"date": today - timedelta(days=6), "amount": 55.0, "category": "Food & Dining", "description": "Daily Meals", "seller": "Mixed", "expense_type": "needs"},
        {"date": today - timedelta(days=6), "amount": 25.0, "category": "Transportation", "description": "Grab Rides", "seller": "Grab", "expense_type": "needs"},
        # Week 2
        {"date": today - timedelta(days=8), "amount": 180.0, "category": "Healthcare", "description": "Medical Checkup", "seller": "Clinic ABC", "expense_type": "needs"},
        {"date": today - timedelta(days=10), "amount": 150.0, "category": "Groceries", "description": "Weekly Shopping", "seller": "Tesco", "expense_type": "needs"},
        {"date": today - timedelta(days=12), "amount": 90.0, "category": "Food & Dining", "description": "Work Lunches", "seller": "Various", "expense_type": "needs"},
        {"date": today - timedelta(days=14), "amount": 100.0, "category": "Transportation", "description": "Fuel", "seller": "Shell", "expense_type": "needs"},
        # Week 3-4
        {"date": today - timedelta(days=18), "amount": 130.0, "category": "Groceries", "description": "Household Items", "seller": "Giant", "expense_type": "needs"},
        {"date": today - timedelta(days=22), "amount": 70.0, "category": "Food & Dining", "description": "Meals", "seller": "Various", "expense_type": "needs"},
        {"date": today - timedelta(days=25), "amount": 110.0, "category": "Transportation", "description": "Weekly Transport", "seller": "Mixed", "expense_type": "needs"},
        # Month 2
        {"date": today - timedelta(days=35), "amount": 2000.0, "category": "Rent", "description": "Monthly Rent", "seller": "Property Management", "expense_type": "needs"},
        {"date": today - timedelta(days=40), "amount": 160.0, "category": "Groceries", "description": "Bulk Shopping", "seller": "Tesco", "expense_type": "needs"},
        {"date": today - timedelta(days=50), "amount": 120.0, "category": "Utilities", "description": "Internet Bill", "seller": "Maxis", "expense_type": "needs"},
        {"date": today - timedelta(days=65), "amount": 2000.0, "category": "Rent", "description": "Monthly Rent", "seller": "Property Management", "expense_type": "needs"},
    ]
    
    # Expense transactions - wants (discretionary spending)
    expense_wants = [
        # Today
        {"date": today, "amount": 28.0, "category": "Dining Out", "description": "Coffee & Pastry", "seller": "Starbucks", "expense_type": "wants"},
        # Yesterday
        {"date": today - timedelta(days=1), "amount": 85.0, "category": "Entertainment", "description": "Movie Tickets", "seller": "GSC", "expense_type": "wants"},
        {"date": today - timedelta(days=1), "amount": 45.0, "category": "Dining Out", "description": "Dinner with Friends", "seller": "Japanese Restaurant", "expense_type": "wants"},
        # 2 days ago
        {"date": today - timedelta(days=2), "amount": 120.0, "category": "Shopping", "description": "New Shirt", "seller": "Uniqlo", "expense_type": "wants"},
        # 3 days ago
        {"date": today - timedelta(days=3), "amount": 55.0, "category": "Dining Out", "description": "Brunch", "seller": "Cafe", "expense_type": "wants"},
        # 4 days ago
        {"date": today - timedelta(days=4), "amount": 35.0, "category": "Entertainment", "description": "Online Subscription", "seller": "Netflix", "expense_type": "wants"},
        # 5 days ago
        {"date": today - timedelta(days=5), "amount": 90.0, "category": "Hobbies", "description": "Sports Equipment", "seller": "Decathlon", "expense_type": "wants"},
        # 6 days ago
        {"date": today - timedelta(days=6), "amount": 65.0, "category": "Dining Out", "description": "Weekend Brunch", "seller": "Brunch Spot", "expense_type": "wants"},
        # Week 2
        {"date": today - timedelta(days=7), "amount": 200.0, "category": "Shopping", "description": "Clothing", "seller": "Zara", "expense_type": "wants"},
        {"date": today - timedelta(days=9), "amount": 75.0, "category": "Entertainment", "description": "Concert Tickets", "seller": "Live Nation", "expense_type": "wants"},
        {"date": today - timedelta(days=11), "amount": 110.0, "category": "Dining Out", "description": "Date Night", "seller": "Italian Restaurant", "expense_type": "wants"},
        {"date": today - timedelta(days=14), "amount": 80.0, "category": "Entertainment", "description": "Gaming", "seller": "Steam", "expense_type": "wants"},
        # Week 3-4
        {"date": today - timedelta(days=16), "amount": 150.0, "category": "Hobbies", "description": "Gym Membership", "seller": "Fitness First", "expense_type": "wants"},
        {"date": today - timedelta(days=20), "amount": 95.0, "category": "Dining Out", "description": "Fancy Dinner", "seller": "Fine Dining", "expense_type": "wants"},
        {"date": today - timedelta(days=22), "amount": 450.0, "category": "Shopping", "description": "Electronics", "seller": "Lazada", "expense_type": "wants"},
        {"date": today - timedelta(days=28), "amount": 300.0, "category": "Travel", "description": "Hotel Booking", "seller": "Booking.com", "expense_type": "wants"},
        # Month 2
        {"date": today - timedelta(days=35), "amount": 180.0, "category": "Shopping", "description": "Shoes", "seller": "Nike", "expense_type": "wants"},
        {"date": today - timedelta(days=42), "amount": 250.0, "category": "Dining Out", "description": "Weekend Dining", "seller": "Various", "expense_type": "wants"},
        {"date": today - timedelta(days=50), "amount": 120.0, "category": "Entertainment", "description": "Shows", "seller": "Mixed", "expense_type": "wants"},
        {"date": today - timedelta(days=60), "amount": 200.0, "category": "Hobbies", "description": "Hobby Supplies", "seller": "Hobby Store", "expense_type": "wants"},
    ]
    
    # Account selection
    account_list = list(accounts.values())
    
    # Insert income
    income_count = 0
    for trans in income_transactions:
        if trans["date"] >= today - timedelta(days=90):
            income = Income(
                user_id=user_id,
                account_id=account_list[0].account_id,  # Main Savings
                amount=trans["amount"],
                description=trans["description"],
                category=trans["category"],
                date_received=trans["date"],
                payer=trans["payer"],
                is_deleted=False
            )
            db.add(income)
            income_count += 1
    
    # Insert expenses
    expense_count = 0
    all_expenses = expense_needs + expense_wants
    for trans in all_expenses:
        if trans["date"] >= today - timedelta(days=90):
            expense = Expense(
                user_id=user_id,
                account_id=random.choice(account_list).account_id,
                amount=trans["amount"],
                description=trans["description"],
                category=trans["category"],
                expense_type=trans.get("expense_type"),
                date_spent=trans["date"],
                seller=trans["seller"],
                is_deleted=False
            )
            db.add(expense)
            expense_count += 1
    
    db.commit()
    print(f"[CREATED] {income_count} income transactions")
    print(f"[CREATED] {expense_count} expense transactions")
    return income_count + expense_count

def create_mock_budgets(db, user_id):
    """Create active budgets"""
    today = date.today()
    budgets_data = [
        {
            "name": "Monthly Groceries Budget",
            "category": "Groceries",
            "limit_amount": 500.0,
            "period_start": date(today.year, today.month, 1),
            "period_end": date(today.year, today.month + 1, 1) - timedelta(days=1),
            "alert_threshold": 0.8
        },
        {
            "name": "Food & Dining Budget",
            "category": "Food & Dining",
            "limit_amount": 400.0,
            "period_start": date(today.year, today.month, 1),
            "period_end": date(today.year, today.month + 1, 1) - timedelta(days=1),
            "alert_threshold": 0.8
        },
        {
            "name": "Transportation Budget",
            "category": "Transportation",
            "limit_amount": 300.0,
            "period_start": date(today.year, today.month, 1),
            "period_end": date(today.year, today.month + 1, 1) - timedelta(days=1),
            "alert_threshold": 0.8
        },
        {
            "name": "Entertainment Budget",
            "category": "Entertainment",
            "limit_amount": 200.0,
            "period_start": date(today.year, today.month, 1),
            "period_end": date(today.year, today.month + 1, 1) - timedelta(days=1),
            "alert_threshold": 0.8
        },
    ]
    
    budgets = []
    for budget_data in budgets_data:
        existing = db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.name == budget_data["name"],
            Budget.is_deleted == False
        ).first()
        
        if existing:
            budgets.append(existing)
            print(f"[EXISTS] Budget: {budget_data['name']} (ID: {existing.budget_id})")
        else:
            budget = Budget(
                user_id=user_id,
                name=budget_data["name"],
                limit_amount=budget_data["limit_amount"],
                category=budget_data["category"],
                period_start=budget_data["period_start"],
                period_end=budget_data["period_end"],
                alert_threshold=budget_data["alert_threshold"],
                is_deleted=False
            )
            db.add(budget)
            db.flush()
            budgets.append(budget)
            print(f"[CREATED] Budget: {budget_data['name']} (ID: {budget.budget_id})")
    
    db.commit()
    return budgets

def create_mock_goals(db, user_id):
    """Create financial goals"""
    today = date.today()
    goals_data = [
        {
            "goal_name": "Emergency Fund",
            "description": "Build 6 months emergency fund",
            "category": "Savings",
            "priority": "High",
            "target_amount": 30000.0,
            "current_amount": 15000.0,
            "target_date": date(today.year + 1, 6, 30)
        },
        {
            "goal_name": "Vacation to Europe",
            "description": "Save for dream vacation",
            "category": "Travel",
            "priority": "Medium",
            "target_amount": 15000.0,
            "current_amount": 5000.0,
            "target_date": date(today.year + 1, 12, 31)
        },
        {
            "goal_name": "New Car Down Payment",
            "description": "Save for car down payment",
            "category": "Transportation",
            "priority": "High",
            "target_amount": 20000.0,
            "current_amount": 8000.0,
            "target_date": date(today.year + 1, 3, 31)
        },
        {
            "goal_name": "Home Renovation",
            "description": "Kitchen and bathroom renovation",
            "category": "Home",
            "priority": "Low",
            "target_amount": 50000.0,
            "current_amount": 12000.0,
            "target_date": date(today.year + 2, 6, 30)
        },
    ]
    
    goals = []
    for goal_data in goals_data:
        existing = db.query(Goal).filter(
            Goal.user_id == user_id,
            Goal.goal_name == goal_data["goal_name"],
            Goal.is_deleted == False
        ).first()
        
        if existing:
            goals.append(existing)
            print(f"[EXISTS] Goal: {goal_data['goal_name']} (ID: {existing.goal_id})")
        else:
            goal = Goal(
                user_id=user_id,
                goal_name=goal_data["goal_name"],
                description=goal_data["description"],
                category=goal_data["category"],
                priority=goal_data["priority"],
                target_amount=goal_data["target_amount"],
                current_amount=goal_data["current_amount"],
                target_date=goal_data["target_date"],
                is_deleted=False
            )
            db.add(goal)
            db.flush()
            goals.append(goal)
            print(f"[CREATED] Goal: {goal_data['goal_name']} (ID: {goal.goal_id})")
    
    db.commit()
    return goals

def main():
    """Main function to create all mock data"""
    db = SessionLocal()
    
    try:
        print("=" * 70)
        print("Comprehensive Mock Data Creation Script")
        print("=" * 70)
        
        user_id = 1
        
        # Create user
        print("\n=== Creating User ===")
        user = create_mock_user(db, user_id)
        
        # Create accounts
        print("\n=== Creating Accounts ===")
        accounts = create_mock_accounts(db, user_id)
        
        # Create credit cards
        print("\n=== Creating Credit Cards ===")
        cards = create_mock_credit_cards(db, user_id)
        
        # Link credit cards to accounts
        print("\n=== Linking Credit Cards to Accounts ===")
        card_list = list(cards.values())
        account_list = list(accounts.values())
        if len(card_list) > 0 and len(account_list) > 0:
            # Link first card to an account if not already linked
            account_with_card = None
            for acc in account_list:
                if acc.account_type == "credit" and not acc.card_id:
                    acc.card_id = card_list[0].card_id
                    account_with_card = acc
                    break
            if account_with_card:
                db.commit()
                print(f"[LINKED] Credit card {card_list[0].card_name} to account")
        
        # Create transactions
        print("\n=== Creating Transactions ===")
        transaction_count = create_mock_transactions(db, user_id, accounts)
        
        # Create budgets
        print("\n=== Creating Budgets ===")
        budgets = create_mock_budgets(db, user_id)
        
        # Create goals
        print("\n=== Creating Goals ===")
        goals = create_mock_goals(db, user_id)
        
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"[OK] User: {user.first_name} {user.last_name}")
        print(f"[OK] Accounts: {len(accounts)}")
        print(f"[OK] Credit Cards: {len(cards)}")
        print(f"[OK] Transactions: {transaction_count}")
        print(f"[OK] Budgets: {len(budgets)}")
        print(f"[OK] Goals: {len(goals)}")
        print("\n[SUCCESS] Mock data created successfully!")
        print("[INFO] You can now test RAG functionality with this data.")
        
    except Exception as e:
        print(f"\n[ERROR] Error creating mock data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

