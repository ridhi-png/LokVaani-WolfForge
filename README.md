# LokVaani - Multilingual Voice-First AI Platform

LokVaani is a cloud-native, multilingual voice-first AI platform that provides accessible digital content consumption through natural language interactions. The platform follows a microservices architecture with specialized components for voice processing, language handling, content simplification, and mobile-optimized delivery.

## Architecture

The platform consists of the following microservices:

- **Voice Processing Service**: Speech-to-text conversion, text-to-speech generation, and audio quality optimization
- **Language Processing Service**: Language detection, preference management, and translation coordination
- **Content Simplification Service**: Complex content analysis, simplification, and technical term explanation
- **Session Management Service**: User session lifecycle, conversation context, and preference persistence
- **API Gateway**: Centralized entry point with authentication, rate limiting, and request routing

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Redis
- PostgreSQL

### Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start services: `docker-compose up -d`
4. Run tests: `pytest`

### Environment Variables

Copy `.env.example` to `.env` and configure the following:

- `REDIS_URL`: Redis connection string
- `DATABASE_URL`: PostgreSQL connection string
- `GOOGLE_CLOUD_API_KEY`: Google Cloud API key for STT/TTS
- `OPENAI_API_KEY`: OpenAI API key for content simplification

## Project Structure

```
lokvaani/
├── services/
│   ├── voice_processing/     # Voice Processing Service
│   ├── language_processing/  # Language Processing Service
│   ├── content_simplification/ # Content Simplification Service
│   ├── session_management/   # Session Management Service
│   └── api_gateway/         # API Gateway
├── shared/
│   ├── models/              # Shared Pydantic models
│   ├── database/            # Database configuration
│   └── utils/               # Shared utilities
├── tests/                   # Test suites
├── docker/                  # Docker configurations
└── frontend/                # React frontend application
```

## Testing

The project uses a dual testing approach:

- **Unit Tests**: Specific examples and edge cases using pytest
- **Property-Based Tests**: Universal properties using Hypothesis

Run tests with: `pytest tests/`

## License

MIT License - see LICENSE file for details.