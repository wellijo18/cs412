from django.db import models

class Voter(models.Model):
    '''
    Store/represent a registered voter.
    name, adress, etc
    '''
    # name
    da_last_name = models.TextField()
    da_first_name = models.TextField()

    # address
    da_street_number = models.TextField()
    da_street_name = models.TextField()
    da_apt_number = models.TextField(blank=True)
    da_zip_code = models.TextField()
    # info
    da_dob = models.DateField()
    da_date_registered = models.DateField()
    da_party = models.CharField(max_length=2)
    da_precinct = models.TextField()

    # election participation
    da_v20state = models.BooleanField(default=False)
    da_v21town = models.BooleanField(default=False)
    da_v21primary = models.BooleanField(default=False)
    da_v22general = models.BooleanField(default=False)
    da_v23town = models.BooleanField(default=False)

    da_voter_score = models.IntegerField()

    def __str__(self): 
        return f'The person is {self.da_first_name} {self.da_last_name} from ({self.da_zip_code}) with a party of: {self.da_party} and score of: {self.da_voter_score}'
    def get_elections_participated(self):
        '''Return list of elections this voter participated in.'''
        elections = []
        if self.da_v20state: elections.append('v20state')
        if self.da_v21town: elections.append('v21town')
        if self.da_v21primary: elections.append('v21primary')
        if self.da_v22general: elections.append('v22general')
        if self.da_v23town: elections.append('v23town')
        return elections

def load_data():
    '''for loading data records from CSV file to Django'''

    # delete existing records:
    Voter.objects.all().delete()
    filename = '/Users/wellingtono/Desktop/examples/newton_voters.csv'
    f = open(filename)
    f.readline() 

    for line in f:
        fields = line.split(',')

        try:
            # new instance of voter
            voter = Voter(
                da_last_name = fields[1],
                da_first_name = fields[2],

                da_street_number = fields[3],
                da_street_name = fields[4],
                da_apt_number = fields[5],
                da_zip_code = fields[6],

                da_dob = fields[7],
                da_date_registered = fields[8],
                da_party = fields[9].strip(),
                da_precinct = fields[10],
                da_v20state = fields[11].strip() == 'TRUE',
                da_v21town = fields[12].strip() == 'TRUE',
                da_v21primary = fields[13].strip() == 'TRUE',
                da_v22general = fields[14].strip() == 'TRUE',
                da_v23town = fields[15].strip() == 'TRUE',

                da_voter_score = fields[16].strip(),
            )

            voter.save() # save to database
            print(f'Created voter: {voter}')

        except:
            print(f"Skipped: {fields}")

    print(f'Done. Created {len(Voter.objects.all())} Voters.')