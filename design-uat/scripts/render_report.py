#!/usr/bin/env python3
"""Render an inspected Design-UAT run as offline HTML and a text-safe CSV register.

Only local evidence inside the input JSON's directory is read. No network,
browser access, translation, issue detection or acceptance decisions occur here.
"""
import argparse
import base64
import csv
import html
import io
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import urlparse

KINDS = {
    'visual-defect': ('defect', 'UI defect'),
    'baseline-mismatch': ('mismatch', 'Baseline mismatch'),
    'design-clarification': ('clarify', 'Design clarification'),
}
TRACKING = {'owner': 'Unassigned', 'target_release': 'Not set',
            'implementation': 'Not assessed', 'retest': 'Not performed'}
REVIEW_DECISIONS = {'unreviewed', 'retain', 'exclude', 'accepted', 'merge', 'defer', 'design-update'}


def text(value, field, required=True):
    if value is None and not required:
        return ''
    if not isinstance(value, str) or (required and not value.strip()):
        raise ValueError(f'{field}: expected a nonempty string' if required else f'{field}: expected text')
    return value


def url(value, field):
    value = text(value, field)
    parsed = urlparse(value)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError(f'{field}: expected an HTTP(S) reference without embedded credentials')
    return value


def text_list(value, field, required=False):
    if not isinstance(value, list) or (required and not value) or not all(isinstance(x, str) and x.strip() for x in value):
        raise ValueError(f'{field}: expected a list of nonempty text')
    return value


def image_info(blob):
    if blob.startswith(b'\x89PNG\r\n\x1a\n') and len(blob) >= 24 and blob[12:16] == b'IHDR':
        return 'image/png', struct.unpack('>II', blob[16:24])
    if blob.startswith(b'\xff\xd8'):
        pos = 2
        while pos < len(blob):
            if blob[pos] != 255:
                pos += 1
                continue
            while pos < len(blob) and blob[pos] == 255:
                pos += 1
            if pos >= len(blob):
                break
            marker = blob[pos]
            pos += 1
            if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
                continue
            if marker == 0xDA or pos + 2 > len(blob):
                break
            size = int.from_bytes(blob[pos:pos + 2], 'big')
            if size < 2 or pos + size > len(blob):
                break
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF) and size >= 7:
                height, width = struct.unpack('>HH', blob[pos + 3:pos + 7])
                return 'image/jpeg', (width, height)
            pos += size
    if len(blob) >= 20 and blob[:4] == b'RIFF' and blob[8:12] == b'WEBP':
        pos = 12
        while pos + 8 <= len(blob):
            kind = blob[pos:pos + 4]
            size = int.from_bytes(blob[pos + 4:pos + 8], 'little')
            chunk = blob[pos + 8:pos + 8 + size]
            if len(chunk) != size:
                break
            if kind == b'VP8X' and size >= 10:
                return 'image/webp', (1 + int.from_bytes(chunk[4:7], 'little'), 1 + int.from_bytes(chunk[7:10], 'little'))
            if kind == b'VP8L' and size >= 5 and chunk[0] == 0x2F:
                bits = int.from_bytes(chunk[1:5], 'little')
                return 'image/webp', ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
            if kind == b'VP8 ' and size >= 10 and chunk[3:6] == b'\x9d\x01\x2a':
                return 'image/webp', (int.from_bytes(chunk[6:8], 'little') & 0x3FFF, int.from_bytes(chunk[8:10], 'little') & 0x3FFF)
            pos += 8 + size + (size % 2)
    raise ValueError('Evidence must be a recognizable PNG, JPEG or WebP image')


class Evidence:
    def __init__(self, root):
        self.root = root.resolve()
        self.images = {}
        self.sizes = {}
        self.paths = set()

    def add(self, value, field):
        value = text(value, field)
        path = Path(value)
        if path.is_absolute():
            raise ValueError(f'{field}: evidence path must be relative to the run directory')
        resolved = (self.root / path).resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError(f'{field}: evidence path escapes the run directory')
        if value not in self.images:
            if not resolved.is_file():
                raise ValueError(f'{field}: evidence file not found: {value}')
            blob = resolved.read_bytes()
            mime, size = image_info(blob)
            if min(size) <= 0:
                raise ValueError(f'{field}: image dimensions must be positive')
            self.images[value] = f'data:{mime};base64,' + base64.b64encode(blob).decode('ascii')
            self.sizes[value] = size
            self.paths.add(resolved)
        return value


