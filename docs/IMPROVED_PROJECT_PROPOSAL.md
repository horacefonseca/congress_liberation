# Congress Connect: Improved Project Proposal

**Project Name:** Congress Connect (formerly "Florida Congress Connect")
**Version:** 2.0 - Addressing Critical Flaws
**Date:** 2025-10-28
**Status:** Design Revision Based on Critical Analysis

---

## EXECUTIVE SUMMARY

This improved proposal addresses the 8 major flaws identified in the critical analysis while maintaining academic feasibility. Key improvements:

1. **ZIP code to district lookup** (solves CRITICAL usability flaw)
2. **Action-oriented design** (provides context for engagement, not just contact info)
3. **Built-in analytics** (measures actual civic impact for academic rigor)
4. **National-ready architecture** (launches with Florida, designed for 50 states)
5. **Link validation system** (ensures data stays current)
6. **Clear differentiation** (focuses on specific niche: first-time civic engagers)

**Still achievable in 4-6 weeks with free tools.**

---

## PART 1: PROBLEM REDEFINITION

### The Real Problem (Research-Backed)
**Original problem statement:** "Enable citizens to find and contact representatives"
**Issue:** Too vague, assumes the barrier is just finding contact info

**Revised problem statement:**
> "First-time civic engagers face three barriers: (1) don't know their district/representatives, (2) don't understand what their representatives are doing, and (3) don't know what to say when contacting them."

### Target User Persona: "Civically Curious Casey"
- **Age:** 22-35 (college student or young professional)
- **Civic experience:** Voted once or twice, never contacted a representative
- **Motivation:** Recent news made them want to "do something"
- **Barriers:**
  - "I don't know who represents me"
  - "I don't know what they've been voting on"
  - "I don't know what to say if I call"
  - "I don't know if my voice matters"

### Success Metrics (Measurable)
1. **Usability:** User finds their rep in < 30 seconds (90%+ success rate)
2. **Engagement:** 20%+ of users click a contact method
3. **Follow-through:** 10%+ report actually contacting their rep (via optional feedback)
4. **Satisfaction:** 4+ stars average user rating

---

## PART 2: DIFFERENTIATION STRATEGY

### How This is Different from Existing Tools

| Feature | Congress Connect | House.gov | GovTrack | 5 Calls |
|---------|------------------|-----------|----------|---------|
| **Target Audience** | First-timers | General | Policy wonks | Activists |
| **ZIP Lookup** | ✅ | ✅ | ✅ | ✅ |
| **Contact Info** | ✅ | ✅ | ⚠️ | ✅ |
| **Social Media Aggregation** | ✅ | ❌ | ⚠️ | ❌ |
| **"Why Contact" Context** | ✅ | ❌ | ❌ | ✅ |
| **Contact Templates** | ✅ | ❌ | ❌ | ✅ |
| **Voting Record** | ⚠️ (Summary) | ❌ | ✅ (Detailed) | ❌ |
| **Beginner-Friendly** | ✅✅ | ⚠️ | ❌ | ⚠️ |
| **Mobile-Optimized** | ✅ | ⚠️ | ⚠️ | ✅ |
| **Impact Tracking** | ✅ | ❌ | ❌ | ❌ |

### Unique Value Proposition
**"The easiest way for first-time civic engagers to find, understand, and contact their representatives - with context for why and how to reach out."**

**Competitive Positioning:**
- **Simpler than:** GovTrack (overwhelming for beginners)
- **More contextual than:** House.gov (just directory info)
- **More general than:** 5 Calls (not tied to specific campaigns)
- **More helpful than:** Google (scattered info from multiple sources)

---

## PART 3: REVISED ARCHITECTURE

### Technology Stack (Still Free)

**Core:**
- Streamlit (Python web framework)
- Pandas (data processing)
- Streamlit Community Cloud (deployment)

**New Additions (Critical):**
- **Google Civic Information API** (free, 25K requests/day) - ZIP to district lookup
- **ProPublica Congress API** (free) - Recent votes, bills, committee info
- **Streamlit Analytics** (privacy-respecting usage tracking)
- **pytest** (automated testing, including link validation)

