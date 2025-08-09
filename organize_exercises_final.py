#!/usr/bin/env python3
import re
import os

def clean_content_start(content):
    """Clean up content that might have artifacts from previous exercise."""
    lines = content.split('\n')
    
    # Find the first line that starts with Assignment name
    assignment_line_idx = -1
    for i, line in enumerate(lines):
        if re.search(r'Assignment name\s*:', line):
            assignment_line_idx = i
            break
    
    if assignment_line_idx >= 0:
        # Keep only from the assignment line onwards
        lines = lines[assignment_line_idx:]
        
        # Clean the first line if it has $ prefix
        if lines[0].startswith('$'):
            lines[0] = lines[0][1:]
        
        return '\n'.join(lines).strip()
    
    return content

def parse_exercises(file_path):
    """Parse the exam_subjects file and extract unique exercises."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dictionary to store unique exercises
    exercises = {}
    
    # More comprehensive pattern to catch all variations:
    assignment_pattern = r'(?://\s*)?(?:\$)?(?:\s*)Assignment name\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)'
    
    # Find all assignment names and their positions
    matches = list(re.finditer(assignment_pattern, content))
    
    print(f"Found {len(matches)} total assignment occurrences")
    
    for i, match in enumerate(matches):
        assignment_name = match.group(1).strip()
        start_pos = match.start()
        
        # Go back to start of line to capture the full assignment
        line_start = content.rfind('\n', 0, start_pos) + 1
        start_pos = line_start
        
        # Determine the end position (start of next assignment or end of file)
        if i + 1 < len(matches):
            next_match = matches[i + 1]
            next_line_start = content.rfind('\n', 0, next_match.start()) + 1
            end_pos = next_line_start
        else:
            end_pos = len(content)
        
        # Extract the exercise content
        exercise_content = content[start_pos:end_pos].strip()
        
        # Clean up the content
        exercise_content = clean_content_start(exercise_content)
        
        # Only keep the first occurrence of each exercise (avoid duplicates)
        if assignment_name not in exercises:
            exercises[assignment_name] = exercise_content
            print(f"Found exercise: {assignment_name}")
        else:
            print(f"Skipping duplicate: {assignment_name}")
    
    return exercises

def create_exercise_files(exercises, output_dir="exercises_clean"):
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
    
    print(f"\nCreating clean individual files...")
    created_files = create_exercise_files(exercises)
    
    print(f"\nSuccessfully created {len(created_files)} clean exercise files!")

if __name__ == "__main__":
    main()
