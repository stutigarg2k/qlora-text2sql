def build_schema(con, exclude=("companies",)):
    """Return the database schema as one line of text, in the same style
    as the training data: CREATE TABLE a (x TEXT); CREATE TABLE b (y REAL)"""
    names = [
        row[0]
        for row in con.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
    ]
    statements = []
    for name in names:
        if name in exclude:
            continue
        columns = con.execute(f'PRAGMA table_info("{name}")').fetchall()
        column_text = ", ".join(f"{col[1]} {col[2]}" for col in columns)
        statements.append(f"CREATE TABLE {name} ({column_text})")
    return "; ".join(statements)