**Data Storage:**
- SQLite (instead of CSV) - easier to update, query, and scale
- Automated data refresh scripts

### System Architecture

```
┌─────────────────────────────────────────────────┐
│           User Interface (Streamlit)            │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ ZIP      │  │ Browse   │  │ About/       │  │
│  │ Lookup   │  │ All Reps │  │ Feedback     │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│          Application Logic Layer                │
│  ┌──────────────────────────────────────────┐  │
│  │ search.py     │ analytics.py             │  │
│  │ data_loader.py│ api_clients.py           │  │
│  │ formatters.py │ content_generator.py     │  │
│  └──────────────────────────────────────────┘  │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│              Data Layer                         │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐  │
│  │ SQLite   │  │ Google Civic │  │ ProPublica│  │
│  │ Database │  │ API          │  │ API       │  │
│  │ (Local)  │  │ (ZIP Lookup) │  │ (Votes)   │  │
│  └──────────┘  └──────────────┘  └──────────┘  │
└─────────────────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│         Maintenance & Monitoring                │
│  ┌──────────────────────────────────────────┐  │
│  │ Daily: Link validator                    │  │
│  │ Weekly: API data refresh                 │  │
│  │ Monthly: Analytics report generation     │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## PART 4: REVISED FEATURES

### MVP Features (Phase 1-2)

#### 1. Smart Search
**Input Options:**
- ZIP code entry (primary)
- District dropdown (fallback)
- State selector (for scaling)

**Flow:**
```
User enters ZIP: 33139
  ↓
Google Civic API returns: FL-27 (Maria Elvira Salazar)
  ↓
App displays representative profile
```

#### 2. Enhanced Representative Profile

**Section A: Who They Are**
- Name, photo (sourced from official sites)
- Party, district, region
- Years in office
- Committee assignments (from ProPublica API)

**Section B: What They're Doing**
- Latest 3 votes (from ProPublica API)
  - Bill name (plain language)
  - Their vote (Yes/No/Abstain)
  - Date
- Most recent sponsored bills (top 3)
- Key policy focus areas

**Section C: How to Reach Them**
- 📞 Phone (click-to-call on mobile)
- 🌐 Website
- ✉️ Contact form
- 📧 Email (if available)
- 📱 Social media (all platforms)
- 📍 DC office address

**Section D: Why & How to Contact**
- "Why contact your representative?" (educational)
- "Tips for effective constituent communication"
- Template generator: "I'm contacting about..." dropdown
  - Healthcare
  - Education
  - Climate
  - Immigration
  - Economy
  - Other (custom)

#### 3. Action Templates

**Email/Call Script Generator:**
```
Input: User selects "Climate" topic
Output:
"Hello, my name is [Your Name] and I'm a constituent from [ZIP code].
I'm calling to express my concern about climate policy and ask that
Representative [Name] support legislation to [reduce emissions/support
renewable energy/etc.]. Thank you for your time."
```

#### 4. Browse & Compare
- Table view of all representatives
- Filter by: State, Party, Committee
- Sort by: Name, District, Party, Years in Office
- "Compare" feature: Side-by-side view of 2-3 reps

#### 5. Feedback & Impact Tracking

**Optional User Feedback:**
After viewing contact info, prompt appears:
- "Did you contact your representative?"
  - Yes / No / Later
- If Yes: "How did you contact them?"
  - Phone / Email / Form / Social Media / In Person
- If Yes: "Was it helpful?" (1-5 stars)

**Analytics Dashboard (Admin View):**
- Total searches
- Top ZIP codes
- Contact method click rates
- Feedback submissions
- Geographic heat map of usage

---

## PART 5: DATA MANAGEMENT

### Database Schema (SQLite)

**Table: representatives**
```sql
CREATE TABLE representatives (
    id INTEGER PRIMARY KEY,
    bioguide_id TEXT UNIQUE,     -- Official Congressional ID
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    office TEXT,                 -- "U.S. Senate" or "U.S. House"
    state TEXT,
    district TEXT,               -- NULL for senators
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
    photo_url TEXT,
    in_office_since DATE,
    last_updated TIMESTAMP,
    data_verified BOOLEAN DEFAULT FALSE
);
```

**Table: votes** (cached from ProPublica API)
```sql
CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    bioguide_id TEXT,
    bill_number TEXT,
    bill_title TEXT,
    vote_position TEXT,          -- "Yes", "No", "Not Voting"
    vote_date DATE,
    chamber TEXT,                -- "House" or "Senate"
    description TEXT,
    FOREIGN KEY (bioguide_id) REFERENCES representatives(bioguide_id)
);
```

**Table: analytics** (privacy-respecting)
```sql
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY,
    event_type TEXT,             -- "search", "contact_click", "feedback"
    timestamp TIMESTAMP,
    state TEXT,
    district TEXT,
    zip_code TEXT,               -- Hashed for privacy
    contact_method TEXT,         -- "phone", "email", etc.
    user_agent TEXT,             -- For mobile vs. desktop tracking
    session_id TEXT              -- Anonymous session tracking
);
```

### Data Update Strategy

**Daily:**
- Validate all external links (websites, contact forms, social media)
- Flag broken links for manual review

**Weekly:**
- Refresh voting records from ProPublica API
- Update committee assignments
- Check for new sponsored bills

**Monthly:**
- Generate data quality report
- Manual review of flagged issues
- Update representative photos if changed

**Post-Election:**
- Alert system to update new representatives
- Archive defeated/retired representatives

### API Integration Details

**Google Civic Information API:**
```python
# Example: ZIP to district lookup
import requests

