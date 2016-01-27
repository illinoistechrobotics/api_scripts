import smtplib
import config as cf

def mail(to, subj, message):
            msg = "\r\n".join((
            "From: %s" % cf.mailfrom,
            "To: %s" % ','.join(to),
            "Subject: %s" % subj ,
            "",
            message
            ))
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(cf.mailfrom, to, msg)         
