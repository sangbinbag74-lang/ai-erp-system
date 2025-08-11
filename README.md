# AI ERP - Next-Generation Enterprise Resource Planning System

[한국어 문서](README_KR.md) | [English Documentation](README.md)

An AI-powered enterprise resource planning system built on ERPNext with advanced LLM integration capabilities.

## Overview

This project revolutionizes the traditional ERP experience by integrating Large Language Models (LLM) as the core engine, enabling natural conversational interfaces and autonomous handling of complex file operations, data analysis, and business process automation.

## Key Features

### 🤖 AI-First Architecture
- LLM-powered file management and analysis
- Autonomous document processing and insights
- Natural language query interface for all ERP functions
- Intelligent workflow automation

### 📁 Advanced File Management
- Automatic file scanning and content analysis
- AI-powered document summarization
- Smart file organization and tagging
- Real-time file modification tracking

### 👥 Simplified Team Management
- One-click team invitation system
- AI-assisted role assignment
- Automated permission management
- Intelligent team collaboration features

### ☁️ Cloud-Native Storage
- External cloud API integration (AWS S3, Google Cloud)
- Distributed file synchronization
- Cost-optimized storage solutions
- Real-time backup and recovery

### 💰 Flexible Pricing Tiers
- **Free Tier**: Up to 5 team members, basic LLM features
- **Pro Tier**: Unlimited members, advanced AI analytics, priority support

## Technology Stack

### Backend
- **Framework**: Python/Frappe (inherited from ERPNext)
- **Database**: MariaDB/PostgreSQL
- **LLM Integration**: OpenAI GPT-4, Anthropic Claude, or Grok API
- **Cloud Storage**: AWS S3, Google Cloud Storage APIs
- **Authentication**: JWT with role-based access control

### Frontend
- **Framework**: Vue.js with Frappe UI components
- **State Management**: Vuex/Pinia
- **Real-time**: WebSocket connections
- **UI Library**: AI-enhanced custom components

### External Integrations
- **LLM APIs**: Usage-based models for cost optimization
- **Payment Processing**: Stripe integration
- **Cloud Storage**: Multi-provider API support
- **Monitoring**: AI-powered system analytics

## Project Structure

```
ai_erp/
├── backend/                 # Python/Frappe backend
│   ├── ai_core/            # LLM integration modules
│   ├── file_manager/       # Enhanced file management
│   ├── team_manager/       # Simplified team operations
│   ├── cloud_storage/      # Cloud API integrations
│   ├── billing/            # Subscription management
│   └── utils/              # Translation and utilities
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── i18n/          # Internationalization (Korean/English)
│   │   ├── components/    # AI-enhanced UI components
│   │   ├── views/         # Main application views
│   │   └── dashboard/     # AI-powered dashboards
├── config/                 # Configuration files
├── docs/                   # Documentation (Korean/English)
└── translations/           # Language files
```

## Core Modules

### 1. AI Core Engine (`/backend/ai_core/`)
- LLM API abstraction layer
- Context management and memory
- Natural language processing
- Intelligent task routing

### 2. File Management System (`/backend/file_manager/`)
- Automated file processing
- Content analysis and extraction
- Version control and audit trails
- AI-powered file recommendations

### 3. Team Management (`/backend/team_manager/`)
- Simplified user onboarding
- Role-based access control
- Team performance analytics
- Collaboration tools

### 4. Cloud Storage Integration (`/backend/cloud_storage/`)
- Multi-provider storage abstraction
- Automatic synchronization
- Data encryption and security
- Cost optimization algorithms

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- MariaDB/PostgreSQL
- Redis (for caching)

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/ai-erp.git
cd ai-erp

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Configuration setup
cp config/.env.example config/.env
# Edit configuration file with your API keys and settings

# Initialize database
cd ../backend
python manage.py migrate

# Start development servers
python manage.py runserver  # Backend
cd ../frontend && npm run dev  # Frontend
```

### Configuration
1. Set up LLM API credentials (OpenAI, Anthropic, etc.)
2. Configure cloud storage providers
3. Set up payment gateway (Stripe)
4. Configure email and notification services

## Internationalization

### Language Support
- **Korean (한국어)**: Complete localization
- **English**: Full support
- Dynamic language switching without refresh

### Translation Files
- `translations/ko/ai_epr.csv` - ERPNext translations
- `frontend/src/i18n/ko.js` - Vue.js Korean language pack
- `config/field_translations.json` - Database field translations

### Translation Utilities
- Automatic field name translation
- Context-aware translations
- Time and file size formatting in Korean
- Validation messages in Korean

## Subscription Tiers

### Free Tier
- Up to 5 team members
- 5GB storage
- 100 AI queries per month
- Basic ERP features
- Email support

### Basic Tier ($29/month)
- Up to 25 team members
- 100GB storage
- 1,000 AI queries per month
- Advanced features
- Priority support

### Pro Tier ($99/month) - Most Popular
- Unlimited team members
- 1TB storage
- 10,000 AI queries per month
- All features
- Phone support
- Custom branding

### Enterprise Tier ($299/month)
- All Pro features
- Dedicated support
- SSO integration
- Custom development
- On-premise options

## Competitive Advantages

### Compared to Traditional ERP
1. **AI-First Architecture**: LLM as core engine, not an add-on
2. **Simplified UX**: Natural language interface reduces training time
3. **Cloud-Native**: Built for modern cloud infrastructure
4. **Cost-Effective**: Usage-based model vs. expensive licenses
5. **Rapid Deployment**: Setup in hours, not months

### Compared to Competitors
1. **True AI Integration**: AI-driven operations, not just chatbots
2. **Multi-Cloud**: Vendor-independent storage and compute
3. **Open Architecture**: API-first design enables customization
4. **Transparent Pricing**: Clear tier structure with no hidden costs
5. **ERPNext Foundation**: Built on proven ERP functionality

## Quick Start

### 1. System Installation
```bash
# Run automated setup
python scripts/setup.py