def get_district_from_zip(zip_code):
    url = f"https://www.googleapis.com/civicinfo/v2/representatives"
    params = {
        "address": zip_code,
        "key": API_KEY,
        "levels": "country",
        "roles": "legislatorLowerBody,legislatorUpperBody"
    }
    response = requests.get(url, params=params)
    data = response.json()
    # Parse to extract district and officials
    return district, officials
```

**ProPublica Congress API:**
```python
# Example: Get recent votes
def get_recent_votes(bioguide_id, limit=3):
    url = f"https://api.propublica.org/congress/v1/members/{bioguide_id}/votes.json"
    headers = {"X-API-Key": PROPUBLICA_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['results'][0]['votes'][:limit]
```

---

## PART 6: REVISED UI/UX

### Mobile-First Design Principles

**1. Homepage (Mobile)**
```
┌─────────────────────────────┐
│   🏛️ CONGRESS CONNECT      │
│   Find & Contact Your Rep   │
├─────────────────────────────┤
│                             │
│   Enter Your ZIP Code:      │
│   ┌───────────────────┐     │
│   │     33139         │     │
│   └───────────────────┘     │
│        [Find My Rep]        │
│                             │
│   or                        │
│   [Browse All Florida Reps] │
│                             │
│   ─────────────────────     │
│   🎓 First time contacting  │
│   a representative?         │
│   [Learn How] →             │
└─────────────────────────────┘
```

**2. Representative Profile (Mobile)**
```
┌─────────────────────────────┐
│   ← Back to Search          │
├─────────────────────────────┤
│   [Photo]                   │
│   Rep. Maria Elvira Salazar │
│   Republican • FL-27        │
│   South Florida (Miami)     │
│                             │
│   📊 Recent Activity        │
│   └─ Voted YES on H.R. 123  │
│      "Defense Authorization"│
│      Jan 15, 2025           │
│   └─ Voted NO on H.R. 456   │
│      "Climate Action Act"   │
│      Jan 10, 2025           │
│                             │
│   📞 CONTACT                │
│   ┌─────────────────────┐   │
│   │  📞 Call Now        │   │
│   │  202-225-3931       │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │  ✉️ Email/Form      │   │
│   └─────────────────────┘   │
│   ┌─────────────────────┐   │
│   │  🌐 Website         │   │
│   └─────────────────────┘   │
│                             │
│   📱 SOCIAL MEDIA           │
│   [Facebook] [Twitter]      │
│   [Instagram] [TikTok]      │
│                             │
│   💬 What to Say            │
│   [Get Call Script] →       │
│                             │
│   📋 Full Profile →         │
└─────────────────────────────┘
```

**3. Call Script Generator (Modal)**
```
┌─────────────────────────────┐
│   What are you calling      │
│   about?                    │
├─────────────────────────────┤
│   [ ] Healthcare            │
│   [ ] Education             │
│   [ ] Climate Change        │
│   [ ] Immigration           │
│   [ ] Economy/Jobs          │
│   [ ] Other: _______        │
│                             │
│   [Generate Script]         │
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│   Your Call Script          │
├─────────────────────────────┤
│   "Hello, my name is [Your  │
│   Name] and I'm a constituent│
│   from ZIP code [33139].    │
│                             │
│   I'm calling to ask that   │
│   Rep. Salazar support      │
│   legislation addressing    │
│   climate change..."        │
│                             │
│   [Copy to Clipboard]       │
│   [Share via SMS]           │
│   [Ready? Call Now]         │
└─────────────────────────────┘
```

### Desktop Experience Enhancements
- Side-by-side comparison tool
- More detailed voting history
- Full committee list
- Interactive district map
- Analytics dashboard (if admin)

---

## PART 7: SCALABILITY PLAN

### Phase 1: Florida Launch (MVP - Weeks 1-4)
- Florida data only (30 representatives)
- ZIP lookup (Google Civic API)
- Basic voting records (ProPublica API)
- Core contact features
- Simple analytics

### Phase 2: National Expansion (Weeks 5-6)
- All 50 states (535 Congress members + 100 Senators)
- State selector on homepage
- National statistics and comparisons
- Enhanced analytics

### Technical Scalability
**Database Size:**
- Florida: 30 records = ~50 KB
- National: 635 records = ~1 MB
- With vote history: ~10-20 MB
- **Conclusion:** Easily fits in free tier SQLite

**API Rate Limits:**
- Google Civic: 25,000 requests/day (free)
- ProPublica: 5,000 requests/day (free)
- Expected traffic: 100-500 searches/day initially
- **Conclusion:** Free tiers sufficient for academic project

**Deployment:**
- Streamlit Community Cloud: Free for public repos
- Supports: SQLite, API calls, analytics
- **Conclusion:** Remains $0 cost at national scale

---

## PART 8: IMPLEMENTATION TIMELINE

### Week 1: Foundation + Critical Feature
- [ ] Set up project structure
- [ ] Initialize SQLite database
- [ ] Import Florida data to database
- [ ] **Implement ZIP code lookup** (Google Civic API)
- [ ] Basic Streamlit UI with search
- [ ] Test: User can find rep by ZIP in < 30 seconds

### Week 2: Context & Contact Features
- [ ] Integrate ProPublica API for recent votes
- [ ] Display voting records on rep profile
- [ ] Implement all contact methods display
- [ ] Add social media icon links
- [ ] Create call script generator
- [ ] Test: All links functional

### Week 3: Polish & Measurement
- [ ] Implement analytics tracking
- [ ] Add feedback mechanism
- [ ] Create "About" and "How to Contact" educational pages
- [ ] Mobile optimization pass
- [ ] Link validation script
- [ ] Automated testing suite

### Week 4: Deploy & Document
- [ ] Deploy to Streamlit Community Cloud
- [ ] Create comprehensive README
- [ ] Write academic paper/report structure
- [ ] User testing with 5-10 people
- [ ] Fix bugs from user testing
- [ ] Launch publicly

### Week 5-6: (Optional) National Expansion
- [ ] Add all state data
- [ ] State selector UI
- [ ] National statistics page
- [ ] Comparative analysis features

---

## PART 9: MEASUREMENT & ACADEMIC CONTRIBUTION

### Data Collection (Privacy-Respecting)

**What We Track:**
- ✅ Number of searches (by state/district)
- ✅ Which contact methods clicked
- ✅ Time on site
- ✅ Mobile vs. desktop usage
- ✅ Optional feedback (did they contact rep?)

**What We DON'T Track:**
- ❌ Individual user identity
- ❌ Personal information
- ❌ Content of messages/calls
- ❌ Cross-site tracking

### Academic Paper Structure

**Title:** "Congress Connect: Reducing Barriers to Civic Engagement Through Contextual Representative Discovery"

**Abstract:** (150 words summarizing problem, solution, results)

**1. Introduction**
- Problem: Low civic engagement among first-time participants
- Research question: Can an integrated tool reduce barriers to contacting representatives?

**2. Literature Review**
- Existing civic technology tools
- Barriers to civic engagement (research citations)
- Gap analysis: Why existing tools fail first-time users

**3. Methodology**
- User persona development
- Technology selection rationale
- Feature prioritization based on user research

**4. Implementation**
- System architecture
- Key technical decisions
- Challenges and solutions

**5. Results**
- Usage statistics (X searches, Y contact clicks, Z feedback responses)
- User feedback analysis
- A/B testing results (if conducted)

**6. Discussion**
- Did the tool reduce barriers?
- What worked? What didn't?
- Comparison to existing tools

**7. Future Work**
- National expansion
- Additional features (town hall finder, bill alerts)
- Integration with other civic platforms

**8. Conclusion**
- Contribution to civic technology
- Lessons learned

### Success Metrics for Academic Evaluation

**Quantitative:**
- User task success rate: > 90% can find their rep in < 30 seconds
- Contact engagement rate: > 20% click a contact method
- Feedback participation: > 10% provide feedback
- System reliability: > 99% uptime
- Link validity: > 95% of links work

**Qualitative:**
- User testimonials
- Ease of use ratings
- Perceived value assessment
- Comparison to existing tool experiences

---

## PART 10: ADDRESSING EACH CRITICAL FLAW

### ✅ Flaw #1: No ZIP Lookup
**Solution:** Google Civic Information API integration (primary search method)
**Status:** Critical - Implemented in Week 1

### ✅ Flaw #2: Static Data
**Solution:**
- SQLite database with last_updated timestamps
- Automated link validation (daily)
- API-driven vote data (refreshed weekly)
- Clear "Last verified" labels on UI
**Status:** Medium priority - Implemented in Week 3

### ✅ Flaw #3: No Differentiation
**Solution:**
- Target niche: First-time civic engagers
- Unique features: Call scripts, voting context, mobile-first
- Beginner-friendly language and design
**Status:** Core strategy - Implemented throughout

### ✅ Flaw #4: No Engagement Measurement
**Solution:**
- Built-in analytics from day one
- Feedback mechanism
- Measurable success metrics for academic paper
**Status:** Critical - Implemented in Week 3

### ✅ Flaw #5: No Legislative Context
**Solution:**
- ProPublica API for recent votes
- Plain-language bill descriptions
- Committee assignments
- Call script generator provides context
**Status:** High priority - Implemented in Week 2

### ✅ Flaw #6: Florida-Only Scope
**Solution:**
- Design for 50 states from day one
- Launch with Florida (feasibility)
- Expand to national in weeks 5-6
- State-agnostic architecture
**Status:** Architectural decision - Built into design

### ✅ Flaw #7: Oversimplified UX
**Solution:**
- User persona-driven design ("Civically Curious Casey")
- User research informing features
- Context provided at every step
- Educational content for first-timers
**Status:** Design philosophy - Implemented throughout

### ✅ Flaw #8: Not Mobile-First
**Solution:**
- Mobile-first design approach
- Click-to-call buttons
- Streamlined mobile UI
- Touch-friendly interface
**Status:** Design priority - Implemented throughout

---

## PART 11: RISK ASSESSMENT & MITIGATION

### Technical Risks

**Risk 1: API Rate Limits**
- **Probability:** Low
- **Impact:** High
- **Mitigation:**
  - Cache API responses (votes stored in database)
  - Implement rate limiting on frontend
  - Monitor daily usage
  - Upgrade to paid tier if needed (still < $50/month)

**Risk 2: API Deprecation**
- **Probability:** Low-Medium
- **Impact:** High
- **Mitigation:**
  - Use multiple API sources (Google + ProPublica)
  - Design abstraction layer for easy API swapping
  - Maintain fallback to manual ZIP-to-district CSV

**Risk 3: Streamlit Cloud Limitations**
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:**
  - Keep app under resource limits (< 1 GB memory)
  - Optimize database queries
  - Have backup deployment plan (Heroku, Railway)

### Academic Risks

**Risk 4: Insufficient User Testing**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:**
  - Built-in feedback mechanism
  - Recruit 10+ testers from university community
  - Offer incentive (gift card) for participation

**Risk 5: Low Usage Numbers**
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:**
  - Share on university networks, social media
  - Reach out to civic engagement groups
  - Focus on qualitative insights if quantitative data limited

### Scope Risks

**Risk 6: Feature Creep**
- **Probability:** High
- **Impact:** Medium
- **Mitigation:**
  - Strict MVP definition
  - Timeline with clear phase gates
  - "Future work" parking lot for additional ideas

---

## PART 12: ESTIMATED EFFORT

### Revised Time Estimate

| Phase | Tasks | Hours | Timeline |
|-------|-------|-------|----------|
| **Phase 1: Foundation** | Setup, DB, ZIP lookup | 10-12 hours | Week 1 |
| **Phase 2: Core Features** | Profile, votes, contact | 12-15 hours | Week 2 |
| **Phase 3: Enhancement** | Scripts, analytics, polish | 10-12 hours | Week 3 |
| **Phase 4: Deployment** | Deploy, test, document | 8-10 hours | Week 4 |
| **Phase 5: (Optional) Scale** | National expansion | 5-8 hours | Week 5-6 |

**Total MVP (Phases 1-4):** 40-49 hours (4-6 weeks part-time)
**Total with National Scale:** 45-57 hours (5-7 weeks part-time)

### Complexity Comparison
- **Original Plan:** Lower complexity, lower value
- **Improved Plan:** Higher complexity, significantly higher value
- **Feasibility:** Still achievable for academic project
- **Additional effort:** +15-20 hours (+50%) for 300% increase in value/differentiation

---

## PART 13: CONCLUSION & RECOMMENDATION

### Why This Improved Version is Better

**Original Plan:**
- ✅ Technically feasible
- ✅ Clear scope
- ❌ Low differentiation
- ❌ Limited academic value
- ❌ Critical usability flaw (no ZIP lookup)
- ❌ No measurement of impact

**Improved Plan:**
- ✅ Still feasible (4-6 weeks)
- ✅ Still $0 cost
- ✅ **High differentiation** (targets specific niche)
- ✅ **Strong academic value** (measurable impact)
- ✅ **Solves critical usability flaw** (ZIP lookup)
- ✅ **Built-in impact measurement**
- ✅ **Scales to national platform**
- ✅ **Portfolio-worthy** (demonstrates advanced thinking)

### Academic Value Comparison

| Aspect | Original | Improved |
|--------|----------|----------|
| Technical demonstration | ✅ | ✅ |
| Problem identification | ⚠️ | ✅ |
| User research | ❌ | ✅ |
| Impact measurement | ❌ | ✅ |
| Comparative analysis | ❌ | ✅ |
| Scalability | ❌ | ✅ |
| Publication potential | ⚠️ | ✅ |

### Final Recommendation

**Proceed with the IMPROVED plan** because:

1. **Solves real problems** instead of duplicating existing tools
2. **Measurable impact** for academic rigor
3. **Differentiated** from competitors
4. **Scalable** beyond class project
5. **Still achievable** in academic timeline
6. **Portfolio-quality** work for future opportunities

**The additional 15-20 hours of work transforms this from:**
- "A class project" → "A civic technology contribution"
- "Directory app" → "Engagement platform"
- "Florida tool" → "National platform (starting with Florida)"

### Next Steps

1. **Review this proposal** with advisor/professor
2. **Validate assumptions** with 3-5 target users (quick interviews)
3. **Set up development environment** (Week 1)
4. **Build ZIP lookup first** (prove feasibility of critical feature)
5. **Iterate based on feedback**

---

## APPENDIX A: Quick Start Implementation Guide

### Day 1: Project Setup
```bash
# Create project structure
mkdir congress_connect
cd congress_connect
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install streamlit pandas requests sqlite3 pytest

