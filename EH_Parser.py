from email.parser import BytesParser
from email.policy import default
import re
from prettytable import PrettyTable,ALL
from email import utils
from dateutil import tz
from datetime import *
from email.utils import *

#list to store header values
sender_host_list=[]
receiver_host_list=[]
protocol_used_list=[]
no_of_hops_list=[]
final_timestamp_list=[]
time_difference_list = []

#list to parse summary
summary_list = ['Message-ID: ','Subject: ','From: ','Reply-To: ','To: ','Date: ']

#list to parse headers
header_list = ['Accept-Language: ','Approved: ','ARC-Authentication-Results: ','ARC-Message-Signature: ','ARC-Seal: ','Archive: ','Archived-At: ','Authentication-Results: ','Auto-Submitted: ','Bcc: ','Body: ','Cancel-Key: ','Cancel-Lock: ','Cc: ','Comments: ','Alternate-Recipient: ','Autoforwarded: ','Autosubmitted: ','Content-Alternative: ','Content-Description: ','Content-Disposition: ','Content-Duration: ','Content-features: ','Content-ID: ','Content-Identifier: ','Content-Language: ','Content-Location: ','Content-MD5: ','Content-Return: ','Content-Transfer-Encoding: ',
'Content-Translation-Type: ','Content-Type: ','Control: ','Conversion: ','Conversion-With-Loss: ','DL-Expansion-History: ','Deferred-Delivery: ','Delivery-Date: ','Discarded-X400-IPMS-Extensions: ','Discarded-X400-MTS-Extensions: ','Disclose-Recipients: ','Disposition-Notification-Options: ','Disposition-Notification-To: ','Distribution: ','DKIM-Signature: ','Downgraded-Final-Recipient: ','Downgraded-In-Reply-To: ','Downgraded-Message-Id: ','Downgraded-Original-Recipient: ','Downgraded-References: ','Encoding: ','Encrypted: ','Expires: ','Expiry-Date: ','Followup-To: ','Generate-Delivery-Report: ',
'Importance: ','In-Reply-To: ','Incomplete-Copy: ','Injection-Date: ','Injection-Info: ','Keywords: ','Language: ','Latest-Delivery-Time: ','Lines: ','List-Archive: ','List-Help: ','List-ID: ','List-Owner: ','List-Owner: ','List-Subscribe: ','List-Unsubscribe: ','List-Unsubscribe-Post: ','Message-Context: ','Message-ID: ','Message-Type: ','MIME-Version: ','MMHS-Exempted-Address: ','MMHS-Extended-Authorisation-Info: ','MMHS-Subject-Indicator-Codes: ','MMHS-Handling-Instructions: ','MMHS-Message-Instructions: ','MMHS-Codress-Message-Indicator: ','MMHS-Originator-Reference: ','MMHS-Primary-Precedence: ','MMHS-Copy-Precedence: ',
'MMHS-Message-Type: ','MMHS-Other-Recipients-Indicator-To: ','MMHS-Other-Recipients-Indicator-CC: ','MMHS-Acp127-Message-Identifier: ','MMHS-Originator-PLAD: ','MT-Priority: ','Newsgroups: ','Obsoletes: ','Organization: ','Original-Encoded-Information-Types: ','Original-From: ','Original-Message-ID: ','Original-Recipient: ','Original-Sender: ','Originator-Return-Address: ','Original-Subject: ','Path: ','PICS-Label: ','Posting-Version: ','Prevent-NonDelivery-Report: ','Priority: ','Received-SPF: ','References: ','Relay-Version: ','Reply-By: ','Require-Recipient-Valid-Since: ','Resent-Bcc: ','Resent-Cc: ','Resent-Date: ','Resent-From: ',
'Resent-Message-ID: ','Resent-Reply-To: ','Resent-Sender: ','Resent-To: ','Return-Path: ','Sender: ','Sensitivity: ','Solicitation: ','Summary: ','Supersedes: ','TLS-Report-Domain: ','TLS-Required: ','TLS-Report-Submitter: ','User-Agent: ','VBR-Info: ','VBR-Info: ','X400-Content-Identifier: ','X400-Content-Return: ','X400-Content-Type: ','X400-MTS-Identifier: ','X400-Originator: ','X400-Received: ','X400-Recipients: ','X400-Trace: ','Xref: ']

