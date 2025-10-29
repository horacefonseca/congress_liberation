# Florida Federal Representatives Finder - Project Outline

## Project Overview
**Name:** Florida Congress Connect
**Purpose:** Enable Florida citizens to easily find, learn about, and contact their federal representatives
**Type:** Academic civic engagement project
**Platform:** Streamlit (free deployment on Streamlit Community Cloud)

---

## 1. PROJECT GOALS

### Primary Objectives
- Make representative information accessible and searchable
- Simplify the process of contacting elected officials
- Increase civic awareness and engagement
- Provide direct links to social media and contact forms

### Success Metrics
- User can find their representative in < 30 seconds
- All contact methods clearly displayed
- Mobile-friendly interface
- Zero cost deployment (freemium)

---

## 2. DATA ANALYSIS

### Available Data Fields
From `FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv`:
- **Identification:** Office, Name (Last, First, Middle), District, Party
- **Contact:** DC Office Address, Phone, Website, Contact Form
- **Social Media:** Facebook, Twitter/X, Instagram, TikTok
- **Geography:** Geographic Region (e.g., "Tampa Bay", "Panhandle")

### Data Structure
- 2 U.S. Senators (statewide)
- 28 U.S. House Representatives (districts FL-01 through FL-28)
- Total: 30 federal officials

---

## 3. FEATURES & FUNCTIONALITY

### Core Features (MVP)
1. **Search by Location**
   - Dropdown for House districts (FL-01 to FL-28)
   - Option to view Senators (statewide)
   - Search by geographic region

2. **Representative Profile Display**
   - Photo placeholder/name
   - Party affiliation
   - District/Region
   - DC Office information

3. **Contact Hub**
   - Phone number (click-to-call on mobile)
   - Website link
   - Contact form link
   - Social media links (Facebook, Twitter, Instagram, TikTok)

4. **Browse All Representatives**
   - Filterable table view
   - Filter by: Party, Region, Office Type
   - Sort by: District, Name, Party

### Enhanced Features (Future)
- ZIP code lookup to district matching
- Email petition template generator
- Legislative voting record integration (via Congress.gov API)
- Local office locations
- Newsletter signup links

---

## 4. TECHNICAL ARCHITECTURE

### Technology Stack
- **Frontend/Backend:** Streamlit (Python)
- **Data Storage:** CSV (current), SQLite (optional upgrade)
- **Deployment:** Streamlit Community Cloud (free)
- **Version Control:** Git + GitHub

### File Structure
```
congress_liberation/
├── app.py                          # Main Streamlit application
├── data/
│   └── FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv
├── utils/
│   ├── data_loader.py             # CSV loading and processing
│   └── search.py                  # Search functionality
├── assets/
│   └── styles.css                 # Custom styling (optional)
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── log.txt                        # Session tracking
└── .streamlit/
    └── config.toml               # Streamlit configuration
```

### Key Libraries
```
streamlit==1.30.0
pandas==2.1.4
pillow==10.1.0  # For image handling
```

---

## 5. DESIGN SPECIFICATIONS

### User Interface Design

#### Home Page
- **Header:** "Find Your Florida Federal Representatives"
- **Tagline:** "Connect with your voice in Congress"
- **Search Section:**
  - "I want to find my:" [Dropdown: U.S. Senator / U.S. House Rep]
  - If House: "Select your district:" [Dropdown: FL-01 through FL-28]
  - [Search Button]

#### Results Display
- **Representative Card:**
  - Name (large, bold)
  - Office & District
  - Party badge (color-coded)
  - Geographic region

- **Contact Section:**
  - "📞 Call: [phone]"
  - "🌐 Website: [link]"
  - "✉️ Contact Form: [link]"
  - "📱 Follow on Social Media:"
    - Facebook | Twitter | Instagram | TikTok icons

- **Actions:**
  - "📝 Send a Message" (opens contact form)
  - "📊 View All Representatives"

#### Browse Page
- Searchable/filterable table
- Columns: Name, Office, District, Party, Region, Contact
- Export functionality

### Color Scheme
- Primary: #003366 (Navy Blue - professional, trustworthy)
- Secondary: #DC143C (Crimson Red - action/engagement)
- Neutral: #F5F5F5 (Light gray background)
- Party colors: Blue (Democrat), Red (Republican)

### Accessibility
- High contrast text
- Screen reader friendly
- Keyboard navigation
- Mobile responsive (Streamlit default)

---

## 6. DEVELOPMENT PHASES

### Phase 1: Setup & Data Preparation (Week 1)
**Tasks:**
- [ ] Set up GitHub repository
- [ ] Create virtual environment
- [ ] Install Streamlit and dependencies
- [ ] Load and validate CSV data
- [ ] Create data processing utilities
- [ ] Design basic page layout

**Deliverables:**
- Working local Streamlit app
- Data successfully loaded

### Phase 2: Core Features (Week 2)
**Tasks:**
- [ ] Implement district search dropdown
- [ ] Create representative profile display
- [ ] Add contact information layout
- [ ] Implement social media link buttons
- [ ] Create "View All" table page
- [ ] Add filtering functionality

**Deliverables:**
- Functional search and display
- All data fields visible

