const path = require('path');
const fs = require('fs');
const { chromium, request } = require('playwright');

const FRONTEND_URL = process.env.FRONTEND_URL || 'http://localhost:3000';
const API_URL = process.env.API_URL || 'http://localhost:8000';
const USERNAME = process.env.DEMO_USER || 'demo';
const PASSWORD = process.env.DEMO_PASS || 'demo123';
const TOKEN_KEY = 'advisory_token';
const VIEWPORT = { width: 1440, height: 900 };

const authRoutes = [
    { name: 'home', path: '/' },
    { name: 'documents', path: '/documents' },
    { name: 'reminders', path: '/reminders' },
    { name: 'chat', path: '/chat' },
];

const publicRoutes = [{ name: 'login', path: '/login' }];

async function ensureDir(dir) {
    fs.mkdirSync(dir, { recursive: true });
}

async function loginAndGetToken() {
    const api = await request.newContext({ baseURL: API_URL });
    const res = await api.post('/api/auth/login', {
        data: { username: USERNAME, password: PASSWORD },
    });
    if (!res.ok()) {
        const body = await res.text();
        throw new Error(`Login failed (${res.status()}): ${body}`);
    }
    const { access_token } = await res.json();
    await api.dispose();
    return access_token;
}

async function screenshotAuthenticatedPages(token, outDir) {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: VIEWPORT });
    await context.addInitScript(([key, value]) => localStorage.setItem(key, value), [TOKEN_KEY, token]);
    const page = await context.newPage();

    for (const route of authRoutes) {
        const url = `${FRONTEND_URL}${route.path}`;
        console.log(`→ ${route.name}: ${url}`);
        await page.goto(url, { waitUntil: 'networkidle' });
        await page.waitForTimeout(1200);
        await page.screenshot({ path: path.join(outDir, `${route.name}.png`), fullPage: true });
    }

    await browser.close();
}

async function screenshotPublicPages(outDir) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: VIEWPORT });

    for (const route of publicRoutes) {
        const url = `${FRONTEND_URL}${route.path}`;
        console.log(`→ ${route.name}: ${url}`);
        await page.goto(url, { waitUntil: 'networkidle' });
        await page.waitForTimeout(1200);
        await page.screenshot({ path: path.join(outDir, `${route.name}.png`), fullPage: true });
    }

    await browser.close();
}

async function main() {
    const outDir = path.join(process.cwd(), 'shots');
    ensureDir(outDir);

    console.log('Logging in to fetch token...');
    const token = await loginAndGetToken();

    console.log('Capturing authenticated pages...');
    await screenshotAuthenticatedPages(token, outDir);

    console.log('Capturing public pages...');
    await screenshotPublicPages(outDir);

    console.log(`Saved screenshots to ${outDir}`);
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