def image_entries(value, field, evidence, required=True):
    if value is None and not required:
        return []
    if not isinstance(value, list) or (required and not value):
        raise ValueError(f'{field}: expected inspected image entries')
    result = []
    for i, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f'{field}[{i}]: expected an object')
        result.append({'path': evidence.add(item.get('path'), f'{field}[{i}].path'),
                       'caption': text(item.get('caption'), f'{field}[{i}].caption')})
    return result


def normalize(source, evidence):
    if not isinstance(source, dict):
        raise ValueError('Report input must be an object')
    out = dict(source)
    for key in ('title', 'project', 'review_date', 'scope'):
        text(out.get(key), key)
    for key in ('findings', 'coverage'):
        if not isinstance(out.get(key), list):
            raise ValueError(f'{key}: expected an array')
    out['stage'] = out.get('stage', 'review')
    if out['stage'] not in ('review', 'dev-handoff'):
        raise ValueError('stage: expected review or dev-handoff')
    review = out.get('design_review')
    if review is not None:
        if not isinstance(review, dict) or review.get('status') not in ('pending', 'confirmed'):
            raise ValueError('design_review: expected pending or confirmed status')
        review = dict(review)
        for key in ('date', 'source'):
            review[key] = text(review.get(key), f'design_review.{key}', review['status'] == 'confirmed')
        out['design_review'] = review
    if out['stage'] == 'dev-handoff' and (review is None or review['status'] != 'confirmed'):
        raise ValueError('dev-handoff requires recorded, confirmed design_review provenance')
    for key in ('language', 'timezone', 'revision', 'review_type', 'summary',
                'baseline_name', 'baseline_status', 'environment', 'priority_note', 'review_focus'):
        if key in out:
            text(out[key], key, required=False)
    for key in ('test_url', 'baseline_url'):
        if out.get(key):
            url(out[key], key)
    for key in ('limits', 'review_notes'):
        if key in out and (not isinstance(out[key], list) or not all(isinstance(x, str) for x in out[key])):
            raise ValueError(f'{key}: expected a list of text')
    defaults = out.get('tracking_defaults', {})
    if not isinstance(defaults, dict):
        raise ValueError('tracking_defaults: expected an object')
    out['tracking_defaults'] = dict(TRACKING)
    for k, v in defaults.items():
        if k not in TRACKING:
            raise ValueError(f'Unknown tracking field: {k}')
        out['tracking_defaults'][k] = text(v, f'tracking_defaults.{k}')
    findings, seen = [], set()
    for index, finding in enumerate(out['findings']):
        base = f'findings[{index}]'
        if not isinstance(finding, dict):
            raise ValueError(f'{base}: expected an object')
        f = dict(finding)
        for key in ('id', 'page', 'state', 'title', 'kind', 'action', 'actual',
                    'expected', 'evidence_basis', 'confidence', 'recommendation'):
            text(f.get(key), f'{base}.{key}')
        if f['id'] in seen:
            raise ValueError(f'Duplicate finding ID: {f["id"]}')
        seen.add(f['id'])
        if f['kind'] not in KINDS:
            raise ValueError(f'{base}.kind: unsupported finding kind')
        f['kind_class'], f['kind_label'] = KINDS[f['kind']]
        f['review_decision'] = text(f.get('review_decision', 'unreviewed'), f'{base}.review_decision')
        if f['review_decision'] not in REVIEW_DECISIONS:
            raise ValueError(f'{base}.review_decision: unsupported decision')
        if out['stage'] == 'dev-handoff' and f['review_decision'] != 'retain':
            raise ValueError(f'{base}: dev-handoff includes only designer-retained items')
        f['route_url'] = url(f['route_url'], f'{base}.route_url') if f.get('route_url') else ''
        f['context'] = text(f.get('context', ''), f'{base}.context', out['stage'] == 'dev-handoff')
        f['acceptance_criteria'] = text_list(f.get('acceptance_criteria', []), f'{base}.acceptance_criteria', out['stage'] == 'dev-handoff')
        if out['stage'] == 'dev-handoff' and not f['route_url']:
            raise ValueError(f'{base}.route_url: dev-handoff requires a direct test URL')
        f['follow_up_scope'] = f.get('follow_up_scope', 'current-review')
        if f['follow_up_scope'] not in ('current-review', 'existing-module'):
            raise ValueError(f'{base}.follow_up_scope: expected current-review or existing-module')
        f['priority'] = text(f.get('priority'), f'{base}.priority', False) or '—'
        for key in ('module', 'priority_note', 'scope_note'):
            f[key] = text(f.get(key, ''), f'{base}.{key}', False)
        if not isinstance(f.get('steps'), list) or not f['steps'] or not all(isinstance(x, str) and x.strip() for x in f['steps']):
            raise ValueError(f'{base}.steps: expected reproduction steps')
        f['images'] = image_entries(f.get('images'), f'{base}.images', evidence)
        f['capture'] = evidence.add(f.get('capture'), f'{base}.capture')
        refs = f.get('references', [])
        if not isinstance(refs, list):
            raise ValueError(f'{base}.references: expected an array')
        f['references'] = []
        for ri, ref in enumerate(refs):
            if not isinstance(ref, dict):
                raise ValueError(f'{base}.references[{ri}]: expected an object')
            f['references'].append({'label': text(ref.get('label'), f'{base}.references.label'),
                                    'url': url(ref.get('url'), f'{base}.references.url')})
        if f.get('compare') is not None:
            compare = f['compare']
            if not isinstance(compare, dict):
                raise ValueError(f'{base}.compare: expected an object')
            expected = evidence.add(compare.get('expected'), f'{base}.compare.expected')
            actual = evidence.add(compare.get('actual'), f'{base}.compare.actual')
            if evidence.sizes[expected] != evidence.sizes[actual]:
                raise ValueError(f'{base}.compare: unequal image bounds; align explicitly instead of stretching')
            f['compare'] = {'expected': expected, 'actual': actual,
                            'caption': text(compare.get('caption'), f'{base}.compare.caption')}
        tracking = dict(out['tracking_defaults'])
        overrides = f.get('tracking', {})
        if not isinstance(overrides, dict):
            raise ValueError(f'{base}.tracking: expected an object')
        for k, v in overrides.items():
            if k not in TRACKING:
                raise ValueError(f'{base}.tracking: unknown field {k}')
            tracking[k] = text(v, f'{base}.tracking.{k}')
        f['tracking'] = tracking
        findings.append(f)
    out['findings'] = findings
    coverage = []
    for index, case in enumerate(out['coverage']):
        base = f'coverage[{index}]'
        if not isinstance(case, dict):
            raise ValueError(f'{base}: expected an object')
        c = dict(case)
        for key in ('page', 'state', 'result', 'detail', 'status'):
            text(c.get(key), f'{base}.{key}')
        if c['status'] not in ('observed', 'blocked', 'not-reviewed'):
            raise ValueError(f'{base}.status: expected observed, blocked or not-reviewed')
        c['images'] = image_entries(c.get('images', []), f'{base}.images', evidence,
                                    required=c['status'] == 'observed')
        coverage.append(c)
    out['coverage'] = coverage
    if not findings and not coverage and not out.get('limits'):
        raise ValueError('No findings or coverage: supply a review limitation instead of an unsupported verdict')
    if out.get('format_reference'):
        ref = out['format_reference']
        if not isinstance(ref, dict):
            raise ValueError('format_reference: expected an object')
        out['format_reference'] = {'label': text(ref.get('label'), 'format_reference.label'),
                                   'url': url(ref.get('url'), 'format_reference.url')}
    return out


