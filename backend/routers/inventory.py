from fastapi import APIRouter, Request, HTTPException
import backend.config.config as config
import pymysql

router = APIRouter()

def get_db_connection():
    return pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

@router.get("/inventory/{user_id}")
async def get_inventory(user_id: str, request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT item, count FROM user_inventory WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            items = cursor.fetchall()
    finally:
        connection.close()

    return {"items": items}

@router.post("/giveitem")
async def give_item(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    user_id = data['user_id']
    item_code = data['item_code']
    count = data['count']

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO user_inventory (user_id, item, count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE count = count + %s"
            cursor.execute(sql, (user_id, item_code, count, count))
        connection.commit()
    finally:
        connection.close()

    return {"status": "item added"}

@router.post("/removeitem")
async def remove_item(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {config.BACKEND_API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    data = await request.json()
    user_id = data['user_id']
    item_code = data['item_code']
    count = data['count']

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE user_inventory SET count = count - %s WHERE user_id = %s AND item = %s"
            cursor.execute(sql, (count, user_id, item_code))
        connection.commit()
    finally:
        connection.close()

    return {"status": "item removed"}
