# Congress Connect

Find and contact your federal representatives - completely free, no signup required, privacy-first.

## Features

- 🔍 **ZIP Code Lookup** - Find your representative instantly
- 💰 **Funding Transparency** - See AIPAC and defense industry funding
- 📱 **Mobile-Friendly** - Works perfectly on any device
- 💬 **Call Scripts** - Get help with what to say
- 🔒 **Privacy-First** - No email, no account, no tracking

## Quick Start

### Run Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database:
```bash
python utils/database.py
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open your browser to http://localhost:8501

### Deploy to Streamlit Cloud (Free)

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select `app.py` as the main file
5. Deploy!

Your app will be live at: `https://[your-app-name].streamlit.app`

## Project Structure

```
congress_liberation/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── data/
│   ├── FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv
│   └── congress.db                 # SQLite database (created on first run)
├── utils/
│   ├── database.py                 # Database operations
│   ├── api_clients.py              # External API clients
│   └── search.py                   # Search logic
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── docs/                           # Project documentation
```

## Data Updates

To update campaign funding information:

1. Open `data/FLORIDA_FEDERAL_OFFICIALS_COMPLETE.csv`
2. Update the `AIPAC_Funded` and `War_Industrial_Complex_Funded` columns
   - Use "No", "Yes", or specific amounts like "$150,000"
3. Re-run database initialization:
```bash
python utils/database.py
```

## Technical Stack

- **Framework:** Streamlit
- **Database:** SQLite
- **APIs:** Google Civic Information API (optional), ProPublica Congress API (optional)
- **Deployment:** Streamlit Community Cloud (free)
- **Cost:** $0

## Privacy Policy

We collect **zero personal information**:
- ❌ No email addresses
- ❌ No account creation
- ❌ No tracking cookies
- ❌ No personal data storage

Your searches are not stored. Your privacy matters.

## License

Open source - built for educational purposes and civic engagement.

## Contributing

To expand this project to other states:

1. Add state data to CSV (or create separate CSV files per state)
2. Update database schema to handle multiple states
3. Modify search logic to support state selection
4. The architecture is already designed for national scale!

## Support

This is an academic project. For questions or issues, please refer to the documentation in the `docs/` folder.

---

**Version:** 1.0 MVP
**Last Updated:** October 2025
**Built with ❤️ for civic engagement**
