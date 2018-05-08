# veckostatistik

## Tools
- Python
- SQLLite
- SQLAlchemy
- Flask
- Visual Studio Code
- Tweepy
- StravaLib

Analysis of Non-Moving Time on Commutes (and comparison with non-commutes)
- For each week, get all activities 
- Flag as Commute (tagged as commutes via commutemarker.com) or Non-Commute
- For each ride that week get:
  - Start time
  - Elapsed Time
  - Moving Time
  - % Non-Moving Time ((elapsed-moving)/elapsed)
