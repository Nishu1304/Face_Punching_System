from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection details
username = 'root'
password = 'password'
host = 'localhost'
database = 'attendance'

# Create database engine
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

# Fetch attendance data with a join to get employee names
query = """
SELECT e.name, en.hours_worked, en.late_arrival
FROM entries en
JOIN employees e ON en.employee_id = e.employee_id;
"""
new = """
SELECT * from status;
"""
df_new = pd.read_sql(new, engine)
df = pd.read_sql(query, engine)
print(df)
print(df_new)
# Average hours worked per employee
avg_hours = df.groupby('name')['hours_worked'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='name', y='hours_worked', data=avg_hours, palette='viridis')
plt.title('Average Hours Worked per Employee')
plt.xlabel('Employee Name')
plt.ylabel('Average Hours Worked')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout for better fit
plt.show()

# Plot late arrivals
late_arrivals = df[df['late_arrival'] == True].groupby('name')['late_arrival'].count().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='name', y='late_arrival', data=late_arrivals, palette='rocket')
plt.title('Late Arrivals per Employee')
plt.xlabel('Employee Name')
plt.ylabel('Count of Late Arrivals')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout for better fit
plt.show()

# Calculate overtime hours
# Assuming overtime is defined as any hours worked beyond 8 hours in a day
df['overtime_hours'] = df['hours_worked'].apply(lambda x: x - 8 if x > 8 else 0)

# Plot total overtime hours per employee
overtime_summary = df.groupby('name')['overtime_hours'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='name', y='overtime_hours', data=overtime_summary, palette='mako')
plt.title('Total Overtime Hours per Employee')
plt.xlabel('Employee Name')
plt.ylabel('Total Overtime Hours')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout for better fit
plt.show()