#dict to store all the timezones
time_zone_dict ={'-1100':'US/Samoa','-1000':'US/Hawaii','-0930':'Pacific/Marquesas','-0900':'Pacific/Gambier','-0800':'Pacific/Pitcairn','-0700':'America/Creston','-0600':'America/Belize','-0500':'America/Atikokan','-0400':'America/Anguilla','-0330':'America/St_Johns','-0300':'America/Argentina/Buenos_Aires','-0200':'America/Noronha','-0100':'Atlantic/Cape_Verde','+0100':'Africa/Bangui','+0200':'Europe/Helsinki','+0300':'Europe/Minsk','+0330':'Iran','+0400':'Europe/Astrakhan','+0430':'Asia/Kabul','+0500':'Asia/Oral','+0530':'Asia/Calcutta','+0545':'Asia/Kathmandu','+0600':'Asia/Thimbu',
'+0630':'Asia/Yangon','+0700':'Asia/Bangkok','+0800':'Asia/Brunei','+0845':'Australia/Eucla','+0900':'Asia/Dili','+0930':'Australia/Darwin','+1000':'Australia/Brisbane','+1030':'Australia/Adelaide','+1100':'Asia/Sakhalin','+1200':'Asia/Anadyr','+1245':'Pacific/Chatham','+1300':'Pacific/Apia','+1400':'Pacific/Kiritimati'}

final_headers_list = summary_list + header_list

#function to parse and store sender host value
def sender_host(a):	
    for i in a:
        tmp = i.split('by')
        try:
            sender_host_list.append(tmp[0].replace("\n","").strip('from'))
        except:
            None
    del sender_host_list[0]
    sender_host_list.reverse()
    
#function to parse and store receiver host value
def received_host(a):
    for i in a:
        t = i.replace("\n",'')
        tmp = re.split('by |with|id |\n', t)
        try:
            receiver_host_list.append(tmp[1])
        except:
            None
    receiver_host_list.reverse()
   
#function to parse and store no of hops
def no_of_hops():
		for i in range(len(receiver_host_list)+1):
			no_of_hops_list.append(i)
		del no_of_hops_list[0]
		
#function to parse and store protocols
def protocol_used(a):
    for i in a:
        t = i.replace("\n",'')
        tmp = re.split('by|with|id|;|\n', t)
        try:
            protocol_used_list.append(tmp[2])
        except:
            None
    protocol_used_list.reverse()
    
