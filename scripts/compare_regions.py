#!/usr/bin/env python3
"""Pair inspected screenshot regions at native scale; optionally annotate boxes.

Requires Pillow. Makes no similarity/defect judgement and never resizes sources.
Crop and mark coordinates are x,y,width,height. Writes a provenance sidecar.
"""
import argparse
import json
from pathlib import Path
import sys


def box_value(raw):
    try:
        box = tuple(int(v.strip()) for v in raw.split(','))
        if len(box) != 4 or min(box) < 0 or min(box[2:]) <= 0:
            raise ValueError
        return box
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Use nonnegative x,y and positive width,height') from exc


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('expected', type=Path)
    p.add_argument('actual', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--expected-crop', type=box_value)
    p.add_argument('--actual-crop', type=box_value)
    p.add_argument('--expected-label', default='Expected / design')
    p.add_argument('--actual-label', default='Actual / browser')
    p.add_argument('--marks', type=Path)
    args = p.parse_args()
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        p.exit(2, 'Pillow is unavailable. Use a supported local runtime or another inspected comparison tool.\n')
    try:
        output = args.output.resolve()
        sidecar = output.with_suffix('.json')
        sources = {args.expected.resolve(), args.actual.resolve()}
        if args.marks:
            sources.add(args.marks.resolve())
        if output in sources or sidecar in sources or output == sidecar:
            raise ValueError('Outputs must not overwrite source files')
        if output.suffix.lower() != '.png':
            raise ValueError('Comparison output must use .png')
        images, provenance = {}, {}
        for side in ('expected', 'actual'):
            path, crop = getattr(args, side), getattr(args, side + '_crop')
            with Image.open(path) as source:
                source.load()
                rgba = source.convert('RGBA')
            original = rgba.size
            if crop:
                x, y, width, height = crop
                if x + width > rgba.width or y + height > rgba.height:
                    raise ValueError(f'{side} crop extends beyond the source image')
                rgba = rgba.crop((x, y, x + width, y + height))
            white = Image.new('RGBA', rgba.size, 'white')
            white.alpha_composite(rgba)
            images[side] = white.convert('RGB')
            provenance[side] = {'source': str(path), 'source_size': list(original),
                                'crop': list(crop) if crop else None, 'region_size': list(rgba.size)}
        font = ImageFont.load_default()
        marks = json.loads(args.marks.read_text(encoding='utf-8')) if args.marks else []
        if not isinstance(marks, list):
            raise ValueError('Marks must be an array')
        for mark in marks:
            if not isinstance(mark, dict) or mark.get('side') not in images:
                raise ValueError('Each mark needs side expected or actual')
            box, label = mark.get('box'), mark.get('label', '')
            if not isinstance(box, list) or len(box) != 4 or not all(type(v) is int for v in box):
                raise ValueError('Each mark box must contain integer x,y,width,height')
            x, y, width, height = box
            im = images[mark['side']]
            if min(box) < 0 or min(width, height) <= 0 or x + width > im.width or y + height > im.height:
                raise ValueError('Mark extends beyond its cropped region')
            if not isinstance(label, str):
                raise ValueError('Mark label must be text')
            draw = ImageDraw.Draw(im)
            draw.rectangle((x, y, x + width - 1, y + height - 1), outline='#c6492d', width=3)
            if label:
                bounds = draw.textbbox((0, 0), label, font=font)
                label_width = min(im.width - x, bounds[2] - bounds[0] + 10)
                top = max(0, y - 19)
                draw.rectangle((x, top, x + label_width, top + 18), fill='#c6492d')
                draw.text((x + 5, top + 2), label, font=font, fill='white')
        left, right = images['expected'], images['actual']
        margin, gap, heading = 20, 24, 44
        canvas = Image.new('RGB', (left.width + right.width + margin * 2 + gap,
                                  max(left.height, right.height) + heading + margin), '#f0f3f7')
        draw = ImageDraw.Draw(canvas)
        draw.text((margin, 15), args.expected_label, font=font, fill='#172a40')
        draw.text((margin + left.width + gap, 15), args.actual_label, font=font, fill='#172a40')
        canvas.paste(left, (margin, heading))
        canvas.paste(right, (margin + left.width + gap, heading))
        provenance.update({'scale': 1, 'resized': False, 'marks': marks,
                           'output_size': list(canvas.size)})
        output.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output)
        sidecar.write_text(json.dumps(provenance, indent=2), encoding='utf-8')
        print(json.dumps({'image': str(output), 'provenance': str(sidecar), 'scale': 1}))
    except (ValueError, OSError) as exc:
        p.exit(2, f'Design UAT comparison: {exc}\n')


if __name__ == '__main__':
    main()
