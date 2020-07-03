Very minor changes from https://github.com/hkustliqi/USCISTracker to run case updates in 2020
I'm not a coder, my stuff is not elegant.

# USCISTracker
Wondering how fast USCIS is processing your application (Green Card, H1B, OPT, etc.)? This python script issues queries to [USCIS check my status webpage] 
(https://egov.uscis.gov/casestatus/landing.do) to give you statistics of applications that was received on dates that you specify.

# Usage
The current version checks a range of neighboring receipt numbers around your application. The script is simply invoked by running
A re-run of the script does not check cases again which are not the right form (I-485 by default) and does not update finally adjudicated cases (approved or rejected)
This will keep your requests to USCIS to a minimum.

```python
python ./USCISTracker.py
```
Sample output

```
*********************************
For 5000 neighbors of LIN1690654088, we found the following statistics: 
total number of I-485 application received:  337  
Case Was Approved:                           27   
Fingerprint Fee Was Received:                150  
Case Was Rejected:                           14   
Case Was Received:                           91   
Case Was Ready for Interview:                7    
Case is RFE:                                 32   
Case Was Transferred:                        3    
Name Was Updated:                            13  

```


Modify the following parameters in the script to tailor to your needs.

**mySC**: Service Center code (MSC = National Benefits Center etc.)

**mycaseNum**: Your Application Number

**numRange**: number of neighboring receipts to check

**expandOnly**: change to 1 if expanding range (does not check updates on known cases); change to 0 to update known cases


# Disclaimer
The author claims no legal responsibility for misuage of this script. User is advised to not spam USCIS website by setting **numRange** small.
