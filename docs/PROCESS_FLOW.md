# Congress Connect - Process Flow Documentation

This document provides visual representations of the application's architecture, data flows, and user interactions.

---

## 1. User Journey Flow

```mermaid
graph TD
    A[User Visits App] --> B{Choose Action}
    B -->|Find My Rep| C[ZIP Code Search]
    B -->|Browse All| D[Browse Representatives]
    B -->|Learn More| E[About Page]

    C --> F[Enter ZIP Code]
    F --> G{Valid ZIP?}
    G -->|Yes| H[Display House Rep + Senators]
    G -->|No| I[Error Message]
    G -->|Fallback| J[Manual District Selection]

    H --> K[View Representative Profile]
    K --> L[Access Multiple Features]

    L --> M[View Funding Info]
    L --> N[Contact Information]
    L --> O[Social Media Links]
    L --> P[Generate Call Script]
    L --> Q[View Election Info]

    D --> R[Apply Filters]
    R --> S[View Data Table]
    S --> T[Select Representative]
    T --> K

    E --> U[Read About Project]
    U --> V[Privacy Policy]

    style A fill:#e1f5ff
    style K fill:#fff4e1
    style M fill:#ffe1e1
    style P fill:#e1ffe1
```

---

## 2. Technical Architecture Flow

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Streamlit Frontend]
        CSS[Custom CSS Styling]
    end

    subgraph "Application Layer"
        MAIN[app.py - Main Application]
        SEARCH[utils/search.py - Search Logic]
        DB[utils/database.py - Database Operations]
        API[utils/api_clients.py - API Clients]
    end

    subgraph "Data Layer"
        SQLITE[(SQLite Database)]
        CSV[CSV Data Files]
    end

    subgraph "External Services - Future"
        GOOGLE[Google Civic API]
        PROPUB[ProPublica API]
    end

    UI --> MAIN
    CSS --> UI
    MAIN --> SEARCH
    MAIN --> DB
    MAIN --> API

    SEARCH --> DB
    DB --> SQLITE
    DB --> CSV

    API -.->|Future| GOOGLE
    API -.->|Future| PROPUB

    style SQLITE fill:#4CAF50
    style CSV fill:#8BC34A
    style GOOGLE fill:#FFC107
    style PROPUB fill:#FFC107
```

---

## 3. Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Data Sources"
        FEC[FEC Campaign Data]
        HOUSE[House.gov Directory]
        SENATE[Senate.gov Directory]
    end

    subgraph "Data Processing"
        CSV1[FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv]
        UPDATE[update_funding_data.py]
        ELECTION[add_election_columns.py]
    end

    subgraph "Storage"
        DB[(congress.db<br/>SQLite Database)]
    end

    subgraph "Application"
        APP[Streamlit App]
        USER[End User]
    end

    FEC -->|Manual Import| UPDATE
    HOUSE -->|Manual Entry| CSV1
    SENATE -->|Manual Entry| CSV1

    CSV1 --> DB
    UPDATE --> CSV1
    ELECTION --> CSV1

    DB --> APP
    APP --> USER

    style FEC fill:#ff9800
    style DB fill:#4CAF50
    style APP fill:#2196F3
    style USER fill:#9C27B0
```

---

## 4. ZIP Code Search Process

```mermaid
flowchart TD
    START[User Enters ZIP Code] --> VALIDATE{Valid ZIP?<br/>5 digits}

    VALIDATE -->|No| ERROR1[Display Error:<br/>Invalid ZIP format]
    VALIDATE -->|Yes| LOOKUP[Lookup in ZIP-District Map]

    LOOKUP --> CHECK{District Found?}

    CHECK -->|No| ERROR2[Display Error:<br/>ZIP not found<br/>Show Manual Selection]
    CHECK -->|Yes| QUERY[Query Database]

    QUERY --> GET_HOUSE[Get House Rep<br/>for District]
    QUERY --> GET_SENATE[Get Both Senators<br/>Statewide]

    GET_HOUSE --> DISPLAY[Display Results]
    GET_SENATE --> DISPLAY

    DISPLAY --> SHOW_HOUSE[Show House Representative]
    DISPLAY --> SHOW_SENATE[Show 2 Senators]

    SHOW_HOUSE --> PROFILE1[Display Full Profile]
    SHOW_SENATE --> PROFILE2[Display Full Profiles]

    PROFILE1 --> END[User Can Interact]
    PROFILE2 --> END

    ERROR2 --> MANUAL[Manual District<br/>Selection Dropdown]
    MANUAL --> DIRECT_QUERY[Direct Database Query]
    DIRECT_QUERY --> PROFILE1

    style START fill:#e3f2fd
    style ERROR1 fill:#ffebee
    style ERROR2 fill:#ffebee
    style END fill:#e8f5e9
```

---

## 5. Database Query Flow

