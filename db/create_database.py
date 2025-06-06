import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = pymysql.connect(host=os.getenv("DB_HOST"),
                                user=os.getenv("DB_USER"),
                                password=os.getenv("DB_PASS"),
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)


    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS db")
            cursor.execute("USE db")
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS Location(
                                            locationId INT AUTO_INCREMENT PRIMARY KEY,
                                            locationName VARCHAR(50) NOT NULL UNIQUE
                           );
                           """)
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS Trip(
                                            tripId int AUTO_INCREMENT PRIMARY KEY,
                                            startTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                                            endTime TIMESTAMP NULL,
                                            distance DECIMAL(10, 2) DEFAULT 0.00,
                                            cost DECIMAL(10, 2) DEFAULT 0.00

                           );   
                           """)
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS Payment(
                                            paymentId INT AUTO_INCREMENT PRIMARY KEY,
                                            amount DECIMAL(10, 2),
                                            method VARCHAR(25) NOT NULL,
                                            date TIMESTAMP NOT NULL
                           );
                           """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Users(
                                            userId int AUTO_INCREMENT PRIMARY KEY,
                                            name VARCHAR(25) NOT NULL,
                                            surname VARCHAR(25) NOT NULL,
                                            patronymic VARCHAR(25),
                                            licenseDriver VARCHAR(10) NOT NULL,
                                            balance DECIMAL(10, 2) DEFAULT 0.00,
                                            password VARCHAR(255) NOT NULL,  
                                            phone VARCHAR(20) UNIQUE,
                                            isAdmin BOOLEAN DEFAULT 0,
                                            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                           """)
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Car(
                                            carId int AUTO_INCREMENT PRIMARY KEY,
                                            model VARCHAR(50) NOT NULL,
                                            status ENUM('available', 'inUse', 'maintenance') NOT NULL,
                                            pricePerMinute DECIMAL(10, 2),
                                            locationId INT NOT NULL,
                                            FOREIGN KEY (locationId) REFERENCES Location(locationId)
                            );
                            """)
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS SessionRental(
                                            sessionId int AUTO_INCREMENT PRIMARY KEY,
                                            startTime TIMESTAMP NOT NULL,
                                            endTime TIMESTAMP NULL,
                                            totalCost DECIMAL(10, 2) DEFAULT 0.00,
                                            userId INT NOT NULL, 
                                            carId INT NOT NULL,   
                                            tripId INT NOT NULL,
                                            paymentId INT NOT NULL,
                                            FOREIGN KEY (userId) REFERENCES Users(userId),
                                            FOREIGN KEY (carId) REFERENCES Car(carId),
                                            FOREIGN KEY (tripId) REFERENCES Trip(tripId),
                                            FOREIGN KEY (paymentId) REFERENCES Payment(paymentId)
                           );
                           """)
            conn.commit()
            print("Создана")    
    finally:
        conn.close()
    
except Exception as ex:
    print(f"Анлак {ex}")