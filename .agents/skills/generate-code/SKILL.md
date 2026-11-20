# Skill: generate-code

## Description
Load this skill when writing any code for the Ausbildung Automator project. This skill enforces ADR-0026 (Code Architecture Standard) and AGENTS.md patterns.

## When to Use
- Writing new Python or TypeScript code
- Modifying existing code
- Reviewing code for pattern compliance

## Instructions

### Pre-Generation Checklist

Before writing any code, answer these:

1. **State machine?** → Discriminated union with `kind` field. No nullable status fields.
2. **Domain ID?** → Branded type. Never bare strings.
3. **Configuration object?** → Builder pattern. Max 3 positional params.
4. **Data pipeline?** → Generator. No `results.append()`.
5. **Resource lifecycle?** → Context manager. No manual cleanup.
6. **Cross-cutting concern?** → Decorator. No `time.sleep` in business logic.
7. **Seam/interface?** → ABC. Import contract, not implementation.
8. **Computation?** → Pure function. No I/O.
9. **Data structure?** → `frozen=True` / `readonly`. Immutability default.
10. **Pattern match?** → Exhaustive cases. No wildcard `_`/`default`.

### Code Templates

#### Python Data Model (Use for any entity)

```python
from dataclasses import dataclass
from enum import Enum

class EntityKind(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass(frozen=True, slots=True)
class Active:
    kind: EntityKind = EntityKind.ACTIVE
    activated_at: str = ""

@dataclass(frozen=True, slots=True)
class Inactive:
    kind: EntityKind = EntityKind.INACTIVE
    deactivated_at: str = ""

EntityStatus = Active | Inactive
```

#### Python ABC (Use for any seam)

```python
from abc import ABC, abstractmethod

class ServiceAdapter(ABC):
    @abstractmethod
    async def fetch(self, query: str) -> list[dict]: ...

    @abstractmethod
    def health(self) -> str: ...
```

#### Python Generator Pipeline (Use for data processing)

```python
from collections.abc import Generator

def fetch_pages(url: str) -> Generator[bytes, None, None]:
    while True:
        data = request(url)
        if not data:
            break
        yield data

def parse(raw: Generator[bytes, None, None]) -> Generator[dict, None, None]:
    for page in raw:
        yield normalize(json.loads(page))

def filter(items: Generator[dict, None, None], criteria: dict) -> Generator[dict, None, None]:
    for item in items:
        if matches(item, criteria):
            yield item
```

#### TypeScript Discriminated Union (Use for any state)

```typescript
type EntityState =
  | { kind: "pending"; created_at: string }
  | { kind: "active"; activated_at: string }
  | { kind: "archived"; archived_at: string };

function stateLabel(state: EntityState): string {
  switch (state.kind) {
    case "pending": return "Pending";
    case "active": return "Active";
    case "archived": return "Archived";
  }
}
```

### Post-Generation Checklist

After writing code, verify:

- [ ] No `status: string` — used discriminated union
- [ ] No `id: str` — used branded type
- [ ] No `for x: results.append(x)` — used generator
- [ ] No `try/finally: close()` — used context manager
- [ ] No `import ConcreteClass` — imported ABC
- [ ] No `time.sleep` in business logic — used decorator
- [ ] No `match x: case _` — exhaustive cases
- [ ] All dataclasses `frozen=True`
- [ ] All TypeScript interfaces `readonly`
- [ ] No comments explaining what code does

### Forbidden Patterns

```python
# FORBIDDEN — mutable default
@dataclass
class Bad:
    items: list = []

# FORBIDDEN — bare string status
@dataclass
class Bad:
    status: str = "pending"

# FORBIDDEN — manual resource cleanup
session = create_session()
try:
    do_work(session)
finally:
    session.close()

# FORBIDDEN — append in loop
results = []
for item in items:
    results.append(transform(item))

# FORBIDDEN — sleep in business logic
def send_email(msg):
    time.sleep(45)
    gmail.send(msg)
```

### Test Generation Rules

- Scoring tests: pure function, known inputs/outputs, no mocks
- Adapter tests: fixture HTML → assert parsed fields
- Dispatcher tests: mock Gmail at HTTP boundary, assert throttling
- Every union variant has at least one test case
- No mock-of-internal — mock ABCs only
