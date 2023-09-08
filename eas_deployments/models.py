# model of EAS instances data
# PyMongo and Flask-PyMongo handle the cnnection to the database
# Pydantic manages data validation and some aspects of data transformation between the db and a JSON representations
from config import db
from enum import Enum

url_regex = "^([0-9A-Za-z]([-0-9A-Za-z]{0,61}[0-9A-Za-z])?\.)+[A-Za-z]{2,63}\.?$"
ipv4_regex = "^(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$"
ipv6_regex ="^((([^:]+:){7}([^:]+))|((([^:]+:)*[^:]+)?::(([^:]+:)*[^:]+)?))$"
groupId_regex = "^[A-Fa-f0-9]{8}-[0-9]{3}-[0-9]{2,3}-([A-Fa-f0-9][A-Fa-f0-9]){1,10}$"
connBand_regex = "^\d+(\.\d+)? (bps|Kbps|Mbps|Gbps|Tbps)$"
sd_regex = "^[A-Fa-f0-9]{6}$"


class Operator(Enum):
   FULL_MATCH = "FULL_MATCH"
   MATCH_ALL = "MATCH_ALL"
   STARTS_WITH = "STARTS_WITH"
   NOT_START_WITH = "NOT_START_WITH"
   ENDS_WITH = "ENDS_WITH"
   NOT_END_WITH = "NOT_END_WITH"
   CONTAINS = "CONTAINS"
   NOT_CONTAIN = "NOT_CONTAIN"

class Snssai(db.EmbeddedDocument):
   sst = db.IntField(min_value=0, max_value=255, required=True)
   sd = db.StringField(regex=sd_regex)

class IpAddr(db.EmbeddedDocument):
   ipv4Addr = db.StringField(regex=ipv4_regex)
   ipv6Addr = db.StringField(regex=ipv6_regex)

class DnsServerId(db.EmbeddedDocument):
   dnsServIpAddr = db.ListField(db.DictField(IpAddr), required=True)
   portNumber = db.IntField(min_value=0, required=True)

class ServiceKPI(db.EmbeddedDocument):
   """Model for EAS service KPIs

   Args:
       Object (EmbeddedDocument): Describes computation characteristics of the Edge Application.
   """
   maxReqRate = db.IntField()
   maxRespTime = db.IntField()
   avail = db.IntField()
   avlComp = db.IntField()
   avlGraComp = db.IntField()
   avlMem = db.IntField()
   avlStrg = db.IntField()
   connBand = db.StringField(regex=connBand_regex)

class DnaiInfos(db.EmbeddedDocument):
   dnai = db.StringField(required=True)
   dnsServIds = db.ListField(db.EmbeddedDocumentField(DnsServerId))
   easIpAddrs = db.ListField(db.EmbeddedDocumentField(IpAddr))
   
class StringMatchingCondition(db.EmbeddedDocument):
   matchingString = db.StringField()
   matchingOperator = db.EnumField(Operator, required=True)

class StringMatchingRule(db.EmbeddedDocument):
   stringMatchingConditions = db.ListField(db.EmbeddedDocumentField(StringMatchingCondition))

class FqdnPatternMatching(db.EmbeddedDocument):
   regex = db.StringField()
   stringMatchingRule = db.EmbeddedDocumentField(StringMatchingRule)

class EasInstance(db.Document):
   """EAS informations to be deployed
   Args:
       Object (EmbeddedDocument): Nested document for multiple fields
   """
   meta = {'collection': 'easInstances'}

   appId = db.StringField(required=True)
   dnaiInfos = db.EmbeddedDocumentField(DnaiInfos)
   dnn = db.StringField()
   fqdnPatternList= db.ListField(db.EmbeddedDocumentField(FqdnPatternMatching), required=True)
   internalGroupId = db.StringField(regex=groupId_regex, max_length=100)
   snssai = db.EmbeddedDocumentField(Snssai)
   svcKpi = db.EmbeddedDocumentField(ServiceKPI, required=True)
