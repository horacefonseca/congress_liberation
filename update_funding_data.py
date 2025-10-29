"""
Update funding data in database and CSV from BOTH_ProIsrael_and_MIC_funded.csv
"""

import pandas as pd
import sqlite3
import sys

def format_amount(amount):
    """Format amount as currency or return 'No'"""
    if pd.isna(amount) or amount == 0:
        return "No"
    return f"${int(amount):,}"

def match_representative(funding_row, our_data):
    """
    Match a row from funding data with our representatives
    Returns: matched row from our_data or None
    """
    cand_name = funding_row['CAND_NAME']
    office = funding_row['CAND_OFFICE']
    district_num = funding_row['CAND_OFFICE_DISTRICT']

    # Parse candidate name (format: "LAST, FIRST MIDDLE" or variations)
    parts = cand_name.split(',')
    if len(parts) < 2:
        return None

    last_name = parts[0].strip()
    first_parts = parts[1].strip().split()
    first_name = first_parts[0] if first_parts else ""

    # Special handling for known variations
    if last_name == "PAULINA LUNA":
        last_name = "LUNA"
        first_name = "ANNA"
    elif "SEN" in cand_name or "MR" in cand_name or "MD" in cand_name:
        # Remove titles
        first_name = first_parts[0] if first_parts else ""

    # Match by office type
    if office == 'S':  # Senate
        # Match senators by last name (only 2 per state)
        matches = our_data[
            (our_data['Office'] == 'U.S. Senate') &
            (our_data['Last_Name'].str.upper() == last_name.upper())
        ]
    else:  # House
        # Convert district number to our format (FL-01, FL-02, etc.)
        district = f"FL-{int(district_num):02d}"

        # Match by district and last name
        matches = our_data[
            (our_data['District'] == district) &
            (our_data['Last_Name'].str.upper() == last_name.upper())
        ]

    if len(matches) == 1:
        return matches.iloc[0]
    elif len(matches) > 1:
        # Multiple matches - try to narrow by first name
        first_matches = matches[
            matches['First_Name'].str.upper().str.startswith(first_name.upper()[:3])
        ]
        if len(first_matches) == 1:
            return first_matches.iloc[0]

    return None

