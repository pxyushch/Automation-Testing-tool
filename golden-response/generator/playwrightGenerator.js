function quote(value = '') {
  return JSON.stringify(String(value));
}

function lineForStep(step) {
  switch (step.type) {
    case 'goto':
      return `  await page.goto(${quote(step.url)});`;
    case 'click':
      return `  await page.locator(${quote(step.selector)}).click();`;
    case 'fill':
      return `  await page.locator(${quote(step.selector)}).fill(${quote(step.value)});`;
    case 'press':
      return `  await page.locator(${quote(step.selector)}).press(${quote(step.value || 'Enter')});`;
    case 'expectText':
      return `  await expect(page.locator(${quote(step.selector)})).toContainText(${quote(step.value)});`;
    case 'expectVisible':
      return `  await expect(page.locator(${quote(step.selector)})).toBeVisible();`;
    default:
      return `  // Unsupported step: ${quote(step.type)}`;
  }
}

export function generatePlaywright(steps = [], options = {}) {
  const name = options.name || 'recorded flow';
  const body = steps.length
    ? steps.map(lineForStep).join('\n')
    : '  // Add steps in AutoTest Recorder before running this test.';

  return `import { test, expect } from '@playwright/test';

test(${quote(name)}, async ({ page }) => {
${body}
});
`;
}
