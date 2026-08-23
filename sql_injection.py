from fastapi import FastAPI, HTTPException
import sqlite3
import uvicorn

app = FastAPI(title="User Directory API")

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/v1/user/search")
async def search_user(username: str):
    """
    Search for a user by their exact username.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # CRITICAL BUG: SQL Injection Vulnerability
        # String concatenation allows arbitrary SQL execution if 'username' contains malicious payloads
        query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
        
        # Log the query for debugging (Simulating a real backend log)
        print(f"Executing Query: {query}")
        
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found in the directory.")
            
        return dict(user)
        
    except Exception as e:
        # Generic error catching that might mask the SQL syntax errors from injections
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)