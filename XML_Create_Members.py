import pandas as pd
import os
from jinja2 import Template

xml_template = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:enr="http://www.healthedge.com/connector/schema/enrollmentsparse">
    <soapenv:Header/>
    <soapenv:Body>
        <enr:enrollment>
            <asOfDate>{{ AsOfDate }}</asOfDate>
            <sendToWorkBasketIfExceptionsPresent>{{ sendToWorkBasketIfExceptionsPresent }}</sendToWorkBasketIfExceptionsPresent>
            <subscription>
                <hccIdentifier>{{ MemberNumber }}</hccIdentifier>
                <originalEffectiveDate>{{ originalEffectiveDate }}</originalEffectiveDate>
                <accountMatchData>
                    <accountHccIdentifier>
                        <accountHccIdentificationNumber>{{ AccountHccIdentificationNumber }}</accountHccIdentificationNumber>
                    </accountHccIdentifier>
                </accountMatchData>
            </subscription>
            <member>
                <maintenanceTypeCode>{{ CreateOrChange }}</maintenanceTypeCode>
                <memberIsSubscriber>{{ memberIsSubscriber }}</memberIsSubscriber>
                <hccIdentifier>{{ MemberNumber }}</hccIdentifier>
                <outOfServiceArea>{{ OutOfServiceArea }}</outOfServiceArea>
                <isMemberInHospice>{{ isMemberInHospice }}</isMemberInHospice>
                <memberMatchData>
                    <definitionName>MemberMatchDefinition</definitionName>
                    <id>{{ MemberNumber }}</id>
                    <topAccount>{{ TopAccount }}</topAccount>
                </memberMatchData>
                <individual>
                    <genderCode>{{ Gender }}</genderCode>
                    <birthDate>{{ DateOfBirth }}</birthDate>
                    <primaryName>
                        <lastName>{{ LastName }}</lastName>
                        <firstName>{{ FirstName }}</firstName>
                        <middleName>{{ MiddleName }}</middleName>
                    </primaryName>
                    <languages>
                        <language>
                            <primaryLanguage>{{ primaryLanguage }}</primaryLanguage>
                            <languageDomainCode>
                                <codeSetName>LanguageDomain</codeSetName>
                                <shortName>{{ PrimarySpokenLanguage }}</shortName>
                            </languageDomainCode>
                        </language>
                    </languages>
                </individual>
                <physicalAddress>
                    <memberPhysicalAddress>
                        <addressInfo>
                            <postalAddress>
                                <address>{{ Address1 }}</address>
                                <stateCode>{{ State }}</stateCode>
                                <zipCode>{{ zipCode }}</zipCode>
                                <zipExtensionCode>{{ zipExtensionCode }}</zipExtensionCode>
                                <cityName>{{ City }}</cityName>
                                <countyCode>{{ COUNTY_CD }}</countyCode>
                                <countryCode>
                                    <countryCode>{{ CountryCode }}</countryCode>
                                </countryCode>
                                <longitude>{{ LONGITUDE }}</longitude>
                                <latitude>{{ LATITUDE }}</latitude>
                                <ignoreAddressCheck>{{ ignoreAddressCheck }}</ignoreAddressCheck>
                            </postalAddress>
                            <addressPhoneList>
                                <telephoneNumber>
                                    <phoneAreaCode>{{ phoneAreaCode }}</phoneAreaCode>
                                    <phoneNumber>{{ phoneNumber }}</phoneNumber>
                                    <individualPhoneTypeCode>
                                        <codeSetName>IndividualPhoneType</codeSetName>
                                        <shortName>Home phone number</shortName>
                                    </individualPhoneTypeCode>
                                </telephoneNumber>
                            </addressPhoneList>
                        </addressInfo>
                        <addressTypeCode>
                            <codeSetName>IndividualAddressType</codeSetName>
                            <shortName>{{ memberPhysicalAddress2_addressTypeCode_shortName }}</shortName>
                        </addressTypeCode>
                    </memberPhysicalAddress>
                </physicalAddress>
                <otherIdNumberList>
                    <identificationNumber>
                        <identificationNumber>{{ SocialSecurityNumber }}</identificationNumber>
                        <identificationTypeCode>
                            <codeSetName>IdentificationType</codeSetName>
                            <shortName>Social Security Number</shortName>
                        </identificationTypeCode>
                    </identificationNumber>
                    <identificationNumber>
                        <identificationNumber>{{ NationalIndividualID }}</identificationNumber>
                        <identificationTypeCode>
                            <codeSetName>IdentificationType</codeSetName>
                            <shortName>NationalIndividualID</shortName>
                        </identificationTypeCode>
                    </identificationNumber>
                </otherIdNumberList>
                <membershipUDTList>
                    <membershipUDT>
                        <udtListValueSet>
                            <attributeRoleName>Ethnicity</attributeRoleName>
                            <attrValueAsString>{{ EthnicityCode }}</attrValueAsString>
                        </udtListValueSet>
                        <userDefinedTermReference>
                            <ID>Ethnicity</ID>
                        </userDefinedTermReference>
                    </membershipUDT>
                </membershipUDTList>
                <relationshipToSubscriberDefinitionReference>
                    <relationshipName>SELF</relationshipName>
                </relationshipToSubscriberDefinitionReference>
                <raceOrEthnicity>
                    <listMode>REPLACE</listMode>
                    <raceOrEthnicityCodes>
                        <codeSetName>RaceOrEthnicityCode</codeSetName>
                        <shortName>{{ Ethnicity }}</shortName>
                    </raceOrEthnicityCodes>
                </raceOrEthnicity>
                <planSelection>
                    <startDate>{{ EffectiveDate }}</startDate>
                    <endDate>{{ ExpirationDate }}</endDate>
                    <benefitPlanMatchData>
                        <benefitPlanHccId>{{ benefitPlanHccId }}</benefitPlanHccId>
                    </benefitPlanMatchData>
                    <planSelectionUDTList>
                        <planSelectionUDT>
                            <udtListValueSet>
                                <attributeRoleName>Aid Code 1</attributeRoleName>
                                <attrValueAsString>{{ aidcode1 }}</attrValueAsString>
                            </udtListValueSet>
                            <userDefinedTermReference>
                                <ID>Aid Code 1</ID>
                            </userDefinedTermReference>
                        </planSelectionUDT>
                        <planSelectionUDT>
                            <udtListValueSet>
                                <attributeRoleName>Aid Code 3</attributeRoleName>
                                <attrValueAsString>{{ aidcode3 }}</attrValueAsString>
                            </udtListValueSet>
                            <userDefinedTermReference>
                                <ID>Aid Code 3</ID>
                            </userDefinedTermReference>
                        </planSelectionUDT>
                    </planSelectionUDTList>
                </planSelection>
                <providerSelections>
                    <providerSelection>
                        <providerRoleType>{{ providerRoleType }}</providerRoleType>
                        <providerDateRanges>
                            <startDate>{{ providerSelection_startDate }}</startDate>
                            <endDate>{{ providerSelection_endDate }}</endDate>
                            <providerMatch>
                                <supplierLocation>
                                    <hccIdentificationNumber>{{ hccIdentificationNumber }}</hccIdentificationNumber>
                                </supplierLocation>
                            </providerMatch>
                            <pcpAutoAssigned>{{ pcpAutoAssigned }}</pcpAutoAssigned>
                        </providerDateRanges>
                    </providerSelection>
                </providerSelections>
            </member>
        </enr:enrollment>
    </soapenv:Body>
</soapenv:Envelope>
"""


excel_file = os.path.join(os.getcwd(), 'INPUT_FILE') 
df = pd.read_excel(excel_file)


date_columns = ['AsOfDate', 'originalEffectiveDate', 'DateOfBirth', 'EffectiveDate', 'ExpirationDate', 'providerSelection_startDate', 'providerSelection_endDate']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')


bool_columns = ['sendToWorkBasketIfExceptionsPresent', 'memberIsSubscriber', 'outOfServiceArea', 'isMemberInHospice', 'primaryLanguage', 'ignoreAddressCheck', 'pcpAutoAssigned']
for col in bool_columns:
    if col in df.columns:
        df[col] = df[col].replace({False: 'false', True: 'true'})

template = Template(xml_template)

for index, row in df.iterrows():
    data = row.to_dict()

    rendered_xml = template.render(data)
    
    output_file = "Output_file"
    
    with open(output_file, 'w') as file:
        file.write(rendered_xml)
    
    print(f"XML for member {index + 1} written to {output_file}")
