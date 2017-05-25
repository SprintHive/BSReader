import fitz
import re

class StandardBankStatementReader:

    def get_account_summary(self, pdf_name, pdf_contents):
        doc = fitz.Document(pdf_name, pdf_contents)
        text=[]
        npages=len(doc)
        for ipage in range(npages):
            this_page=doc[ipage].getText(output = 'text').split('\n')
            text.extend(this_page)

        # Remove blank elements
        text=list(filter(None,text))

        address=[]
        for it,t in enumerate(text[:20]):
            if it == 15:
                name=t
            if 16 <= it <= 18:
                address.append(t)
            else:
                pass

        print(name)
        print(address)

        acct_num=re.compile(r'(?<=Account\sNumber)[\d\ ]+')
        for n,idd in enumerate(text):
            if acct_num.search(idd):
                acct_number=acct_num.search(idd).group(0)
                break

        print(acct_number)

        yy=re.compile(r'[\d\,\.]+(?=\d{2}\s\d{2})') # semi-valid date
        nn=re.compile(r'[1-9][0-9\.]+\,\d{2}\-{,1}(?=\d{2}\s\d{2})') # numeric,dot,comma,minus only
        total_in=0.0
        for it,t in enumerate(text):
            if nn.search(t) and yy.search(t):
                    inflow=yy.search(t).group(0)
                    zz=inflow.replace('.','')
                    inflow=zz.replace(',','.')
                    total_in+=float(inflow)

        print(total_in)

        print('==== SUMMARY ============')

        print(name)
        for a in address:
            print(a)
        print('A/C %s'%acct_number)
        print('Total inflow: R%10.2f'%total_in)
        print('Should be     R  33115.89')
        print('=========================')
        return {
            "address": address,
            "total_income": total_in
        }
