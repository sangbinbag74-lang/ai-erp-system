"""
계정과목(Account) DocType 정의
ERPNext의 Account 모듈과 동일한 구조
"""
from sqlalchemy import Column, String, Float, Boolean, DateTime, Text
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype


class Account(DocTypeBase, Base):
    """계정과목 마스터"""
    
    __tablename__ = 'tabAccount'
    
    # 기본 정보
    account_name = Column(String(100), nullable=False)
    account_number = Column(String(20))
    parent_account = Column(String(140))  # 상위 계정
    company = Column(String(100), nullable=False)
    
    # 계정 분류
    account_type = Column(String(50))  # Asset, Liability, Income, Expense, Equity
    root_type = Column(String(20))     # Asset, Liability, Income, Expense, Equity
    
    # 그룹 계정 여부
    is_group = Column(Boolean, default=False)
    
    # 잔액 정보
    account_currency = Column(String(10), default='KRW')
    opening_balance = Column(Float, default=0)
    credit_limit = Column(Float, default=0)
    
    # 세금 설정
    tax_rate = Column(Float, default=0)
    
    # 상태
    disabled = Column(Boolean, default=False)
    freeze_account = Column(String(10))  # No, Yes
    
    def get_required_fields(self):
        return ['account_name', 'company', 'root_type']
    
    def validate(self):
        errors = super().validate()
        
        if not self.account_name or not self.account_name.strip():
            errors.append("계정과목명은 필수입니다.")
        
        if not self.company or not self.company.strip():
            errors.append("회사는 필수입니다.")
        
        if self.root_type not in ['Asset', 'Liability', 'Income', 'Expense', 'Equity']:
            errors.append("계정 유형이 올바르지 않습니다.")
        
        return errors


# DocType 메타데이터
account_meta = DocTypeMeta({
    "name": "Account",
    "module": "Accounts",
    "autoname": "field:account_name",
    "title_field": "account_name",
    "search_fields": ["account_name", "account_number"],
    "sort_field": "account_name",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "account_name",
            "fieldtype": "Data",
            "label": "계정과목명",
            "reqd": 1,
            "length": 100
        },
        {
            "fieldname": "account_number",
            "fieldtype": "Data",
            "label": "계정번호",
            "length": 20
        },
        {
            "fieldname": "parent_account",
            "fieldtype": "Link",
            "label": "상위 계정",
            "options": "Account"
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company",
            "reqd": 1
        },
        {
            "fieldname": "account_type",
            "fieldtype": "Select",
            "label": "계정 유형",
            "options": "Asset\nLiability\nIncome\nExpense\nEquity"
        },
        {
            "fieldname": "root_type",
            "fieldtype": "Select",
            "label": "루트 유형",
            "options": "Asset\nLiability\nIncome\nExpense\nEquity",
            "reqd": 1
        },
        {
            "fieldname": "is_group",
            "fieldtype": "Check",
            "label": "그룹 계정",
            "default": 0
        },
        {
            "fieldname": "account_currency",
            "fieldtype": "Link",
            "label": "통화",
            "options": "Currency",
            "default": "KRW"
        },
        {
            "fieldname": "opening_balance",
            "fieldtype": "Float",
            "label": "기초 잔액",
            "precision": 2,
            "default": 0
        },
        {
            "fieldname": "disabled",
            "fieldtype": "Check",
            "label": "비활성화",
            "default": 0
        }
    ],
    "permissions": [
        {
            "role": "Accounts Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Accounts User",
            "read": 1,
            "write": 1,
            "create": 1
        }
    ]
})

register_doctype("Account", account_meta, Account)