"""
Add election information columns to FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv
"""

import pandas as pd
import sqlite3

def add_election_columns():
    """Add election columns to CSV and database"""

    print("Loading Florida federal officials data...")
    df = pd.read_csv('data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv')

    print(f"Found {len(df)} officials")

    # Add new columns with default values
    df['End_Current_Term'] = ''
    df['Next_Primary_Election'] = ''
    df['Next_General_Election'] = ''

    # Election dates for 2026
    PRIMARY_2026 = "August 18, 2026"
    GENERAL_2026 = "November 3, 2026"

    print("\nUpdating election information...")
    print("="*80)

    # Update for each representative
    for idx, row in df.iterrows():
        office = row['Office']
        name = f"{row['First_Name']} {row['Last_Name']}"

        if office == 'U.S. Senate':
            # Senators
            if row['Last_Name'] == 'Scott':
                # Rick Scott - re-elected 2024, term ends 2031
                df.at[idx, 'End_Current_Term'] = "January 3, 2031"
                df.at[idx, 'Next_Primary_Election'] = "August 2030"
                df.at[idx, 'Next_General_Election'] = "November 2030"
                print(f"[Senate] {name}: Term ends 2031, next election 2030")

            elif row['Last_Name'] == 'Rubio':
                # Marco Rubio seat - Special election 2026 (Rubio became Secretary of State)
                df.at[idx, 'End_Current_Term'] = "January 3, 2027 (Special Election)"
                df.at[idx, 'Next_Primary_Election'] = PRIMARY_2026
                df.at[idx, 'Next_General_Election'] = GENERAL_2026
                print(f"[Senate] {name}: SPECIAL ELECTION 2026 (seat vacant - Rubio to Secretary of State)")

        elif office == 'U.S. House':
            # All House members elected in 2024, terms end January 2027
            # All up for re-election in 2026
            df.at[idx, 'End_Current_Term'] = "January 3, 2027"
            df.at[idx, 'Next_Primary_Election'] = PRIMARY_2026
            df.at[idx, 'Next_General_Election'] = GENERAL_2026
            print(f"[House] {name} ({row['District']}): Term ends 2027, election 2026")

    # Save updated CSV
    print("\n" + "="*80)
    print("Saving updated CSV...")
    df.to_csv('data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv', index=False)
    print("[OK] CSV updated: data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv")

    # Update SQLite database schema and data
    print("\nUpdating SQLite database...")
    conn = sqlite3.connect('data/congress.db')
    cursor = conn.cursor()

    # Add new columns to database
    try:
        cursor.execute("ALTER TABLE representatives ADD COLUMN end_current_term TEXT")
        print("[OK] Added column: end_current_term")
    except sqlite3.OperationalError:
        print("[INFO] Column end_current_term already exists")

    try:
        cursor.execute("ALTER TABLE representatives ADD COLUMN next_primary_election TEXT")
        print("[OK] Added column: next_primary_election")
    except sqlite3.OperationalError:
        print("[INFO] Column next_primary_election already exists")

    try:
        cursor.execute("ALTER TABLE representatives ADD COLUMN next_general_election TEXT")
        print("[OK] Added column: next_general_election")
    except sqlite3.OperationalError:
        print("[INFO] Column next_general_election already exists")

    # Update data in database
    db_updates = 0
    for _, row in df.iterrows():
        cursor.execute("""
            UPDATE representatives
            SET end_current_term = ?,
                next_primary_election = ?,
                next_general_election = ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE last_name = ? AND first_name = ?
        """, (
            row['End_Current_Term'],
            row['Next_Primary_Election'],
            row['Next_General_Election'],
            row['Last_Name'],
            row['First_Name']
        ))
        if cursor.rowcount > 0:
            db_updates += 1

    conn.commit()
    conn.close()

    print(f"[OK] Database updated: {db_updates} representatives")

    # Summary
    print("\n" + "="*80)
    print("ELECTION INFORMATION SUMMARY")
    print("="*80)

    # Count upcoming elections
    election_2026 = df[df['Next_General_Election'] == GENERAL_2026]

    print(f"\nTotal Florida Federal Officials: {len(df)}")
    print(f"  - Senators: {len(df[df['Office'] == 'U.S. Senate'])}")
    print(f"  - House Representatives: {len(df[df['Office'] == 'U.S. House'])}")

    print(f"\nUp for Election in 2026: {len(election_2026)}")
    print(f"  - Senate Special Election: 1 (Marco Rubio's seat)")
    print(f"  - House Seats: 28 (all House seats)")

    print(f"\n2026 Election Dates:")
    print(f"  - Primary: {PRIMARY_2026}")
    print(f"  - General Election: {GENERAL_2026}")

    # Show who's up in 2026
    print("\n" + "-"*80)
    print("OFFICIALS UP FOR ELECTION IN 2026:")
    print("-"*80)

    # Senate special election
    senate_2026 = election_2026[election_2026['Office'] == 'U.S. Senate']
    if len(senate_2026) > 0:
        print("\n[SENATE SPECIAL ELECTION 2026]")
        for _, row in senate_2026.iterrows():
            print(f"  Marco Rubio's seat (currently vacant - became Secretary of State)")

    # House elections
    print("\n[ALL HOUSE SEATS UP FOR RE-ELECTION 2026]")
    house_2026 = election_2026[election_2026['Office'] == 'U.S. House']
    for _, row in house_2026.iterrows():
        print(f"  {row['First_Name']} {row['Last_Name']} ({row['District']}) - {row['Party']}")

    # Rick Scott not up until 2030
    print("\n[NOT UP FOR ELECTION UNTIL 2030]")
    not_2026 = df[df['Next_General_Election'] != GENERAL_2026]
    for _, row in not_2026.iterrows():
        print(f"  Rick Scott (U.S. Senate) - Term ends 2031, next election 2030")

    print("\n" + "="*80)
    print("[OK] ELECTION COLUMNS ADDED SUCCESSFULLY!")
    print("="*80)

    print("\nNew columns added:")
    print("  1. End_Current_Term - When current term ends")
    print("  2. Next_Primary_Election - Next primary election date")
    print("  3. Next_General_Election - Next general election date")

    print("\nNext steps:")
    print("1. Review the updated CSV file")
    print("2. Update app.py to display election information")
    print("3. Test the app locally")
    print("4. Push changes to GitHub")

    return True

if __name__ == "__main__":
    try:
        success = add_election_columns()
        if success:
            print("\n[SUCCESS] Election data updated!")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