```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant Search
    participant Database
    participant SQLite

    User->>Streamlit: Enter ZIP Code
    Streamlit->>Search: search_by_zip(zip_code, db)

    Search->>Search: Validate ZIP format
    Search->>Search: Lookup district mapping

    alt District Found
        Search->>Database: get_representative_by_district(district)
        Database->>SQLite: SELECT * WHERE district = ?
        SQLite-->>Database: House Rep Record
        Database-->>Search: Representative Data

        Search->>Database: get_senators()
        Database->>SQLite: SELECT * WHERE office = 'U.S. Senate'
        SQLite-->>Database: 2 Senator Records
        Database-->>Search: Senators Data

        Search-->>Streamlit: Success + All Reps
        Streamlit-->>User: Display 3 Representatives
    else District Not Found
        Search-->>Streamlit: Error Message
        Streamlit-->>User: Show Manual Selection
        User->>Streamlit: Select District Manually
        Streamlit->>Search: search_by_district(district)
        Search->>Database: get_representative_by_district(district)
        Database->>SQLite: SELECT * WHERE district = ?
        SQLite-->>Database: Rep Record
        Database-->>Search: Representative Data
        Search-->>Streamlit: Success + Rep
        Streamlit-->>User: Display Representative
    end
```

---

## 6. Representative Profile Display Flow

```mermaid
flowchart TD
    START[Representative Selected] --> LOAD[Load Representative Data]

    LOAD --> BASIC[Display Basic Info]
    BASIC --> NAME[Name + Photo Placeholder]
    BASIC --> PARTY[Party Badge<br/>Red: Republican<br/>Blue: Democrat]
    BASIC --> OFFICE[Office + District]
    BASIC --> REGION[Geographic Region]

    LOAD --> ELECTION[Display Election Info]
    ELECTION --> TERM[Current Term End Date]
    ELECTION --> PRIMARY[Next Primary Date]
    ELECTION --> GENERAL[Next General Election<br/>Highlighted if 2026]

    LOAD --> FUNDING[Display Funding Transparency]
    FUNDING --> AIPAC{AIPAC Funded?}
    AIPAC -->|Yes| AIPAC_RED[Red Badge + Amount]
    AIPAC -->|No| AIPAC_GREEN[Green Badge: No]

    FUNDING --> WAR{War Industry Funded?}
    WAR -->|Yes| WAR_RED[Red Badge + Amount]
    WAR -->|No| WAR_GREEN[Green Badge: No]

    LOAD --> CONTACT[Display Contact Methods]
    CONTACT --> PHONE[Phone Number Button]
    CONTACT --> WEBSITE[Official Website Link]
    CONTACT --> FORM[Contact Form Link]
    CONTACT --> EMAIL[Email Link if available]
    CONTACT --> ADDRESS[DC Office Address]

    LOAD --> SOCIAL[Display Social Media]
    SOCIAL --> FACEBOOK[Facebook Link]
    SOCIAL --> TWITTER[Twitter/X Link]
    SOCIAL --> INSTAGRAM[Instagram Link]
    SOCIAL --> TIKTOK[TikTok Link]

    LOAD --> TOOLS[Action Tools]
    TOOLS --> SCRIPT[Call Script Generator]
    SCRIPT --> TOPIC[Select Topic]
    TOPIC --> GENERATE[Generate Custom Script]
    GENERATE --> COPY[Copy/Use Script]

    style START fill:#e3f2fd
    style AIPAC_RED fill:#ffebee
    style AIPAC_GREEN fill:#e8f5e9
    style WAR_RED fill:#ffebee
    style WAR_GREEN fill:#e8f5e9
    style GENERATE fill:#fff3e0
```

---

## 7. Browse & Filter Flow

