"""
프로젝트(Project) DocType 정의
ERPNext의 Project와 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, Date
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype
from datetime import datetime


class Project(DocTypeBase, Base):
    """프로젝트 마스터"""
    
    __tablename__ = 'tabProject'
    
    # 기본 정보
    project_name = Column(String(140), nullable=False)
    project_type = Column(String(50), default='Internal')
    status = Column(String(50), default='Open')
    priority = Column(String(20), default='Medium')
    
    # 고객/계약 정보
    customer = Column(String(140))
    customer_name = Column(String(140))
    sales_order = Column(String(140))
    
    # 날짜 정보
    expected_start_date = Column(Date)
    expected_end_date = Column(Date)
    actual_start_date = Column(Date)
    actual_end_date = Column(Date)
    
    # 프로젝트 매니저
    project_manager = Column(String(140))
    
    # 회사 정보
    company = Column(String(140))
    department = Column(String(140))
    
    # 비용 정보
    estimated_costing = Column(Float, default=0)
    total_costing_amount = Column(Float, default=0)
    total_billable_amount = Column(Float, default=0)
    total_billed_amount = Column(Float, default=0)
    total_expense_claim = Column(Float, default=0)
    
    # 진행률
    percent_complete = Column(Float, default=0)
    percent_complete_method = Column(String(50), default='Manual')
    
    # 설명
    notes = Column(Text)
    project_template = Column(String(140))
    
    # 상태
    is_active = Column(String(10), default='Yes')
    
    def get_required_fields(self):
        return ['project_name']
    
    def validate(self):
        errors = super().validate()
        
        # 시작일과 종료일 검증
        if self.expected_start_date and self.expected_end_date:
            if self.expected_end_date <= self.expected_start_date:
                errors.append("예상 종료일은 예상 시작일보다 늦어야 합니다.")
        
        if self.actual_start_date and self.actual_end_date:
            if self.actual_end_date <= self.actual_start_date:
                errors.append("실제 종료일은 실제 시작일보다 늦어야 합니다.")
        
        # 진행률 검증
        if self.percent_complete < 0 or self.percent_complete > 100:
            errors.append("진행률은 0-100 사이의 값이어야 합니다.")
        
        return errors


class Task(DocTypeBase, Base):
    """작업/태스크"""
    
    __tablename__ = 'tabTask'
    
    # 기본 정보
    subject = Column(String(140), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='Open')
    priority = Column(String(20), default='Medium')
    
    # 프로젝트 연결
    project = Column(String(140))
    
    # 담당자 정보
    assigned_to = Column(String(140))
    assigned_to_name = Column(String(140))
    
    # 날짜 정보
    exp_start_date = Column(Date)
    exp_end_date = Column(Date)
    act_start_date = Column(Date)
    act_end_date = Column(Date)
    
    # 진행 정보
    progress = Column(Float, default=0)
    duration = Column(Float, default=0)  # in hours
    expected_time = Column(Float, default=0)
    actual_time = Column(Float, default=0)
    
    # 의존성
    depends_on = Column(String(140))  # 의존하는 작업
    
    # 회사 정보
    company = Column(String(140))
    
    # 이슈 추적
    issue = Column(String(140))
    
    # 상태
    is_group = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)
    
    def get_required_fields(self):
        return ['subject']
    
    def validate(self):
        errors = super().validate()
        
        # 시작일과 종료일 검증
        if self.exp_start_date and self.exp_end_date:
            if self.exp_end_date <= self.exp_start_date:
                errors.append("예상 종료일은 예상 시작일보다 늦어야 합니다.")
        
        # 진행률 검증
        if self.progress < 0 or self.progress > 100:
            errors.append("진행률은 0-100 사이의 값이어야 합니다.")
        
        return errors


class Timesheet(DocTypeBase, Base):
    """근무시간 기록"""
    
    __tablename__ = 'tabTimesheet'
    
    # 기본 정보
    employee = Column(String(140), nullable=False)
    employee_name = Column(String(140))
    
    # 날짜 정보
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # 총 시간
    total_hours = Column(Float, default=0)
    total_billable_hours = Column(Float, default=0)
    total_billed_hours = Column(Float, default=0)
    total_billable_amount = Column(Float, default=0)
    total_billed_amount = Column(Float, default=0)
    total_costing_amount = Column(Float, default=0)
    
    # 회사 정보
    company = Column(String(140))
    
    # 상태
    status = Column(String(50), default='Draft')
    per_billed = Column(Float, default=0)
    
    def get_required_fields(self):
        return ['employee', 'start_date', 'end_date']
    
    def validate(self):
        errors = super().validate()
        
        # 시작일과 종료일 검증
        if self.end_date <= self.start_date:
            errors.append("종료일은 시작일보다 늦어야 합니다.")
        
        return errors


class TimesheetDetail(DocTypeBase, Base):
    """근무시간 상세"""
    
    __tablename__ = 'tabTimesheetDetail'
    
    # 부모 문서 연결
    parent = Column(String(140), nullable=False)
    parenttype = Column(String(50), default='Timesheet')
    
    # 활동 정보
    activity_type = Column(String(140), nullable=False)
    from_time = Column(DateTime, nullable=False)
    to_time = Column(DateTime, nullable=False)
    hours = Column(Float, nullable=False, default=0)
    
    # 프로젝트/작업 연결
    project = Column(String(140))
    task = Column(String(140))
    
    # 설명
    description = Column(Text)
    
    # 청구 정보
    is_billable = Column(Boolean, default=True)
    billing_hours = Column(Float, default=0)
    billing_rate = Column(Float, default=0)
    billing_amount = Column(Float, default=0)
    costing_rate = Column(Float, default=0)
    costing_amount = Column(Float, default=0)
    
    def get_required_fields(self):
        return ['activity_type', 'from_time', 'to_time', 'hours']


# Project DocType 메타데이터
project_meta = DocTypeMeta({
    "name": "Project",
    "module": "Projects",
    "autoname": "field:project_name",
    "title_field": "project_name",
    "search_fields": ["project_name", "customer_name", "project_manager"],
    "sort_field": "expected_start_date",
    "sort_order": "DESC",
    "fields": [
        {
            "fieldname": "project_name",
            "fieldtype": "Data",
            "label": "프로젝트명",
            "reqd": 1,
            "length": 140
        },
        {
            "fieldname": "project_type",
            "fieldtype": "Select",
            "label": "프로젝트 유형",
            "options": "Internal\nExternal\nOther",
            "default": "Internal"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Open\nCompleted\nCancelled",
            "default": "Open"
        },
        {
            "fieldname": "priority",
            "fieldtype": "Select",
            "label": "우선순위",
            "options": "Low\nMedium\nHigh\nCritical",
            "default": "Medium"
        },
        {
            "fieldname": "customer",
            "fieldtype": "Link",
            "label": "고객",
            "options": "Customer"
        },
        {
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "label": "고객명",
            "read_only": 1,
            "length": 140
        },
        {
            "fieldname": "sales_order",
            "fieldtype": "Link",
            "label": "주문서",
            "options": "Sales Order"
        },
        {
            "fieldname": "expected_start_date",
            "fieldtype": "Date",
            "label": "예상 시작일"
        },
        {
            "fieldname": "expected_end_date",
            "fieldtype": "Date",
            "label": "예상 종료일"
        },
        {
            "fieldname": "project_manager",
            "fieldtype": "Link",
            "label": "프로젝트 매니저",
            "options": "User"
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company"
        },
        {
            "fieldname": "estimated_costing",
            "fieldtype": "Float",
            "label": "예상 비용",
            "precision": 2
        },
        {
            "fieldname": "total_costing_amount",
            "fieldtype": "Float",
            "label": "총 비용",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "total_billable_amount",
            "fieldtype": "Float",
            "label": "총 청구 가능 금액",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "percent_complete",
            "fieldtype": "Float",
            "label": "진행률(%)",
            "precision": 2
        },
        {
            "fieldname": "percent_complete_method",
            "fieldtype": "Select",
            "label": "진행률 계산 방법",
            "options": "Manual\nTask Completion\nTask Progress\nTask Weight",
            "default": "Manual"
        },
        {
            "fieldname": "notes",
            "fieldtype": "Text",
            "label": "참고사항"
        },
        {
            "fieldname": "is_active",
            "fieldtype": "Select",
            "label": "활성화",
            "options": "Yes\nNo",
            "default": "Yes"
        }
    ],
    "permissions": [
        {
            "role": "Projects User",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Projects Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "cancel": 1
        }
    ]
})

# Task DocType 메타데이터
task_meta = DocTypeMeta({
    "name": "Task",
    "module": "Projects",
    "autoname": "naming_series:",
    "title_field": "subject",
    "search_fields": ["subject", "project", "assigned_to"],
    "sort_field": "exp_end_date",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "subject",
            "fieldtype": "Data",
            "label": "제목",
            "reqd": 1,
            "length": 140
        },
        {
            "fieldname": "description",
            "fieldtype": "Text",
            "label": "설명"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Open\nWorking\nPending Review\nOverdue\nTemplate\nCompleted\nCancelled",
            "default": "Open"
        },
        {
            "fieldname": "priority",
            "fieldtype": "Select",
            "label": "우선순위",
            "options": "Low\nMedium\nHigh\nUrgent",
            "default": "Medium"
        },
        {
            "fieldname": "project",
            "fieldtype": "Link",
            "label": "프로젝트",
            "options": "Project"
        },
        {
            "fieldname": "assigned_to",
            "fieldtype": "Link",
            "label": "담당자",
            "options": "User"
        },
        {
            "fieldname": "exp_start_date",
            "fieldtype": "Date",
            "label": "예상 시작일"
        },
        {
            "fieldname": "exp_end_date",
            "fieldtype": "Date",
            "label": "예상 종료일"
        },
        {
            "fieldname": "progress",
            "fieldtype": "Float",
            "label": "진행률(%)",
            "precision": 2
        },
        {
            "fieldname": "expected_time",
            "fieldtype": "Float",
            "label": "예상 시간",
            "precision": 2
        },
        {
            "fieldname": "actual_time",
            "fieldtype": "Float",
            "label": "실제 시간",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "is_group",
            "fieldtype": "Check",
            "label": "그룹 작업",
            "default": 0
        }
    ],
    "permissions": [
        {
            "role": "Projects User",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "Employee",
            "read": 1,
            "write": 1,
            "create": 1
        }
    ]
})

# Timesheet DocType 메타데이터
timesheet_meta = DocTypeMeta({
    "name": "Timesheet",
    "module": "Projects",
    "autoname": "naming_series:",
    "search_fields": ["employee", "employee_name", "start_date"],
    "sort_field": "start_date",
    "sort_order": "DESC",
    "is_submittable": 1,
    "fields": [
        {
            "fieldname": "employee",
            "fieldtype": "Link",
            "label": "직원",
            "options": "Employee",
            "reqd": 1
        },
        {
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "label": "직원명",
            "read_only": 1,
            "length": 140
        },
        {
            "fieldname": "start_date",
            "fieldtype": "Date",
            "label": "시작일",
            "reqd": 1
        },
        {
            "fieldname": "end_date",
            "fieldtype": "Date",
            "label": "종료일",
            "reqd": 1
        },
        {
            "fieldname": "total_hours",
            "fieldtype": "Float",
            "label": "총 시간",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "total_billable_hours",
            "fieldtype": "Float",
            "label": "청구 가능 시간",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "total_billable_amount",
            "fieldtype": "Float",
            "label": "청구 가능 금액",
            "read_only": 1,
            "precision": 2
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Draft\nSubmitted\nBilled\nCancelled",
            "default": "Draft"
        }
    ],
    "permissions": [
        {
            "role": "Projects User",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
            "cancel": 1
        },
        {
            "role": "Employee",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1
        }
    ]
})

# DocType 등록
register_doctype("Project", project_meta, Project)
register_doctype("Task", task_meta, Task)
register_doctype("Timesheet", timesheet_meta, Timesheet)
register_doctype("Timesheet Detail", None, TimesheetDetail)