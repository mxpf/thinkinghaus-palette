"""Regenerate the distributable palette files from thinkinghaus.tokens.json."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def exports(data):
    primitives = {f'{family}-{stop}': value
                  for family, scale in data['scales'].items() for stop, value in scale.items()}
    primitives.update(data['fills'])
    aliases = data['anchorAliases']
    css = f'/* Thinkinghaus palette v{data["version"]}. */\n:root {{\n'
    css += ''.join(f'  --th-{name}: {value};\n' for name, value in primitives.items())
    css += ''.join(f'  --th-{name}: var(--th-{ref});\n' for name, ref in aliases.items()) + '}\n'
    for mode, roles in data['modes'].items():
        css += (':root, [data-theme="dark"]' if mode == 'dark' else '[data-theme="light"]') + ' {\n'
        css += f'  color-scheme: {mode};\n'
        css += ''.join(f'  --th-{name}: var(--th-{ref});\n' for name, ref in roles.items())
        for blog, role in [('background', 'bg'), ('foreground', 'text'), ('body', 'text-body'), ('muted', 'text-muted')]:
            css += f'  --blog-{blog}: var(--th-{role});\n'
        css += '}\n'

    def token(value, description):
        return {'value': value, 'type': 'color', 'description': description}

    figma = {'primitives': {'palette': {
        name: token(value, f'CSS: var(--th-{name})') for name, value in primitives.items()}}}
    figma['primitives']['palette'].update({
        name: token('{palette.' + ref + '}', f'Original Thinkinghaus {name}; CSS: var(--th-{name})')
        for name, ref in aliases.items()})
    for mode, roles in data['modes'].items():
        figma[mode] = {'color': {
            name: token('{palette.' + ref + '}', f'{mode.title()} mode; CSS: var(--th-{name})')
            for name, ref in roles.items()}}
    figma['$themes'] = [{'id': f'thinkinghaus-{mode}', 'name': mode.title(), 'group': 'Color',
                         'selectedTokenSets': {'primitives': 'source', mode: 'enabled'}}
                        for mode in data['modes']]
    figma['$metadata'] = {'tokenSetOrder': ['primitives', *data['modes']]}

    # Preserve the established terminal's typography and spacing; every color has a token.
    ansi = ['neutral-850', 'clay-solid', 'moss-solid', 'ochre-solid', 'slate-600', 'heather-600',
            'patina-solid', 'neutral-400', 'neutral-700', 'clay-400', 'moss-400', 'ochre-400',
            'slate-400', 'heather-400', 'patina-400', 'neutral-0']
    ghostty = f'''# Ghosttyhaus — Thinkinghaus palette v{data['version']}
# https://keeping.haus/thinkinghaus-palette/
# Window
window-padding-x = 20
window-padding-y = 20

# Typography (Paper Mono is installed separately)
font-family = "Paper Mono"
font-size = 15
adjust-cell-height = 10%

# neutral-1000 / neutral-0
background = {primitives['neutral-1000']}
foreground = {primitives['neutral-0']}
'''
    for i, ref in enumerate(ansi):
        ghostty += f'\n# {ref}\npalette = {i}={primitives[ref]}\n'
    for name, ref in [('selection-background', 'neutral-700'), ('selection-foreground', 'neutral-0'),
                      ('cursor-color', 'clay-400'), ('cursor-text', 'neutral-1000')]:
        ghostty += f'\n# {ref}\n{name} = {primitives[ref]}\n'
    return {'thinkinghaus.css': css, 'thinkinghaus.figma.json': json.dumps(figma, indent=2) + '\n',
            'ghosttyhaus.conf': ghostty}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed exports are stale')
    args = parser.parse_args()
    data = json.loads((ROOT / 'thinkinghaus.tokens.json').read_text())
    for name, value in exports(data).items():
        if args.check:
            if (ROOT / name).read_text() != value:
                raise SystemExit(f'Stale export: {name}; run python3 palette/export.py')
        else:
            (ROOT / name).write_text(value)
    print('Palette exports match.' if args.check else 'Palette exports generated.')
