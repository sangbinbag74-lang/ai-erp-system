"""
AI ERP 시스템 콘텐츠 분석기

비즈니스 문서에서 인사이트, 패턴 및 실행 가능한 
정보를 추출하는 AI 기반 콘텐츠 분석 도구
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json

# AI/ML libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    FINANCIAL = "financial"
    INVENTORY = "inventory"
    CUSTOMER = "customer"
    SUPPLIER = "supplier"
    SALES = "sales"
    PURCHASE = "purchase"
    GENERAL = "general"


class ContentCategory(Enum):
    INVOICE = "invoice"
    QUOTATION = "quotation"
    PURCHASE_ORDER = "purchase_order"
    DELIVERY_NOTE = "delivery_note"
    FINANCIAL_REPORT = "financial_report"
    INVENTORY_REPORT = "inventory_report"
    CUSTOMER_DATA = "customer_data"
    SUPPLIER_DATA = "supplier_data"
    CONTRACT = "contract"
    EMAIL = "email"
    OTHER = "other"


@dataclass
class AnalysisResult:
    """Result of content analysis"""
    category: ContentCategory
    confidence: float
    key_insights: List[str]
    extracted_entities: Dict[str, List[str]]
    financial_data: Optional[Dict[str, Any]] = None
    recommendations: List[str] = None
    sentiment: Optional[str] = None
    urgency_level: int = 1  # 1-5 scale
    metadata: Dict[str, Any] = None


@dataclass
class EntityExtraction:
    """Extracted entities from content"""
    amounts: List[float]
    dates: List[str]
    companies: List[str]
    people: List[str]
    products: List[str]
    currencies: List[str]
    addresses: List[str]
    emails: List[str]
    phone_numbers: List[str]


class ContentAnalyzer:
    """
    AI-powered content analyzer for ERP documents
    """
    
    def __init__(self, llm_client=None, config: Dict[str, Any] = None):
        self.llm_client = llm_client
        self.config = config or {}
        
        # Patterns for entity extraction
        self.patterns = self._initialize_patterns()
        
        # Category keywords
        self.category_keywords = self._initialize_category_keywords()
        
        # Initialize ML models
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.clustering_model = None
    
    def _initialize_patterns(self) -> Dict[str, str]:
        """Initialize regex patterns for entity extraction"""
        
        return {
            'amounts': r'(?:USD|EUR|GBP|INR|\$|€|£|₹)\s*[\d,]+\.?\d*|[\d,]+\.?\d*\s*(?:USD|EUR|GBP|INR|\$|€|£|₹)',
            'dates': r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b',
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phones': r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            'currencies': r'\b(?:USD|EUR|GBP|INR|JPY|CAD|AUD)\b',
            'po_numbers': r'(?:PO|Purchase Order|P\.O\.)\s*[#:]?\s*([A-Z0-9-]+)',
            'invoice_numbers': r'(?:Invoice|INV|Bill)\s*[#:]?\s*([A-Z0-9-]+)',
            'tax_numbers': r'(?:GST|VAT|Tax ID|TIN)\s*[#:]?\s*([A-Z0-9-]+)'
        }
    
    def _initialize_category_keywords(self) -> Dict[ContentCategory, List[str]]:
        """Initialize keywords for document categorization"""
        
        return {
            ContentCategory.INVOICE: [
                'invoice', 'bill', 'payment due', 'amount due', 'billing', 'charges',
                'invoice number', 'bill to', 'remit to', 'payment terms'
            ],
            ContentCategory.QUOTATION: [
                'quotation', 'quote', 'proposal', 'estimate', 'rfq', 'request for quote',
                'valid until', 'expiry', 'quoted price'
            ],
            ContentCategory.PURCHASE_ORDER: [
                'purchase order', 'po number', 'order confirmation', 'delivery date',
                'shipping address', 'vendor', 'supplier'
            ],
            ContentCategory.DELIVERY_NOTE: [
                'delivery note', 'shipping', 'dispatch', 'consignment', 'delivery date',
                'received by', 'shipped to', 'tracking'
            ],
            ContentCategory.FINANCIAL_REPORT: [
                'balance sheet', 'profit loss', 'p&l', 'income statement', 'cash flow',
                'financial report', 'revenue', 'expenses', 'assets', 'liabilities'
            ],
            ContentCategory.INVENTORY_REPORT: [
                'inventory', 'stock report', 'warehouse', 'stock level', 'reorder',
                'stock valuation', 'item code', 'quantity on hand'
            ],
            ContentCategory.CUSTOMER_DATA: [
                'customer', 'client', 'billing address', 'contact person',
                'customer id', 'account manager'
            ],
            ContentCategory.SUPPLIER_DATA: [
                'supplier', 'vendor', 'manufacturer', 'supplier id',
                'vendor code', 'payment terms'
            ],
            ContentCategory.CONTRACT: [
                'contract', 'agreement', 'terms and conditions', 'service agreement',
                'license', 'renewal', 'termination'
            ],
            ContentCategory.EMAIL: [
                'subject', 'from', 'to', 'cc', 'bcc', 'sent', 'received'
            ]
        }
    
    async def analyze_content(
        self, 
        content: str, 
        document_type: str = None,
        context: Dict[str, Any] = None
    ) -> AnalysisResult:
        """
        Comprehensive content analysis
        """
        
        try:
            logger.info(f"Analyzing content (length: {len(content)})")
            
            # Extract entities
            entities = self._extract_entities(content)
            
            # Categorize document
            category, confidence = self._categorize_document(content)
            
            # Extract key insights
            insights = await self._extract_insights(content, category)
            
            # Analyze financial data if present
            financial_data = self._analyze_financial_data(content, entities)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(content, category, entities)
            
            # Determine urgency
            urgency = self._assess_urgency(content, entities)
            
            # Sentiment analysis (basic)
            sentiment = self._analyze_sentiment(content)
            
            result = AnalysisResult(
                category=category,
                confidence=confidence,
                key_insights=insights,
                extracted_entities=self._entities_to_dict(entities),
                financial_data=financial_data,
                recommendations=recommendations,
                sentiment=sentiment,
                urgency_level=urgency,
                metadata={
                    "analysis_timestamp": datetime.now().isoformat(),
                    "content_length": len(content),
                    "word_count": len(content.split()),
                    "document_type": document_type,
                    "context": context
                }
            )
            
            logger.info(f"Analysis completed: {category.value} (confidence: {confidence:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            return AnalysisResult(
                category=ContentCategory.OTHER,
                confidence=0.0,
                key_insights=[f"Analysis failed: {str(e)}"],
                extracted_entities={}
            )
    
    def _extract_entities(self, content: str) -> EntityExtraction:
        """Extract structured entities from content"""
        
        # Extract amounts
        amounts = []
        amount_matches = re.findall(self.patterns['amounts'], content, re.IGNORECASE)
        for match in amount_matches:
            # Clean and convert to float
            cleaned = re.sub(r'[^\d.]', '', match)
            try:
                amounts.append(float(cleaned))
            except ValueError:
                continue
        
        # Extract dates
        dates = re.findall(self.patterns['dates'], content, re.IGNORECASE)
        
        # Extract emails
        emails = re.findall(self.patterns['emails'], content, re.IGNORECASE)
        
        # Extract phone numbers
        phone_numbers = re.findall(self.patterns['phones'], content)
        
        # Extract currencies
        currencies = re.findall(self.patterns['currencies'], content, re.IGNORECASE)
        
        # Extract companies (basic pattern - words followed by Ltd, Inc, Corp, etc.)
        company_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Ltd|Inc|Corp|LLC|Co\.?|Company|Technologies|Tech|Solutions|Systems|Services|Group)\b'
        companies = re.findall(company_pattern, content)
        
        # Extract people names (basic pattern - capitalized words)
        name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        people = re.findall(name_pattern, content)
        
        # Extract products/items (words with item codes or SKU patterns)
        product_pattern = r'\b(?:Item|SKU|Product|Part)\s*[#:]?\s*([A-Z0-9-]+)\b'
        products = re.findall(product_pattern, content, re.IGNORECASE)
        
        # Extract addresses (basic pattern)
        address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln)[\s,]+[A-Za-z\s]+,?\s*[A-Z]{2}\s*\d{5}'
        addresses = re.findall(address_pattern, content)
        
        return EntityExtraction(
            amounts=list(set(amounts))[:10],  # Limit to 10 unique amounts
            dates=list(set(dates))[:10],
            companies=list(set(companies))[:10],
            people=list(set(people))[:10],
            products=list(set(products))[:10],
            currencies=list(set(currencies))[:5],
            addresses=list(set(addresses))[:5],
            emails=list(set(emails))[:10],
            phone_numbers=list(set(phone_numbers))[:5]
        )
    
    def _categorize_document(self, content: str) -> Tuple[ContentCategory, float]:
        """Categorize document based on content"""
        
        content_lower = content.lower()
        best_category = ContentCategory.OTHER
        best_score = 0.0
        
        for category, keywords in self.category_keywords.items():
            score = 0.0
            matched_keywords = 0
            
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1.0
                    matched_keywords += 1
                # Partial matches
                elif any(word in content_lower for word in keyword.split()):
                    score += 0.5
            
            # Normalize score
            if len(keywords) > 0:
                score = score / len(keywords)
            
            # Boost score for multiple keyword matches
            if matched_keywords > 1:
                score += 0.2
            
            if score > best_score:
                best_score = score
                best_category = category
        
        # Ensure minimum confidence threshold
        confidence = min(best_score, 1.0)
        if confidence < 0.3:
            best_category = ContentCategory.OTHER
            confidence = 0.1
        
        return best_category, confidence
    
    async def _extract_insights(self, content: str, category: ContentCategory) -> List[str]:
        """Extract key insights from content"""
        
        insights = []
        
        # Category-specific insights
        if category == ContentCategory.INVOICE:
            insights.extend(self._analyze_invoice_insights(content))
        elif category == ContentCategory.FINANCIAL_REPORT:
            insights.extend(self._analyze_financial_insights(content))
        elif category == ContentCategory.INVENTORY_REPORT:
            insights.extend(self._analyze_inventory_insights(content))
        
        # General insights
        insights.extend(self._analyze_general_insights(content))
        
        # Use LLM for advanced insights if available
        if self.llm_client:
            try:
                llm_insights = await self._get_llm_insights(content, category)
                insights.extend(llm_insights)
            except Exception as e:
                logger.warning(f"LLM insights failed: {str(e)}")
        
        return insights[:10]  # Limit to top 10 insights
    
    def _analyze_invoice_insights(self, content: str) -> List[str]:
        """Extract invoice-specific insights"""
        
        insights = []
        
        # Check for overdue payments
        if any(word in content.lower() for word in ['overdue', 'past due', 'late payment']):
            insights.append("Payment appears to be overdue - requires immediate attention")
        
        # Check for payment terms
        payment_terms = re.search(r'payment terms?:?\s*([^.\n]+)', content, re.IGNORECASE)
        if payment_terms:
            insights.append(f"Payment terms: {payment_terms.group(1).strip()}")
        
        # Check for discounts
        if re.search(r'discount|early payment', content, re.IGNORECASE):
            insights.append("Early payment discount may be available")
        
        return insights
    
    def _analyze_financial_insights(self, content: str) -> List[str]:
        """Extract financial report insights"""
        
        insights = []
        
        # Look for profit/loss indicators
        if re.search(r'profit.*increase|revenue.*up|sales.*growth', content, re.IGNORECASE):
            insights.append("Positive financial performance indicators detected")
        elif re.search(r'loss.*increase|revenue.*down|sales.*decline', content, re.IGNORECASE):
            insights.append("Concerning financial performance trends identified")
        
        # Cash flow analysis
        if re.search(r'cash flow.*negative|liquidity.*concern', content, re.IGNORECASE):
            insights.append("Potential cash flow issues detected")
        elif re.search(r'cash flow.*positive|strong.*liquidity', content, re.IGNORECASE):
            insights.append("Healthy cash flow position identified")
        
        return insights
    
    def _analyze_inventory_insights(self, content: str) -> List[str]:
        """Extract inventory-specific insights"""
        
        insights = []
        
        # Stock level analysis
        if re.search(r'low stock|out of stock|shortage', content, re.IGNORECASE):
            insights.append("Stock shortage alerts detected - reordering may be required")
        elif re.search(r'excess.*inventory|overstock', content, re.IGNORECASE):
            insights.append("Excess inventory levels identified - consider promotional strategies")
        
        # Reorder points
        if re.search(r'reorder.*point|minimum.*stock', content, re.IGNORECASE):
            insights.append("Reorder point thresholds mentioned - review inventory policies")
        
        return insights
    
    def _analyze_general_insights(self, content: str) -> List[str]:
        """Extract general insights"""
        
        insights = []
        
        # Urgency indicators
        urgent_keywords = ['urgent', 'asap', 'immediate', 'critical', 'emergency']
        if any(keyword in content.lower() for keyword in urgent_keywords):
            insights.append("Document contains urgency indicators - requires priority handling")
        
        # Action items
        action_patterns = [r'action required', r'please.*(?:confirm|approve|review)', r'need.*(?:your|approval)']
        for pattern in action_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                insights.append("Action items or approvals required")
                break
        
        # Compliance mentions
        compliance_keywords = ['compliance', 'regulation', 'audit', 'tax', 'legal']
        if any(keyword in content.lower() for keyword in compliance_keywords):
            insights.append("Compliance or regulatory content detected")
        
        return insights
    
    async def _get_llm_insights(self, content: str, category: ContentCategory) -> List[str]:
        """Get insights using LLM"""
        
        if not self.llm_client:
            return []
        
        prompt = f"""
        Analyze this {category.value} document and provide 3-5 key business insights:
        
        Document content:
        {content[:2000]}  # Limit content length
        
        Focus on:
        1. Financial implications
        2. Operational insights
        3. Risk factors
        4. Opportunities
        5. Action items
        
        Provide concise, actionable insights.
        """
        
        try:
            response = await self.llm_client.generate_response(prompt)
            insights_text = response.content
            
            # Parse insights (assuming they're in a list format)
            insights = []
            lines = insights_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    # Clean up formatting
                    insight = re.sub(r'^[-•\d.]+\s*', '', line).strip()
                    if insight:
                        insights.append(insight)
            
            return insights[:5]  # Return top 5 insights
            
        except Exception as e:
            logger.error(f"Error getting LLM insights: {str(e)}")
            return []
    
    def _analyze_financial_data(self, content: str, entities: EntityExtraction) -> Optional[Dict[str, Any]]:
        """Analyze financial data in the content"""
        
        if not entities.amounts:
            return None
        
        financial_data = {
            "total_amounts": entities.amounts,
            "currency_detected": entities.currencies[0] if entities.currencies else "USD",
            "amount_count": len(entities.amounts),
            "max_amount": max(entities.amounts),
            "min_amount": min(entities.amounts),
            "total_sum": sum(entities.amounts)
        }
        
        # Calculate statistics if multiple amounts
        if len(entities.amounts) > 1:
            amounts_array = np.array(entities.amounts)
            financial_data.update({
                "mean_amount": float(np.mean(amounts_array)),
                "median_amount": float(np.median(amounts_array)),
                "std_amount": float(np.std(amounts_array))
            })
        
        # Detect financial patterns
        patterns = []
        
        # Tax calculations (look for percentages)
        tax_pattern = r'(?:tax|gst|vat).*?(\d+(?:\.\d+)?)\s*%'
        tax_matches = re.findall(tax_pattern, content, re.IGNORECASE)
        if tax_matches:
            patterns.append(f"Tax rates detected: {', '.join(tax_matches)}%")
        
        # Discount patterns
        discount_pattern = r'discount.*?(\d+(?:\.\d+)?)\s*%'
        discount_matches = re.findall(discount_pattern, content, re.IGNORECASE)
        if discount_matches:
            patterns.append(f"Discounts detected: {', '.join(discount_matches)}%")
        
        if patterns:
            financial_data["patterns"] = patterns
        
        return financial_data
    
    async def _generate_recommendations(
        self, 
        content: str, 
        category: ContentCategory, 
        entities: EntityExtraction
    ) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Category-specific recommendations
        if category == ContentCategory.INVOICE:
            if any(word in content.lower() for word in ['overdue', 'past due']):
                recommendations.append("Follow up on overdue payment immediately")
            
            if entities.amounts:
                max_amount = max(entities.amounts)
                if max_amount > 10000:  # Configurable threshold
                    recommendations.append("Consider payment plan options for high-value invoice")
        
        elif category == ContentCategory.INVENTORY_REPORT:
            if 'low stock' in content.lower():
                recommendations.append("Create purchase orders for low-stock items")
            if 'overstock' in content.lower():
                recommendations.append("Review pricing strategy to move excess inventory")
        
        elif category == ContentCategory.FINANCIAL_REPORT:
            if any(word in content.lower() for word in ['loss', 'decline', 'decrease']):
                recommendations.append("Analyze cost structure and revenue optimization opportunities")
        
        # General recommendations
        if entities.dates:
            # Check for upcoming deadlines
            recommendations.append("Review all dates mentioned for upcoming deadlines")
        
        if entities.emails or entities.phone_numbers:
            recommendations.append("Update contact database with extracted contact information")
        
        # Use LLM for advanced recommendations if available
        if self.llm_client:
            try:
                llm_recommendations = await self._get_llm_recommendations(content, category)
                recommendations.extend(llm_recommendations)
            except Exception as e:
                logger.warning(f"LLM recommendations failed: {str(e)}")
        
        return recommendations[:8]  # Limit to 8 recommendations
    
    async def _get_llm_recommendations(self, content: str, category: ContentCategory) -> List[str]:
        """Get recommendations using LLM"""
        
        if not self.llm_client:
            return []
        
        prompt = f"""
        Based on this {category.value} document, provide 3-5 specific, actionable business recommendations:
        
        Document content:
        {content[:1500]}
        
        Focus on:
        1. Immediate actions needed
        2. Process improvements
        3. Risk mitigation
        4. Business opportunities
        
        Provide concise, specific recommendations.
        """
        
        try:
            response = await self.llm_client.generate_response(prompt)
            recommendations_text = response.content
            
            # Parse recommendations
            recommendations = []
            lines = recommendations_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    recommendation = re.sub(r'^[-•\d.]+\s*', '', line).strip()
                    if recommendation:
                        recommendations.append(recommendation)
            
            return recommendations[:5]
            
        except Exception as e:
            logger.error(f"Error getting LLM recommendations: {str(e)}")
            return []
    
    def _assess_urgency(self, content: str, entities: EntityExtraction) -> int:
        """Assess urgency level (1-5 scale)"""
        
        urgency_score = 1
        content_lower = content.lower()
        
        # High urgency keywords
        high_urgency = ['urgent', 'emergency', 'critical', 'asap', 'immediate']
        medium_urgency = ['important', 'priority', 'needed', 'required']
        
        if any(keyword in content_lower for keyword in high_urgency):
            urgency_score = 5
        elif any(keyword in content_lower for keyword in medium_urgency):
            urgency_score = 3
        
        # Financial thresholds
        if entities.amounts:
            max_amount = max(entities.amounts)
            if max_amount > 100000:  # High value transactions
                urgency_score = max(urgency_score, 4)
            elif max_amount > 10000:
                urgency_score = max(urgency_score, 3)
        
        # Overdue items
        if any(word in content_lower for word in ['overdue', 'past due', 'late']):
            urgency_score = max(urgency_score, 4)
        
        # Legal/compliance issues
        if any(word in content_lower for word in ['legal', 'compliance', 'audit', 'penalty']):
            urgency_score = max(urgency_score, 3)
        
        return min(urgency_score, 5)
    
    def _analyze_sentiment(self, content: str) -> str:
        """Basic sentiment analysis"""
        
        positive_words = ['good', 'excellent', 'satisfied', 'pleased', 'happy', 'success', 'profit', 'growth']
        negative_words = ['bad', 'poor', 'unsatisfied', 'disappointed', 'problem', 'issue', 'loss', 'decline']
        
        content_lower = content.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _entities_to_dict(self, entities: EntityExtraction) -> Dict[str, List[str]]:
        """Convert EntityExtraction to dictionary"""
        
        return {
            "amounts": [str(amount) for amount in entities.amounts],
            "dates": entities.dates,
            "companies": entities.companies,
            "people": entities.people,
            "products": entities.products,
            "currencies": entities.currencies,
            "addresses": entities.addresses,
            "emails": entities.emails,
            "phone_numbers": entities.phone_numbers
        }
    
    async def analyze_batch(
        self, 
        contents: List[Tuple[str, str]], 
        max_concurrent: int = 3
    ) -> List[AnalysisResult]:
        """Analyze multiple contents concurrently"""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def analyze_single(content, doc_type):
            async with semaphore:
                return await self.analyze_content(content, doc_type)
        
        tasks = [analyze_single(content, doc_type) for content, doc_type in contents]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error analyzing content {i}: {str(result)}")
                error_result = AnalysisResult(
                    category=ContentCategory.OTHER,
                    confidence=0.0,
                    key_insights=[f"Analysis failed: {str(result)}"],
                    extracted_entities={}
                )
                final_results.append(error_result)
            else:
                final_results.append(result)
        
        return final_results
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get analyzer statistics"""
        
        return {
            "supported_categories": [cat.value for cat in ContentCategory],
            "analysis_types": [at.value for at in AnalysisType],
            "entity_types": list(self.patterns.keys()),
            "llm_enabled": self.llm_client is not None
        }


def create_content_analyzer(llm_client=None, **config) -> ContentAnalyzer:
    """Factory function to create content analyzer"""
    return ContentAnalyzer(llm_client=llm_client, config=config)