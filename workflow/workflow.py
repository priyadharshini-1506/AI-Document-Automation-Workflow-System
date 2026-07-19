def recommend_workflow(
    priority,
    department
):
 
    if not priority:
        return """
        Low Priority Workflow:
 
        1. Archive document
        2. Store for future reference
        """
 
    priority = priority.lower()
 
    if priority == "high":
 
        return f"""
        Immediate Action Required:
 
        1. Notify {department} department
        2. Assign responsible employee
        3. Complete document review
        4. Send confirmation
        """
 
    elif priority == "medium":
 
        return f"""
        Standard Workflow:
 
        1. Send to {department}
        2. Review document
        3. Update status
        """
 
    else:
 
        return """
        Low Priority Workflow:
 
        1. Archive document
        2. Store for future reference
        """