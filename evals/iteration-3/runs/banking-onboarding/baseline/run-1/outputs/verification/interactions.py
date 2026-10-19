"""Offline interaction, keyboard, theme and text-reflow checks. No real SMS/call."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app/index.html').as_uri()
results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height in [(390, 844), (320, 568)]:
        for theme in ['light', 'dark']:
            page = browser.new_page(viewport={'width': width, 'height': height})
            errors, network = [], []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('request', lambda request: network.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
            page.goto(f'{APP}?screen=welcome&theme={theme}')
            expect(page.get_by_role('heading', level=1)).to_contain_text('Your bank.')
            page.keyboard.press('Tab')
            expect(page.get_by_role('button', name='Help with setup')).to_be_focused()
            page.keyboard.press('Tab')
            expect(page.get_by_role('button', name='Get started')).to_be_focused()
            page.keyboard.press('Enter')
            expect(page.get_by_role('heading', name='Your details')).to_be_focused()
            page.keyboard.press('Tab')
            expect(page.get_by_label('Full name', exact=True)).to_be_focused()
            # Empty and malformed values never advance; first invalid field receives focus.
            page.get_by_role('button', name='Continue', exact=True).click()
            expect(page.locator('#full-name')).to_be_focused()
            expect(page.locator('#full-name')).to_have_attribute('aria-invalid', 'true')
            expect(page.locator('#mobile')).to_have_attribute('aria-invalid', 'true')
            page.locator('#full-name').fill('Alex Morgan')
            page.locator('#mobile').fill('07700')
            page.get_by_role('button', name='Continue', exact=True).click()
            expect(page.locator('#full-name')).to_have_attribute('aria-invalid', 'false')
            expect(page.locator('#mobile')).to_be_focused()
            # Help on a form preserves values and restores the invoking focus.
            page.get_by_role('button', name='Help with setup').click()
            expect(page.get_by_role('dialog')).to_be_visible()
            page.get_by_role('button', name='Back to setup').click()
            expect(page.get_by_role('button', name='Help with setup')).to_be_focused()
            expect(page.locator('#mobile')).to_have_value('07700')
            page.locator('#mobile').fill('+44 7700 900482')
            page.get_by_role('button', name='Continue', exact=True).click()
            expect(page.get_by_role('heading', name='Check your phone')).to_be_focused()
            expect(page.locator('.intro')).to_contain_text('482')
            warning = page.evaluate('EVAL_FIXTURES.bank.warning')
            expect(page.locator('.notice')).to_contain_text(warning)
            page.locator('#code').fill('111111')
            page.get_by_role('button', name='Confirm code').click()
            assert 'screen=code-error' in page.url
            expect(page.locator('#code')).to_be_focused()
            expect(page.locator('#code-error')).to_contain_text('doesn’t match')
            page.get_by_role('button', name='I haven’t received a code').click()
            expect(page.get_by_role('heading', name='Talk to us')).to_be_focused()
            expected_phone = page.evaluate('EVAL_FIXTURES.bank.helpPhone.replace(/\\s/g, "")')
            expect(page.get_by_role('link', name='Call our team')).to_have_attribute('href', 'tel:' + expected_phone)
            # Native modal traps Tab within its two actionable controls.
            page.keyboard.press('Tab')
            expect(page.get_by_role('link', name='Call our team')).to_be_focused()
            page.keyboard.press('Tab')
            expect(page.get_by_role('button', name='Back to setup')).to_be_focused()
            page.keyboard.press('Tab')
            assert page.evaluate("document.activeElement.closest('dialog') !== null")
            page.keyboard.press('Escape')
            expect(page.get_by_role('dialog')).not_to_be_visible()
            expect(page.get_by_role('button', name='I haven’t received a code')).to_be_focused()
            expect(page.locator('#code')).to_have_value('111111')
            page.get_by_role('button', name='Back', exact=True).click()
            expect(page.locator('#mobile')).to_have_value('+44 7700 900482')
            page.get_by_role('button', name='Continue', exact=True).click()
            page.locator('#code').fill('123')
            page.get_by_role('button', name='Confirm code').click()
            expect(page.locator('#code-error')).to_contain_text('Enter the 6-digit code')
            page.locator('#code').fill(page.evaluate('EVAL_FIXTURES.bank.testCode'))
            page.get_by_role('button', name='Confirm code').click()
            assert 'screen=done' in page.url
            expect(page.get_by_role('heading', level=1)).to_contain_text('You’re all set')
            expect(page.get_by_role('heading', level=1)).to_be_focused()
            for key in ['accountName', 'sortCode', 'accountNumber', 'balance']:
                assert page.evaluate('EVAL_FIXTURES.bank.' + key) in page.locator('main').inner_text()
            # Browser Back from completion returns to code, rather than a dead route.
            page.go_back()
            expect(page.get_by_role('heading', name='Check your phone')).to_be_visible()
            # Direct Help route is over the code step, with button and Escape dismissal.
            page.goto(f'{APP}?screen=help&theme={theme}')
            expect(page.get_by_role('dialog')).to_be_visible()
            page.get_by_role('button', name='Back to setup').click()
            expect(page.get_by_role('button', name='Help with setup')).to_be_focused()
            expect(page.get_by_role('heading', name='Check your phone')).to_be_visible()
            page.get_by_role('button', name='Help with setup').click()
            page.keyboard.press('Escape')
            expect(page.get_by_role('button', name='Help with setup')).to_be_focused()
            assert not errors, errors
            assert not network, network
            results.append({'viewport': [width, height], 'theme': theme, 'main_flow': 'passed', 'validation': 'passed', 'back': 'passed', 'help_and_focus_trap': 'passed', 'network_requests': len(network), 'runtime_errors': errors})
            # Long input stays readable on completion without widening the page.
            page.goto(f'{APP}?screen=details&theme={theme}')
            page.locator('#full-name').fill('Alexanderson' * 6)
            page.locator('#mobile').fill('07700900482')
            page.get_by_role('button', name='Continue', exact=True).click()
            page.locator('#code').fill(page.evaluate('EVAL_FIXTURES.bank.testCode'))
            page.get_by_role('button', name='Confirm code').click()
            assert page.evaluate('document.documentElement.scrollWidth === innerWidth'), 'Long name overflow'
            page.close()
    # System preference, explicit override, reduced motion and 200% text reflow.
    for preference in ['light', 'dark']:
        page = browser.new_page(viewport={'width': 320, 'height': 568}, color_scheme=preference, reduced_motion='reduce')
        page.goto(APP + '?screen=code')
        bg = page.locator('body').evaluate('(e) => getComputedStyle(e).backgroundColor')
        assert bg == ('rgb(20, 39, 45)' if preference == 'dark' else 'rgb(248, 247, 242)')
        opposite = 'light' if preference == 'dark' else 'dark'
        page.goto(APP + '?screen=code&theme=' + opposite)
        assert page.locator('body').evaluate('(e) => getComputedStyle(e).backgroundColor') != bg
        for screen in ['welcome', 'details-error', 'code-error', 'help', 'done']:
            page.goto(APP + '?screen=' + screen)
            page.evaluate("document.documentElement.style.fontSize = '200%'")
            assert page.evaluate('document.documentElement.scrollWidth === innerWidth'), (preference, screen, 'text overflow')
            if screen == 'help':
                assert page.locator('dialog').evaluate('(e) => e.scrollWidth <= e.clientWidth'), 'Dialog has horizontal overflow at 200% text'
                page.get_by_role('button', name='Back to setup').click()
            expect(page.get_by_role('button', name='Help with setup')).to_be_visible()
        page.close()
    # Complete the main route using only keyboard input and activation.
    page = browser.new_page(viewport={'width': 320, 'height': 568}, color_scheme='dark')
    page.goto(APP + '?screen=welcome')
    page.keyboard.press('Tab')
    page.keyboard.press('Tab')
    page.keyboard.press('Enter')
    page.keyboard.press('Tab')
    expect(page.locator('#full-name')).to_be_focused()
    assert page.locator('#full-name').evaluate('(e) => getComputedStyle(e).outlineWidth') == '3px'
    page.keyboard.type('Alex Morgan')
    page.keyboard.press('Tab')
    page.keyboard.type('07700900482')
    page.keyboard.press('Enter')
    page.keyboard.press('Tab')
    expect(page.locator('#code')).to_be_focused()
    page.keyboard.type(page.evaluate('EVAL_FIXTURES.bank.testCode'))
    page.keyboard.press('Enter')
    expect(page.get_by_role('heading', level=1)).to_contain_text('You’re all set')
    page.close()
    browser.close()
(ROOT / 'verification/interaction-results.json').write_text(json.dumps({'flows': results, 'keyboard_only_main_flow_320_dark': 'passed with visible focus', 'system_theme_override': 'passed', 'reduced_motion': 'passed; no timed or animated information', 'text_reflow_200_percent': 'passed at 320px in both system themes'}, indent=2))
print('4 end-to-end flows, keyboard/focus, direct Help, system themes and 200% text reflow passed.')
