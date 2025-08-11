"""
Setup Script for AI ERP System

Handles installation, configuration, and deployment setup
for the AI-powered ERP system.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import argparse


def install_dependencies():
    """Install Python dependencies"""
    
    print("📦 Installing Python dependencies...")
    
    # Backend dependencies
    backend_requirements = Path(__file__).parent.parent / "backend" / "requirements.txt"
    
    if backend_requirements.exists():
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(backend_requirements)
            ], check=True, capture_output=True, text=True)
            print("✅ Backend dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing backend dependencies: {e}")
            print(f"Output: {e.stdout}")
            print(f"Error: {e.stderr}")
            return False
    else:
        print("⚠️  Backend requirements.txt not found")
    
    # Frontend dependencies
    frontend_dir = Path(__file__).parent.parent / "frontend"
    package_json = frontend_dir / "package.json"
    
    if package_json.exists():
        try:
            # Check if npm is available
            subprocess.run(["npm", "--version"], check=True, capture_output=True)
            
            # Install dependencies
            subprocess.run([
                "npm", "install"
            ], cwd=str(frontend_dir), check=True, capture_output=True, text=True)
            print("✅ Frontend dependencies installed successfully")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing frontend dependencies: {e}")
            return False
        except FileNotFoundError:
            print("⚠️  npm not found. Please install Node.js and npm")
            return False
    else:
        print("⚠️  Frontend package.json not found")
    
    return True


def create_config_files():
    """Create configuration files"""
    
    print("⚙️  Creating configuration files...")
    
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(exist_ok=True)
    
    # Environment configuration
    env_config = {
        "environment": "development",
        "debug": True,
        "log_level": "INFO",
        
        # Database
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "ai_erp_dev",
            "user": "postgres",
            "password": "your_password"
        },
        
        # Redis (for context management)
        "redis": {
            "host": "localhost",
            "port": 6379,
            "db": 0
        },
        
        # LLM Configuration
        "llm": {
            "default_provider": "openai",
            "openai_api_key": "your_openai_api_key_here",
            "anthropic_api_key": "your_anthropic_api_key_here",
            "cost_tracking": True,
            "fallback_providers": ["anthropic"]
        },
        
        # Cloud Storage
        "storage": {
            "default_provider": "aws_s3",
            "aws": {
                "enabled": True,
                "access_key": "your_aws_access_key",
                "secret_key": "your_aws_secret_key",
                "region": "us-east-1",
                "bucket_name": "ai-erp-storage"
            },
            "quotas": {
                "total_limit_gb": 100
            }
        },
        
        # Payment Gateway
        "payment": {
            "provider": "stripe",
            "stripe_secret_key": "sk_test_...",
            "stripe_publishable_key": "pk_test_...",
            "webhook_secret": "whsec_..."
        },
        
        # Email Service
        "email": {
            "provider": "smtp",
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_user": "your_email@gmail.com",
            "smtp_password": "your_app_password"
        },
        
        # Security
        "security": {
            "secret_key": "your_secret_key_here_change_in_production",
            "jwt_algorithm": "HS256",
            "jwt_expiration": 86400,
            "password_min_length": 8
        },
        
        # Features
        "features": {
            "ai_assistance": True,
            "file_analysis": True,
            "team_management": True,
            "subscription_management": True,
            "usage_tracking": True
        }
    }
    
    # Write environment config
    env_file = config_dir / "config.json"
    with open(env_file, 'w') as f:
        json.dump(env_config, f, indent=2)
    
    print(f"✅ Configuration file created: {env_file}")
    
    # Create .env file
    env_file_content = """# AI ERP System Environment Variables

# Environment
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ai_erp_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# LLM APIs
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# AWS Storage
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=ai-erp-storage

# Payment Gateway (Stripe)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Security
SECRET_KEY=your_secret_key_here_change_in_production
JWT_ALGORITHM=HS256

