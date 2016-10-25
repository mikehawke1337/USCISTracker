# USCISTracker
Wondering how fast USCIS is processing your application (Green Card, H1B, OPT, etc.)? This python script issues queries to [USCIS check my status webpage] 
(https://egov.uscis.gov/casestatus/landing.do) to give you statistics of applications that was received on dates that you specify.

# Usage
The current version checks a range of neighboring receipt numbers around your application. The script is simply invoked by running

```python
python ./USCISTracker.py
```
Sample output

```
*********************************
For Form I-485 received by USCIS on May 12, we found the following statistics: 
total number of I-485 application received: 17
Case Was Approved: 0
Fingerprint Fee Was Received 17
Case Was Rejected 0

```


Modify the following parameters in the script to tailor to your needs.

**date**: Application receipt date

**mycaseNum**: Your Application Number

**numRange**: number of neighboring receipts to check


# Disclaimer
The author claims no legal responsibility for misuage of this script. User is advised to not spam USCIS website by setting **numRange** small.
