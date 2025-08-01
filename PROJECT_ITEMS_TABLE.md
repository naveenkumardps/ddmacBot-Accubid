# Project Ext Table Documentation

## Overview

The `project_ext` table has been successfully created with all the requested fields and proper foreign key relationships to the `users` and `projects` tables.

## Table Structure

### Foreign Keys
- `project_id` → `projects.id` (required)
- `user_id` → `users.id` (required)

### Core Fields
| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `id` | Integer | Primary key | Yes |
| `project_id` | Integer | Foreign key to projects table | Yes |
| `user_id` | Integer | Foreign key to users table | Yes |
| `description` | Text | Item description | Yes |
| `quantity` | Float | Item quantity | No (default: 1.0) |
| `date` | DateTime | Item date | No (default: current timestamp) |

### Pricing Information
| Field | Type | Description |
|-------|------|-------------|
| `trade_price` | Float | Trade price |
| `price_unit` | String(50) | Price unit (e.g., "month", "year", "one-time") |
| `discount_percent` | Float | Discount percentage (default: 0.0) |
| `link_price` | Float | Link price |
| `cost_adjustment_percent` | Float | Cost adjustment percentage (default: 0.0) |
| `net_cost` | Float | Net cost |

### Labor Information
| Field | Type | Description |
|-------|------|-------------|
| `db_labor` | Float | Database labor cost |
| `labor` | Float | Labor cost |
| `labor_unit` | String(50) | Labor unit |
| `labor_adjustment_percent` | Float | Labor adjustment percentage (default: 0.0) |

### Totals
| Field | Type | Description |
|-------|------|-------------|
| `total_material` | Float | Total material cost |
| `total_hours` | Float | Total hours |

### Conditions
| Field | Type | Description |
|-------|------|-------------|
| `material_condition` | String(100) | Material condition |
| `labor_condition` | String(100) | Labor condition |

### Weight Information
| Field | Type | Description |
|-------|------|-------------|
| `weight` | Float | Item weight |
| `weight_unit` | String(20) | Weight unit |
| `total_weight` | Float | Total weight |

### Manufacturer & Catalog
| Field | Type | Description |
|-------|------|-------------|
| `manufacturer_name` | String(200) | Manufacturer name |
| `catalog_number` | String(100) | Catalog number |
| `price_code` | String(50) | Price code |
| `reference` | String(200) | Reference information |

### Supplier Information
| Field | Type | Description |
|-------|------|-------------|
| `supplier_name` | String(200) | Supplier name |
| `supplier_code` | String(100) | Supplier code |

### Sort Codes (8 fields)
| Field | Type | Description |
|-------|------|-------------|
| `sort_code_1` to `sort_code_8` | String(100) | Sort codes for categorization |

### Quick Takeoff
| Field | Type | Description |
|-------|------|-------------|
| `quick_takeoff_code` | String(100) | Quick takeoff code |

### Timestamps
| Field | Type | Description |
|-------|------|-------------|
| `created_at` | DateTime | Creation timestamp (auto) |
| `updated_at` | DateTime | Last update timestamp (auto) |

## Relationships

### With Projects Table
```python
# One-to-Many: Project → ProjectExt
project = db.query(Project).first()
project_items = project.project_items  # List of all items for this project
```

### With Users Table
```python
# One-to-Many: User → ProjectExt
user = db.query(User).first()
user_items = user.project_items  # List of all items created by this user
```

## Sample Data

The table has been populated with 5 sample project items:

1. **Premium Web Hosting Package** (Project: Website Redesign, User: admin)
   - Trade Price: $99.99/month
   - Discount: 10%
   - Net Cost: $89.99
   - Manufacturer: HostGator

2. **SSL Certificate** (Project: Website Redesign, User: john_doe)
   - Trade Price: $49.99/year
   - Net Cost: $49.99
   - Manufacturer: DigiCert

3. **iOS Developer License** (Project: Mobile App Development, User: jane_smith)
   - Trade Price: $99.00/year
   - Net Cost: $99.00
   - Manufacturer: Apple Inc.

4. **Android Developer License** (Project: Mobile App Development, User: admin)
   - Trade Price: $25.00 (one-time)
   - Net Cost: $25.00
   - Manufacturer: Google

5. **Database Backup Service** (Project: Database Migration, User: john_doe)
   - Trade Price: $19.99/month
   - Quantity: 12
   - Discount: 15%
   - Net Cost: $203.87
   - Manufacturer: AWS

## Usage Examples

### Creating a New Project Item
```python
from src.database import SessionLocal
from src.models import ProjectItem

db = SessionLocal()
try:
    new_item = ProjectItem(
        project_id=1,
        user_id=1,
        description="New Item Description",
        quantity=2.0,
        trade_price=50.00,
        price_unit="piece",
        net_cost=100.00,
        manufacturer_name="Example Corp",
        supplier_name="Example Supplier"
    )
    db.add(new_item)
    db.commit()
finally:
    db.close()
```

### Querying Project Items
```python
# Get all items for a specific project
project_items = db.query(ProjectItem).filter(ProjectItem.project_id == 1).all()

# Get all items created by a specific user
user_items = db.query(ProjectItem).filter(ProjectItem.user_id == 1).all()

# Get items with specific manufacturer
manufacturer_items = db.query(ProjectItem).filter(
    ProjectItem.manufacturer_name == "HostGator"
).all()
```

## Database Status

- **Table Created**: ✅ Yes (project_ext)
- **Foreign Keys**: ✅ Properly configured
- **Sample Data**: ✅ 5 items added
- **Migration Applied**: ✅ Version 40d90b5672cb

## Available Scripts

- `python check_mysql_tables.py` - View all tables and data
- `python add_sample_project_items.py` - Add sample project items
- `python manage_migrations.py status` - Check migration status 