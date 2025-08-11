import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas.calculation import (
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse
)
from app.models.calculation import Power, Root

def test_create_calculation_valid():
    """Test creating a valid CalculationCreate schema."""
    data = {
        "type": "addition",
        "inputs": [5.5, 2.5],
        "user_id": uuid4()
    }
    calc = CalculationCreate(**data)
    assert calc.type == "addition"
    assert calc.inputs == [5.5, 2.5]
    assert calc.user_id is not None

def test_create_calculation_missing_type():
    """Test CalculationCreate fails if 'type' is missing."""
    data = {
        "inputs": [7.2, 1.8],
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    # Look for a substring that indicates a missing required field.
    assert "required" in str(exc_info.value).lower()

def test_create_calculation_missing_inputs():
    """Test CalculationCreate fails if 'inputs' is missing."""
    data = {
        "type": "multiplication",
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    assert "required" in str(exc_info.value).lower()

def test_create_calculation_invalid_inputs():
    """Test CalculationCreate fails if 'inputs' is not a list of floats."""
    data = {
        "type": "division",
        "inputs": 123,
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    error_message = str(exc_info.value)
    # Ensure that our custom error message is present (case-insensitive)
    assert "input should be a valid list" in error_message.lower(), error_message

def test_create_calculation_unsupported_type():
    """Test CalculationCreate fails if an unsupported calculation type is provided."""
    data = {
        "type": "cube_root",  # Unsupported type
        "inputs": [8],
        "user_id": uuid4()
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    error_message = str(exc_info.value).lower()
    # Check that the error message indicates the value is not permitted.
    assert "one of" in error_message or "not a valid" in error_message

def test_update_calculation_valid():
    """Test a valid partial update with CalculationUpdate."""
    data = {
        "inputs": [15.0, 3.0]
    }
    calc_update = CalculationUpdate(**data)
    assert calc_update.inputs == [15.0, 3.0]

def test_update_calculation_no_fields():
    """Test that an empty update is allowed (i.e., no fields)."""
    calc_update = CalculationUpdate()
    assert calc_update.inputs is None

def test_response_calculation_valid():
    """Test creating a valid CalculationResponse schema."""
    data = {
        "id": uuid4(),
        "user_id": uuid4(),
        "type": "multiplication",
        "inputs": [6, 7],
        "result": 42.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    calc_response = CalculationResponse(**data)
    assert calc_response.id is not None
    assert calc_response.user_id is not None
    assert calc_response.type == "multiplication"
    assert calc_response.inputs == [6, 7]
    assert calc_response.result == 42.0

# Power tests

def test_power_get_result_chained():
    """Test Power.get_result with chained exponents."""
    values = [2, 3, 2]  # 2 ** 3 ** 2 = 2 ** 9 = 512
    power = Power(user_id=uuid4(), inputs=values)
    assert power.get_result() == 512

def test_power_invalid_inputs():
    """Test Power.get_result raises ValueError for invalid inputs."""
    power = Power(user_id=uuid4(), inputs=[5])
    with pytest.raises(ValueError, match="Power operation requires at least two numbers."):
        power.get_result()

def test_power_two_inputs():
    """Test Power.get_result with exactly two inputs."""
    power = Power(user_id=uuid4(), inputs=[2, 3])
    assert power.get_result() == 8

def test_power_three_inputs():
    """Test Power.get_result with three inputs ."""
    power = Power(user_id=uuid4(), inputs=[2, 3, 2])
    assert power.get_result() == 512

# Root tests

def test_root_get_result_chained():
    """Test Root.get_result with chained roots."""
    values = [16, 2, 2]  # sqrt(sqrt(16)) = sqrt(4) = 2
    root = Root(user_id=uuid4(), inputs=values)
    assert root.get_result() == 2

def test_root_invalid_inputs():
    """Test Root.get_result raises ValueError for invalid inputs."""
    root = Root(user_id=uuid4(), inputs=[9])
    with pytest.raises(ValueError, match="Root operation requires at least two numbers."):
        root.get_result()

def test_root_degree_zero():
    """Test Root.get_result raises ValueError when root degree is zero."""
    root = Root(user_id=uuid4(), inputs=[9, 0])
    with pytest.raises(ValueError, match="Root degree cannot be zero."):
        root.get_result()

