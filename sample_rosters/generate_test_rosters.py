"""
Generate test CSV rosters with various configurations for testing.
Run this script to create sample CSV files.
"""

import csv
from seating_algorithm import generate_random_roster

def save_roster(singers, filename):
    """Save a roster to a CSV file."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'voice_part', 'height'])
        writer.writeheader()
        for s in singers:
            writer.writerow({'name': s.name, 'voice_part': s.voice_part, 'height': s.height})
    print(f"Created {filename} with {len(singers)} singers")


if __name__ == '__main__':
    # Test 1: Unequal SATB (typical real-world scenario)
    # More sopranos and altos than tenors and basses
    singers = generate_random_roster(
        num_singers=50,
        parts=['Soprano', 'Alto', 'Tenor', 'Bass'],
        distribution=[15, 18, 8, 9]  # 50 total, heavy on upper voices
    )
    save_roster(singers, 'test_unequal_50.csv')

    # Test 2: Very unequal small choir
    singers = generate_random_roster(
        num_singers=25,
        parts=['Soprano', 'Alto', 'Tenor', 'Bass'],
        distribution=[10, 8, 4, 3]  # Very unbalanced
    )
    save_roster(singers, 'test_unequal_25.csv')

    # Test 3: Large choir with split parts
    singers = generate_random_roster(
        num_singers=120,
        parts=['Soprano 1', 'Soprano 2', 'Alto 1', 'Alto 2', 'Tenor', 'Bass'],
        distribution=[25, 22, 28, 20, 12, 13]
    )
    save_roster(singers, 'test_split_parts_120.csv')

    # Test 4: Prime number of singers (awkward for layouts)
    singers = generate_random_roster(
        num_singers=47,
        parts=['Soprano', 'Alto', 'Tenor', 'Bass'],
        distribution=[14, 16, 9, 8]
    )
    save_roster(singers, 'test_prime_47.csv')

    # Test 5: Small ensemble with just 3 parts
    singers = generate_random_roster(
        num_singers=18,
        parts=['High', 'Middle', 'Low'],
        distribution=[7, 6, 5]
    )
    save_roster(singers, 'test_3parts_18.csv')

    # Test 6: Large 200+ choir
    singers = generate_random_roster(
        num_singers=210,
        parts=['Soprano 1', 'Soprano 2', 'Alto 1', 'Alto 2', 'Tenor 1', 'Tenor 2', 'Bass 1', 'Bass 2'],
        distribution=[30, 28, 32, 26, 22, 20, 28, 24]
    )
    save_roster(singers, 'test_large_210.csv')

    # Test 7: "Men's Chorus"
    singers = generate_random_roster(
        num_singers=201,
        parts=['Tenor 1', 'Tenor 2', 'Baritone', 'Bass'],
        distribution=[35, 45, 55, 66]
    )
    save_roster(singers, 'test_mens_chorus.csv')

    print("\nAll test rosters generated!")