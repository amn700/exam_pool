#!/usr/bin/env python3
import os
import shutil

def merge_exercise_folders():
    """Merge exercises from both folders and remove duplicates."""
    
    # Source directories
    exercises_dir = "/workspaces/exam_pool/exercises"
    exercises_subs2_dir = "/workspaces/exam_pool/exercises_subs2"
    
    # Target directory
    merged_dir = "/workspaces/exam_pool/exercises_merged"
    
    # Create the merged directory
    os.makedirs(merged_dir, exist_ok=True)
    
    # Track exercises and their sources
    exercises_tracker = {}
    copied_files = []
    duplicates_found = []
    
    # Process exercises from first directory
    if os.path.exists(exercises_dir):
        print("Processing exercises from 'exercises' directory...")
        for filename in os.listdir(exercises_dir):
            if filename.endswith('.txt'):
                exercise_name = filename[:-4]  # Remove .txt extension
                source_path = os.path.join(exercises_dir, filename)
                target_path = os.path.join(merged_dir, filename)
                
                # Copy file and track it
                shutil.copy2(source_path, target_path)
                exercises_tracker[exercise_name] = 'exercises'
                copied_files.append(filename)
                print(f"  Copied: {filename}")
    
    # Process exercises from second directory
    if os.path.exists(exercises_subs2_dir):
        print("\nProcessing exercises from 'exercises_subs2' directory...")
        for filename in os.listdir(exercises_subs2_dir):
            if filename.endswith('.txt'):
                exercise_name = filename[:-4]  # Remove .txt extension
                source_path = os.path.join(exercises_subs2_dir, filename)
                target_path = os.path.join(merged_dir, filename)
                
                # Check if exercise already exists
                if exercise_name in exercises_tracker:
                    print(f"  DUPLICATE FOUND: {filename} (skipping - already exists from '{exercises_tracker[exercise_name]}' directory)")
                    duplicates_found.append(exercise_name)
                else:
                    # Copy file and track it
                    shutil.copy2(source_path, target_path)
                    exercises_tracker[exercise_name] = 'exercises_subs2'
                    copied_files.append(filename)
                    print(f"  Copied: {filename}")
    
    return exercises_tracker, copied_files, duplicates_found

def compare_duplicate_content(duplicates):
    """Compare the content of duplicate exercises to see if they're identical."""
    exercises_dir = "/workspaces/exam_pool/exercises"
    exercises_subs2_dir = "/workspaces/exam_pool/exercises_subs2"
    
    print("\nComparing duplicate exercise content...")
    
    for exercise_name in duplicates:
        file1 = os.path.join(exercises_dir, f"{exercise_name}.txt")
        file2 = os.path.join(exercises_subs2_dir, f"{exercise_name}.txt")
        
        if os.path.exists(file1) and os.path.exists(file2):
            with open(file1, 'r', encoding='utf-8') as f1:
                content1 = f1.read().strip()
            with open(file2, 'r', encoding='utf-8') as f2:
                content2 = f2.read().strip()
            
            if content1 == content2:
                print(f"  {exercise_name}: IDENTICAL content")
            else:
                print(f"  {exercise_name}: DIFFERENT content - manual review needed")
                
                # Show first few lines of each
                lines1 = content1.split('\n')[:3]
                lines2 = content2.split('\n')[:3]
                print(f"    Source 1 (exercises): {' | '.join(lines1)}")
                print(f"    Source 2 (exercises_subs2): {' | '.join(lines2)}")

def main():
    print("=" * 60)
    print("MERGING EXERCISE FOLDERS AND REMOVING DUPLICATES")
    print("=" * 60)
    
    # Merge folders
    exercises_tracker, copied_files, duplicates_found = merge_exercise_folders()
    
    # Show summary
    print(f"\n" + "=" * 60)
    print("MERGE SUMMARY")
    print("=" * 60)
    print(f"Total unique exercises: {len(exercises_tracker)}")
    print(f"Files copied to merged directory: {len(copied_files)}")
    print(f"Duplicates found and skipped: {len(duplicates_found)}")
    
    if duplicates_found:
        print(f"\nDuplicate exercises (kept from 'exercises' directory):")
        for dup in sorted(duplicates_found):
            print(f"  - {dup}")
        
        # Compare duplicate content
        compare_duplicate_content(duplicates_found)
    
    print(f"\nAll unique exercises are now in: /workspaces/exam_pool/exercises_merged/")
    
    # Show breakdown by source
    from_exercises = sum(1 for source in exercises_tracker.values() if source == 'exercises')
    from_exercises_subs2 = sum(1 for source in exercises_tracker.values() if source == 'exercises_subs2')
    
    print(f"\nSource breakdown:")
    print(f"  From 'exercises' directory: {from_exercises}")
    print(f"  From 'exercises_subs2' directory: {from_exercises_subs2}")
    print(f"  Total unique: {len(exercises_tracker)}")

if __name__ == "__main__":
    main()
