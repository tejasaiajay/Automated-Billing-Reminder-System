def check_customer_due(customer_row, target_date):
    due_date = customer_row["Due Date"]

    if due_date == target_date:
        return True

    return False