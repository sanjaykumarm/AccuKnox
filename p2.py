import requests
import matplotlib.pyplot as plt

# REST API endpoint URL
API_URL = "https://raw.githubusercontent.com/sanjaykumarm/AccuKnox/refs/heads/main/students-test-score.json"

def fetch_student_data(url):
    """Fetches data from the  API and handles network errors gracefully."""
    print("Fetching student test score from API ...")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors (404, 500, etc.)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred while fetching data: {e}")
        return None
    except ValueError:
        print("Error: The response payload was not valid JSON data.")
        return None

def process_and_visualize(students):
    if not students:
        print("No student data available to process.")
        return

    student_count = len(students)
    
    print(f"Processing {student_count} students ...")

    # Extract names and scores dynamically while scrubbing trailing/leading spaces
    names = [student.get("name", f"Unknown ID:{student.get('id')}").strip() for student in students]
    scores = [student.get("score", 0) for student in students]

    # Calculate the average test/exam score
    total_score = sum(scores)
    average_score = total_score / student_count if student_count > 0 else 0
    
    print("\n" + "="*45)
    print(f"Total Students Processed: {student_count}")
    print(f"Overall Class Average Score: {average_score:.2f}")
    print("="*45 + "\n")

    # Create the Bar Chart Visualization (Width * Height), so it looks rectangle and nice to see graph.
    plt.figure(figsize=(10, 6))
    
    # Generate the bars with a verticle graph line
    bars = plt.bar(names, scores, color='#3498db', edgecolor='#2980b9', width=0.6)
    
    # Draw a distinct horizontal dashed line marking the calculated average score
    plt.axhline(y=average_score, color='#e74c3c', linestyle='--', linewidth=1.5, 
                label=f'Class Average ({average_score:.2f})')
    
    # Add text labels on top of each bar for high precision scanning
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height + 1, f'{height}', 
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Visual refinement (Titles, labels, and boundary layout adjustments)
    plt.title("Students' Test Scores Breakdown", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Student Name", fontsize=12, labelpad=10)
    plt.ylabel("Test Score", fontsize=12, labelpad=10)
    
    plt.ylim(0, 110)      # Pad upper boundary so labels aren't clipped off
    plt.xticks(rotation=45, ha='right')  # Rotate names neatly to avoid overlapping
    plt.grid(axis='y', linestyle=':', alpha=0.6) # Subtle y-axis grids only
    plt.legend(loc='upper right')
    
    plt.tight_layout()    # Prevent axis labels from getting clipped out
    
    # Display the final plot window to the user
    print("Displaying chart ...")
    plt.show()

if __name__ == "__main__":
    # Fetch the data from the API
    student_records = fetch_student_data(API_URL)
    
    # Pass the fetched value to show in a graph/bar chart.
    process_and_visualize(student_records)