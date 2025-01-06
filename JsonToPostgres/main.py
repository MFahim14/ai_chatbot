import json
from datetime import datetime
from database.db_operations import Database

# Helper function to parse and format date
def format_date(date_str):
    try:
        return datetime.strptime(date_str, '%b %d, %I:%M %p').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(f"Error parsing date: {date_str}. Error: {e}")
        return None

def main():
    # Load JSON data from files
    with open('rental_data.json', 'r') as rental_file:
        rental_data = json.load(rental_file)
    
    with open('comments_data.json', 'r') as comments_file:
        comments_data = json.load(comments_file)

    db = Database()
    db.connect()
    db.create_tables()

    # Insert rental data
    for rental in rental_data:
        db.insert_rental(rental)

    # Insert comments data
    for rental_id, comments in comments_data.items():
        for comment in comments:
            comment["rental_id"] = rental_id
            # Convert comment date to valid timestamp
            comment["commentDate"] = format_date(comment["commentDate"])
            if comment["commentDate"]:  # Only insert if the date was successfully parsed
                db.insert_comment(comment)
            else:
                print(f"Skipping comment with invalid date: {comment}")

    db.close()
    print("All data from both files inserted successfully!")

if __name__ == '__main__':
    main()
