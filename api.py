import asyncpg
import asyncio

async def edit_user_data(email, name=None, phone=None, address=None):

    # Prepare the SQL statement dynamically based on the fields provided
    set_clauses = []
    params = []

    if name:
        set_clauses.append(f"name = ${len(params) + 1}")
        params.append(name)
    if phone:
        set_clauses.append(f"phone = ${len(params) + 1}")
        params.append(phone)
    if address:
        set_clauses.append(f"address = ${len(params) + 1}")
        params.append(address)

    if not set_clauses:
        raise ValueError("At least one field to update must be provided")

    params.append(email)
    
    set_clause_str = ", ".join(set_clauses)
    sql = f"UPDATE users SET {set_clause_str} WHERE email = ${len(params)}"

    pool = await asyncpg.create_pool(
                user='postgres', password='', database='career', host='localhost'
            )
    async with pool.acquire() as connection:
        result = await connection.execute(sql, *params)
        # Check the number of rows affected
        if result == "UPDATE 0":
            raise Exception("User not found.")

# Example usage
async def trying():
    try:
        await edit_user_data(email="tuhin.paul.518@gmail.com", name="me", phone="1234", address="Delhi")
    
    except Exception as e:
        print(e)

asyncio.run(trying())
