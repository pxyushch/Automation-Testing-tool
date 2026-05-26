export function generateSelector(element) {
  return {
    primary: `page.locator('${element.tagName.toLowerCase()}')`
  };
}
