import logging
import re
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("inventory.api")


def _format_json_syntax_error(raw_body: str, error_detail: str, pos: int | None) -> str:
    """Translates Python's JSONDecodeError into a clear message with field name, line & column."""
    # Look backward from the error position to find the closest JSON key (e.g., "product_name":)
    field_hint = ""
    if isinstance(pos, int) and raw_body:
        text_before = raw_body[:pos]
        key_matches = re.findall(r'"([^"]+)"\s*:', text_before)
        if key_matches:
            field_hint = f" for field '{key_matches[-1]}'"

    friendly_reason = error_detail
    if "Expecting value" in error_detail:
        friendly_reason = (
            f"Invalid or unquoted value{field_hint}. "
            "Wrap text values in double quotes (e.g., \"abcd\") or remove extra commas."
        )
    elif "Expecting property name enclosed in double quotes" in error_detail:
        friendly_reason = "Remove the trailing comma before '}' or enclose property names in double quotes."
    elif "Extra data" in error_detail:
        friendly_reason = "Extra characters or multiple JSON objects found after closing '}'."
    elif "Expecting ',' delimiter" in error_detail:
        friendly_reason = f"Missing a comma ',' after value{field_hint}."
    elif "Expecting ':' delimiter" in error_detail:
        friendly_reason = f"Missing a colon ':' after key{field_hint}."
    elif "Unterminated string" in error_detail:
        friendly_reason = f"Unclosed double quote '\"' in value{field_hint}."

    if isinstance(pos, int) and raw_body:
        line_no = raw_body.count("\n", 0, pos) + 1
        last_newline = raw_body.rfind("\n", 0, pos)
        col_no = pos - last_newline if last_newline != -1 else pos + 1
        return f"Invalid JSON at line {line_no}, column {col_no}: {friendly_reason}"

    return f"Invalid JSON format: {friendly_reason}"



def _format_pydantic_error(err: dict, field_name: str) -> str:
    """Converts Pydantic v2 error types into user-friendly sentences."""
    err_type = err.get("type", "")
    ctx = err.get("ctx", {})
    default_msg = err.get("msg", "Invalid value")

    # 1. Required / Empty
    if err_type == "missing":
        return f"'{field_name}' is required."

    # 2. Data Types
    if err_type == "string_type":
        return f"'{field_name}' must be a text string."
    if err_type in ("int_type", "int_parsing"):
        return f"'{field_name}' must be a valid whole number (integer)."
    if err_type in ("float_type", "float_parsing", "decimal_parsing"):
        return f"'{field_name}' must be a valid number."
    if err_type in ("bool_type", "bool_parsing"):
        return f"'{field_name}' must be true or false."
    if err_type == "list_type":
        return f"'{field_name}' must be a list/array."
    if err_type == "dict_type":
        return f"'{field_name}' must be a JSON object."

    # 3. Date & Time
    if err_type in ("date_parsing", "date_from_datetime_inexact"):
        return f"'{field_name}' must be a valid date (YYYY-MM-DD)."
    if err_type in ("datetime_parsing", "datetime_type"):
        return f"'{field_name}' must be a valid date and time (YYYY-MM-DD HH:MM:SS)."

    # 4. String Constraints
    if err_type == "string_too_short":
        min_len = ctx.get("min_length")
        return f"'{field_name}' must be at least {min_len} character(s) long."
    if err_type == "string_too_long":
        max_len = ctx.get("max_length")
        return f"'{field_name}' cannot exceed {max_len} character(s)."
    if err_type == "string_pattern_mismatch":
        return f"'{field_name}' format is invalid."

    # 5. Number Constraints
    if err_type == "greater_than":
        return f"'{field_name}' must be greater than {ctx.get('gt')}."
    if err_type == "greater_than_equal":
        return f"'{field_name}' must be at least {ctx.get('ge')}."
    if err_type == "less_than":
        return f"'{field_name}' must be less than {ctx.get('lt')}."
    if err_type == "less_than_equal":
        return f"'{field_name}' cannot exceed {ctx.get('le')}."

    # 6. Special Formats & Enums
    if "email" in err_type:
        return f"'{field_name}' must be a valid email address."
    if "url" in err_type:
        return f"'{field_name}' must be a valid URL."
    if err_type == "enum":
        expected = ctx.get("expected", "allowed values")
        return f"'{field_name}' must be one of: {expected}."
    if err_type == "extra_forbidden":
        return f"'{field_name}' is not an allowed field."

    # 7. Custom @field_validator ValueError
    if err_type == "value_error":
        clean = default_msg.replace("Value error, ", "")
        return f"'{field_name}': {clean}"

    return f"'{field_name}': {default_msg}."