### Phase 3: Enhancement & Polish (Week 3)
**Tasks:**
- [ ] Add custom styling/branding
- [ ] Implement region-based search
- [ ] Add party filtering
- [ ] Create "About" page explaining the project
- [ ] Add usage instructions
- [ ] Optimize mobile layout
- [ ] Test all links and functionality

**Deliverables:**
- Polished, user-friendly interface
- All features tested

### Phase 4: Deployment & Documentation (Week 4)
**Tasks:**
- [ ] Create comprehensive README
- [ ] Write deployment guide
- [ ] Deploy to Streamlit Community Cloud
- [ ] Test deployed version
- [ ] Create user guide
- [ ] Document academic context and purpose

**Deliverables:**
- Live, publicly accessible application
- Complete documentation

---

## 7. DEPLOYMENT PLAN

### Streamlit Community Cloud Setup
1. **Prerequisites:**
   - GitHub repository with code
   - requirements.txt file
   - Streamlit account (free)

2. **Deployment Steps:**
   - Push code to GitHub
   - Connect Streamlit Cloud to GitHub repo
   - Select branch and main file (app.py)
   - Deploy (automatic)

3. **URL Structure:**
   - Format: `https://[app-name]-[username].streamlit.app`
   - Custom subdomain available

### Alternative Free Platforms
- **Heroku** (Free tier available with limitations)
- **Railway** (Free tier: $5 credit/month)
- **Render** (Free tier available)
- **PythonAnywhere** (Free tier with limitations)

**Recommendation:** Streamlit Community Cloud (best for Streamlit apps, easiest deployment)

---

## 8. TESTING PLAN

### Functional Testing
- [ ] Search by each district (FL-01 to FL-28)
- [ ] Search for Senators
- [ ] Verify all contact links work
- [ ] Test all social media links
- [ ] Filter by party
- [ ] Filter by region
- [ ] Mobile responsiveness

### User Acceptance Testing
- [ ] Can users find their representative quickly?
- [ ] Are contact methods clear?
- [ ] Is the interface intuitive?
- [ ] Get feedback from 3-5 test users

### Data Validation
- [ ] All 30 officials present
- [ ] No broken links
- [ ] Phone numbers formatted correctly
- [ ] District assignments accurate

---

## 9. MAINTENANCE & UPDATES

### Regular Updates Needed
- **Post-Election:** Update representatives after elections (every 2 years)
- **Contact Info:** Verify links quarterly
- **Social Media:** Update handles if changed

### Data Sources for Updates
- House.gov official directory
- Senate.gov official directory
- Individual representative websites

---

## 10. ACADEMIC CONTEXT

### Learning Objectives
- Data-driven web application development
- Civic technology and digital democracy
- User-centered design
- Cloud deployment and DevOps
- Python/Streamlit framework

### Documentation Requirements
- Code comments explaining functionality
- README with project purpose
- User guide
- Technical documentation
- Academic reflection on civic impact

### Ethical Considerations
- Accuracy of information
- Neutral presentation (no bias)
- Privacy (no tracking of user searches)
- Accessibility for all citizens

---

## 11. BUDGET & RESOURCES

### Costs: $0
- Streamlit Community Cloud: Free
- GitHub: Free
- Domain (optional): ~$12/year
- All development tools: Free/Open Source

### Time Estimate
- **Development:** 20-30 hours
- **Testing:** 5-10 hours
- **Documentation:** 5 hours
- **Total:** 30-45 hours (4-6 weeks part-time)

---

## 12. SUCCESS CRITERIA

### MVP Launch Checklist
- [ ] All 30 representatives searchable
- [ ] All contact methods functional
- [ ] Mobile responsive
- [ ] Deployed and accessible via public URL
- [ ] Documentation complete
- [ ] Zero critical bugs

### Post-Launch Goals
- Share with Florida community groups
- Gather user feedback
- Potential to expand to other states
- Academic presentation/publication

---

## 13. NEXT STEPS

1. **Immediate Actions:**
   - Review and approve this outline
   - Set up development environment
   - Create GitHub repository
   - Start Phase 1 development

2. **First Development Session:**
   - Install Streamlit
   - Create basic app.py
   - Load CSV and display first representative
   - Test local deployment

---

## APPENDIX: Sample Code Structure

### app.py (Main Application)
```python
import streamlit as st
import pandas as pd
from utils.data_loader import load_officials

# Page config
st.set_page_config(
    page_title="Florida Congress Connect",
    page_icon="🏛️",
    layout="wide"
)

# Load data
officials = load_officials()

# Main interface
st.title("🏛️ Find Your Florida Federal Representatives")
st.markdown("Connect with your voice in Congress")

# Search section
office_type = st.selectbox("I want to find my:", ["U.S. House Representative", "U.S. Senator"])

# Search logic and display...
```

### utils/data_loader.py
```python
import pandas as pd

def load_officials():
    """Load and process official data from CSV"""
    df = pd.read_csv('data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv')
    return df

def get_senators(df):
    """Return only senators"""
    return df[df['Office'] == 'U.S. Senate']

def get_representative_by_district(df, district):
    """Get house rep by district"""
    return df[df['District'] == district]
```

---

**Project Status:** Planning Complete - Ready for Development
**Last Updated:** 2025-10-28
**Next Milestone:** Phase 1 - Setup & Data Preparation
