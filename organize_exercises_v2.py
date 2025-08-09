#!/usr/bin/env python3
import re
import os

def parse_exercises(file_path):
    """Parse the exam_subjects file and extract unique exercises."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dictionary to store unique exercises
    exercises = {}
    
    # Improved pattern to handle all variations:
    # - // Assignment name  : name
    # - Assignment name  : name 
    # - $Assignment name  : name
    # -    Assignment name  : name (indented)
    assignment_pattern = r'(?:^|\n)\s*(?://\s*)?(?:\$\s*)?(?:\s*)Assignment name\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)'
    
    # Find all assignment names and their positions
    matches = list(re.finditer(assignment_pattern, content, re.MULTILINE))
    
    for i, match in enumerate(matches):
        assignment_name = match.group(1).strip()
        start_pos = match.start()
        
        # Determine the end position (start of next assignment or end of file)
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        
        # Extract the exercise content
        exercise_content = content[start_pos:end_pos].strip()
        
        # Clean up the content - remove leading newlines and whitespace
        exercise_content = exercise_content.lstrip('\n\r\t ')
        
        # Only keep the first occurrence of each exercise (avoid duplicates)
        if assignment_name not in exercises:
            exercises[assignment_name] = exercise_content
            print(f"Found exercise: {assignment_name}")
        else:
            print(f"Skipping duplicate: {assignment_name}")
    
    return exercises

def create_exercise_files(exercises, output_dir="exercises"):
    """Create individual files for each exercise."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    created_files = []
    
    for name, content in exercises.items():
        file_path = os.path.join(output_dir, f"{name}.txt")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created_files.append(file_path)
        print(f"Created: {file_path}")
    
    return created_files

def main():
    input_file = "/workspaces/exam_pool/exam_subjects"
    
    print("Parsing exercises from exam_subjects file...")
    exercises = parse_exercises(input_file)
    
    print(f"\nFound {len(exercises)} unique exercises:")
    for name in sorted(exercises.keys()):
        print(f"  - {name}")
    
    print(f"\nCreating individual files...")
    created_files = create_exercise_files(exercises)
    
    print(f"\nSuccessfully created {len(created_files)} exercise files in the 'exercises' directory!")

if __name__ == "__main__":
    main()
