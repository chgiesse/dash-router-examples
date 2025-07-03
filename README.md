# Dash Router Examples

A Dash application with advanced routing capabilities using dash-router.

## Docker Setup

This project includes Docker configurations for both development and production environments.

### Development

To run the application in development mode with hot reloading:

```bash
# Start development environment
docker-compose --profile dev up

# Or build and run manually
docker build -f Dockerfile.dev -t dash-dev .
docker run -p 8050:8050 -v $(pwd):/app dash-dev
```

The development server will be available at `http://localhost:8050` with debug mode enabled.

### Production

To run the application in production mode with Gunicorn:

```bash
# Start production environment
docker-compose --profile prod up

# Or build and run manually
docker build -t dash-prod .
docker run -p 8050:8050 dash-prod
```

### Local Development (without Docker)

If you prefer to run the application locally:

```bash
# Install dependencies
poetry install

# Run the application
python dash_app.py
```

## Features

- **Advanced Routing**: Uses dash-router for complex nested routing
- **Mantine Components**: Modern UI components with dash-mantine-components
- **Data Visualization**: Plotly integration for charts and graphs
- **Caching**: Redis-based caching with aiocache
- **Database**: PostgreSQL support with SQLAlchemy
- **Responsive Design**: Mobile-friendly layouts

## Project Structure

```
├── dash_app.py          # Main Dash application (standard Flask)
├── app.py              # Alternative Flash-based application (async)
├── dash_pages/         # Page components and routing
├── global_components/  # Shared UI components
├── assets/            # Static assets (CSS, JS, images)
├── api/               # API endpoints and database models
├── Dockerfile         # Production Docker configuration
├── Dockerfile.dev     # Development Docker configuration
└── docker-compose.yaml # Multi-service orchestration
```

## Environment Variables

Create a `.env` file for local development:

```env
# Database
POSTGRES_PASSWORD=your_password
REDIS_HOST=localhost
REDIS_PASSWORD=your_redis_password

# Application
FLASK_ENV=development
DASH_DEBUG=true
```

## Dependencies

The project uses Poetry for dependency management. Key dependencies include:

- `dash`: Core Dash framework
- `dash-router`: Advanced routing capabilities
- `dash-mantine-components`: Modern UI components
- `gunicorn`: Production WSGI server
- `redis`: Caching and session storage
- `sqlalchemy`: Database ORM
- `plotly`: Data visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 