```mermaid
flowchart TD
    START[User Selects Browse Tab] --> LOAD[Load All Representatives<br/>30 Florida Officials]

    LOAD --> FILTERS[Display Filter Options]

    FILTERS --> F1[Office Filter<br/>All/Senate/House]
    FILTERS --> F2[Party Filter<br/>All/Republican/Democrat]
    FILTERS --> F3[AIPAC Filter<br/>All/Yes/No]
    FILTERS --> F4[War Industry Filter<br/>All/Yes/No]

    F1 --> APPLY[Apply Filters]
    F2 --> APPLY
    F3 --> APPLY
    F4 --> APPLY

    APPLY --> FILTER_LOGIC{Filter Logic}

    FILTER_LOGIC --> OFFICE{Office Filter?}
    OFFICE -->|All| SKIP1[Skip]
    OFFICE -->|Specific| FILTER1[Filter by Office]

    FILTER_LOGIC --> PARTY{Party Filter?}
    PARTY -->|All| SKIP2[Skip]
    PARTY -->|Specific| FILTER2[Filter by Party]

    FILTER_LOGIC --> AIPAC{AIPAC Filter?}
    AIPAC -->|All| SKIP3[Skip]
    AIPAC -->|Yes| FILTER3[Show AIPAC Funded]
    AIPAC -->|No| FILTER4[Show NOT AIPAC Funded]

    FILTER_LOGIC --> WAR{War Industry Filter?}
    WAR -->|All| SKIP4[Skip]
    WAR -->|Yes| FILTER5[Show War Industry Funded]
    WAR -->|No| FILTER6[Show NOT War Industry Funded]

    SKIP1 --> RESULT[Filtered Results]
    SKIP2 --> RESULT
    SKIP3 --> RESULT
    SKIP4 --> RESULT
    FILTER1 --> RESULT
    FILTER2 --> RESULT
    FILTER3 --> RESULT
    FILTER4 --> RESULT
    FILTER5 --> RESULT
    FILTER6 --> RESULT

    RESULT --> TABLE[Display Data Table]
    TABLE --> COUNT[Show Count:<br/>X representatives]

    TABLE --> SELECT[User Selects Representative]
    SELECT --> DETAIL[Display Full Profile]

    style START fill:#e3f2fd
    style RESULT fill:#fff3e0
    style DETAIL fill:#e8f5e9
```

---

## 8. Call Script Generator Flow

```mermaid
flowchart LR
    START[User Expands<br/>Call Script Section] --> SELECT[Select Topic]

    SELECT --> TOPICS{Topic Options}

    TOPICS -->|1| T1[Healthcare]
    TOPICS -->|2| T2[Education]
    TOPICS -->|3| T3[Climate Change]
    TOPICS -->|4| T4[Immigration]
    TOPICS -->|5| T5[Economy/Jobs]
    TOPICS -->|6| T6[Gun Policy]
    TOPICS -->|7| T7[Other]

    T1 --> GENERATE[Generate Script]
    T2 --> GENERATE
    T3 --> GENERATE
    T4 --> GENERATE
    T5 --> GENERATE
    T6 --> GENERATE
    T7 --> GENERATE

    GENERATE --> BUILD[Build Custom Script]

    BUILD --> GREETING[Greeting Template]
    BUILD --> TOPIC_REF[Topic Reference]
    BUILD --> PLACEHOLDER[Personalization Placeholders]
    BUILD --> REQUEST[Request Template]
    BUILD --> TIPS[Effectiveness Tips]

    GREETING --> DISPLAY[Display Script in Text Area]
    TOPIC_REF --> DISPLAY
    PLACEHOLDER --> DISPLAY
    REQUEST --> DISPLAY
    TIPS --> DISPLAY

    DISPLAY --> USER_ACTION{User Action}
    USER_ACTION -->|Copy| COPY[User Copies Script]
    USER_ACTION -->|Customize| EDIT[User Edits Script]
    USER_ACTION -->|Use| CALL[User Makes Call]

    style START fill:#e3f2fd
    style GENERATE fill:#fff3e0
    style DISPLAY fill:#e8f5e9
    style CALL fill:#c8e6c9
```

---

## 9. Data Update Pipeline

```mermaid
flowchart TB
    subgraph "External Data Sources"
        FEC[Federal Election Commission<br/>FEC.gov]
        HOUSE_DIR[House.gov<br/>Official Directory]
        SENATE_DIR[Senate.gov<br/>Official Directory]
    end

    subgraph "Manual Data Collection"
        EXPORT[Export FEC Data<br/>CSV Format]
        SCRAPE[Collect Contact Info<br/>Manual Entry]
    end

    subgraph "Data Processing Scripts"
        UPDATE_FUND[update_funding_data.py]
        UPDATE_ELECT[add_election_columns.py]
    end

    subgraph "Data Storage"
        CSV_FILE[FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv]
        DATABASE[(congress.db)]
    end

    subgraph "Validation"
        VERIFY[Verify Data Integrity]
        COUNT[Count Records]
        CHECK[Check for Duplicates]
    end

    subgraph "Deployment"
        GIT[Git Commit]
        GITHUB[Push to GitHub]
        STREAMLIT[Auto-Deploy Streamlit Cloud]
    end

    FEC --> EXPORT
    HOUSE_DIR --> SCRAPE
    SENATE_DIR --> SCRAPE

    EXPORT --> UPDATE_FUND
    SCRAPE --> CSV_FILE

    UPDATE_FUND --> CSV_FILE
    UPDATE_ELECT --> CSV_FILE

    CSV_FILE --> DATABASE

    DATABASE --> VERIFY
    VERIFY --> COUNT
    COUNT --> CHECK

    CHECK --> GIT
    GIT --> GITHUB
    GITHUB --> STREAMLIT

    style FEC fill:#ff9800
    style DATABASE fill:#4CAF50
    style STREAMLIT fill:#2196F3
    style VERIFY fill:#9C27B0
```

