from django.db import models

class Voter(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    residential_street_number = models.CharField(max_length=10)
    residential_street_name = models.CharField(max_length=100)
    residential_apartment_number = models.CharField(max_length=10, blank=True, null=True)
    residential_zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=5)
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"

    @staticmethod
    def load_data(file_path):
        import csv
        from datetime import datetime
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            voters = []
            for row in reader:
                voter = Voter(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    residential_street_number=row['Residential Address - Street Number'],
                    residential_street_name=row['Residential Address - Street Name'],
                    residential_apartment_number=row.get('Residential Address - Apartment Number', None),
                    residential_zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d'),
                    date_of_registration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d'),
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=row['v20state'].upper() == 'TRUE',
                    v21town=row['v21town'].upper() == 'TRUE',
                    v21primary=row['v21primary'].upper() == 'TRUE',
                    v22general=row['v22general'].upper() == 'TRUE',
                    v23town=row['v23town'].upper() == 'TRUE',
                    voter_score=int(row['voter_score'])
                )
                voters.append(voter)
            Voter.objects.bulk_create(voters)
