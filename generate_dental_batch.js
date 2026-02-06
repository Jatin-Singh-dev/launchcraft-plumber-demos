const fs = require('fs');
const path = require('path');
// const csv = require('d3-dsv'); // Removed dependency

const CSV_PATH = path.join(__dirname, 'briefs', 'burdubai-batch.csv');
const TEMPLATE_DIR = path.join(__dirname, 'sites', 'bur-dubai-dental-clinic-demo');
const SITES_DIR = path.join(__dirname, 'sites');

async function generateBatch() {
    console.log('Starting Dental Batch Generation...');

    // 1. Read CSV
    if (!fs.existsSync(CSV_PATH)) {
        console.error('CSV not found:', CSV_PATH);
        return;
    }
    const csvContent = fs.readFileSync(CSV_PATH, 'utf-8');
    // Simple manual CSV parse since we know the format simple
    const rows = csvContent.trim().split('\n');
    const headers = rows.shift().split(',');

    // Helper to parse line with quotes
    const parseLine = (line) => {
        const result = [];
        let start = 0;
        let inQuotes = false;
        for (let i = 0; i < line.length; i++) {
            if (line[i] === '"') {
                inQuotes = !inQuotes;
            } else if (line[i] === ',' && !inQuotes) {
                result.push(line.substring(start, i).replace(/^"|"$/g, '').trim());
                start = i + 1;
            }
        }
        result.push(line.substring(start).replace(/^"|"$/g, '').trim());
        return result;
    };

    const data = rows.map(line => {
        if (!line.trim()) return null;
        const cols = parseLine(line);
        return {
            slug: cols[0],
            business_name: cols[1],
            location: cols[2],
            phone: cols[3]
        };
    }).filter(r => r);

    console.log(`Found ${data.length} businesses to process.`);

    // 2. Read Template
    const templateHtmlPath = path.join(TEMPLATE_DIR, 'index.html');
    if (!fs.existsSync(templateHtmlPath)) {
        console.error('Template HTML not found:', templateHtmlPath);
        return;
    }
    let templateHtml = fs.readFileSync(templateHtmlPath, 'utf-8');

    // 3. Process each row
    for (const item of data) {
        console.log(`Processing: ${item.business_name} (${item.slug})`);

        const targetDir = path.join(SITES_DIR, item.slug);

        // Create directory
        if (!fs.existsSync(targetDir)) {
            fs.mkdirSync(targetDir, { recursive: true });
        }

        // Copy Assets
        const sourceAssets = path.join(TEMPLATE_DIR, 'assets');
        const targetAssets = path.join(targetDir, 'assets');

        // Check if source assets exist (they should)
        if (fs.existsSync(sourceAssets)) {
            // New Node versions have fs.cpSync
            try {
                fs.cpSync(sourceAssets, targetAssets, { recursive: true });
            } catch (e) {
                // Fallback for older node or if failure
                copyRecursiveSync(sourceAssets, targetAssets);
            }
        } else {
            console.warn(`Warning: Assets dir not found at ${sourceAssets}`);
        }

        // Prepare replacements
        let html = templateHtml;

        // Clean Phone Data
        // Input: "+971508597853" or similar
        // Display: "+971 50 859 7853" (Rough formatting)
        // Href: "971508597853" (No +)

        const cleanPhone = item.phone.replace(/[^0-9]/g, ''); // 971508597853
        const displayPhone = item.phone; // Use as provided for display, or format if needed

        // REPLACEMENTS
        // 1. Business Name
        // Replace "Bur Dubai Dental Clinic" but NOT "Bur Dubai" in location if separate
        // HTML has "Bur Dubai <span>Dental Clinic</span>" in logo
        // And "Bur Dubai Dental Clinic" in title/meta/footer

        // We need to be specific with regex to preserve structure if possible, 
        // OR just simple string replace.
        // The template has "Bur Dubai Dental Clinic" in text nodes.

        // Strategy: Replace specific full strings first
        html = html.replace(/Bur Dubai Dental Clinic/g, item.business_name);

        // Logo specific replacement: The logo HTML is:
        // <div>Bur Dubai <span>Dental Clinic</span></div>
        // We might want to replace the whole innerHTML of the logo div or just let the global replace handle it.
        // Global replace above might break the <span> if it matched across tags (it doesn't).
        // Since "Bur Dubai Dental Clinic" is the string, the logo text "Bur Dubai <span>Dental Clinic</span>" won't match exactly.

        // Let's replace the Logic text specifically regex
        html = html.replace(/<div>Bur Dubai <span>Dental Clinic<\/span><\/div>/g, `<div>${item.business_name}</div>`);

        // 2. Location (Address)
        html = html.replace(/Bur Dubai, Dubai, UAE/g, item.location);

        // 2b. Location (Headlines/Titles) 
        // "Premium Dental Care in Bur Dubai" -> "Premium Dental Care in Dubai, UAE" (or similar)
        // We use a regex to catch the specific phrase
        html = html.replace(/Premium Dental Care in Bur Dubai/g, `Premium Dental Care in ${item.location}`);

        // 2c. Schema Locality
        // "addressLocality": "Bur Dubai"
        const locality = item.location.split(',')[0].trim();
        html = html.replace(/"addressLocality": "Bur Dubai"/g, `"addressLocality": "${locality}"`);

        // 3. Phone (Display)
        html = html.replace(/\+971 50 123 4567/g, displayPhone);

        // 4. Phone (Href/clean)
        // The template uses +971501234567 in tel: and data-phone
        // And 971501234567 in whastapp
        html = html.replace(/\+971501234567/g, item.phone); // tel:
        html = html.replace(/971501234567/g, cleanPhone); // wa.me and data-phone

        // Write file
        fs.writeFileSync(path.join(targetDir, 'index.html'), html);

        // 5. PATCH MAIN.JS (Dynamic Translation Fix)
        // Requires reading the JS file from target (already copied), replacing the hardcoded string, and saving.
        const targetJsPath = path.join(targetDir, 'assets', 'js', 'main.js');
        if (fs.existsSync(targetJsPath)) {
            let jsContent = fs.readFileSync(targetJsPath, 'utf-8');
            // Regex to find "heroHeadline": "Premium Dental Care in Bur Dubai"
            // We want to replace it with item.location
            // NOTE: The main.js has keys like: heroHeadline: "Premium Dental Care in Bur Dubai",

            // Fix English Headline
            jsContent = jsContent.replace(
                /heroHeadline:\s*"Premium Dental Care in Bur Dubai"/g,
                `heroHeadline: "Premium Dental Care in ${item.location}"`
            );

            // Fix Arabic Headline (Optional: Just replace Bur Dubai with Dubai or generic if we can't translate)
            // Current arabic: "رعاية أسنان متميزة في بر دبي"
            // We'll leave it or basic patch if possible. For now, key focus is English.

            fs.writeFileSync(targetJsPath, jsContent);
        }
    }

    console.log('Batch generation complete.');
}

function copyRecursiveSync(src, dest) {
    const exists = fs.existsSync(src);
    const stats = exists && fs.statSync(src);
    const isDirectory = exists && stats.isDirectory();
    if (isDirectory) {
        if (!fs.existsSync(dest)) {
            fs.mkdirSync(dest);
        }
        fs.readdirSync(src).forEach(function (childItemName) {
            copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
        });
    } else {
        fs.copyFileSync(src, dest);
    }
}

generateBatch().catch(console.error);
