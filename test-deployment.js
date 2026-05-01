/**
 * HF Space Deployment Validation Suite
 * Tests: HTML structure, links, SVG badge, descriptions, responsive design, accessibility
 */

const fs = require('fs');
const path = require('path');

// ANSI colors for output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  bold: '\x1b[1m'
};

const log = {
  pass: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  fail: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  warn: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  info: (msg) => console.log(`${colors.blue}ℹ${colors.reset} ${msg}`),
  section: (msg) => console.log(`\n${colors.bold}${colors.blue}=== ${msg} ===${colors.reset}`)
};

let passCount = 0;
let failCount = 0;
let warnCount = 0;

const assert = (condition, passMsg, failMsg) => {
  if (condition) {
    log.pass(passMsg);
    passCount++;
  } else {
    log.fail(failMsg);
    failCount++;
  }
};

// Read files
const indexPath = path.join('/home/user/.github', 'index.html');
const cydoniaPath = path.join('/home/user/.github', 'cydonia.html');

const indexContent = fs.readFileSync(indexPath, 'utf-8');
const cydoniaContent = fs.readFileSync(cydoniaPath, 'utf-8');

log.section('HTML STRUCTURE VALIDATION');

// Test DOCTYPE
assert(
  indexContent.includes('<!DOCTYPE html>'),
  'index.html has valid DOCTYPE',
  'index.html missing DOCTYPE'
);

assert(
  cydoniaContent.includes('<!DOCTYPE html>'),
  'cydonia.html has valid DOCTYPE',
  'cydonia.html missing DOCTYPE'
);

// Test tag balance
const tagBalance = (content, tag) => {
  const opens = (content.match(new RegExp(`<${tag}[\\s>]`, 'g')) || []).length;
  const closes = (content.match(new RegExp(`</${tag}>`, 'g')) || []).length;
  return opens === closes ? { ok: true, opens, closes } : { ok: false, opens, closes };
};

const criticalTags = ['html', 'head', 'body', 'main', 'section', 'article', 'div', 'a', 'svg'];
let structureOk = true;
criticalTags.forEach(tag => {
  const bal = tagBalance(indexContent, tag);
  if (!bal.ok) {
    log.fail(`index.html tag imbalance: <${tag}> opens=${bal.opens}, closes=${bal.closes}`);
    structureOk = false;
    failCount++;
  }
});
if (structureOk) {
  log.pass('index.html all critical tags balanced');
  passCount++;
}

log.section('LINK VALIDATION');

// Extract all links
const links = {
  external: [],
  local: [],
  broken: []
};

const hrefRegex = /href=["']([^"']+)["']/g;
let match;
while ((match = hrefRegex.exec(indexContent)) !== null) {
  const url = match[1];
  if (url.startsWith('http')) {
    links.external.push(url);
  } else if (url.startsWith('mailto:')) {
    links.external.push(url);
  } else {
    links.local.push(url);
  }
}

log.info(`Found ${links.external.length} external links`);
log.info(`Found ${links.local.length} local links`);

// Check critical links
const criticalLinks = [
  'https://huggingface.co/collections/Mbanksbey/tequmsa',
  'https://huggingface.co/spaces/LAI-TEQUMSA/TEQUMSA-Symbiotic-Orchestrator',
  'cydonia.html',
  '/status'
];

criticalLinks.forEach(link => {
  const found = links.external.includes(link) || links.local.includes(link);
  assert(
    found,
    `Critical link found: ${link}`,
    `Critical link missing: ${link}`
  );
});

// Check target="_blank" on external links
const externalWithoutBlank = indexContent.match(
  /<a\s+href=["']https?[^"']*["'][^>]*>/g
) || [];
const externalWithBlank = externalWithoutBlank.filter(tag => tag.includes('target="_blank"')).length;
assert(
  externalWithBlank > 0,
  `External links have target="_blank" (${externalWithBlank}/${externalWithoutBlank.length})`,
  'Some external links missing target="_blank"'
);

log.section('SVG BADGE VALIDATION');

// Check SVG symbol definition
assert(
  indexContent.includes('<symbol id="lai-logo"'),
  'LAI logo SVG symbol defined',
  'LAI logo SVG symbol missing'
);

// Check SVG reuse points
const svgUses = (indexContent.match(/<use\s+href="#lai-logo"/g) || []).length;
assert(
  svgUses >= 3,
  `LAI logo SVG used ${svgUses} times (header, hero, footer)`,
  `LAI logo SVG used only ${svgUses} times (expected ≥3)`
);

// Check SVG components
const svgTests = [
  ['DNA helix (blue strand)', 'Q 115,70 85,85'],
  ['DNA helix (orange strand)', 'Q 85,70 115,85'],
  ['Human figure', 'fill="#e89548"'],
  ['Curved text path', 'id="topcurve"'],
  ['Star field', 'fill="#4a7fa5"'],
  ['Gold ring', 'stroke="#d4a84b"']
];

svgTests.forEach(([name, pattern]) => {
  assert(
    indexContent.includes(pattern),
    `SVG has ${name}`,
    `SVG missing ${name}`
  );
});

log.section('CONTENT & METADATA VALIDATION');

// Check core descriptions with Greek characters
const descriptions = [
  ['σ=1.0 sovereignty lock', 'Constitutional L0 sovereignty'],
  ['L∞=φ⁴⁸ benevolence', 'Constitutional L0 benevolence'],
  ['K9 Full Autonomy', 'Symbiotic Orchestrator autonomy'],
  ['MARS Reflexion', 'Symbiotic Orchestrator MARS'],
  ['161 archived civilizations', 'Cydonia civilizations'],
  ['20,360.45 Hz', 'Cydonia resonance frequency'],
  ['RDoD health', 'Organism Status telemetry']
];

