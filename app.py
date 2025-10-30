"""
Congress Connect - Find and Contact Your Federal Representatives
A free, privacy-first tool for civic engagement
"""

import streamlit as st
import pandas as pd
from utils.database import CongressDatabase
from utils.search import search_by_zip, search_by_district, get_all_florida_reps

# Page configuration
st.set_page_config(
    page_title="Congress Connect - Find Your Representatives",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database connection
@st.cache_resource
def get_database():
    """Get or create database connection"""
    db = CongressDatabase()
    db.connect()
    return db

# Custom CSS for mobile-first responsive design
def inject_custom_css():
    st.markdown("""
    <style>
    /* Mobile-first base styles */
    .main {
        padding: 1rem;
    }

    /* Privacy badge */
    .privacy-badge {
        background: #E8F5E9;
        color: #2E7D32;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.875rem;
        display: inline-block;
        margin: 0.5rem 0;
    }

    /* Representative card */
    .rep-card {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    /* Funding transparency highlight */
    .funding-info {
        background: #FFF3CD;
        border-left: 4px solid #FFC107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }

    .funding-label {
        font-weight: bold;
        color: #856404;
        margin-right: 0.5rem;
    }

    .funding-value-no {
        color: #28a745;
        font-weight: bold;
    }

    .funding-value-yes {
        color: #dc3545;
        font-weight: bold;
    }

    /* Contact buttons */
    .contact-btn {
        display: block;
        width: 100%;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #003366;
        color: white;
        text-align: center;
        border-radius: 6px;
        text-decoration: none;
        font-size: 16px;
    }

    .contact-btn:hover {
        background: #004080;
    }

    /* Desktop styles */
    @media (min-width: 992px) {
        .main {
            padding: 2rem 4rem;
        }
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    inject_custom_css()

    # Header
    st.title("🏛️ Congress Connect")
    st.subheader("Find and Contact Your Federal Representatives")

    # Privacy notice
    st.markdown("""
    <div class="privacy-badge">
        🔒 100% Free • No Signup • No Email Required • Private & Anonymous
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Initialize database
    db = get_database()

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🔍 Find My Rep", "📋 Browse All", "ℹ️ About"])

    with tab1:
        show_search_page(db)

    with tab2:
        show_browse_page(db)

    with tab3:
        show_about_page()


def show_search_page(db):
    """Search for representatives by ZIP code or district"""
    st.markdown("### Find Your Representative")

    col1, col2 = st.columns([2, 1])

    with col1:
        zip_code = st.text_input(
            "📍 Enter your ZIP code:",
            max_chars=5,
            placeholder="33139",
            help="We'll find your representative based on your ZIP code"
        )

    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        search_button = st.button("Find My Rep", type="primary", use_container_width=True)

    # Manual district selection fallback
    with st.expander("Or select your district manually"):
        districts = [f"FL-{str(i).zfill(2)}" for i in range(1, 29)]
        selected_district = st.selectbox("Select District:", [""] + districts)
        if selected_district:
            rep = search_by_district(selected_district, db)
            if rep:
                display_representative(rep)

    # Search by ZIP
    if search_button and zip_code:
        with st.spinner("Searching..."):
            result = search_by_zip(zip_code, db)

            if result["success"]:
                st.success(f"✅ {result['message']}")

                # Display house representative
                if result["house_rep"]:
                    st.markdown("### Your U.S. House Representative")
                    display_representative(result["house_rep"])

                # Display senators
                if result["senators"]:
                    st.markdown("### Your U.S. Senators")
                    for senator in result["senators"]:
                        display_representative(senator)
            else:
                st.error(result["message"])


def display_representative(rep: dict):
    """Display a representative's information"""
    with st.container():
        # Basic info
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"## {rep['first_name']} {rep['last_name']}")
            party_color = "#DC143C" if rep['party'] == "Republican" else "#0015BC"
            st.markdown(f"""
            <div style="display: inline-block; background-color: {party_color}; color: white;
                        padding: 0.25rem 0.75rem; border-radius: 12px; font-weight: bold;">
                {rep['party']}
            </div>
            <span style="margin-left: 1rem;">
                {rep['office']} • {rep['district'] if rep['district'] != 'Statewide' else 'Statewide'}
            </span>
            """, unsafe_allow_html=True)

            if rep['region']:
                st.caption(f"📍 {rep['region']}")

            # Election Information
            if rep.get('next_general_election'):
                if '2026' in rep['next_general_election']:
                    st.info(f"🗳️ **Up for election:** {rep['next_general_election']}")
                else:
                    st.caption(f"🗳️ Next election: {rep['next_general_election']}")

        # Funding Transparency Section
        st.markdown("---")
        st.markdown("### 💰 Campaign Funding Transparency")

        funding_col1, funding_col2 = st.columns(2)

        with funding_col1:
            aipac = rep.get('aipac_funded', 'No')
            aipac_class = "funding-value-no" if aipac == "No" else "funding-value-yes"
            st.markdown(f"""
            <div class="funding-info">
                <span class="funding-label">AIPAC Funded:</span>
                <span class="{aipac_class}">{aipac}</span>
            </div>
            """, unsafe_allow_html=True)

        with funding_col2:
            war_industry = rep.get('war_industrial_complex_funded', 'No')
            war_class = "funding-value-no" if war_industry == "No" else "funding-value-yes"
            st.markdown(f"""
            <div class="funding-info">
                <span class="funding-label">War Industry Funded:</span>
                <span class="{war_class}">{war_industry}</span>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("ℹ️ What does this mean?"):
            st.write("""
            **Campaign Funding Transparency:**
            - **AIPAC**: American Israel Public Affairs Committee funding
            - **War Industrial Complex**: Defense contractor campaign contributions

            This information helps you understand potential influences on your representative's policy positions.
            """)

        # Contact Information
        st.markdown("---")
        st.markdown("### 📞 Contact Information")

        contact_col1, contact_col2 = st.columns(2)

        with contact_col1:
            if rep['dc_phone']:
                st.markdown(f"""
                <a href="tel:{rep['dc_phone']}" class="contact-btn">
                    📞 Call: {rep['dc_phone']}
                </a>
                """, unsafe_allow_html=True)

            if rep['website']:
                st.markdown(f"""
                <a href="{rep['website']}" target="_blank" class="contact-btn">
                    🌐 Official Website
                </a>
                """, unsafe_allow_html=True)

        with contact_col2:
            if rep['contact_form']:
                st.markdown(f"""
                <a href="{rep['contact_form']}" target="_blank" class="contact-btn">
                    ✉️ Contact Form
                </a>
                """, unsafe_allow_html=True)

            if rep['email'] and rep['email'] != "Use web form":
                st.markdown(f"""
                <a href="mailto:{rep['email']}" class="contact-btn">
                    📧 Email
                </a>
                """, unsafe_allow_html=True)

        # Office Address
        if rep['dc_office_address']:
            st.markdown("**DC Office:**")
            st.write(f"{rep['dc_office_address']}, Washington, DC {rep['dc_zip']}")

        # Social Media
        st.markdown("---")
        st.markdown("### 📱 Social Media")

        social_links = []
        if rep['facebook']:
            social_links.append(f"[Facebook]({rep['facebook']})")
        if rep['twitter']:
            social_links.append(f"[Twitter/X]({rep['twitter']})")
        if rep['instagram']:
            social_links.append(f"[Instagram]({rep['instagram']})")
        if rep['tiktok']:
            social_links.append(f"[TikTok]({rep['tiktok']})")

        if social_links:
            st.markdown(" • ".join(social_links))

        # Call Script Generator
        st.markdown("---")
        with st.expander("💬 Need help contacting? Get a call script"):
            rep_key = f"{rep['last_name']}_{rep['first_name']}_{rep.get('district', 'senate')}"
            topic = st.selectbox(
                "What are you calling about?",
                ["Healthcare", "Education", "Climate Change", "Immigration",
                 "Economy/Jobs", "Gun Policy", "Other"],
                key=f"topic_{rep_key}"
            )

            if st.button("Generate Call Script", key=f"script_btn_{rep_key}"):
                script = generate_call_script(rep, topic)
                st.text_area("Your Call Script:", script, height=200, key=f"script_area_{rep_key}")
                st.info("Tip: Feel free to personalize this script with your own story!")

        st.markdown("---")


def generate_call_script(rep: dict, topic: str) -> str:
    """Generate a basic call script"""
    name = f"{rep['first_name']} {rep['last_name']}"
    title = "Senator" if rep['office'] == "U.S. Senate" else "Representative"

    script = f"""Hello, my name is [YOUR NAME] and I'm a constituent from [YOUR CITY/ZIP CODE].

I'm calling to speak with {title} {name} about {topic.lower()}.

[EXPLAIN YOUR CONCERN OR POSITION]

I would like to know {title} {name}'s position on this issue and respectfully request that they [YOUR SPECIFIC REQUEST - e.g., support/oppose specific legislation, hold a town hall, etc.].

Thank you for your time.

---
Tips for an effective call:
- Be polite and respectful
- Keep it brief (1-2 minutes)
- Share your personal story if relevant
- Ask for a response or follow-up
- Get the name of the staffer you speak with
"""
    return script


def show_browse_page(db):
    """Browse all representatives with filters"""
    st.markdown("### Browse All Florida Representatives")

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        office_filter = st.selectbox("Office:", ["All", "U.S. Senate", "U.S. House"])

    with col2:
        party_filter = st.selectbox("Party:", ["All", "Republican", "Democrat", "Independent"])

    with col3:
        aipac_filter = st.selectbox("AIPAC Funded:", ["All", "Yes", "No"])

    with col4:
        war_filter = st.selectbox("War Industry:", ["All", "Yes", "No"])

    # Get all reps
    all_reps = get_all_florida_reps(db)

    # Apply filters
    filtered_reps = all_reps

    if office_filter != "All":
        filtered_reps = [r for r in filtered_reps if r['office'] == office_filter]

    if party_filter != "All":
        filtered_reps = [r for r in filtered_reps if r['party'] == party_filter]

    if aipac_filter != "All":
        if aipac_filter == "Yes":
            filtered_reps = [r for r in filtered_reps if r['aipac_funded'] != "No"]
        else:
            filtered_reps = [r for r in filtered_reps if r['aipac_funded'] == "No"]

    if war_filter != "All":
        if war_filter == "Yes":
            filtered_reps = [r for r in filtered_reps if r['war_industrial_complex_funded'] != "No"]
        else:
            filtered_reps = [r for r in filtered_reps if r['war_industrial_complex_funded'] == "No"]

    # Display count
    st.write(f"Showing {len(filtered_reps)} representatives")

    # Convert to dataframe for display
    if filtered_reps:
        df = pd.DataFrame(filtered_reps)

        # Select columns to display
        display_df = df[[
            'last_name', 'first_name', 'party', 'district',
            'aipac_funded', 'war_industrial_complex_funded', 'dc_phone'
        ]].copy()

        display_df.columns = [
            'Last Name', 'First Name', 'Party', 'District',
            'AIPAC Funded', 'War Industry', 'Phone'
        ]

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Detailed view
        st.markdown("---")
        st.markdown("### View Details")
        selected_name = st.selectbox(
            "Select a representative for full details:",
            [f"{r['first_name']} {r['last_name']} ({r['district']})" for r in filtered_reps]
        )

        if selected_name:
            # Find selected rep
            selected_rep = next(
                (r for r in filtered_reps
                 if f"{r['first_name']} {r['last_name']} ({r['district']})" == selected_name),
                None
            )
            if selected_rep:
                display_representative(selected_rep)


def show_about_page():
    """About page with information about the project"""
    st.markdown("### About Congress Connect")

    st.write("""
    **Congress Connect** is a free, privacy-first tool to help citizens find and contact
    their federal representatives.

    #### Why We Built This

    Many existing tools require email signups, collect personal data, or charge fees.
    We believe civic engagement should be:
    - **Free** - No cost, no paywall
    - **Private** - No email, no account, no tracking
    - **Accessible** - Works on any device, no app required
    - **Transparent** - Shows campaign funding information

    #### Features

    - 🔍 **ZIP Code Lookup** - Find your rep instantly
    - 💰 **Funding Transparency** - See AIPAC and defense industry funding
    - 📱 **Mobile-Friendly** - Works perfectly on phones
    - 💬 **Call Scripts** - Get help with what to say
    - 🔒 **Privacy-First** - We don't collect your data

    #### Data Sources

    - Representative contact information: Official House.gov and Senate.gov directories
    - Campaign funding: Federal Election Commission (FEC) 2023-2024 election cycle data

    #### How to Help

    - **Share** this tool with fellow citizens
    - **Use** it to contact your representatives about issues you care about
    - **Provide feedback** to help us improve

    #### Privacy Policy

    We collect **zero personal information**:
    - No email addresses
    - No account creation
    - No tracking cookies
    - No analytics that identify individuals

    Your searches are not stored. Your privacy matters.

    #### Open Source

    This project is open source and built for educational purposes.

    ---

    **Last Updated:** October 2025
    **Version:** 1.0 MVP
    """)


if __name__ == "__main__":
    main()
