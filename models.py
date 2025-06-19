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
    
def create_rental(user_id, car_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO SessionRental (userId, carId) VALUES (%s, %s)", (user_id, car_id))
        cursor.execute("UPDATE Car SET status='inUse' WHERE carId=%s", (car_id,))
        conn.commit()

def get_active_rental(user_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT sr.sessionId, sr.carId, c.model FROM SessionRental sr
            JOIN Car c ON c.carId = sr.carId
            WHERE sr.userId = %s AND sr.endTime IS NULL
        """, (user_id,))
        return cursor.fetchone()
    
def cancel_rental(session_id, car_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        # начало аренды
        cursor.execute("SELECT startTime FROM SessionRental WHERE sessionId=%s", (session_id,))
        session = cursor.fetchone()

        if not session:
            return

        # цену за минуту
        cursor.execute("SELECT pricePerMinute FROM Car WHERE carId=%s", (car_id,))
        car = cursor.fetchone()

        if not car:
            return

        # вычисляем продолжительность аренды в минутах
        cursor.execute("""
            SELECT TIMESTAMPDIFF(MINUTE, startTime, NOW()) AS duration 
            FROM SessionRental WHERE sessionId=%s
        """, (session_id,))
        duration = cursor.fetchone()['duration']

        price_per_minute = car['pricePerMinute']
        cost = round(duration * price_per_minute, 2)

        # примерное расст 0.5 км/мин
        distance = round(duration * 0.5, 2)

        cursor.execute("""
            INSERT INTO Trip (endTime, distance, cost) 
            VALUES (NOW(), %s, %s)
        """, (distance, cost))
        trip_id = cursor.lastrowid

        # обновляем сессию 
        cursor.execute("""
            UPDATE SessionRental 
            SET endTime=NOW(), tripId=%s 
            WHERE sessionId=%s
        """, (trip_id, session_id))

        # освобождаем машинку
        cursor.execute("""
            UPDATE Car SET status='available' 
            WHERE carId=%s
        """, (car_id,))

        conn.commit()