def csv_safe(value):
    value = str(value)
    return "'" + value if value.lstrip(' \t\r\n').startswith(('=', '+', '-', '@')) else value


def make_csv(report):
    buf = io.StringIO(newline='')
    writer = csv.writer(buf)
    writer.writerow(['ID', 'Module', 'Page', 'State', 'Type', 'Priority', 'Actual result',
                     'Expected result', 'Next action', 'Owner', 'Target release',
                     'Implementation', 'Retest', 'References', 'Scope note',
                     'Direct test URL', 'Location / context', 'Acceptance criteria',
                     'Follow-up scope', 'Review decision'])
    for f in report['findings']:
        t = f['tracking']
        writer.writerow(map(csv_safe, [f['id'], f.get('module', ''), f['page'], f['state'],
            f['kind_label'], f['priority'], f['actual'], f['expected'], f['recommendation'],
            t['owner'], t['target_release'], t['implementation'], t['retest'],
            '\n'.join(r['url'] for r in f['references']), f['scope_note'], f['route_url'],
            f['context'], '\n'.join(f['acceptance_criteria']), f['follow_up_scope'], f['review_decision']]))
    return '\ufeff' + buf.getvalue()


def make_checklist(report):
    if not any(f['acceptance_criteria'] for f in report['findings']):
        return None
    buf = io.StringIO(newline='')
    writer = csv.writer(buf)
    writer.writerow(['ID', 'Module', 'Page', 'Direct test URL', 'Location / context',
                     'Acceptance criterion', 'Priority', 'Owner', 'Target release', 'Retest'])
    for f in report['findings']:
        for criterion in f['acceptance_criteria']:
            writer.writerow(map(csv_safe, [f['id'], f.get('module', ''), f['page'],
                f['route_url'], f['context'], criterion, f['priority'], f['tracking']['owner'],
                f['tracking']['target_release'], f['tracking']['retest']]))
    return '\ufeff' + buf.getvalue()


