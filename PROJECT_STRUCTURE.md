# Project Structure

```
smart-cloud-ai/
├── app/                          # Main application directory
│   ├── ai/                       # AI processing modules
│   │   ├── enhanced_processor.py # Multi-provider AI processor
│   │   ├── openai_client.py      # OpenAI API integration
│   │   ├── simple_ai_client.py   # Lightweight AI client
│   │   ├── query.py              # File querying system
│   │   └── tagging.py            # File tagging system
│   ├── auth/                     # Authentication modules
│   │   ├── auth_handler.py       # JWT token handling
│   │   ├── auth_routes.py        # Auth endpoints
│   │   └── dependencies.py       # Auth dependencies
│   ├── model/                    # Database models
│   │   ├── file.py              # File metadata model
│   │   ├── share.py             # Shared links model
│   │   └── user.py              # User model
│   ├── tasks/                    # Background tasks
│   │   └── file_tasks.py        # File processing tasks
│   ├── utils/                    # Utility functions
│   │   └── auth_utils.py        # Authentication utilities
│   ├── database.py               # Database configuration
│   ├── main.py                   # FastAPI application
│   └── worker.py                 # Celery worker configuration
├── uploaded_files/               # File storage directory
│   └── .gitkeep                 # Maintains directory in git
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── AI_FEATURES.md               # AI capabilities documentation
├── PROJECT_STRUCTURE.md         # This file
├── run.py                       # Application startup script
├── .gitignore                   # Git ignore rules
└── cloudai.db                   # SQLite database (auto-generated)
```

## Key Components

### AI System (`app/ai/`)
- **enhanced_processor.py**: Main AI orchestrator with multiple providers
- **openai_client.py**: OpenAI GPT integration
- **simple_ai_client.py**: Lightweight rule-based AI
- **query.py**: Document querying functionality
- **tagging.py**: Automatic file tagging

### Authentication (`app/auth/`)
- JWT-based authentication
- User registration and login
- Protected endpoints

### Models (`app/model/`)
- **file.py**: File metadata and AI analysis results
- **share.py**: Shared file links
- **user.py**: User accounts

### Background Processing (`app/tasks/`)
- Celery tasks for AI processing
- Asynchronous file analysis

## File Storage

Files are stored in `uploaded_files/{user_id}/` directories, with metadata stored in the SQLite database.

## Database

Uses SQLite for simplicity, with tables for:
- Users
- File metadata
- Shared links
- AI analysis results 