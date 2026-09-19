# gdb/tests/test_interface_factory.py
from gdb.domain.account_factory import AccountFactory
from gdb.domain.iaccount import IAccount
from gdb.exceptions import AccountException


def main():
    print("=== Activity 12: Factory-Driven System Suite ===")

    # ------------------------------------------------------------------
    # Step 1: Create one account of each type ONLY through the factory
    # ------------------------------------------------------------------
    savings = AccountFactory.create_account(
        "SAVINGS", "SAV001", "Alice", 30, 5000.0, "Active", "1234"
    )
    current = AccountFactory.create_account(
        "CURRENT", "CUR001", "Bob", 40, 2000.0, "Active", "5678"
    )
    salary = AccountFactory.create_account(
        "SALARY", "SAL001", "Charlie", 25, 1000.0, "Active", "9012"
    )
    fixed_deposit = AccountFactory.create_account(
        "FIXEDDEPOSIT", "FD001", "Diana", 35, 10000.0, "Active", "3456"
    )

    accounts = [
        ("SAVINGS", savings, 5000.0, "Savings"),
        ("CURRENT", current, 2000.0, "Current"),
        ("SALARY", salary, 1000.0, "Salary"),
        ("FIXEDDEPOSIT", fixed_deposit, 10000.0, "FixedDeposit"),
    ]

    # ------------------------------------------------------------------
    # Step 2: Exercise methods and assert properties purely through IAccount
    # ------------------------------------------------------------------
    for acc_type, acc, expected_balance, expected_type in accounts:
        # All accounts must be usable as IAccount
        assert isinstance(acc, IAccount), f"{acc_type} does not implement IAccount"
        assert acc.balance == expected_balance, f"{acc_type} initial balance mismatch"
        assert acc.get_account_type() == expected_type, f"{acc_type} type name mismatch"
        print(f"Created {acc_type}: {acc.get_account_type()}, Balance: {acc.balance}")

    # --- Savings account operations ---
    savings.deposit(1000.0)
    assert savings.balance == 6000.0
    savings.withdraw(500.0)
    assert savings.balance == 5500.0
    print("Savings deposit/withdraw OK")

    # --- Current account operations (overdraft allowed) ---
    current.deposit(500.0)
    assert current.balance == 2500.0
    current.withdraw(3000.0)          # 2500 + 10000 overdraft = 12500 available
    assert current.balance == -500.0
    print("Current deposit/withdraw with overdraft OK")

    # --- Salary account operations ---
    salary.deposit(2000.0)
    assert salary.balance == 3000.0
    salary.withdraw(1000.0)
    assert salary.balance == 2000.0
    print("Salary deposit/withdraw OK")

    # --- Fixed deposit operations ---
    fixed_deposit.deposit(5000.0)
    assert fixed_deposit.balance == 15000.0
    interest = fixed_deposit.calculate_interest()
    # interest = 15000 * 6.5 * (12/12) / 100 = 975.0
    assert abs(interest - 975.0) < 0.001, "Fixed deposit interest calculation mismatch"
    print("FixedDeposit deposit and interest OK")

    # ------------------------------------------------------------------
    # Extra checks: abstractness and invalid factory input
    # ------------------------------------------------------------------
    try:
        IAccount()
        assert False, "IAccount should be abstract and cannot be instantiated"
    except TypeError:
        print("IAccount is abstract – cannot instantiate directly.")

    try:
        AccountFactory.create_account("UNKNOWN", "X", "Y", 20, 0.0)
        assert False, "Expected AccountException for unknown account type"
    except AccountException as e:
        print(f"Unknown account type correctly raised: {e}")

    print("=== All Activity 12 tests passed! ===")


if __name__ == "__main__":
    main()