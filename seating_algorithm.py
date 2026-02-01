"""
Seating algorithm for choir chart generation.
Places singers in straight rows based on voice part and height.
"""

import math
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Singer:
    name: str
    voice_part: str
    height: float  # in inches

    @property
    def height_display(self) -> str:
        """Return height formatted as feet'inches", supporting half inches."""
        feet = int(self.height // 12)
        remaining_inches = self.height % 12
        # Check if we have a half inch
        if remaining_inches % 1 == 0.5:
            return f"{feet}'{int(remaining_inches)}.5\""
        elif remaining_inches % 1 == 0:
            return f"{feet}'{int(remaining_inches)}\""
        else:
            # For other decimals, show one decimal place
            return f"{feet}'{remaining_inches:.1f}\""


@dataclass
class Seat:
    row: int
    position: int
    singer: Optional[Singer] = None


def generate_seating_chart(
    singers: List[Singer],
    rows: int,
    seats_per_row: int,
    part_order: List[str],
    layout: str = "side-by-side",
    row_sizes: Optional[List[int]] = None
) -> List[List[Seat]]:
    """
    Generate a seating chart for straight rows.

    Args:
        singers: List of Singer objects
        rows: Number of rows
        seats_per_row: Number of seats per row (max width)
        part_order: List of voice parts in left-to-right order
        layout: "side-by-side" (parts next to each other) or "stacked" (parts behind each other)
        row_sizes: Optional list of seats per row (back to front), overrides seats_per_row

    Returns:
        2D list of Seat objects (row 0 = back, row -1 = front)
    """
    # Group singers by voice part
    groups = {}
    for part in part_order:
        groups[part] = []

    for singer in singers:
        part = singer.voice_part
        if part in groups:
            groups[part].append(singer)

    # Sort each group by height (tallest first for back rows)
    for part in groups:
        groups[part].sort(key=lambda s: s.height, reverse=True)

    # Initialize empty chart with variable row sizes
    chart = []
    for r in range(rows):
        row_width = row_sizes[r] if row_sizes else seats_per_row
        row = []
        for p in range(row_width):
            row.append(Seat(row=r, position=p, singer=None))
        chart.append(row)

    if layout == "side-by-side":
        _place_side_by_side_variable(chart, groups, part_order, row_sizes) if row_sizes else _place_side_by_side(chart, groups, part_order, rows, seats_per_row)
    else:  # stacked
        _place_stacked(chart, groups, part_order, rows, seats_per_row)

    return chart


def _place_side_by_side(
    chart: List[List[Seat]],
    groups: dict,
    part_order: List[str],
    rows: int,
    seats_per_row: int
) -> None:
    """
    Place voice parts side by side (left to right) in columns.
    Each part gets a column width based on ceil(singers/rows).
    Parts are placed adjacently with no gaps.
    """
    num_parts = len(part_order)
    if num_parts == 0:
        return

    total_singers = sum(len(groups[part]) for part in part_order)
    if total_singers == 0:
        return

    # Calculate column width needed for each part (ceil of singers/rows)
    part_widths = []
    for part in part_order:
        count = len(groups[part])
        width = math.ceil(count / rows) if count > 0 else 0
        part_widths.append(width)

    # Total width needed
    total_width = sum(part_widths)

    # Center offset for the whole chart
    chart_offset = (seats_per_row - total_width) // 2

    # Place each part in its column
    current_pos = chart_offset
    for i, part in enumerate(part_order):
        part_width = part_widths[i]
        if part_width > 0:
            _place_section(chart, groups[part],
                           start_row=0, end_row=rows,
                           start_pos=current_pos, end_pos=current_pos + part_width)
            current_pos += part_width


def _place_side_by_side_variable(
    chart: List[List[Seat]],
    groups: dict,
    part_order: List[str],
    row_sizes: List[int]
) -> None:
    """
    Place voice parts side by side with variable row widths.
    Each part gets a strict column section - no mixing between parts.
    """
    num_parts = len(part_order)
    rows = len(row_sizes)
    if num_parts == 0 or rows == 0:
        return

    total_singers = sum(len(groups[part]) for part in part_order)
    if total_singers == 0:
        return

    # Calculate the proportion each part should take
    part_proportions = []
    for part in part_order:
        count = len(groups[part])
        proportion = count / total_singers if total_singers > 0 else 0
        part_proportions.append(proportion)

    # Create queues for each voice part (tallest first)
    queues = {part: list(groups[part]) for part in part_order}

    # For each row, divide it into sections for each part
    for row_idx in range(rows):
        row_width = row_sizes[row_idx]

        # Calculate how many seats each part gets in this row
        part_seats = []
        remaining_width = row_width
        for i, part in enumerate(part_order):
            if i == len(part_order) - 1:
                # Last part gets remaining width
                seats = remaining_width
            else:
                seats = round(row_width * part_proportions[i])
                seats = min(seats, remaining_width)
            part_seats.append(seats)
            remaining_width -= seats

        # Calculate starting position for each part (centered as a group)
        total_used = sum(part_seats)
        start_offset = (row_width - total_used) // 2

        # Place each part's singers in their section
        current_pos = start_offset
        for i, part in enumerate(part_order):
            section_width = part_seats[i]
            if section_width <= 0:
                continue

            # How many singers to place from this part in this row?
            # Distribute evenly across rows based on remaining singers
            remaining_rows = rows - row_idx
            remaining_singers = len(queues[part])
            if remaining_rows > 0 and remaining_singers > 0:
                # Place ceil(remaining/remaining_rows) but capped by section width
                to_place = min(section_width, math.ceil(remaining_singers / remaining_rows))

                # Center within the section
                section_offset = (section_width - to_place) // 2

                for j in range(to_place):
                    if queues[part]:
                        pos = current_pos + section_offset + j
                        if pos < len(chart[row_idx]):
                            chart[row_idx][pos].singer = queues[part].pop(0)

            current_pos += section_width


def _place_stacked(
    chart: List[List[Seat]],
    groups: dict,
    part_order: List[str],
    rows: int,
    seats_per_row: int
) -> None:
    """
    Place voice parts stacked (back to front).
    Parts are arranged in horizontal bands from back to front.
    """
    num_parts = len(part_order)
    if num_parts == 0:
        return

    # Divide rows among parts
    rows_per_part = rows // num_parts
    extra_rows = rows % num_parts

    current_row = 0
    for i, part in enumerate(part_order):
        # Give extra rows to back parts
        part_rows = rows_per_part + (1 if i < extra_rows else 0)
        end_row = current_row + part_rows

        _place_section(chart, groups[part],
                       start_row=current_row, end_row=end_row,
                       start_pos=0, end_pos=seats_per_row)
        current_row = end_row


def _place_section(chart: List[List[Seat]], singers: List[Singer],
                   start_row: int, end_row: int,
                   start_pos: int, end_pos: int) -> None:
    """
    Place a group of singers in a rectangular section of the chart.
    Fills from back row to front, centered within each row.
    """
    section_width = end_pos - start_pos
    num_rows = end_row - start_row
    total_singers = len(singers)

    if total_singers == 0 or section_width == 0 or num_rows == 0:
        return

    singer_idx = 0
    for row in range(start_row, end_row):
        # Calculate how many singers go in this row
        remaining = total_singers - singer_idx
        if remaining <= 0:
            break

        # Fill full rows, last row gets remainder
        rows_left = end_row - row
        if rows_left > 1:
            # Not the last row - try to fill evenly
            singers_this_row = min(section_width, math.ceil(remaining / rows_left))
        else:
            # Last row - place all remaining
            singers_this_row = min(section_width, remaining)

        # Calculate centering offset
        offset = (section_width - singers_this_row) // 2

        # Place singers centered in this row
        for i in range(singers_this_row):
            if singer_idx < total_singers:
                pos = start_pos + offset + i
                chart[row][pos].singer = singers[singer_idx]
                singer_idx += 1


def calculate_min_width(singers: List[Singer], part_order: List[str], rows: int) -> int:
    """
    Calculate the minimum seats_per_row needed for side-by-side layout.

    This accounts for per-part column widths which can exceed ceil(total/rows)
    due to cumulative rounding.
    """
    # Count singers per part
    part_counts = {part: 0 for part in part_order}
    for singer in singers:
        if singer.voice_part in part_counts:
            part_counts[singer.voice_part] += 1

    # Calculate width needed for each part
    total_width = 0
    for part in part_order:
        count = part_counts[part]
        width = math.ceil(count / rows) if count > 0 else 0
        total_width += width

    return total_width


def calculate_chart_dimensions(num_singers: int, num_parts: int, layout: str) -> tuple[int, int]:
    """
    Calculate reasonable row and seat counts for a given number of singers.

    Args:
        num_singers: Total number of singers
        num_parts: Number of voice parts
        layout: "side-by-side" or "stacked"

    Returns:
        Tuple of (rows, seats_per_row)
    """
    # Aim for roughly 10-15 singers per row
    target_per_row = 12
    rows = max(2, math.ceil(num_singers / target_per_row))

    if layout == "stacked":
        # Make rows divisible by num_parts for clean splits
        while rows % num_parts != 0:
            rows += 1

    seats_per_row = math.ceil(num_singers / rows)

    if layout == "side-by-side":
        # Make seats divisible by num_parts for clean splits
        while seats_per_row % num_parts != 0:
            seats_per_row += 1

    return rows, seats_per_row


def get_unique_parts(singers: List[Singer]) -> List[str]:
    """Extract unique voice parts from singers, preserving first-seen order."""
    seen = set()
    parts = []
    for singer in singers:
        if singer.voice_part not in seen:
            seen.add(singer.voice_part)
            parts.append(singer.voice_part)
    return parts


def calculate_dimensions_with_user_input(
    num_singers: int,
    num_parts: int,
    layout: str,
    user_rows: Optional[int] = None,
    user_max_per_row: Optional[int] = None
) -> tuple[int, int]:
    """
    Calculate chart dimensions, respecting user input where provided.

    Args:
        num_singers: Total number of singers
        num_parts: Number of voice parts
        layout: "side-by-side" or "stacked"
        user_rows: User-specified number of rows (optional)
        user_max_per_row: User-specified max per row (optional, blank = auto)

    Returns:
        Tuple of (rows, seats_per_row)
    """
    if user_rows and user_max_per_row:
        # User specified both - use as-is
        return user_rows, user_max_per_row

    if user_rows and not user_max_per_row:
        # User specified rows only - calculate seats per row
        seats_per_row = math.ceil(num_singers / user_rows)
        if layout == "side-by-side":
            while seats_per_row % num_parts != 0:
                seats_per_row += 1
        return user_rows, seats_per_row

    if user_max_per_row and not user_rows:
        # User specified max per row only - calculate rows
        rows = math.ceil(num_singers / user_max_per_row)
        if layout == "stacked":
            while rows % num_parts != 0:
                rows += 1
        return rows, user_max_per_row

    # Neither specified - auto calculate
    return calculate_chart_dimensions(num_singers, num_parts, layout)


def generate_random_roster(
    num_singers: int,
    parts: List[str],
    height_range: tuple[float, float] = (60, 78),
    distribution: Optional[List[int]] = None,
    seed: Optional[int] = None
) -> List[Singer]:
    """
    Generate a random roster of singers for testing.

    Args:
        num_singers: Number of singers to generate
        parts: List of voice parts to distribute among
        height_range: (min_height, max_height) in inches
        distribution: Optional list of counts per part (must sum to num_singers)
                     If None, distributes evenly with round-robin
        seed: Optional random seed for reproducibility

    Returns:
        List of Singer objects
    """
    import random

    if seed is not None:
        random.seed(seed)

    # Gendered first names based on voice part
    female_names = [
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
        "Jessica", "Sarah", "Karen", "Emma", "Ava", "Sophia", "Isabella", "Mia",
        "Charlotte", "Amelia", "Harper", "Evelyn", "Abigail", "Emily", "Ella",
        "Madison", "Scarlett", "Victoria", "Grace", "Chloe", "Lily", "Hannah",
        "Natalie", "Zoe", "Leah", "Hazel", "Violet", "Aurora", "Savannah",
        "Audrey", "Brooklyn", "Bella", "Claire", "Lucy", "Anna", "Caroline"
    ]

    male_names = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard",
        "Joseph", "Thomas", "Charles", "Oliver", "Elijah", "Lucas", "Mason",
        "Logan", "Alexander", "Ethan", "Jacob", "Liam", "Noah", "Aiden",
        "Benjamin", "Henry", "Sebastian", "Jack", "Daniel", "Matthew", "Owen",
        "Ryan", "Nathan", "Connor", "Andrew", "Isaac", "Joshua", "Dylan",
        "Luke", "Gabriel", "Anthony", "Christian", "Jonathan", "Samuel", "Eric"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
        "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
        "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green"
    ]

    def is_female_part(part: str) -> bool:
        """Determine if a voice part is typically female."""
        part_lower = part.lower()
        return any(p in part_lower for p in ['soprano', 'alto', 'mezzo'])

    def get_name(part: str) -> str:
        """Get a name appropriate for the voice part."""
        if is_female_part(part):
            first = random.choice(female_names)
        else:
            first = random.choice(male_names)
        return f"{first} {random.choice(last_names)}"

    singers = []
    min_h, max_h = height_range

    if distribution:
        # Use specified distribution
        for part_idx, count in enumerate(distribution):
            part = parts[part_idx % len(parts)]
            for _ in range(count):
                name = get_name(part)
                base_height = random.uniform(min_h, max_h)
                height = round(base_height * 2) / 2
                singers.append(Singer(name=name, voice_part=part, height=height))
    else:
        # Round-robin distribution
        for i in range(num_singers):
            part = parts[i % len(parts)]
            name = get_name(part)
            base_height = random.uniform(min_h, max_h)
            height = round(base_height * 2) / 2
            singers.append(Singer(name=name, voice_part=part, height=height))

    return singers