"""
Flask application for choir seating chart generation.
"""

import csv
import io
import json
import base64
from flask import Flask, render_template, request, redirect, url_for, flash

from seating_algorithm import (
    Singer, generate_seating_chart, get_unique_parts,
    calculate_dimensions_with_user_input, generate_random_roster
)

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # For flash messages


@app.route('/', methods=['GET'])
def index():
    """Display the upload form."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """Handle CSV upload and show configuration page."""
    if 'file' not in request.files:
        flash('No file uploaded')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file')
        return redirect(url_for('index'))

    try:
        content = file.read().decode('utf-8')
        singers = parse_csv(content)

        if not singers:
            flash('No valid singers found in CSV')
            return redirect(url_for('index'))

        return show_configure_page(singers)

    except Exception as e:
        flash(f'Error processing file: {str(e)}')
        return redirect(url_for('index'))


@app.route('/generate-random', methods=['POST'])
def generate_random():
    """Generate a random roster and show configuration page."""
    try:
        num_singers = int(request.form.get('num_singers', 40))
        parts_str = request.form.get('parts', 'Soprano,Alto,Tenor,Bass')
        parts = [p.strip() for p in parts_str.split(',') if p.strip()]

        if num_singers < 1 or num_singers > 500:
            flash('Number of singers must be between 1 and 500')
            return redirect(url_for('index'))

        if not parts:
            flash('Please specify at least one voice part')
            return redirect(url_for('index'))

        singers = generate_random_roster(num_singers, parts)
        return show_configure_page(singers)

    except Exception as e:
        flash(f'Error generating roster: {str(e)}')
        return redirect(url_for('index'))


def show_configure_page(singers: list[Singer]):
    """Show the configuration page for a list of singers."""
    parts = get_unique_parts(singers)
    singers_data = [
        {'name': s.name, 'voice_part': s.voice_part, 'height': s.height}
        for s in singers
    ]
    singers_json = base64.b64encode(json.dumps(singers_data).encode()).decode()

    return render_template('configure.html',
                           parts=parts,
                           num_singers=len(singers),
                           singers_data=singers_json)


@app.route('/preview', methods=['POST'])
def preview():
    """Generate chart and go directly to edit page."""
    try:
        chart_data = generate_chart_from_form()
        # Default staggered to true for new charts
        chart_data['staggered'] = True
        return render_template('edit.html', **chart_data)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error generating chart: {str(e)}')
        return redirect(url_for('index'))


@app.route('/edit', methods=['POST'])
def edit():
    """Show editable seating chart with drag/drop."""
    try:
        chart_data = get_chart_data_from_form()
        return render_template('edit.html', **chart_data)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error loading editor: {str(e)}')
        return redirect(url_for('index'))


@app.route('/finalize', methods=['POST'])
def finalize():
    """Show finalized seating chart for viewing/download."""
    try:
        chart_data = get_chart_data_from_form()
        return render_template('finalize.html', **chart_data)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error finalizing chart: {str(e)}')
        return redirect(url_for('index'))


def generate_chart_from_form() -> dict:
    """Parse form data and generate a new seating chart."""
    singers_json = request.form.get('singers_data', '')
    singers_data = json.loads(base64.b64decode(singers_json).decode())
    singers = [Singer(**s) for s in singers_data]

    layout = request.form.get('layout', 'side-by-side')
    part_order_str = request.form.get('part_order', '')
    part_order = [p.strip() for p in part_order_str.split(',') if p.strip()]

    if not part_order:
        raise ValueError('Please specify voice part order')

    # Check for variable row sizes first
    row_sizes_str = request.form.get('row_sizes', '').strip()
    if row_sizes_str:
        # Parse variable row sizes (back to front)
        row_sizes = [int(s.strip()) for s in row_sizes_str.split(',') if s.strip()]
        rows = len(row_sizes)
        seats_per_row = max(row_sizes)  # For chart allocation
        chart = generate_seating_chart(singers, rows, seats_per_row, part_order, layout, row_sizes)
    else:
        # Get optional row/seat configuration
        rows_str = request.form.get('rows', '').strip()
        max_per_row_str = request.form.get('max_per_row', '').strip()

        user_rows = int(rows_str) if rows_str else None
        user_max_per_row = int(max_per_row_str) if max_per_row_str else None

        rows, seats_per_row = calculate_dimensions_with_user_input(
            len(singers), len(part_order), layout, user_rows, user_max_per_row
        )
        chart = generate_seating_chart(singers, rows, seats_per_row, part_order, layout)

    # Get display options
    flipped = request.form.get('flipped') == 'true'
    staggered = request.form.get('staggered') == 'true'
    curved = request.form.get('curved') == 'true'

    # Get aisle position
    aisle_str = request.form.get('aisle_after', '').strip()
    aisle_after = int(aisle_str) if aisle_str else None

    # Prepare data for templates
    chart_json = encode_chart(chart)

    return {
        'chart': chart,
        'chart_data': chart_json,
        'num_singers': len(singers),
        'part_order': part_order,
        'layout': layout,
        'rows': rows,
        'seats_per_row': seats_per_row,
        'flipped': flipped,
        'staggered': staggered,
        'curved': curved,
        'aisle_after': aisle_after,
        'singers_data': request.form.get('singers_data', '')
    }


def get_chart_data_from_form() -> dict:
    """Get chart data from form (either from chart_data or regenerate)."""
    chart_json = request.form.get('chart_data', '')

    if chart_json:
        # Decode existing chart
        chart = decode_chart(chart_json)
    else:
        # Regenerate chart
        return generate_chart_from_form()

    part_order_str = request.form.get('part_order', '')
    part_order = [p.strip() for p in part_order_str.split(',') if p.strip()]
    flipped = request.form.get('flipped') == 'true'
    staggered = request.form.get('staggered') == 'true'
    curved = request.form.get('curved') == 'true'
    aisle_str = request.form.get('aisle_after', '').strip()
    aisle_after = int(aisle_str) if aisle_str else None

    return {
        'chart': chart,
        'chart_data': chart_json,
        'num_singers': int(request.form.get('num_singers', 0)),
        'part_order': part_order,
        'layout': request.form.get('layout', 'side-by-side'),
        'rows': len(chart),
        'seats_per_row': len(chart[0]) if chart else 0,
        'curved': curved,
        'aisle_after': aisle_after,
        'flipped': flipped,
        'staggered': staggered,
        'singers_data': request.form.get('singers_data', '')
    }


def encode_chart(chart) -> str:
    """Encode a chart to JSON string for form storage."""
    data = []
    for row in chart:
        row_data = []
        for seat in row:
            if seat.singer:
                row_data.append({
                    'row': seat.row,
                    'position': seat.position,
                    'singer': {
                        'name': seat.singer.name,
                        'voice_part': seat.singer.voice_part,
                        'height': seat.singer.height
                    }
                })
            else:
                row_data.append({
                    'row': seat.row,
                    'position': seat.position,
                    'singer': None
                })
        data.append(row_data)
    return base64.b64encode(json.dumps(data).encode()).decode()


def decode_chart(chart_json: str):
    """Decode a chart from JSON string."""
    from seating_algorithm import Seat
    data = json.loads(base64.b64decode(chart_json).decode())
    chart = []
    for row_data in data:
        row = []
        for seat_data in row_data:
            singer = None
            if seat_data.get('singer'):
                singer = Singer(**seat_data['singer'])
            row.append(Seat(
                row=seat_data['row'],
                position=seat_data['position'],
                singer=singer
            ))
        chart.append(row)
    return chart


def parse_csv(content: str) -> list[Singer]:
    """
    Parse CSV content into Singer objects.
    Accepts any voice_part values and supports decimal heights.
    """
    singers = []
    reader = csv.DictReader(io.StringIO(content))

    for row in reader:
        try:
            name = row.get('name', '').strip()
            voice_part = row.get('voice_part', '').strip()
            height_str = row.get('height', '').strip()

            if not name or not voice_part or not height_str:
                continue

            height = float(height_str)
            singers.append(Singer(name=name, voice_part=voice_part, height=height))

        except (ValueError, KeyError):
            continue

    return singers


if __name__ == '__main__':
    app.run(debug=True)