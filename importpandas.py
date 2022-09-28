import pyodbc
import pandas as pd
import configparser
# insert data from csv file into dataframe.
# working directory for csv file: type "pwd" in Azure Data Studio or Linux
# working directory in Windows c:\users\username
# get data from configuration file

config = configparser.ConfigParser()
try:
    config.read('config.ini')
except Exception as e:
    print('could not read configuration file:' + str(e))
    sys.exit();


    # read settings from configuration file
startDate = config['CONFIG']['startDate']
url = config['CONFIG']['url']
server = config['CONFIG']['server']
database = config['CONFIG']['database']
username= config['CONFIG']['User']
password = config['CONFIG']['Password']

csvFile='C:\\Download\\CSV\\communityandcommunitylegal.csv'

data = pd.read_csv(csvFile)

  
# overwriting data after changing format
data["CommunityCreatedDate"]= pd.to_datetime(data["CommunityCreatedDate"])
data["CommunityModifiedDate"]= pd.to_datetime(data["CommunityModifiedDate"])
#data["BirthDate"]= pd.to_datetime(data["BirthDate"])
data["DeceasedDate"]= pd.to_datetime(data["DeceasedDate"])
data["WorkWithChildrenCheckExpiryDate"]= pd.to_datetime(data["WorkWithChildrenCheckExpiryDate"])
data["WorkWithChildrenCheckVerifiedDate"]= pd.to_datetime(data["WorkWithChildrenCheckVerifiedDate"])
data["CourtOrderDate"]= pd.to_datetime(data["CourtOrderDate"])
data["ModifiedDate"]= pd.to_datetime(data["ModifiedDate"])



 

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# Insert Dataframe into SQL Server:
for index, row in data.iterrows():
     cursor.execute("INSERT INTO [communityandcommunitylegal] (ID,AddressID,SpouseID,SpouseFlag,CommunityCreatedDate,CommunityCreatedBy,CommunityModifiedDate,CommunityModifiedBy,Surname,SurnamePrevious \
                    ,Title,Initials,SuffixPreferred,Given1,Given2,OccupCode,OccupDesc,OccupCompany,OccupIndustryCode,OccupPositionCode,OccupPhone,OccupFax,OccupEmail,MailFormat,SalutFormat,BirthDate,DeceasedDate \
                    ,DeceasedFlag,Gender,MobilePhone,Email,ReligionCode,CountryOfBirthCode,HomeLanguageCode,Education,Qualifications,HighestSecondaryYearLevel,LastYearOfStudy,MaritalStatus,MailNamePrimary, \
                     MailNameJoint,MailSalutationPrimary,MailSalutationJoint,OccupMobilePhone,OccupAddressFull,ParishCode,NationalityCode,InitialsOverrideFlag,OccupCompanyAttn,DefaultEmailCode,NetworkLogin, \
                     Barcode,MobilePhoneActual,NameInternal,NameInternalOverrideFlag,NameExternal,NameExternalOverrideFlag,PreferredFormal,LegalFullName,LegalFullNameOverrideFlag,UserFlag1,UserFlag2,UserFlag3, \
                     UserFlag4,UserFlag5,MailNamePrimaryOverrideFlag,MailNameJointOverrideFlag,MailSalutationPrimaryOverrideFlag,MailSalutationJointOverrideFlag,CountryCitizenshipCode,HighestQualificationLevel, \
                     PublishToAssociatedFlag,HighestNonNationalQualificationCode,WorkWithChildrenCheckStatus,WorkWithChildrenCheckRegistrationNumber,WorkWithChildrenCheckExpiryDate,DefaultMobilePhoneCode, \
                     WorkWithChildrenCheckVerifiedDate,RefugeeFlag,FacetimeAddress,SkypeAddress,FacebookUrl,TwitterUrl,LinkedInUrl,CurrentWWCRequiredFlag,ExternalValidationFlag,ParentsSeparatedFlag,ParentsSeparatedReason \
                    ,CourtOrderType,CourtOrderDetails,CourtOrderDate,PhotoWebFlag,PhotoPromFlag,PhotoPublicationFlag,PrivacyPolicyAgreedFlag,ModifiedBy,ModifiedDate \
                    ) values(?,?,?)", row.DepartmentID, row.Name, row.GroupName)
cnxn.commit()
cursor.close()