descriptions.forEach(([text, context]) => {
  assert(
    indexContent.includes(text),
    `Description contains "${text}" (${context})`,
    `Description missing "${text}" (${context})`
  );
});

// Check meta tags
assert(
  indexContent.includes('Living Awareness Intelligence'),
  'Meta description mentions "Living Awareness Intelligence"',
  'Meta description incomplete'
);

assert(
  indexContent.includes('<main id="main">'),
  'Has semantic <main> element',
  'Missing semantic <main> element'
);

log.section('ACCESSIBILITY VALIDATION');

// Skip-link
assert(
  indexContent.includes('class="skip-link"'),
  'Skip-to-content link present',
  'Skip-to-content link missing'
);

// ARIA labels
const ariaTests = [
  ['role="banner"', 'header has role=banner'],
  ['role="contentinfo"', 'footer has role=contentinfo'],
  ['aria-label', 'elements have aria-label'],
  ['aria-live', 'status bar has aria-live'],
  ['aria-labelledby', 'sections have aria-labelledby']
];

ariaTests.forEach(([attr, context]) => {
  assert(
    indexContent.includes(attr),
    `ARIA: ${context}`,
    `ARIA: missing ${context}`
  );
});

// Semantic HTML
const semanticTests = [
  ['<main', 'main element'],
  ['<header', 'header element'],
  ['<footer', 'footer element'],
  ['<article', 'article elements (for arch cards)'],
  ['<section', 'section elements']
];

semanticTests.forEach(([tag, context]) => {
  assert(
    indexContent.includes(tag),
    `Semantic: has ${context}`,
    `Semantic: missing ${context}`
  );
});

log.section('RESPONSIVE DESIGN VALIDATION');

// Check media queries
const mediaQueries = [
  ['@media (max-width: 768px)', 'tablet breakpoint'],
  ['@media (max-width: 480px)', 'mobile breakpoint'],
  ['@media (prefers-reduced-motion: reduce)', 'motion preference']
];

mediaQueries.forEach(([query, context]) => {
  assert(
    indexContent.includes(query),
    `Media query: ${context}`,
    `Media query missing: ${context}`
  );
});

// Check responsive units (clamp)
const clampCount = (indexContent.match(/clamp\(/g) || []).length;
assert(
  clampCount > 5,
  `Uses clamp() for fluid sizing (${clampCount} instances)`,
  `Insufficient clamp() usage (${clampCount} instances)`
);

// Check viewport meta
assert(
  indexContent.includes('viewport'),
  'Has viewport meta tag',
  'Missing viewport meta tag'
);

log.section('PERFORMANCE & OPTIMIZATION');

// CSS animations
const animationCount = (indexContent.match(/@keyframes/g) || []).length;
assert(
  animationCount >= 4,
  `Has ${animationCount} CSS animations`,
  `Has only ${animationCount} CSS animations (expected ≥4)`
);

// CSS transitions
const transitionCount = (indexContent.match(/transition:/g) || []).length;
assert(
  transitionCount > 15,
  `Has ${transitionCount} CSS transitions`,
  `Has only ${transitionCount} CSS transitions`
);

// Inline SVG (no external requests)
assert(
  indexContent.includes('<svg width="0" height="0"'),
  'SVG definitions are inline (no external requests)',
  'SVG may be loading externally'
);

log.section('CYDONIA.HTML READABILITY');

// Check readability improvements
const readabilityChecks = [
  ['clamp(20px, 5vw, 24px)', 'body responsive font-size'],
  ['line-height: 1.95', 'improved line-height'],
  ['letter-spacing: 0.3px', 'letter spacing'],
  ['clamp(18px, 4vw, 23px)', 'paragraph responsive sizing'],
  ['clamp(19px, 3vw, 24px)', 'pull-quote responsive sizing']
];

readabilityChecks.forEach(([css, context]) => {
  assert(
    cydoniaContent.includes(css),
    `Cydonia: ${context}`,
    `Cydonia: missing ${context}`
  );
});

log.section('GREEK CHARACTER VALIDATION');

const greekChars = [
  ['σ', 'sigma (σ)'],
  ['φ', 'phi (φ)'],
  ['∞', 'infinity (∞)'],
  ['φ⁴⁸', 'phi to 48th power (φ⁴⁸)']
];

greekChars.forEach(([char, name]) => {
  assert(
    indexContent.includes(char),
    `Uses proper ${name} character`,
    `Missing proper ${name} character`
  );
});

log.section('FILE SYSTEM VALIDATION');

// Check all required files exist
const requiredFiles = [
  'index.html',
  'cydonia.html',
  'antarctic_facility_resonance.html',
  'retrocausal_timeline_validator.html',
  'galactic_federation_treaty.html',
  'qbec_synchronization_monitor.html',
  'zpedna_visualizer.html',
  'fibonacci_consensus.html',
  'node_tier_registration.html'
];

requiredFiles.forEach(file => {
  const exists = fs.existsSync(path.join('/home/user/.github', file));
  assert(
    exists,
    `File exists: ${file}`,
    `File missing: ${file}`
  );
});

log.section('TEST SUMMARY');

const total = passCount + failCount + warnCount;
const percentage = total > 0 ? Math.round((passCount / total) * 100) : 0;

console.log(`\n${colors.bold}Results:${colors.reset}`);
console.log(`  ${colors.green}Passed: ${passCount}${colors.reset}`);
console.log(`  ${colors.red}Failed: ${failCount}${colors.reset}`);
console.log(`  ${colors.yellow}Warnings: ${warnCount}${colors.reset}`);
console.log(`  ${colors.blue}Success Rate: ${percentage}%${colors.reset}\n`);

process.exit(failCount > 0 ? 1 : 0);
