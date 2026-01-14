"""
Migration script to add new security columns to users table.

Run this script to update existing databases:
    python -m app.migrations.add_api_key_token
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.models.database import engine, Base, SessionLocal
from app.models.user import User


def migrate():
    """Add new columns to users table."""
    print("Starting migration: Add API key token and security columns...")

    # Get database connection
    with engine.connect() as conn:
        # Check if columns already exist
        result = conn.execute(text("PRAGMA table_info(users)"))
        existing_columns = {row[1] for row in result.fetchall()}

        # Add api_key_token column if not exists
        if 'api_key_token' not in existing_columns:
            print("Adding api_key_token column...")
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN api_key_token VARCHAR UNIQUE"
            ))
            conn.commit()
            print("✓ api_key_token column added")
        else:
            print("✓ api_key_token column already exists")

        # Add must_change_password column if not exists
        if 'must_change_password' not in existing_columns:
            print("Adding must_change_password column...")
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN must_change_password BOOLEAN DEFAULT 0"
            ))
            conn.commit()
            print("✓ must_change_password column added")
        else:
            print("✓ must_change_password column already exists")

        # Update default values for existing users
        db = SessionLocal()
        try:
            # Update default AI provider to deepseek for users with openai
            print("Updating default AI provider to deepseek...")
            db.query(User).filter(
                User.ai_provider == "openai",
                User.ai_model == "gpt-3.5-turbo"
            ).update({
                "ai_provider": "deepseek",
                "ai_model": "deepseek-chat"
            })
            db.commit()
            print("✓ Default AI provider updated to deepseek")

            # Set must_change_password for admin user with default password
            print("Setting password change requirement for admin...")
            admin = db.query(User).filter(User.username == "admin").first()
            if admin and admin.verify_password("admin123"):
                admin.must_change_password = True
                db.commit()
                print("✓ Admin user must change default password")
            else:
                print("✓ Admin password already changed or user not found")

        except Exception as e:
            print(f"Error updating users: {e}")
            db.rollback()
        finally:
            db.close()

    print("\nMigration completed successfully!")
    print("\nNOTE: If you're using PostgreSQL, you may need to run:")
    print("  ALTER TABLE users ADD COLUMN api_key_token VARCHAR UNIQUE;")
    print("  ALTER TABLE users ADD COLUMN must_change_password BOOLEAN DEFAULT FALSE;")


if __name__ == "__main__":
    migrate()
