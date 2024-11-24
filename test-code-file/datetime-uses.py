from datetime import datetime

# Examples of datetime usage:
# Get current date and time
now = datetime.now()
print(f"Current time: {now}")

# Format date as string
formatted_date = now.strftime('%Y-%m-%d')
print(f"Formatted date: {formatted_date}")

# Parse string to date
date_string = "2024-03-20"
parsed_date = datetime.strptime(date_string, '%Y-%m-%d')
print(f"Parsed date: {parsed_date}")