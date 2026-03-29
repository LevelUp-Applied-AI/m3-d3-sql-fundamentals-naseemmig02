import sqlite3


def top_departments(db_path):
    """
    Task 1 — Aggregation
    Returns the top 3 departments by total salary expenditure.
    Result: [(dept_name, total_salary), ...] sorted descending by total salary.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT d.name, SUM(e.salary) AS total_salary
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        GROUP BY d.dept_id, d.name
        ORDER BY total_salary DESC
        LIMIT 3
    """)

    results = cursor.fetchall()
    conn.close()
    return results


def employees_with_projects(db_path):
    """
    Task 2 — JOIN
    Returns all (employee_name, project_name) pairs for employees
    assigned to at least one project.
    Result: [(employee_name, project_name), ...]
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.name, p.name
        FROM employees e
        INNER JOIN project_assignments pa ON e.emp_id = pa.emp_id
        INNER JOIN projects p ON pa.project_id = p.project_id
    """)

    results = cursor.fetchall()
    conn.close()
    return results


def salary_rank_by_department(db_path):
    """
    Task 3 — Window Function
    Returns each employee's salary rank within their department.
    Rank is computed with RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC).
    Result: [(employee_name, dept_name, salary, rank), ...]
    ordered by department name then rank.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            e.name,
            d.name,
            e.salary,
            RANK() OVER (PARTITION BY e.dept_id ORDER BY e.salary DESC) AS salary_rank
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        ORDER BY d.name, salary_rank
    """)

    results = cursor.fetchall()
    conn.close()
    return results