# Create folder structure
mkdir -p app data utils tests docs deployment
```

### Day 1: Google Civic API Test
```python
# test_zip_lookup.py
import requests

API_KEY = "your_google_api_key_here"

def test_zip_lookup():
    zip_code = "33139"
    url = "https://www.googleapis.com/civicinfo/v2/representatives"
    params = {
        "address": zip_code,
        "key": API_KEY,
        "levels": "country",
        "roles": ["legislatorLowerBody", "legislatorUpperBody"]
    }
    response = requests.get(url, params=params)
    print(response.json())

test_zip_lookup()
```

**If this works, you've validated the most critical technical risk.**

### Day 2: Database Setup
```python
# utils/db_setup.py
import sqlite3
import pandas as pd

def create_database():
    conn = sqlite3.connect('data/congress.db')
    cursor = conn.cursor()

    # Create representatives table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS representatives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bioguide_id TEXT UNIQUE,
            first_name TEXT,
            last_name TEXT,
            office TEXT,
            state TEXT,
            district TEXT,
            party TEXT,
            dc_phone TEXT,
            website TEXT,
            contact_form TEXT,
            facebook TEXT,
            twitter TEXT,
            instagram TEXT,
            tiktok TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def import_csv_data():
    df = pd.read_csv('../FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv')
    conn = sqlite3.connect('data/congress.db')

    # Transform and load data
    # (Implementation details...)

    conn.close()

