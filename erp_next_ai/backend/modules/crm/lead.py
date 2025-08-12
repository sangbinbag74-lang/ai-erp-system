"""
리드(Lead) DocType 정의
ERPNext의 Lead와 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, Date
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype
from datetime import datetime


class Lead(DocTypeBase, Base):
    """리드(잠재고객) 마스터"""
    
    __tablename__ = 'tabLead'
    
    # 기본 정보
    lead_name = Column(String(140), nullable=False)
    organization_lead = Column(Boolean, default=False)
    company_name = Column(String(140))
    lead_type = Column(String(50), default='Client')
    
    # 개인 정보 (개인 리드인 경우)
    salutation = Column(String(20))
    first_name = Column(String(50))
    middle_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(20))
    
    # 연락처 정보
    email_id = Column(String(140))
    mobile_no = Column(String(20))
    phone = Column(String(20))
    
    # 주소 정보
    address_line_1 = Column(String(140))
    address_line_2 = Column(String(140))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default='South Korea')
    pincode = Column(String(20))
    
    # 소스 정보
    source = Column(String(50))  # Web Form, Email, Phone, etc.
    campaign_name = Column(String(140))
    
    # 상태
    status = Column(String(50), default='Lead')
    qualification_status = Column(String(50))
    
    # 영업 정보
    market_segment = Column(String(140))
    industry = Column(String(140))
    territory = Column(String(140))
    
    # 담당자
    lead_owner = Column(String(140))
    
    # 회사 정보
    company = Column(String(140))
    
    # 관심 상품
    request_type = Column(String(50))
    
    # 참고사항
    notes = Column(Text)
    
    def get_required_fields(self):
        return ['lead_name']
    
    def validate(self):
        errors = super().validate()
        
        # 이메일 유효성 검사
        if self.email_id:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email_id):
                errors.append("올바른 이메일 주소를 입력하세요.")
        
        # 조직 리드인 경우 회사명 필수
        if self.organization_lead and not self.company_name:
            errors.append("조직 리드인 경우 회사명은 필수입니다.")
        
        return errors


class Opportunity(DocTypeBase, Base):
    """영업 기회"""
    
    __tablename__ = 'tabOpportunity'
    
    # 기본 정보
    opportunity_from = Column(String(50), nullable=False)  # Lead, Customer
    party_name = Column(String(140), nullable=False)  # Lead or Customer name
    customer_name = Column(String(140))
    
    # 영업 정보
    opportunity_type = Column(String(50), default='Sales')
    source = Column(String(50))
    sales_stage = Column(String(50), default='Prospecting')
    
    # 금액 정보
    opportunity_amount = Column(Float, default=0)
    probability = Column(Float, default=0)  # 성사 확률 (%)
    
    # 날짜 정보
    expected_closing = Column(Date)
    
    # 상태
    status = Column(String(50), default='Open')
    
    # 담당자
    contact_person = Column(String(140))
    contact_email = Column(String(140))
    contact_mobile = Column(String(20))
    
    # 회사 정보
    company = Column(String(140))
    territory = Column(String(140))
    
    # 참고사항
    notes = Column(Text)
    
    def get_required_fields(self):
        return ['opportunity_from', 'party_name']
    
    def validate(self):
        errors = super().validate()
        
        # 확률 범위 검증
        if self.probability < 0 or self.probability > 100:
            errors.append("성사 확률은 0-100% 사이의 값이어야 합니다.")
        
        # 이메일 유효성 검사
        if self.contact_email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.contact_email):
                errors.append("올바른 이메일 주소를 입력하세요.")
        
        return errors


class Campaign(DocTypeBase, Base):
    """마케팅 캠페인"""
    
    __tablename__ = 'tabCampaign'
    
    # 기본 정보
    campaign_name = Column(String(140), nullable=False)
    naming_series = Column(String(50), default='CAM-')
    
    # 캠페인 설정
    campaign_schedules = Column(Text)
    description = Column(Text)
    
    def get_required_fields(self):
        return ['campaign_name']


class CommunicationLog(DocTypeBase, Base):
    """커뮤니케이션 로그"""
    
    __tablename__ = 'tabCommunication'
    
    # 기본 정보
    subject = Column(String(140), nullable=False)
    content = Column(Text)
    communication_type = Column(String(50), default='Communication')
    
    # 날짜 및 시간
    communication_date = Column(DateTime, default=datetime.utcnow)
    
    # 연결 정보
    reference_doctype = Column(String(50))  # Lead, Customer, Opportunity 등
    reference_name = Column(String(140))
    
    # 발신/수신 정보
    sender = Column(String(140))
    recipients = Column(Text)
    
    # 상태
    sent_or_received = Column(String(20), default='Sent')
    delivery_status = Column(String(50))
    
    def get_required_fields(self):
        return ['subject']


# Lead DocType 메타데이터
lead_meta = DocTypeMeta({
    "name": "Lead",
    "module": "CRM",
    "autoname": "naming_series:",
    "title_field": "lead_name",
    "search_fields": ["lead_name", "email_id", "mobile_no", "company_name"],
    "sort_field": "creation",
    "sort_order": "DESC",
    "fields": [
        {
            "fieldname": "lead_name",
            "fieldtype": "Data",
            "label": "리드명",
            "reqd": 1,
            "length": 140
        },
        {
            "fieldname": "organization_lead",
            "fieldtype": "Check",
            "label": "조직 리드",
            "default": 0
        },
        {
            "fieldname": "company_name",
            "fieldtype": "Data",
            "label": "회사명",
            "length": 140
        },
        {
            "fieldname": "lead_type",
            "fieldtype": "Select",
            "label": "리드 유형",
            "options": "Client\nChannel Partner\nConsultant",
            "default": "Client"
        },
        {
            "fieldname": "salutation",
            "fieldtype": "Link",
            "label": "호칭",
            "options": "Salutation"
        },
        {
            "fieldname": "first_name",
            "fieldtype": "Data",
            "label": "성",
            "length": 50
        },
        {
            "fieldname": "last_name",
            "fieldtype": "Data",
            "label": "이름",
            "length": 50
        },
        {
            "fieldname": "gender",
            "fieldtype": "Select",
            "label": "성별",
            "options": "Male\nFemale\nOther"
        },
        {
            "fieldname": "email_id",
            "fieldtype": "Data",
            "label": "이메일",
            "length": 140
        },
        {
            "fieldname": "mobile_no",
            "fieldtype": "Data",
            "label": "휴대폰",
            "length": 20
        },
        {
            "fieldname": "phone",
            "fieldtype": "Data",
            "label": "전화번호",
            "length": 20
        },
        {
            "fieldname": "address_line_1",
            "fieldtype": "Data",
            "label": "주소 1",
            "length": 140
        },
        {
            "fieldname": "city",
            "fieldtype": "Data",
            "label": "도시",
            "length": 100
        },
        {
            "fieldname": "state",
            "fieldtype": "Data",
            "label": "시/도",
            "length": 100
        },
        {
            "fieldname": "country",
            "fieldtype": "Link",
            "label": "국가",
            "options": "Country",
            "default": "South Korea"
        },
        {
            "fieldname": "source",
            "fieldtype": "Select",
            "label": "소스",
            "options": "Existing Customer\nReference\nAdvertisement\nCold Calling\nExhibition\nSupplier Reference\nMass Mailing\nCustomer's Vendor\nCampaign\nWalk In\nWebsite\nFacebook\nLinkedIn\nTwitter\nOther"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Lead\nOpen\nReplied\nOpportunity\nQuotation\nLost Quotation\nInterested\nConverted\nDo Not Contact",
            "default": "Lead"
        },
        {
            "fieldname": "territory",
            "fieldtype": "Link",
            "label": "지역",
            "options": "Territory"
        },
        {
            "fieldname": "lead_owner",
            "fieldtype": "Link",
            "label": "담당자",
            "options": "User"
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company"
        },
        {
            "fieldname": "notes",
            "fieldtype": "Text",
            "label": "참고사항"
        }
    ],
    "permissions": [
        {
            "role": "Sales User",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Sales Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "cancel": 1
        }
    ]
})

# Opportunity DocType 메타데이터
opportunity_meta = DocTypeMeta({
    "name": "Opportunity",
    "module": "CRM",
    "autoname": "naming_series:",
    "search_fields": ["party_name", "customer_name", "opportunity_type"],
    "sort_field": "expected_closing",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "opportunity_from",
            "fieldtype": "Select",
            "label": "기회 출처",
            "options": "Lead\nCustomer",
            "reqd": 1
        },
        {
            "fieldname": "party_name",
            "fieldtype": "Dynamic Link",
            "label": "고객/리드",
            "options": "opportunity_from",
            "reqd": 1
        },
        {
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "label": "고객명",
            "read_only": 1,
            "length": 140
        },
        {
            "fieldname": "opportunity_type",
            "fieldtype": "Link",
            "label": "기회 유형",
            "options": "Opportunity Type",
            "default": "Sales"
        },
        {
            "fieldname": "source",
            "fieldtype": "Select",
            "label": "소스",
            "options": "Existing Customer\nReference\nAdvertisement\nCold Calling\nExhibition\nSupplier Reference\nMass Mailing\nCustomer's Vendor\nCampaign\nWalk In\nWebsite"
        },
        {
            "fieldname": "sales_stage",
            "fieldtype": "Select",
            "label": "영업 단계",
            "options": "Prospecting\nQualification\nNeeds Analysis\nValue Proposition\nIdentify Decision Makers\nProposal/Price Quote\nNegotiation/Review\nClosed Won\nClosed Lost",
            "default": "Prospecting"
        },
        {
            "fieldname": "opportunity_amount",
            "fieldtype": "Float",
            "label": "기회 금액",
            "precision": 2
        },
        {
            "fieldname": "probability",
            "fieldtype": "Float",
            "label": "성사 확률(%)",
            "precision": 2
        },
        {
            "fieldname": "expected_closing",
            "fieldtype": "Date",
            "label": "예상 성사일"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Open\nQuotation\nReplied\nClosed\nLost",
            "default": "Open"
        },
        {
            "fieldname": "contact_person",
            "fieldtype": "Data",
            "label": "담당자",
            "length": 140
        },
        {
            "fieldname": "contact_email",
            "fieldtype": "Data",
            "label": "이메일",
            "length": 140
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company"
        },
        {
            "fieldname": "notes",
            "fieldtype": "Text",
            "label": "참고사항"
        }
    ],
    "permissions": [
        {
            "role": "Sales User",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Sales Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "cancel": 1
        }
    ]
})

# DocType 등록
register_doctype("Lead", lead_meta, Lead)
register_doctype("Opportunity", opportunity_meta, Opportunity)
register_doctype("Campaign", None, Campaign)
register_doctype("Communication", None, CommunicationLog)