def register_exception_handlers(app: FastAPI) -> None:
    """Registers all global request, validation, HTTP, and database exception handlers."""

    # -------------------------------------------------------------------------
    # 1. Request & JSON Validation Errors (400 / 422)
    # -------------------------------------------------------------------------
    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError):
        formatted_errors = []

        for err in exc.errors():
            # Handle broken JSON syntax before Pydantic field validation
            if err.get("type") == "json_invalid":
                raw_bytes = await request.body()
                raw_text = raw_bytes.decode("utf-8", errors="replace")
                detail = err.get("ctx", {}).get("error", "Invalid JSON format")
                loc = err.get("loc", ())
                pos = loc[1] if len(loc) > 1 and isinstance(loc[1], int) else None

                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "success": False,
                        "error_type": "JSON_SYNTAX_ERROR",
                        "message": _format_json_syntax_error(raw_text, detail, pos),
                    },
                )

            # Build dot-separated field path (skip 'body', 'query', 'path')
            loc_parts = [
                str(item) for item in err.get("loc", ()) if item not in ("body", "query", "path")
            ]
            field_name = ".".join(loc_parts) if loc_parts else "request"

            formatted_errors.append({
                "field": field_name,
                "message": _format_pydantic_error(err, field_name),
                "code": err.get("type"),
            })

        # Surface the first error message at the top level for quick UI display
        top_message = (
            formatted_errors[0]["message"]
            if len(formatted_errors) == 1
            else f"Validation failed on {len(formatted_errors)} field(s)."
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "success": False,
                "error_type": "VALIDATION_ERROR",
                "message": top_message,
                "errors": formatted_errors,
            },
        )

    # -------------------------------------------------------------------------
    # 2. Database Integrity Errors (Duplicate Row, Null Column, Foreign Key)
    # -------------------------------------------------------------------------
    @app.exception_handler(IntegrityError)
    async def db_integrity_handler(request: Request, exc: IntegrityError):
        raw_msg = str(exc.orig) if exc.orig else str(exc)
        lower_msg = raw_msg.lower()

        error_type = "DATABASE_INTEGRITY_ERROR"
        message = "Database constraint violation."
        column = None
        status_code = status.HTTP_409_CONFLICT

        # Duplicate / Unique Constraint
        if "unique" in lower_msg or "duplicate" in lower_msg:
            error_type = "DUPLICATE_ENTRY"
            pg_match = re.search(r"Key \((.*?)\)=\((.*?)\)", raw_msg)
            sqlite_match = re.search(r"UNIQUE constraint failed: \w+\.(\w+)", raw_msg)
            mysql_match = re.search(r"for key '(?:\w+\.)?(\w+)'", raw_msg)

            if pg_match:
                column, val = pg_match.group(1), pg_match.group(2)
                message = f"A record with {column} '{val}' already exists."
            elif sqlite_match:
                column = sqlite_match.group(1)
                message = f"Duplicate value for '{column}'. This record already exists."
            elif mysql_match:
                column = mysql_match.group(1)
                message = f"Duplicate entry for '{column}'. This record already exists."
            else:
                message = "This record already exists."

        # Not-Null Constraint
        elif "not null" in lower_msg or "cannot be null" in lower_msg:
            error_type = "NULL_COLUMN_ERROR"
            status_code = status.HTTP_400_BAD_REQUEST
            col_match = re.search(r'(?:column|failed: \w+\.)["\']?(\w+)["\']?', raw_msg, re.IGNORECASE)
            column = col_match.group(1) if col_match else None
            message = f"Required column '{column}' cannot be empty." if column else "A required database column was left empty."

        # Foreign Key Constraint
        elif "foreign key" in lower_msg:
            error_type = "FOREIGN_KEY_ERROR"
            status_code = status.HTTP_400_BAD_REQUEST
            pg_fk = re.search(r"Key \((.*?)\)=\((.*?)\)", raw_msg)
            if pg_fk:
                column, val = pg_fk.group(1), pg_fk.group(2)
                message = f"Invalid reference: '{column}' with value '{val}' does not exist."
            elif "delete" in lower_msg or "update" in lower_msg:
                message = "Cannot delete or update this record because other records depend on it."
            else:
                message = "Referenced parent record does not exist."

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error_type": error_type,
                "message": message,
                "column": column,
            },
        )
