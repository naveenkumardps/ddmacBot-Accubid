# Labor Factoring Table Documentation

## Overview

The `project_lbfac` table has been successfully created with all the Labor Factoring fields and proper foreign key relationships to the `users` and `projects` tables.

## Table Structure

### Foreign Keys
- `project_id` → `projects.id` (required)
- `user_id` → `users.id` (required)

### Labor Factoring Fields
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `project_id` | Integer | Foreign key to projects table |
| `user_id` | Integer | Foreign key to users table |
| `labor_factoring` | Text | Type of labor factoring (e.g., "Direct Labor", "Indirect Labor") |
| `factor` | Text | Labor factor multiplier |
| `percent_of_direct_hrs` | Text | Percentage of direct hours |
| `hours` | Text | Number of hours |
| `rate` | Text | Hourly rate |
| `sub_total` | Text | Subtotal calculation |
| `brdn_percent` | Text | Burden percentage |
| `frng` | Text | Fringe amount |
| `brdn_total` | Text | Total burden amount |
| `frng_total` | Text | Total fringe amount |
| `total` | Text | Total amount |
| `full_rate` | Text | Full rate including all factors |
| `code` | Text | Labor code |
| `type` | Text | Labor type |
| `created_at` | DateTime | Creation timestamp (auto) |
| `updated_at` | DateTime | Last update timestamp (auto) |

## Sample Data

The table has been populated with 5 sample Labor Factoring records:

1. **Direct Labor** (Project: Website Redesign, User: admin)
   - Factor: 1.25
   - Hours: 40
   - Rate: $25.00
   - Total: $1,300.00
   - Code: DL001

2. **Indirect Labor** (Project: Website Redesign, User: john_doe)
   - Factor: 1.15
   - Hours: 8
   - Rate: $20.00
   - Total: $192.00
   - Code: IL001

3. **Overtime Labor** (Project: Mobile App Development, User: jane_smith)
   - Factor: 1.5
   - Hours: 10
   - Rate: $30.00
   - Total: $420.00
   - Code: OT001

4. **Supervision** (Project: Mobile App Development, User: admin)
   - Factor: 1.35
   - Hours: 6
   - Rate: $35.00
   - Total: $260.40
   - Code: SUP001

5. **Specialty Labor** (Project: Database Migration, User: john_doe)
   - Factor: 1.4
   - Hours: 12
   - Rate: $40.00
   - Total: $652.80
   - Code: SPL001

## Usage Examples

### Creating a New Labor Factoring Record
```python
from src.database import SessionLocal
from src.models import ProjectLbfac

db = SessionLocal()
try:
    new_lbfac = ProjectLbfac(
        project_id=1,
        user_id=1,
        labor_factoring="Direct Labor",
        factor="1.25",
        percent_of_direct_hrs="100",
        hours="40",
        rate="25.00",
        sub_total="1000.00",
        brdn_percent="15",
        frng="150.00",
        brdn_total="150.00",
        frng_total="150.00",
        total="1300.00",
        full_rate="32.50",
        code="DL001",
        type="Direct"
    )
    db.add(new_lbfac)
    db.commit()
finally:
    db.close()
```

### Querying Labor Factoring Records
```python
# Get all labor factoring records for a specific project
lbfac_records = db.query(ProjectLbfac).filter(ProjectLbfac.project_id == 1).all()

# Get all labor factoring records created by a specific user
user_lbfac = db.query(ProjectLbfac).filter(ProjectLbfac.user_id == 1).all()

# Get records with specific labor type
direct_labor = db.query(ProjectLbfac).filter(
    ProjectLbfac.type == "Direct"
).all()
```

## Database Status

- **Table Created**: ✅ Yes (project_lbfac)
- **Foreign Keys**: ✅ Properly configured
- **Sample Data**: ✅ 5 records added
- **Migration Applied**: ✅ Version 8355f29da39e

## Available Scripts

- `python check_mysql_tables.py` - View all tables and data
- `python add_sample_lbfac_data.py` - Add sample Labor Factoring data
- `python manage_migrations.py status` - Check migration status

## Field Mapping

The table fields correspond to the following Labor Factoring columns:
- **Labor Factoring** → `labor_factoring`
- **Factor** → `factor`
- **% of Direct Hrs** → `percent_of_direct_hrs`
- **Hours** → `hours`
- **Rate $** → `rate`
- **SubTotal** → `sub_total`
- **Brdn %** → `brdn_percent`
- **Frng $** → `frng`
- **Brdn Tot.** → `brdn_total`
- **Frng Tot.** → `frng_total`
- **Total** → `total`
- **Full Rate** → `full_rate`
- **Code** → `code`
- **Type** → `type` 