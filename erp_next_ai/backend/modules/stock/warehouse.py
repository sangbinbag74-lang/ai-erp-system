"""
창고(Warehouse) DocType 정의
ERPNext의 Warehouse와 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype


class Warehouse(DocTypeBase, Base):
    """창고 마스터"""
    
    __tablename__ = 'tabWarehouse'
    
    # 기본 정보
    warehouse_name = Column(String(140), nullable=False)
    warehouse_type = Column(String(50), default='Transit')
    
    # 상위 창고 (계층 구조)
    parent_warehouse = Column(String(140))
    is_group = Column(Boolean, default=False)
    
    # 주소 정보
    address_line_1 = Column(String(140))
    address_line_2 = Column(String(140))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default='South Korea')
    pin = Column(String(20))
    
    # 연락처 정보
    phone_no = Column(String(20))
    mobile_no = Column(String(20))
    email_id = Column(String(140))
    
    # 회사 정보
    company = Column(String(140))
    
    # 계정 설정
    account = Column(String(140))  # Stock Account
    
    # 상태
    disabled = Column(Boolean, default=False)
    
    # 창고 설정
    is_rejected_warehouse = Column(Boolean, default=False)
    
    def get_required_fields(self):
        return ['warehouse_name']
    
    def validate(self):
        errors = super().validate()
        
        # 그룹 창고인 경우 상위 창고가 있으면 안됨
        if self.is_group and self.parent_warehouse:
            errors.append("그룹 창고는 상위 창고를 가질 수 없습니다.")
        
        # 이메일 유효성 검사
        if self.email_id:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email_id):
                errors.append("올바른 이메일 주소를 입력하세요.")
        
        return errors


class StockEntry(DocTypeBase, Base):
    """재고 이동 전표"""
    
    __tablename__ = 'tabStockEntry'
    
    # 기본 정보
    stock_entry_type = Column(String(50), nullable=False)
    purpose = Column(String(50), nullable=False)
    
    # 날짜 정보
    posting_date = Column(DateTime, nullable=False)
    posting_time = Column(String(10))
    
    # 창고 정보
    from_warehouse = Column(String(140))
    to_warehouse = Column(String(140))
    
    # 총계
    total_outgoing_value = Column(Float, default=0)
    total_incoming_value = Column(Float, default=0)
    value_difference = Column(Float, default=0)
    total_additional_costs = Column(Float, default=0)
    
    # 참조 정보
    work_order = Column(String(140))
    bom_no = Column(String(140))
    fg_completed_qty = Column(Float, default=0)
    
    # 프로젝트 정보
    project = Column(String(140))
    
    # 상태
    per_transferred = Column(Float, default=0)
    
    def get_required_fields(self):
        return ['stock_entry_type', 'purpose', 'posting_date']
    
    def validate(self):
        errors = super().validate()
        
        # 이동 목적에 따른 창고 검증
        if self.purpose in ['Material Transfer', 'Material Issue']:
            if not self.from_warehouse:
                errors.append(f"{self.purpose}에는 출고 창고가 필요합니다.")
        
        if self.purpose in ['Material Transfer', 'Material Receipt']:
            if not self.to_warehouse:
                errors.append(f"{self.purpose}에는 입고 창고가 필요합니다.")
        
        return errors


class StockEntryDetail(DocTypeBase, Base):
    """재고 이동 상세"""
    
    __tablename__ = 'tabStockEntryDetail'
    
    # 부모 문서 연결
    parent = Column(String(140), nullable=False)
    parenttype = Column(String(50), default='Stock Entry')
    
    # 아이템 정보
    item_code = Column(String(140), nullable=False)
    item_name = Column(String(140))
    description = Column(Text)
    item_group = Column(String(140))
    
    # 창고 정보
    s_warehouse = Column(String(140))  # Source Warehouse (출고)
    t_warehouse = Column(String(140))  # Target Warehouse (입고)
    
    # 수량 및 단위
    qty = Column(Float, nullable=False, default=0)
    transfer_qty = Column(Float, default=0)
    uom = Column(String(50))
    stock_uom = Column(String(50))
    conversion_factor = Column(Float, default=1)
    
    # 가격 정보
    basic_rate = Column(Float, default=0)
    valuation_rate = Column(Float, default=0)
    basic_amount = Column(Float, default=0)
    amount = Column(Float, default=0)
    
    # 배치/시리얼 정보
    batch_no = Column(String(140))
    serial_no = Column(Text)
    
    # 실제 수량 (실사용)
    actual_qty = Column(Float, default=0)
    
    def get_required_fields(self):
        return ['item_code', 'qty']


# Warehouse DocType 메타데이터
warehouse_meta = DocTypeMeta({
    "name": "Warehouse",
    "module": "Stock",
    "autoname": "field:warehouse_name",
    "title_field": "warehouse_name",
    "search_fields": ["warehouse_name", "city", "company"],
    "sort_field": "warehouse_name",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "warehouse_name",
            "fieldtype": "Data",
            "label": "창고명",
            "reqd": 1,
            "length": 140
        },
        {
            "fieldname": "warehouse_type",
            "fieldtype": "Select",
            "label": "창고 유형",
            "options": "Transit\nReceiving\nWork In Progress\nFinished Goods\nRetail\nSample",
            "default": "Transit"
        },
        {
            "fieldname": "parent_warehouse",
            "fieldtype": "Link",
            "label": "상위 창고",
            "options": "Warehouse"
        },
        {
            "fieldname": "is_group",
            "fieldtype": "Check",
            "label": "그룹 창고",
            "default": 0
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company"
        },
        {
            "fieldname": "address_line_1",
            "fieldtype": "Data",
            "label": "주소 1",
            "length": 140
        },
        {
            "fieldname": "address_line_2",
            "fieldtype": "Data",
            "label": "주소 2",
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
            "fieldname": "pin",
            "fieldtype": "Data",
            "label": "우편번호",
            "length": 20
        },
        {
            "fieldname": "phone_no",
            "fieldtype": "Data",
            "label": "전화번호",
            "length": 20
        },
        {
            "fieldname": "email_id",
            "fieldtype": "Data",
            "label": "이메일",
            "length": 140
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
            "role": "Stock Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Stock User",
            "read": 1,
            "write": 1,
            "create": 1
        }
    ]
})

# Stock Entry DocType 메타데이터
stock_entry_meta = DocTypeMeta({
    "name": "Stock Entry",
    "module": "Stock",
    "autoname": "naming_series:",
    "search_fields": ["stock_entry_type", "from_warehouse", "to_warehouse"],
    "sort_field": "posting_date",
    "sort_order": "DESC",
    "is_submittable": 1,
    "fields": [
        {
            "fieldname": "stock_entry_type",
            "fieldtype": "Link",
            "label": "재고 이동 유형",
            "options": "Stock Entry Type",
            "reqd": 1
        },
        {
            "fieldname": "purpose",
            "fieldtype": "Select",
            "label": "목적",
            "options": "Material Issue\nMaterial Receipt\nMaterial Transfer\nMaterial Transfer for Manufacture\nMaterial Consumption for Manufacture\nManufacture\nRepack\nSend to Subcontractor",
            "reqd": 1
        },
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": "전기일",
            "reqd": 1,
            "default": "Today"
        },
        {
            "fieldname": "posting_time",
            "fieldtype": "Time",
            "label": "전기시간",
            "default": "Now"
        },
        {
            "fieldname": "from_warehouse",
            "fieldtype": "Link",
            "label": "출고 창고",
            "options": "Warehouse"
        },
        {
            "fieldname": "to_warehouse",
            "fieldtype": "Link",
            "label": "입고 창고",
            "options": "Warehouse"
        },
        {
            "fieldname": "total_outgoing_value",
            "fieldtype": "Float",
            "label": "총 출고 가액",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "total_incoming_value",
            "fieldtype": "Float",
            "label": "총 입고 가액",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "project",
            "fieldtype": "Link",
            "label": "프로젝트",
            "options": "Project"
        }
    ],
    "permissions": [
        {
            "role": "Stock User",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
            "cancel": 1
        },
        {
            "role": "Stock Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1
        }
    ]
})

# DocType 등록
register_doctype("Warehouse", warehouse_meta, Warehouse)
register_doctype("Stock Entry", stock_entry_meta, StockEntry)
register_doctype("Stock Entry Detail", None, StockEntryDetail)  # Child table은 메타데이터 간소화