const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Configuration
const CSV_PATH = path.join(__dirname, 'briefs', 'handyman-batch.csv');
const TEMPLATE_DIR = path.join(__dirname, 'sites', 'handyman-demo-template');
const SITES_ROOT = path.join(__dirname, 'sites');

async function main() {
    console.log('Starting batch generation...');

    // 1. Read Template
    const templatePath = path.join(TEMPLATE_DIR, 'index.html');
    let templateHtml = fs.readFileSync(templatePath, 'utf8');

    // Normalize template placeholders for easier replacement if needed, 
    // but we will simple replace specific string constants from the known template.
    // Template known values:
    const TPL_NAME = "Arlington Handyman Pros";
    const TPL_CITY = "Arlington";
    const TPL_STATE = "TX";
    const TPL_PHONE = "817-555-0142"; // Check format in HTML
    const TPL_PHONE_DISPLAY = "(817) 555-0142";
    const TPL_PHONE_LINK = "+18175550142";

    // 2. Read CSV
    const fileStream = fs.createReadStream(CSV_PATH);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    let isHeader = true;
    let headers = [];

    for await (const line of rl) {
        if (isHeader) {
            headers = line.split(',');
            console.log('Headers:', headers);
            isHeader = false;
            continue;
        }

        // Regex to handle CSV with quoted fields
        const regex = /(?:^|,)(?:"([^"]*)"|([^",]*))/g;
        let cols = [];
        let match;
        while ((match = regex.exec(line)) !== null) {
            // match[1] is quoted value, match[2] is unquoted value
            let val = match[1] !== undefined ? match[1] : match[2];
            cols.push(val.trim());
        }

        // Remove the empty match that regex might produce at the end if not careful, 
        // but typically this regex works for standard CSV. 
        // A safer standard parser approach:
        // const cols = line.match(/(".*?"|[^",\s]+)(?=\s*,|\s*$)/g).map(v => v.replace(/^"|"$/g, '')); 
        // But let's stick to the while loop which is fairly robust for this simple case.
        if (cols.length < 5) continue;

        const data = {
            slug: cols[0],
            business_name: cols[1],
            city: cols[2],
            state: cols[3],
            phone: cols[4], // e.g. +1 817-210-2874
            // CSV v2 has no rating/reviews, defaulting for demo purposes
            rating: cols[5] || '4.9',
            reviews: cols[6] || '42'
        };

        // Clean phone for tel: link
        const phoneLink = data.phone.replace(/[^0-9+]/g, '');
        // Format phone for display if needed, or just use as is from CSV
        const phoneDisplay = data.phone.replace('+1 ', '');

        console.log(`Generating: ${data.slug}`);

        // 3. Create Directory Structure
        const siteDir = path.join(SITES_ROOT, data.slug);
        const assetsDir = path.join(siteDir, 'assets');

        if (!fs.existsSync(siteDir)) fs.mkdirSync(siteDir, { recursive: true });
        if (!fs.existsSync(assetsDir)) fs.mkdirSync(assetsDir, { recursive: true });

        // 4. Copy Assets
        const templateAssets = path.join(TEMPLATE_DIR, 'assets');
        const assetFiles = fs.readdirSync(templateAssets);
        for (const file of assetFiles) {
            fs.copyFileSync(path.join(templateAssets, file), path.join(assetsDir, file));
        }

        // 5. Customize HTML
        let html = templateHtml;

        // Replace Business Name Global
        html = html.replaceAll(TPL_NAME, data.business_name);

        // Replace Business Name in Logo
        // Template has: <a href="#" class="logo">Arlington <span>PROS</span></a>
        // We want to replace this with the actual business name.
        // We will preserve the two-tone style by keeping the last word in the span if it has multiple words.
        const nameParts = data.business_name.split(' ');
        let logoHtml = data.business_name;
        if (nameParts.length > 1) {
            const lastWord = nameParts.pop();
            logoHtml = `${nameParts.join(' ')} <span>${lastWord}</span>`;
        }
        html = html.replace(/Arlington <span>PROS<\/span>/g, logoHtml);

        // Replace Phone
        // Link: tel:+18175550142
        html = html.replaceAll(TPL_PHONE_LINK, phoneLink);
        // Display: (817) 555-0142
        html = html.replaceAll(TPL_PHONE_DISPLAY, phoneDisplay);

        // Handle multiline phone in footer
        // (817)
        // 555-0142
        html = html.replace(/\(817\)\s+555-0142/g, phoneDisplay);

        // Replace City/State locations
        // "Handyman in Arlington, TX"
        html = html.replaceAll(`Handyman in ${TPL_CITY}, ${TPL_STATE}`, `Handyman in ${data.city}, ${data.state}`);
        html = html.replaceAll(`${TPL_CITY}, ${TPL_STATE}`, `${data.city}, ${data.state}`);

        // "Arlington-Based"
        html = html.replaceAll(`${TPL_CITY}-Based`, `${data.city}-Based`);

        // General City replacements (Service areas, intro text)
        // Be careful not to break "Arlington Handyman Pros" which was already replaced?
        // Actually simplest is global replace of "Arlington" with new City, EXCEPT where we specifically handled Business Name.
        // Since we already replaced Business Name, "Arlington" might only remain in text content.
        html = html.replaceAll(TPL_CITY, data.city);

        // Replace Reviews
        // "4.8 ★ from 63 Google reviews"
        // We need to find this pattern using regex because the template might have changed slightly or exact numbers vary
        html = html.replace(/4\.8 ★ from 63 Google reviews/g, `${data.rating} ★ from ${data.reviews} Google reviews`);
        html = html.replace(/Rated 4\.8\/5/g, `Rated ${data.rating}/5`);

        // 6. Write HTML
        fs.writeFileSync(path.join(siteDir, 'index.html'), html);
    }

    console.log('Batch generation complete.');
}

main().catch(console.error);
