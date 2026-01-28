# Environment Setup

## Virtual Environment Setup

This project uses a Python virtual environment to manage dependencies. Follow these steps to set up your development environment:

### 1. Activate the Virtual Environment

```bash
# Navigate to the project directory
cd /Users/muhammadfariskamal/RayyAI/rayyai-backend1/rayyai-backend

# Activate the virtual environment
source venv/bin/activate

# Or use the provided script
./activate_env.sh
```

### 2. Install Dependencies

```bash
# Dependencies should already be installed, but if needed:
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
# Check Python version
python --version

# Check SQLAlchemy installation
python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"
```

### 4. IDE Configuration

The project includes VS Code settings (`.vscode/settings.json`) that configure:
- Python interpreter path to use the virtual environment
- Terminal activation of the virtual environment
- Analysis paths for proper import resolution

### 5. Troubleshooting

If you're still seeing import errors in your IDE:

1. **Restart your IDE** after setting up the virtual environment
2. **Select the correct Python interpreter** in your IDE:
   - In VS Code: `Cmd+Shift+P` → "Python: Select Interpreter" → Choose `./venv/bin/python`
3. **Verify the virtual environment is activated** in your terminal:
   - You should see `(venv)` in your terminal prompt
   - Run `which python` to confirm it points to the venv

### 6. Running the Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the FastAPI application
uvicorn main:app --reload
```

## Database Setup

The project uses Alembic for database migrations. The `alembic/env.py` file is configured to work with the virtual environment and should resolve import issues once the environment is properly activated.
