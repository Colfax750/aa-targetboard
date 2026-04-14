# AA Target Board

A Target Board plugin for [Alliance Auth](https://allianceauth.readthedocs.io/) — track EVE Online structure and sovereignty targets with priority, status, timers, and update notes.

## Features

- Track structure targets (Astrahus, Fortizar, Keepstar, etc.), sovereignty, POCOs, and more
- Set objective (Reinforce, Final, Defend, Other), priority (1–5), and status
- Record timer windows (start and final)
- Post threaded updates/comments on each target
- Filter and sort the target list
- Permission-based access control integrated with Alliance Auth

## Installation

### 1. Install the package

```bash
pip install aa-targetboard
```

Or install directly from a local copy or GitHub:

```bash
pip install /path/to/aa-targetboard
# or
pip install git+https://github.com/your-org/aa-targetboard.git
```

### 2. Add to `INSTALLED_APPS`

In your Alliance Auth project's `local.py` settings file, add:

```python
INSTALLED_APPS += [
    "aa_targetboard",
]
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Restart services

```bash
supervisorctl restart myauth:
```

## Permissions

| Permission | Description |
|---|---|
| `aa_targetboard.view_target` | View the target list and target details |
| `aa_targetboard.add_target` | Create new targets |
| `aa_targetboard.change_target` | Edit any target (creators can always edit their own) |
| `aa_targetboard.delete_target` | Delete targets |

Assign these in the Alliance Auth admin panel under **Authentication → Groups**.

## Changelog

### 1.0.0
- Initial release