# Or manual installation
pip install -r backend/requirements.txt
cd frontend && npm install
```

### 2. Environment Configuration
```bash
# Set environment variables
cp config/.env.example config/.env

# Configure API keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
AWS_ACCESS_KEY_ID=your_aws_key
STRIPE_SECRET_KEY=your_stripe_key
```

### 3. Database Setup
```bash
# Create PostgreSQL database
createdb ai_erp_dev

# Run migrations
python backend/manage.py migrate
```

### 4. Start System
```bash
# Start backend server
cd backend && python manage.py runserver

# Start frontend server (in new terminal)
cd frontend && npm run dev

# Run demo
python demo/main.py
```

## Usage Examples

### AI-Assisted Team Creation
```python
# Simple team creation
team_service.create_team(
    name="Marketing Team",
    owner_email="manager@company.com",
    description="Digital marketing team"
)
# AI automatically suggests roles and permissions
```

### Natural Language File Analysis
```python
# File upload and automatic analysis
result = ai_erp.analyze_file(
    file_path="contract.pdf",
    query="What are the key terms and expiration date of this contract?"
)
# AI analyzes content and extracts key information
```

### Intelligent Query Processing
```python
# Natural language business queries
response = ai_erp.query(
    "Show me top 5 customers with highest revenue this quarter"
)
# AI searches database and provides visualized results
```

## Security & Compliance

- **Data Encryption**: End-to-end encryption of all data
- **Access Control**: Role-based permissions with audit logging
- **API Security**: JWT tokens with refresh mechanisms
- **Storage Security**: Encrypted cloud storage with secure access
- **Compliance**: GDPR-compliant data processing and user privacy controls

## Monitoring & Analytics

### Real-time Dashboard
- Team activity and performance metrics
- AI usage and cost tracking
- System health and alerts
- User engagement analytics

### AI Insights
- Automated business intelligence
- Predictive analytics and recommendations
- Cost optimization suggestions
- Performance benchmarking

## Support & Community

- 📧 Email: support@ai-erp.com
- 💬 Community: [Discord/Slack channels]
- 📖 Documentation: [docs.ai-erp.com]
- 🎥 Tutorials: [YouTube channel]

## License

This project is built upon ERPNext's GPL v3 license. Additional AI enhancements are provided under the same license terms.

## Contributing

Contributions are welcome! Please read our contribution guidelines before submitting pull requests for improvements.

### Development Guidelines
1. Code Style: Use Black formatter
2. Testing: Add tests for new features
3. Documentation: Update docs for public APIs
4. Commit Messages: Follow existing conventions

## Roadmap

### Q1 2024
- [x] Core AI engine implementation
- [x] Basic team management features
- [x] File processing system
- [x] Cloud storage integration
- [x] Korean localization

### Q2 2024 (Planned)
- [ ] Mobile applications
- [ ] Advanced analytics dashboard
- [ ] Third-party integrations (Slack, MS Teams)
- [ ] Extended multilingual support

### Q3 2024 (Planned)
- [ ] Industry-specific modules
- [ ] AI marketplace
- [ ] Advanced workflow automation
- [ ] Enterprise SSO integration

## FAQ

**Q: Can I migrate from existing ERPNext?**
A: Yes, we provide compatibility layers to preserve existing data and customizations.

**Q: Can AI features be disabled?**
A: Yes, AI features can be selectively disabled to operate in traditional ERPNext mode.

**Q: Do you support on-premise deployment?**
A: Yes, on-premise deployment options are available for Enterprise tier.

**Q: Where is data stored?**
A: Data is stored in your chosen cloud provider (AWS, Google Cloud, Azure) or on-premise.

---

**Note**: This is an enhanced version of ERPNext with advanced AI capabilities. All original ERPNext features are preserved while adding advanced LLM-powered functionality.

## Contact

For questions or suggestions about the project, feel free to contact us:

- **Email**: info@ai-erp.com
- **Website**: https://ai-erp.com
- **GitHub**: [Project Repository]
- **LinkedIn**: [Company Page]

---

*Next-generation ERP solution for forward-thinking businesses*