#function to parse, calculate and store timestamp and time delay 
def time_stamp(a):
    tmpts=[]
    contz=[]
    tmzone=[]
    tmp_timestamp = []
    final_timestamp = []

    for i in a:
        t = i.replace("\n",'')
        tmp = re.split('; |X-|\n', t)
        try:
            tmpts.append(tmp[1])
        except:
            None
    tmpts.reverse()
        
    for i in tmpts:
        for j in final_headers_list:
            z = i.strip()  
            r = z.find(j)
            if len(z)==37 or len(z)==31 or len(z)==38 or len(z)==32:
                final_timestamp_list.append(z)
                break
            if r>0:
                f = z.split(j)
                if len(f[0])==37 or len(f[0])==31 or len(f[0])==38 or len(f[0])==32:
                    final_timestamp_list.append(f[0])
    
    for i in final_timestamp_list:
        try:
            date = utils.parsedate_to_datetime(i)
            d1 = date.strftime('%Y/%m/%d %H:%M:%S')
            d2 = date.strftime('%z')
            contz.append(d1+d2)
            tmzone.append(d2)
        
        except:
            None
    
    def tmp_time_fun(tim,zn):
        for i,k in time_zone_dict.items():
            if i == zn:
                from_zone = tz.gettz(k)
                to_zone = tz.gettz("UTC")
                utc = datetime.strptime(tim, '%Y/%m/%d %H:%M:%S')
                utc = utc.replace(tzinfo=from_zone)
                central = utc.astimezone(tz =to_zone)
                tmp_timestamp.append(str(central))

    for (i,j) in zip(contz,tmzone):
        if '+0000' in i:
            tmp = i.split('+')
            ntmp = tmp[0].replace('/','-')
            tmp_timestamp.append(ntmp+'+00:00')
        else:
            if '+' in i:
                tmp = i.split('+')
            else:
                tmp = i.split('-')
            
            tmp_time_fun(tmp[0],j)

    for i in tmp_timestamp:
        if '+' in i:
            t1 = i.split('+')
        else:
            t1 = i.split('-')
        final_timestamp.append(t1[0])
    
    count1=0
    count2=0
    count3=1
    
    for i in final_timestamp:
        if count1==0:
            time_difference_list.append(" ")
            count1+=1
        else:
            tmp1 = final_timestamp[count2]
            tmp2 = final_timestamp[count3]
            to_zone = tz.gettz("UTC")
            utc1 = datetime.strptime(tmp1, '%Y-%m-%d %H:%M:%S')
            utc2 = datetime.strptime(tmp2, '%Y-%m-%d %H:%M:%S')

            central1 = utc1.astimezone(tz =to_zone)
            central2 = utc2.astimezone(tz =to_zone)
            
            fin = central2-central1

            time_difference_list.append(str(fin))
            count2+=1
            count3+=1
    
#function to parse and store summary
def summary(b,sum):
    try:
        tmp = str(sum).replace('\\n','').split(b)
    except:
        None
    try:
        a = tmp[1]
    except:
        None
    d = list(a.split("\n"))
    try:
        print(' {} {}'.format(b,d[0]))
    except:
        None

#function to parse and store headers other than X
def otherheaders(b):
    with open('Input/sample.txt','rb') as fp:
        for i in fp:
            z = str(i).strip("b'")
            try:
                tmp =str(z).replace('\\n','').split(b)
            except:
                None
            try:
                a = tmp[1]
            except:
                None
        try:
            print(' {} {}'.format(b,a))
        except:
            None

#function to call the summary function
def call_summary(sum):
    for i in summary_list:
        if i in str(sum):
            summary(i,sum)
    print("\n")

#function to call the header function that don't contain X
def call_otherheaders(sum):
    for i in header_list:
        if i in str(sum):
            otherheaders(i)

#function to parse and store sender X headers
def X_headers():
    with open('Input/sample.txt', 'rb') as fp:
        for i in fp:
            a = str(i).strip("b'")
            b = a.split('X-')
            try:
                print(" X-"+b[1].replace('\\n','').replace('\\r',''))
            except:
                None

#function to integrate all into one 
def call_EH_functions():
    with open('Input/sample.txt', 'rb') as fp:
        headers = BytesParser(policy=default).parse(fp)
        #For Received headers
        a = str(headers).split('Received: ')
        sender_host(a)
        received_host(a)
        no_of_hops()
        protocol_used(a)
        time_stamp(a)
        t = PrettyTable(['Hop','Sender', 'receiver','Protocol','Time','Delay'])
        t.hrules=ALL
        for (a,b,c,d,e,f) in zip(no_of_hops_list,sender_host_list,receiver_host_list,protocol_used_list,final_timestamp_list,time_difference_list):
            t.add_row([a,b,c,d,e,f])
    
        print(t)
        print('\n')
        print("-------------------------------------------------------------")
        print("			Summary		")
        print("-------------------------------------------------------------")
        call_summary(headers)

        print("-------------------------------------------------------------")
        print("			Other-Headers		")
        print("-------------------------------------------------------------")
        call_otherheaders(headers)
        X_headers()