if __name__ == "__main__":
    create_database()
    import_csv_data()
    print("Database created and data imported successfully!")
```

### Day 3: Minimal Viable Search
```python
# app.py
import streamlit as st
from utils.search import lookup_by_zip
from utils.db_manager import get_representative

st.title("🏛️ Congress Connect")
st.subheader("Find Your Representative")

zip_code = st.text_input("Enter your ZIP code:")

if st.button("Find My Rep"):
    if len(zip_code) == 5 and zip_code.isdigit():
        district = lookup_by_zip(zip_code)
        rep = get_representative(district)

        if rep:
            st.success(f"Your representative: {rep['first_name']} {rep['last_name']}")
            st.write(f"📞 {rep['dc_phone']}")
            st.write(f"🌐 {rep['website']}")
        else:
            st.error("Representative not found")
    else:
        st.error("Please enter a valid 5-digit ZIP code")
```

**If you can get to this point by Day 3, the project is feasible.**

---

## APPENDIX B: API Setup Guides

### Google Civic Information API
1. Go to https://console.cloud.google.com/
2. Create new project: "congress-connect"
3. Enable "Google Civic Information API"
4. Create credentials (API key)
5. Restrict API key to Civic Information API only
6. Store in environment variable or Streamlit secrets

### ProPublica Congress API
1. Go to https://www.propublica.org/datastore/api/propublica-congress-api
2. Request API key (free, instant approval)
3. Store in environment variable

### Streamlit Secrets (for deployment)
```toml
# .streamlit/secrets.toml
GOOGLE_CIVIC_API_KEY = "your_key_here"
PROPUBLICA_API_KEY = "your_key_here"
```

---

**Document Status:** COMPLETE
**Next Action:** User decision - Proceed with improved plan or iterate further
**Last Updated:** 2025-10-28