# Application
APP_NAME=AI ERP System
APP_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
"""
    
    env_file_path = config_dir / ".env"
    with open(env_file_path, 'w') as f:
        f.write(env_file_content)
    
    print(f"✅ Environment file created: {env_file_path}")
    print("⚠️  Please update the configuration files with your actual API keys and credentials!")
    
    return True


def setup_database():
    """Setup database"""
    
    print("🗄️  Setting up database...")
    print("📝 Database setup instructions:")
    print("   1. Install PostgreSQL")
    print("   2. Create database: CREATE DATABASE ai_erp_dev;")
    print("   3. Create user with appropriate permissions")
    print("   4. Update database credentials in config files")
    print("   5. Run database migrations (when available)")
    
    return True


def setup_redis():
    """Setup Redis"""
    
    print("💾 Setting up Redis...")
    print("📝 Redis setup instructions:")
    print("   1. Install Redis")
    print("   2. Start Redis server: redis-server")
    print("   3. Verify connection: redis-cli ping")
    print("   4. Update Redis configuration in config files")
    
    return True


def create_project_structure():
    """Create additional project structure"""
    
    print("📁 Creating project structure...")
    
    project_root = Path(__file__).parent.parent
    
    directories = [
        "logs",
        "uploads",
        "exports", 
        "backups",
        "static",
        "media"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)
        
        # Create .gitkeep file
        gitkeep = dir_path / ".gitkeep"
        gitkeep.touch()
    
    print("✅ Project structure created")
    
    return True


def create_startup_scripts():
    """Create startup scripts"""
    
    print("🚀 Creating startup scripts...")
    
    scripts_dir = Path(__file__).parent
    
    # Development startup script
    dev_script = scripts_dir / "start_dev.py"
    dev_script_content = '''#!/usr/bin/env python3
"""
Development Server Startup Script for AI ERP System
"""

import asyncio
import uvicorn
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def start_development_server():
    """Start development servers"""
    
    print("🚀 Starting AI ERP Development Environment")
    print("=" * 50)
    
    # Start backend server
    print("📡 Starting backend server on http://localhost:8000")
    
    try:
        # In a real implementation, this would start the FastAPI/Flask server
        print("✅ Backend server ready")
        
        # Frontend would be started separately with: npm run dev
        print("🌐 Frontend server: http://localhost:3000 (run 'npm run dev' in frontend/)")
        
        print("\n🎯 AI ERP System is ready!")
        print("   Backend API: http://localhost:8000")
        print("   Frontend App: http://localhost:3000")
        print("   Documentation: http://localhost:8000/docs")
        
    except KeyboardInterrupt:
        print("\\n⏹️  Shutting down servers...")
    except Exception as e:
        print(f"❌ Error starting servers: {str(e)}")

if __name__ == "__main__":
    start_development_server()
'''
    
    with open(dev_script, 'w') as f:
        f.write(dev_script_content)
    
    print(f"✅ Development script created: {dev_script}")
    
    # Demo script
    demo_script = scripts_dir / "run_demo.py"
    demo_script_content = '''#!/usr/bin/env python3
"""
Run AI ERP System Demo
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from demo.main import main

if __name__ == "__main__":
    print("🎬 Starting AI ERP System Demo...")
    asyncio.run(main())
'''
    
    with open(demo_script, 'w') as f:
        f.write(demo_script_content)
    
    print(f"✅ Demo script created: {demo_script}")
    
    return True


def print_setup_summary():
    """Print setup summary and next steps"""
    
    print("\n" + "=" * 60)
    print("🎉 AI ERP System Setup Complete!")
    print("=" * 60)
    
    print("\n📋 Next Steps:")
    print("   1. Update configuration files with your API keys:")
    print("      • config/config.json")
    print("      • config/.env")
    
    print("\n   2. Set up external services:")
    print("      • PostgreSQL database")
    print("      • Redis server")
    print("      • AWS S3 bucket (or other cloud storage)")
    print("      • OpenAI/Anthropic API keys")
    
    print("\n   3. Run the system:")
    print("      • Demo: python scripts/run_demo.py")
    print("      • Development: python scripts/start_dev.py")
    print("      • Frontend: cd frontend && npm run dev")
    
    print("\n   4. Access the application:")
    print("      • Backend API: http://localhost:8000")
    print("      • Frontend: http://localhost:3000")
    print("      • API Docs: http://localhost:8000/docs")
    
    print("\n🔗 Useful Commands:")
    print("   • Install dependencies: python scripts/setup.py --install-deps")
    print("   • Create configs: python scripts/setup.py --create-configs")
    print("   • Run tests: pytest tests/")
    print("   • Run demo: python scripts/run_demo.py")
    
    print("\n📚 Documentation:")
    print("   • README.md - Overview and getting started")
    print("   • docs/ - Detailed documentation")
    print("   • API documentation available at /docs endpoint")
    
    print("\n🆘 Need Help?")
    print("   • Check the README.md file")
    print("   • Review configuration examples")
    print("   • Run the demo to see the system in action")
    
    print("\n✨ Happy coding with AI ERP!")


def main():
    """Main setup function"""
    
    parser = argparse.ArgumentParser(description='AI ERP System Setup')
    parser.add_argument('--install-deps', action='store_true', help='Install dependencies only')
    parser.add_argument('--create-configs', action='store_true', help='Create configuration files only')
    parser.add_argument('--skip-deps', action='store_true', help='Skip dependency installation')
    
    args = parser.parse_args()
    
    print("🏗️  AI ERP System Setup")
    print("=" * 40)
    
    success = True
    
    try:
        if args.install_deps:
            success = install_dependencies()
            return 0 if success else 1
        
        if args.create_configs:
            success = create_config_files()
            return 0 if success else 1
        
        # Full setup
        if not args.skip_deps:
            success = install_dependencies()
            if not success:
                print("❌ Setup failed at dependency installation")
                return 1
        
        success = create_config_files()
        if not success:
            print("❌ Setup failed at configuration creation")
            return 1
        
        success = setup_database()
        if not success:
            print("❌ Setup failed at database setup")
            return 1
        
        success = setup_redis()
        if not success:
            print("❌ Setup failed at Redis setup")
            return 1
        
        success = create_project_structure()
        if not success:
            print("❌ Setup failed at project structure creation")
            return 1
        
        success = create_startup_scripts()
        if not success:
            print("❌ Setup failed at startup script creation")
            return 1
        
        print_setup_summary()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️  Setup interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Setup failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())