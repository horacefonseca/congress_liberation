"""
Database operations for Congress Connect
Handles SQLite database creation, data import, and queries
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional


class CongressDatabase:
    """Manages the SQLite database for congressional representatives"""

    def __init__(self, db_path: str = "data/congress.db"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        return self.conn

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Create database tables with full schema"""
        cursor = self.conn.cursor()

        # Drop existing table if it exists (for development)
        cursor.execute("DROP TABLE IF EXISTS representatives")

        # Create representatives table
        cursor.execute("""
            CREATE TABLE representatives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bioguide_id TEXT UNIQUE,
                first_name TEXT,
                middle_name TEXT,
                last_name TEXT,
                office TEXT,
                state TEXT,
                district TEXT,
                party TEXT,
                region TEXT,
                dc_office_address TEXT,
                dc_zip TEXT,
                dc_phone TEXT,
                website TEXT,
                contact_form TEXT,
                email TEXT,
                facebook TEXT,
                twitter TEXT,
                instagram TEXT,
                tiktok TEXT,
                aipac_funded TEXT DEFAULT 'No',
                war_industrial_complex_funded TEXT DEFAULT 'No',
                photo_url TEXT,
                in_office_since DATE,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_verified BOOLEAN DEFAULT FALSE
            )
        """)

        # Create indexes for fast querying
        cursor.execute("CREATE INDEX idx_state ON representatives(state)")
        cursor.execute("CREATE INDEX idx_district ON representatives(district)")
        cursor.execute("CREATE INDEX idx_party ON representatives(party)")
        cursor.execute("CREATE INDEX idx_aipac ON representatives(aipac_funded)")
        cursor.execute("CREATE INDEX idx_war_industry ON representatives(war_industrial_complex_funded)")

        self.conn.commit()
        print("[OK] Database tables created successfully")

    def import_csv_data(self, csv_path: str = "data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv"):
        """Import data from CSV file into database"""
        # Read CSV
        df = pd.read_csv(csv_path)

        # Map CSV columns to database columns
        column_mapping = {
            'Office': 'office',
            'Last_Name': 'last_name',
            'First_Name': 'first_name',
            'Middle_Name': 'middle_name',
            'District': 'district',
            'Party': 'party',
            'DC_Office_Address': 'dc_office_address',
            'DC_Zip': 'dc_zip',
            'DC_Phone': 'dc_phone',
            'Website': 'website',
            'Contact_Form': 'contact_form',
            'Email': 'email',
            'Facebook': 'facebook',
            'Twitter_X': 'twitter',
            'Instagram': 'instagram',
            'TikTok': 'tiktok',
            'Geographic_Region': 'region',
            'AIPAC_Funded': 'aipac_funded',
            'War_Industrial_Complex_Funded': 'war_industrial_complex_funded'
        }

        # Rename columns
        df_renamed = df.rename(columns=column_mapping)

        # Add state column (extract from district or set to FL for senators)
        df_renamed['state'] = df_renamed['district'].apply(
            lambda x: 'FL' if pd.isna(x) or x == 'Statewide' else x.split('-')[0]
        )

        # Generate simple bioguide_id (for now, use last_name + first initial)
        df_renamed['bioguide_id'] = (
            df_renamed['last_name'].str.upper() +
            df_renamed['first_name'].str[0].str.upper()
        )

        # Select and order columns for database
        db_columns = [
            'bioguide_id', 'first_name', 'middle_name', 'last_name',
            'office', 'state', 'district', 'party', 'region',
            'dc_office_address', 'dc_zip', 'dc_phone',
            'website', 'contact_form', 'email',
            'facebook', 'twitter', 'instagram', 'tiktok',
            'aipac_funded', 'war_industrial_complex_funded'
        ]

        df_final = df_renamed[db_columns]

        # Insert into database
        df_final.to_sql('representatives', self.conn, if_exists='append', index=False)

        self.conn.commit()
        print(f"[OK] Imported {len(df_final)} representatives into database")

        return len(df_final)

    def get_representative_by_district(self, district: str) -> Optional[Dict]:
        """Get representative by district code (e.g., 'FL-01')"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM representatives
            WHERE district = ? AND office = 'U.S. House'
        """, (district,))

        row = cursor.fetchone()
        return dict(row) if row else None

    def get_senators_by_state(self, state: str = 'FL') -> List[Dict]:
        """Get both senators for a state"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM representatives
            WHERE state = ? AND office = 'U.S. Senate'
            ORDER BY last_name
        """, (state,))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_all_representatives(self, state: str = None, party: str = None) -> List[Dict]:
        """Get all representatives with optional filters"""
        cursor = self.conn.cursor()

        query = "SELECT * FROM representatives WHERE 1=1"
        params = []

        if state:
            query += " AND state = ?"
            params.append(state)

        if party:
            query += " AND party = ?"
            params.append(party)

        query += " ORDER BY state, office DESC, district"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def search_representatives(
        self,
        state: str = None,
        party: str = None,
        aipac_funded: str = None,
        war_industry_funded: str = None
    ) -> List[Dict]:
        """Advanced search with multiple filters"""
        cursor = self.conn.cursor()

        query = "SELECT * FROM representatives WHERE 1=1"
        params = []

        if state:
            query += " AND state = ?"
            params.append(state)

        if party:
            query += " AND party = ?"
            params.append(party)

        if aipac_funded and aipac_funded != "All":
            if aipac_funded == "Yes":
                query += " AND aipac_funded != 'No'"
            else:
                query += " AND aipac_funded = 'No'"

        if war_industry_funded and war_industry_funded != "All":
            if war_industry_funded == "Yes":
                query += " AND war_industrial_complex_funded != 'No'"
            else:
                query += " AND war_industrial_complex_funded = 'No'"

        query += " ORDER BY state, office DESC, district"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_stats(self) -> Dict:
        """Get database statistics"""
        cursor = self.conn.cursor()

        stats = {}

        # Total representatives
        cursor.execute("SELECT COUNT(*) FROM representatives")
        stats['total'] = cursor.fetchone()[0]

        # By party
        cursor.execute("""
            SELECT party, COUNT(*) as count
            FROM representatives
            GROUP BY party
        """)
        stats['by_party'] = {row[0]: row[1] for row in cursor.fetchall()}

        # By state
        cursor.execute("""
            SELECT state, COUNT(*) as count
            FROM representatives
            GROUP BY state
        """)
        stats['by_state'] = {row[0]: row[1] for row in cursor.fetchall()}

        # AIPAC funded count
        cursor.execute("""
            SELECT COUNT(*) FROM representatives
            WHERE aipac_funded != 'No'
        """)
        stats['aipac_funded_count'] = cursor.fetchone()[0]

        # War industry funded count
        cursor.execute("""
            SELECT COUNT(*) FROM representatives
            WHERE war_industrial_complex_funded != 'No'
        """)
        stats['war_industry_funded_count'] = cursor.fetchone()[0]

        return stats


def initialize_database():
    """Initialize database and import data"""
    db = CongressDatabase()
    db.connect()

    print("Creating database tables...")
    db.create_tables()

    print("Importing CSV data...")
    count = db.import_csv_data()

    print(f"\n[OK] Database initialized with {count} representatives")

    # Show stats
    stats = db.get_stats()
    print(f"\nDatabase Statistics:")
    print(f"  Total: {stats['total']}")
    print(f"  By Party: {stats['by_party']}")
    print(f"  AIPAC Funded: {stats['aipac_funded_count']}")
    print(f"  War Industry Funded: {stats['war_industry_funded_count']}")

    db.close()
    return True


if __name__ == "__main__":
    # Run initialization if executed directly
    initialize_database()
