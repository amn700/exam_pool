#!/usr/bin/env python3
import re
import os

def parse_exercises(file_path):
    """Parse the exam_subjects file and extract unique exercises."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dictionary to store unique exercises
    exercises = {}
    
    # More comprehensive pattern to catch all variations:
    # - "// Assignment name  : name"
    # - "Assignment name  : name" 
    # - "    Assignment name  : name" (indented)
    # - "$Assignment name  : name" (with $ prefix)
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
        
        # Clean up any leading characters that might be artifacts
        lines = exercise_content.split('\n')
        if lines and lines[0].startswith('$'):
            lines[0] = lines[0][1:]  # Remove leading $
        exercise_content = '\n'.join(lines).strip()
        
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

def verify_parsing(input_file):
    """Verify that we captured all assignments by doing a comprehensive check."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count all assignment patterns
    all_patterns = [
        r'//\s*Assignment name\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)',  # Commented
        r'^\s*Assignment name\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)',   # Normal
        r'^\s+Assignment name\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)',   # Indented
        r'^\$Assignment name\s*:\s*([a-zA-Z_][a-zA-Z0-9_]*)',    # $ prefix
    ]
    
    all_assignments = []
    for pattern in all_patterns:
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            assignment_name = match.group(1).strip()
            all_assignments.append((assignment_name, match.start()))
    
    # Sort by position in file
    all_assignments.sort(key=lambda x: x[1])
    
    print(f"\nVerification: Found {len(all_assignments)} total assignments")
    assignment_names = [name for name, pos in all_assignments]
    unique_names = list(dict.fromkeys(assignment_names))  # Preserve order, remove duplicates
    
    print(f"Unique assignments: {len(unique_names)}")
    return unique_names

def main():
    input_file = "/workspaces/exam_pool/exam_subjects"
    
    print("Verifying all assignments in the file...")
    all_unique = verify_parsing(input_file)
    
    print("\nParsing exercises from exam_subjects file...")
    exercises = parse_exercises(input_file)
    
    print(f"\nFound {len(exercises)} unique exercises:")
    for name in sorted(exercises.keys()):
        print(f"  - {name}")
    
    # Check if we missed any
    parsed_names = set(exercises.keys())
    expected_names = set(all_unique)
    
    if parsed_names == expected_names:
        print(f"\n✅ SUCCESS: All {len(expected_names)} unique exercises were captured!")
    else:
        missed = expected_names - parsed_names
        extra = parsed_names - expected_names
        if missed:
            print(f"\n❌ MISSED {len(missed)} exercises: {sorted(missed)}")
        if extra:
            print(f"\n❓ EXTRA {len(extra)} exercises: {sorted(extra)}")
    
    print(f"\nCreating individual files...")
    created_files = create_exercise_files(exercises)
    
    print(f"\nSuccessfully created {len(created_files)} exercise files in the 'exercises' directory!")

if __name__ == "__main__":
    main()