---

## 10. Privacy-First Architecture

```mermaid
flowchart LR
    subgraph "User Side"
        BROWSER[User Browser]
        NO_COOKIES[No Cookies Set]
        NO_TRACK[No Tracking Scripts]
        NO_LOGIN[No Login Required]
    end

    subgraph "Application Layer"
        STREAMLIT_APP[Streamlit Application]
        NO_ANALYTICS[No Personal Analytics]
        NO_STORAGE[No User Data Storage]
        NO_LOGS[No Search Logging]
    end

    subgraph "Data Layer"
        DB[(Public Data Only)]
        NO_USER_DATA[No User Information]
        OFFICIAL_DATA[Official Government Data]
        FEC_DATA[Public FEC Data]
    end

    BROWSER --> NO_COOKIES
    BROWSER --> NO_TRACK
    BROWSER --> NO_LOGIN

    BROWSER --> STREAMLIT_APP

    STREAMLIT_APP --> NO_ANALYTICS
    STREAMLIT_APP --> NO_STORAGE
    STREAMLIT_APP --> NO_LOGS

    STREAMLIT_APP --> DB

    DB --> NO_USER_DATA
    DB --> OFFICIAL_DATA
    DB --> FEC_DATA

    style BROWSER fill:#e3f2fd
    style NO_COOKIES fill:#e8f5e9
    style NO_TRACK fill:#e8f5e9
    style NO_LOGIN fill:#e8f5e9
    style NO_ANALYTICS fill:#e8f5e9
    style NO_STORAGE fill:#e8f5e9
    style NO_LOGS fill:#e8f5e9
    style NO_USER_DATA fill:#e8f5e9
```

---

## Key Features Summary

### User-Facing Features
1. **ZIP Code Lookup** - Instant representative search
2. **Browse & Filter** - Explore all 30 Florida officials
3. **Funding Transparency** - AIPAC and War Industry funding data
4. **Election Information** - 2026 election dates and term limits
5. **Contact Methods** - Phone, email, web forms, social media
6. **Call Script Generator** - Customizable call scripts for civic engagement
7. **Mobile Responsive** - Works on all devices

### Technical Features
1. **Privacy-First** - Zero personal data collection
2. **Fast Performance** - SQLite database with indexed queries
3. **Offline Capable** - Static data, no external API dependencies (currently)
4. **Free Hosting** - Streamlit Community Cloud
5. **Open Source** - GitHub repository
6. **Easy Updates** - CSV-based data management

### Data Features
1. **30 Representatives** - 2 Senators + 28 House Members
2. **25 with Funding Data** - Real FEC 2023-2024 campaign data
3. **Election Dates** - 2026 primary and general elections
4. **Contact Information** - Phone, email, websites, social media
5. **Geographic Coverage** - All Florida districts

---

## Performance Metrics

```mermaid
graph LR
    A[Page Load Time] -->|< 2 seconds| B[Excellent]
    C[Database Query] -->|< 100ms| D[Fast]
    E[ZIP Lookup] -->|< 50ms| F[Instant]
    G[Filter Application] -->|< 200ms| H[Responsive]

    style B fill:#4CAF50
    style D fill:#4CAF50
    style F fill:#4CAF50
    style H fill:#4CAF50
```

---

## Deployment Flow

```mermaid
flowchart TD
    DEV[Local Development] --> TEST[Local Testing<br/>streamlit run app.py]
    TEST --> GIT[Git Add + Commit]
    GIT --> PUSH[Push to GitHub]
    PUSH --> STREAMLIT[Streamlit Cloud<br/>Auto-Detect Changes]
    STREAMLIT --> BUILD[Build Application]
    BUILD --> DEPLOY[Deploy to Production]
    DEPLOY --> LIVE[Live at congressliberation.streamlit.app]

    LIVE --> MONITOR{Monitor}
    MONITOR -->|Error| FIX[Fix in Local Dev]
    MONITOR -->|Success| MAINTAIN[Maintain]

    FIX --> DEV

    style DEV fill:#e3f2fd
    style LIVE fill:#4CAF50
    style FIX fill:#ffebee
```

---

## Future Enhancements (Planned)

```mermaid
mindmap
  root((Future Features))
    API Integration
      Google Civic Info API
      ProPublica Congress API
      Voting Records
      Bill Tracking
    Data Expansion
      All 50 States
      State Legislators
      Local Officials
      Real-time Updates
    User Features
      Email Alerts
      Bill Notifications
      Town Hall Calendar
      Donation Tracking
    Analytics
      Aggregate Usage Stats
      Popular Topics
      Contact Effectiveness
      Privacy-Preserving Metrics
```

---

**Document Version:** 1.0
**Last Updated:** October 29, 2025
**Application Version:** Production MVP
**Live URL:** https://congressliberation.streamlit.app
