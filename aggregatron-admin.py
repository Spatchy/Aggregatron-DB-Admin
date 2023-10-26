import psycopg2
import base64
import os
from PIL import Image
import requests
from io import BytesIO


# Database connection details
db_connection = {
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": "127.0.0.1",
    "port": "5432"
}

# Function to list services
def list_services():
    try:
        conn = psycopg2.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("SELECT service FROM Services")
        services = cursor.fetchall()

        print("List of Services:")
        for service in services:
            print(service[0])

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to add a new service
def add_service():
    try:
        new_service = input("Enter the new service name: ")

        conn = psycopg2.connect(**db_connection)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Services (service) VALUES (%s)", (new_service,))
        conn.commit()

        print(f"Service '{new_service}' added successfully!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Function to insert a new activity
def insert_activity():
    try:
        conn = psycopg2.connect(**db_connection)
        cursor = conn.cursor()

        service = input("Service: ")
        published_date = input("Published Date (YYYY-MM-DD HH:MM:SS): ")
        title = input("Title: ")
        url = input("URL: ")
        # Ask the user for the URL of the remote image
        image_url = input("Enter the URL of the thumbnail image: ")

        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code == 200:
            # Encode the image as base64
            thumbnail_base64 = base64.b64encode(response.content).decode("utf-8")

            # Get image dimensions
            with Image.open(BytesIO(response.content)) as img:
                width, height = img.size
                print(f"Downloaded image dimensions: {width}x{height}")

        else:
            print(f"Failed to download the image from {image_url}")
            return

        print("\nReview the data:")
        print(f"Service: {service}")
        print(f"Published Date: {published_date}")
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Thumbnail: {width}x{height}")

        confirmation = input("Confirm (yes/no): ").strip().lower()
        if confirmation == "yes":
            cursor.execute(
                "INSERT INTO Activities (service, published_date, title, url, thumbnail) "
                "VALUES (%s, %s, %s, %s, decode(%s, 'base64'))",
                (service, published_date, title, url, thumbnail_base64.strip()),
            )
            conn.commit()
            print("Data inserted successfully!")
        else:
            print("Data insertion canceled.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Main menu
while True:
    print("\nOptions:")
    print("1. List services")
    print("2. Add new service")
    print("3. Insert new activity")
    print("4. Quit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        list_services()
    elif choice == "2":
        add_service()
    elif choice == "3":
        insert_activity()
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