def update_funding_data():
    """Main function to update funding data"""

    print("Loading funding data...")
    funding_df = pd.read_csv('BOTH_ProIsrael_and_MIC_funded.csv')

    # Filter for Florida only
    fl_funding = funding_df[funding_df['CAND_OFFICE_ST'] == 'FL'].copy()
    print(f"Found {len(fl_funding)} Florida representatives with funding data")

    print("\nLoading our representative data...")
    our_df = pd.read_csv('data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv')
    print(f"Found {len(our_df)} representatives in our database")

    # Create update tracking
    updates = []
    matched = 0
    unmatched = []

    print("\nMatching representatives...")
    print("="*80)

    for idx, funding_row in fl_funding.iterrows():
        match = match_representative(funding_row, our_df)

        if match is not None:
            aipac_amount = format_amount(funding_row['total_amount'])
            mic_amount = format_amount(funding_row['mic_total_amount'])

            updates.append({
                'Last_Name': match['Last_Name'],
                'First_Name': match['First_Name'],
                'District': match['District'],
                'AIPAC_Funded': aipac_amount,
                'War_Industrial_Complex_Funded': mic_amount
            })

            print(f"[OK] Matched: {match['First_Name']} {match['Last_Name']} ({match['District']})")
            print(f"  AIPAC: {aipac_amount}, War Industry: {mic_amount}")
            matched += 1
        else:
            unmatched.append(funding_row['CAND_NAME'])
            print(f"[X] No match: {funding_row['CAND_NAME']} ({funding_row['CAND_OFFICE']}-{funding_row['CAND_OFFICE_DISTRICT']})")

    print("\n" + "="*80)
    print(f"\nMatching Summary:")
    print(f"  Matched: {matched}")
    print(f"  Unmatched: {len(unmatched)}")

    if unmatched:
        print(f"\nUnmatched candidates:")
        for name in unmatched:
            print(f"  - {name}")

    if matched == 0:
        print("\nNo matches found. Exiting without changes.")
        return False

    # Apply updates to DataFrame
    print("\nApplying updates to CSV data...")
    for update in updates:
        mask = (
            (our_df['Last_Name'] == update['Last_Name']) &
            (our_df['First_Name'] == update['First_Name']) &
            (our_df['District'] == update['District'])
        )
        our_df.loc[mask, 'AIPAC_Funded'] = update['AIPAC_Funded']
        our_df.loc[mask, 'War_Industrial_Complex_Funded'] = update['War_Industrial_Complex_Funded']

    # Save updated CSV
    print("Saving updated CSV...")
    our_df.to_csv('data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv', index=False)
    print("[OK] CSV updated: data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv")

    # Update SQLite database
    print("\nUpdating SQLite database...")
    conn = sqlite3.connect('data/congress.db')
    cursor = conn.cursor()

    db_updates = 0
    for update in updates:
        # Determine if Senate or House
        if update['District'] == 'Statewide':
            cursor.execute("""
                UPDATE representatives
                SET aipac_funded = ?,
                    war_industrial_complex_funded = ?,
                    last_updated = CURRENT_TIMESTAMP
                WHERE last_name = ? AND first_name = ? AND office = 'U.S. Senate'
            """, (
                update['AIPAC_Funded'],
                update['War_Industrial_Complex_Funded'],
                update['Last_Name'],
                update['First_Name']
            ))
        else:
            cursor.execute("""
                UPDATE representatives
                SET aipac_funded = ?,
                    war_industrial_complex_funded = ?,
                    last_updated = CURRENT_TIMESTAMP
                WHERE last_name = ? AND first_name = ? AND district = ?
            """, (
                update['AIPAC_Funded'],
                update['War_Industrial_Complex_Funded'],
                update['Last_Name'],
                update['First_Name'],
                update['District']
            ))

        if cursor.rowcount > 0:
            db_updates += 1

    conn.commit()
    conn.close()

    print(f"[OK] Database updated: {db_updates} representatives")

    # Show summary statistics
    print("\n" + "="*80)
    print("FUNDING SUMMARY:")
    print("="*80)

    aipac_funded = our_df[our_df['AIPAC_Funded'] != 'No']
    war_funded = our_df[our_df['War_Industrial_Complex_Funded'] != 'No']
    both_funded = our_df[(our_df['AIPAC_Funded'] != 'No') & (our_df['War_Industrial_Complex_Funded'] != 'No')]

    print(f"\nRepresentatives with AIPAC funding: {len(aipac_funded)}")
    print(f"Representatives with War Industry funding: {len(war_funded)}")
    print(f"Representatives with BOTH: {len(both_funded)}")
    print(f"Representatives with NO funding from these sources: {len(our_df) - len(both_funded)}")

    # Show top funded
    print("\n" + "-"*80)
    print("Top 5 AIPAC Funded (Florida):")
    print("-"*80)
    aipac_top = aipac_funded.nlargest(5, 'AIPAC_Funded', keep='all')[['First_Name', 'Last_Name', 'District', 'AIPAC_Funded']]
    for _, row in aipac_top.iterrows():
        print(f"  {row['First_Name']} {row['Last_Name']} ({row['District']}): {row['AIPAC_Funded']}")

    print("\n" + "-"*80)
    print("Top 5 War Industry Funded (Florida):")
    print("-"*80)
    war_top = war_funded.nlargest(5, 'War_Industrial_Complex_Funded', keep='all')[['First_Name', 'Last_Name', 'District', 'War_Industrial_Complex_Funded']]
    for _, row in war_top.iterrows():
        print(f"  {row['First_Name']} {row['Last_Name']} ({row['District']}): {row['War_Industrial_Complex_Funded']}")

    print("\n" + "="*80)
    print("[OK] UPDATE COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("1. Restart your Streamlit app to see changes: streamlit run app.py")
    print("2. Test the funding filters in the Browse tab")
    print("3. View individual representatives to see funding details")

    return True

if __name__ == "__main__":
    try:
        success = update_funding_data()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
