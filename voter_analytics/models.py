# File: models.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/15/2025  
# Description: Defines the Voter model for the Voter app


from django.db import models

import csv
from datetime import datetime

# Create your models here.

class Voter(models.Model):
    """Represents a registered voter in Newton, MA."""

    # Identity & Address
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True, null=True)
    zip_code = models.TextField()

    # Meta
    date_of_birth = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)

    # Election participation
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # Score
    voter_score = models.IntegerField()

    def __str__(self):
        """Return a string representation of the voter."""

        return f'{self.first_name} {self.last_name} ({self.street_number} {self.street_name})'



def load_data():
    """Load voters from CSV file into the database."""
    
    # Clear existing records
    Voter.objects.all().delete()

    filename = '/Users/Veer/Desktop/Summer/CS412/django/newton_voters.csv'
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                voter = Voter(
                    first_name=row['First Name'].strip(),
                    last_name=row['Last Name'].strip(),
                    street_number=row['Residential Address - Street Number'].strip(),
                    street_name=row['Residential Address - Street Name'].strip(),
                    apartment_number=row['Residential Address - Apartment Number'].strip() or None,
                    zip_code=row['Residential Address - Zip Code'].strip(),
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                    registration_date=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'].strip(),

                    v20state=row['v20state'].strip().lower() == 'true',
                    v21town=row['v21town'].strip().lower() == 'true',
                    v21primary=row['v21primary'].strip().lower() == 'true',
                    v22general=row['v22general'].strip().lower() == 'true',
                    v23town=row['v23town'].strip().lower() == 'true',
                    voter_score=int(row['voter_score']),
                )
                voter.save()
                print(f'Created: {voter}')
            except Exception as e:
                print(f"Skipped row due to error: {e}")
    
    print(f'Imported {Voter.objects.count()} voters.')