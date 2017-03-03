import json

class Party_bills(object):
    def __init__(self, party_id, bills = []):
        self.party_id = party_id
        self.bills = bills

    def creat_party_bills_file(self):
        json.dump(self.bills,open('parties_bills/' + self.party_id + '.txt','w'))
    
    def edit_party_bills(self, bill_record, edit):
        if edit == 'add':
            self.bills.append(bill_record)
        elif edit == 'del':
            self.bills.remove(bill_record)
        json.dump(self.bills,open('parties_bills/' + self.party_id + '.txt','w'))
