[![Build Status](https://travis-ci.com/uva-slp/georgias.svg?token=ZV3LB7kBeSnciH5XtvyA&branch=master)](https://travis-ci.com/uva-slp/georgias)
# SLP Requirements Document(Updated) - Georgia's Healing House Sys
Development: Django Framework

## Requirements (minimum):
I.	Create Applicant

II.	Create Interview

III.	Accept or Deny (with reason)

IV.	Resident Intake

    a.	Date of arrival (date box)
    b.	Mentor Assigned (text box)
V.	Monthly Reports (individual resident reports)

    a.	# of AA/NA meetings attended
    b.	# of house meetings attended
    c.	Employment status
            i.	Unemployed
            ii.	Part time
            iii.	Fulltime
            iv.	Disabled
    d.	Employer name (text box)
    e.	Any critical incidents (yes/no)
    f.	Community programs utilized (text box)
VI.	Critical Incidents

    a.	Incident Information
          i.	Types
              1.	Drinking or drug use
              2.	AWOL
              3.	Altercation
              4.	Injury
              5.	Theft
              6.	Violation of House Rule
          ii.	Explanation (text)
      b.	Date
      c.	Time
VII.	Discharge (differentiate termination between each stage)

      a.	Date
      b.	Successful/unsuccessful
            i.	If unsuccessful, reason 
                1.	(drop down)
                    a.	Quit program
                    b.	Terminated for substance use
                    c.	Arrested
                    d.	Violation of house rules
                2.	Explanation
      c.	Details (text box)
      d.	Community Plan
            i.	Resident address
            ii.	Who the resident will live with


## Requirements (desired):
*	Report and statistic generation
*	Financial tracking
*	Nice UI that is understandable by non-technical people 
*	Full export to CSV and data backup (waiting for their data)
*	Custom fields