def build(report, evidence, csv_text):
    e = lambda s: html.escape(str(s), quote=True)
    def link(value, label):
        return f'<a href="{e(value)}" target="_blank" rel="noreferrer">{e(label)} ↗</a>'
    def picture(path, caption):
        return f'<figure><img src="{evidence.images[path]}" alt="{e(caption)}" data-zoom loading="lazy"><figcaption>{e(caption)}</figcaption></figure>'
    findings = report['findings']
    counts = {k: sum(f['kind'] == k for f in findings) for k in KINDS}
    rows = ''
    for i, f in enumerate(findings):
        priority_class = 'p1' if f['priority'] in ('P0', 'P1') else ''
        location = ' / '.join(v for v in (f['module'], f['page']) if v)
        scope_label = ' · Existing module follow-up' if f['follow_up_scope'] == 'existing-module' else ''
        rows += f'''<tr data-issue="{e(f['id'])}" data-kind="{f['kind_class']}" class="{'selected' if i == 0 else ''}"><td><button class="issue-link" data-select="{e(f['id'])}" aria-pressed="{'true' if i == 0 else 'false'}">{e(f['id'])}</button></td><td><strong>{e(location)}</strong><small>{e(f['state'])}</small></td><td><strong>{e(f['title'])}</strong><small>{e(f['kind_label'] + scope_label)}</small></td><td><span class="priority {priority_class}">{e(f['priority'])}</span></td><td><span class="action {f['kind_class']}">{e(f['action'])}</span></td></tr>'''
    filters = ''
    if findings:
        labels = [('all', f'All {len(findings)}')] + [(KINDS[k][0], f'{KINDS[k][1]} {v}') for k, v in counts.items() if v]
        filters = '<div class="filters" aria-label="Filter findings">' + ''.join(
            f'<button data-filter="{kind}" aria-pressed="{str(kind == "all").lower()}">{e(label)}</button>' for kind, label in labels) + '</div>'
    coverage = ''
    for c in report['coverage']:
        result_class = '' if c['status'] == 'observed' else 'coverage-pending'
        coverage += f'''<details class="coverage-item"><summary><span><b>{e(c['page'])} <span class="muted">/ {e(c['state'])}</span></b><small>{e(c['detail'])}</small></span><span class="coverage-result {result_class}">{e(c['result'])}</span></summary>{''.join(picture(im['path'], im['caption']) for im in c['images'])}</details>'''
    if not coverage:
        coverage = '<p class="muted">No reviewed states recorded. See the limitations below.</p>'
    reference = report.get('format_reference')
    reference_html = '<p>Report organization informed by ' + link(reference['url'], reference['label']) + '; this is not an implicit UI design baseline.</p>' if reference else ''
    focus = '<div class="callout">' + e(report['review_focus']) + '</div>' if report.get('review_focus') else ''
    summary = report.get('summary') or f'{len(findings)} findings in the recorded review scope. Inspect the evidence and coverage before making acceptance decisions.'
    payload = json.dumps({'issues': findings, 'images': evidence.images}, ensure_ascii=False)
    payload = payload.replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    context_lists = lambda key: '<ul>' + ''.join('<li>' + e(v) + '</li>' for v in report.get(key, [])) + '</ul>'
    replacements = {
        'TITLE': e(report['title']), 'LANG': e(report.get('language', 'en')),
        'PROJECT': e(report['project']), 'REVISION': e(report.get('revision', 'Initial review')),
        'SUMMARY': e(summary), 'SCOPE': e(report['scope']),
        'DATE': e(report['review_date']), 'REVIEW_TYPE': e(report.get('review_type', 'AI-assisted visual review')),
        'BASELINE': link(report['baseline_url'], report.get('baseline_name') or 'Design reference') if report.get('baseline_url') else e(report.get('baseline_name') or 'Reference not supplied'),
        'BASELINE_STATUS': e(report.get('baseline_status') or 'Baseline acceptance/version status not confirmed'),
        'ENVIRONMENT': link(report['test_url'], 'Test environment') if report.get('test_url') else 'See recorded scope',
        'ENVIRONMENT_NOTE': e(report.get('environment') or 'See captured state details'),
        'STAGE_LABEL': 'Developer handoff' if report['stage'] == 'dev-handoff' else 'Review draft',
        'DESIGN_REVIEW': ('<p class="review-status">Design review confirmed · ' + e(report['design_review']['date']) + '</p>') if report.get('design_review', {}).get('status') == 'confirmed' else '',
        'CSV_URI': 'data:text/csv;charset=utf-8;base64,' + base64.b64encode(csv_text.encode()).decode(),
        'COUNT': str(len(findings)), 'FOCUS': focus, 'FILTERS': filters, 'ROWS': rows,
        'PRIORITY_NOTE': e(report.get('priority_note') or 'Priority and follow-up status are proposals unless explicitly confirmed.'),
        'EMPTY': '' if findings else '<p class="empty-review">No findings recorded. This does not imply acceptance of unreviewed or blocked states.</p>',
        'DETAIL_HIDDEN': '' if findings else 'hidden', 'COVERAGE': coverage,
        'LIMITS': context_lists('limits'), 'NOTES': context_lists('review_notes'),
        'FORMAT_REFERENCE': reference_html, 'PAYLOAD': payload,
    }
    template = (Path(__file__).resolve().parent.parent / 'assets' / 'report.html').read_text(encoding='utf-8')
    keys = set(re.findall(r'@@([A-Z_]+)@@', template))
    if keys - replacements.keys():
        raise ValueError(f'Unknown report template keys: {sorted(keys - replacements.keys())}')
    return re.sub(r'@@([A-Z_]+)@@', lambda match: replacements[match[1]], template)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--csv', type=Path)
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args()
    try:
        src = args.report.resolve()
        evidence = Evidence(src.parent)
        report = normalize(json.loads(src.read_text(encoding='utf-8-sig')), evidence)
        if args.validate_only:
            print(json.dumps({'valid': True, 'findings': len(report['findings']), 'images': len(evidence.images)}))
            return
        output = (args.output or src.with_suffix('.html')).resolve()
        csv_path = (args.csv or output.parent / 'issue-register.csv').resolve()
        if output.suffix.lower() != '.html' or csv_path.suffix.lower() != '.csv':
            raise ValueError('Output extensions must be .html and .csv')
        if len({src, output, csv_path}) != 3 or output in evidence.paths or csv_path in evidence.paths:
            raise ValueError('Output files must not overwrite report input or evidence')
        csv_text = make_csv(report)
        checklist_text = make_checklist(report)
        checklist_path = (output.parent / 'acceptance-checklist.csv').resolve()
        if checklist_text is not None and (checklist_path in {src, output, csv_path} or checklist_path in evidence.paths):
            raise ValueError('Acceptance checklist must not overwrite input, evidence or another output')
        result = build(report, evidence, csv_text)
        output.parent.mkdir(parents=True, exist_ok=True)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result, encoding='utf-8')
        csv_path.write_text(csv_text, encoding='utf-8')
        if checklist_text is not None:
            checklist_path.write_text(checklist_text, encoding='utf-8')
        print(json.dumps({'report': str(output), 'register': str(csv_path),
                          'checklist': str(checklist_path) if checklist_text is not None else None,
                          'findings': len(report['findings']), 'images': len(evidence.images),
                          'html_bytes': len(result.encode())}))
    except (ValueError, OSError, KeyError, struct.error) as exc:
        print(f'Design UAT report: {exc}', file=sys.stderr)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
