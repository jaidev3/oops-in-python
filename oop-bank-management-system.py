
# Problem Statement: Create a bank account management system that handles different types of accounts with proper encapsulation and class methods.

# Your Task: Write the complete classes from scratch to support the following operations

class Account:
    # Class variables
    _total_accounts = 0
    bank_name = "Default Bank"
    _minimum_balance = 0
    
    def __init__(self, account_number, account_holder, initial_balance):
        # Validate inputs
        if not account_number or not account_holder:
            raise ValueError("Account number and account holder cannot be empty")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        # Private attributes (encapsulation)
        self._account_number = account_number
        self._account_holder = account_holder
        self._balance = initial_balance
        
        # Increment total accounts
        Account._total_accounts += 1
    
    # Getter methods (encapsulation)
    def get_account_number(self):
        return self._account_number
    
    def get_account_holder(self):
        return self._account_holder
    
    def get_balance(self):
        return self._balance
    
    # Deposit method
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        return True
    
    # Withdraw method (to be overridden in subclasses)
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance >= amount:
            self._balance -= amount
            return True
        return False
    
    # Class methods
    @classmethod
    def get_total_accounts(cls):
        return cls._total_accounts
    
    @classmethod
    def set_bank_name(cls, name):
        cls.bank_name = name
    
    @classmethod
    def set_minimum_balance(cls, amount):
        cls._minimum_balance = amount
    
    # String representation
    def __str__(self):
        return f"Account({self._account_number}, {self._account_holder}, Balance: ${self._balance})"


class SavingsAccount(Account):
    def __init__(self, account_number, account_holder, initial_balance, interest_rate):
        # Validate interest rate
        if interest_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        
        super().__init__(account_number, account_holder, initial_balance)
        self._interest_rate = interest_rate
    
    def get_interest_rate(self):
        return self._interest_rate
    
    def calculate_monthly_interest(self):
        """Calculate monthly interest based on current balance and interest rate"""
        monthly_rate = self._interest_rate / 100 / 12  # Convert percentage to decimal and divide by 12
        return self._balance * monthly_rate
    
    def apply_interest(self):
        """Apply monthly interest to the account"""
        interest = self.calculate_monthly_interest()
        self._balance += interest
        return interest
    
    def __str__(self):
        return f"SavingsAccount({self._account_number}, {self._account_holder}, Balance: ${self._balance}, Interest Rate: {self._interest_rate}%)"


class CheckingAccount(Account):
    def __init__(self, account_number, account_holder, initial_balance, overdraft_limit):
        # Validate overdraft limit
        if overdraft_limit < 0:
            raise ValueError("Overdraft limit cannot be negative")
        
        super().__init__(account_number, account_holder, initial_balance)
        self._overdraft_limit = overdraft_limit
    
    def get_overdraft_limit(self):
        return self._overdraft_limit
    
    def withdraw(self, amount):
        """Override withdraw method to allow overdraft"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        # Check if withdrawal is possible with overdraft
        available_funds = self._balance + self._overdraft_limit
        
        if amount <= available_funds:
            self._balance -= amount
            return True
        return False
    
    def get_available_balance(self):
        """Get total available balance including overdraft"""
        return self._balance + self._overdraft_limit
    
    def __str__(self):
        return f"CheckingAccount({self._account_number}, {self._account_holder}, Balance: ${self._balance}, Overdraft Limit: ${self._overdraft_limit})"


# Test Case 1: Creating different types of accounts
savings_account = SavingsAccount("SA001", "Alice Johnson", 1000, 2.5)
checking_account = CheckingAccount("CA001", "Bob Smith", 500, 200)

print(f"Savings Account: {savings_account}")
print(f"Checking Account: {checking_account}")

# Test Case 2: Deposit and Withdrawal operations
print(f"Savings balance before: ${savings_account.get_balance()}")
savings_account.deposit(500)
print(f"After depositing $500: ${savings_account.get_balance()}")

withdrawal_result = savings_account.withdraw(200)
print(f"Withdrawal result: {withdrawal_result}")
print(f"Balance after withdrawal: ${savings_account.get_balance()}")

# Test Case 3: Overdraft protection in checking account
print(f"Checking balance: ${checking_account.get_balance()}")
overdraft_result = checking_account.withdraw(600)  # Should use overdraft
print(f"Overdraft withdrawal: {overdraft_result}")
print(f"Balance after overdraft: ${checking_account.get_balance()}")

# Test Case 4: Interest calculation for savings
interest_earned = savings_account.calculate_monthly_interest()
print(f"Monthly interest earned: ${interest_earned}")

# Test Case 5: Class methods and variables
print(f"Total accounts created: {Account.get_total_accounts()}")
print(f"Bank name: {Account.bank_name}")

# Change bank settings using class method
Account.set_bank_name("New National Bank")
Account.set_minimum_balance(100)

# Test Case 6: Account validation
try:
    invalid_account = SavingsAccount("SA002", "", -100, 1.5)  # Should raise error
except ValueError as e:
    print(f"Validation error: {e}")

# Expected outputs should show proper account creation, transaction handling,
# interest calculation, and class-level operations
