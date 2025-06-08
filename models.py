from db.db import get_connection
import hashlib

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login_user(phone, password):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE phone=%s AND password=%s", (phone, hash_password(password)))
        return cursor.fetchone()

def get_all_cars():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Car")
        return cursor.fetchall()

def get_available_cars():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Car WHERE status='available'")
        return cursor.fetchall()

def update_car_status(car_id, status):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE Car SET status=%s WHERE carId=%s", (status, car_id))
        conn.commit()

def add_car(model, price, location_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO Car (model, status, pricePerMinute, locationId) VALUES (%s, 'available', %s, %s)",
                       (model, price, location_id))
        conn.commit()

def delete_car(car_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Car WHERE carId=%s", (car_id,))
        conn.commit()

def get_rental_history(user_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT 
                s.sessionId,
                t.tripid,
                t.startTime,
                t.endTime,
                t.distance,
                t.cost,
                c.model,
                CASE 
                    WHEN t.endTime IS NULL THEN 'Активна'
                    ELSE 'Завершена'
                END as status
            FROM sessionrental s
            JOIN trip t ON s.tripId = t.tripId  
            JOIN car c ON s.carId = c.carId       
            WHERE s.userId = %s
            ORDER BY t.startTime DESC
        """, (user_id,))
        return cursor.fetchall()
    