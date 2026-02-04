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

        // Detect Contractor
        const isContractor = /contractor|construction|remodeling|renovation|solutions|woodwork|custom|repair|surface|improvement/i.test(data.business_name);

        // 5. Customize HTML
        let html = templateHtml;

        // Replace Business Name Global
        html = html.replaceAll(TPL_NAME, data.business_name);

        // Replace Business Name in Logo
        const nameParts = data.business_name.split(' ');
        let logoHtml = data.business_name;
        if (nameParts.length > 1) {
            const lastWord = nameParts.pop();
            logoHtml = `${nameParts.join(' ')} <span>${lastWord}</span>`;
        }
        html = html.replace(/Arlington <span>PROS<\/span>/g, logoHtml);

        // Replace Phone
        html = html.replaceAll(TPL_PHONE_LINK, phoneLink);
        html = html.replaceAll(TPL_PHONE_DISPLAY, phoneDisplay);
        html = html.replace(/\(817\)\s+555-0142/g, phoneDisplay);

        // Replace City/State
        html = html.replaceAll(`Handyman in ${TPL_CITY}, ${TPL_STATE}`, `Handyman in ${data.city}, ${data.state}`);
        html = html.replaceAll(`${TPL_CITY}, ${TPL_STATE}`, `${data.city}, ${data.state}`);
        html = html.replaceAll(`${TPL_CITY}-Based`, `${data.city}-Based`);
        html = html.replaceAll(TPL_CITY, data.city);

        // Replace Reviews
        html = html.replace(/4\.8 ★ from 63 Google reviews/g, `${data.rating} ★ from ${data.reviews} Google reviews`);
        html = html.replace(/Rated 4\.8\/5/g, `Rated ${data.rating}/5`);

        // CONTRACTOR LOGIC
        if (isContractor) {
            console.log(`  -> Applying Contractor Mode for ${data.slug}`);

            // Text Replacements
            // Replace "Handyman in City" -> "General Contractor in City" (We already did Handyman in City above, so we replace that result)
            html = html.replace(new RegExp(`Handyman in ${data.city}`, 'g'), `General Contractor in ${data.city}`);

            // "Professional handyman services" -> "Professional general contractor services"
            html = html.replace(/Professional handyman services/gi, "Professional general contractor services");

            // "Trusted Handyman Services" -> "Trusted General Contractor"
            html = html.replace(/Trusted Handyman Services/g, "Trusted General Contractor Services");

            // FAQ Replacement
            html = html.replace(/general handyman work/g, "general contractor work");

            // Services Replacement
            const contractorServices = `
                <div class="service-card"><div class="service-icon">🔨</div><h3>Kitchen & Bath Updates</h3></div>
                <div class="service-card"><div class="service-icon">🎨</div><h3>Drywall & Painting</h3></div>
                <div class="service-card"><div class="service-icon">🪵</div><h3>Flooring Installation</h3></div>
                <div class="service-card"><div class="service-icon">🚧</div><h3>Deck & Fence Repair</h3></div>
                <div class="service-card"><div class="service-icon">🚪</div><h3>Doors, Trim & Carpentry</h3></div>
                <div class="service-card"><div class="service-icon">🏠</div><h3>Small Remodels</h3></div>
            `;

            const servicesStartMarker = '<div class="grid services-grid">';
            const servicesEndMarker = '<div class="text-center" style="margin-top: 40px;">';
            const sStartIndex = html.indexOf(servicesStartMarker);
            const sEndIndex = html.indexOf(servicesEndMarker, sStartIndex);

            if (sStartIndex !== -1 && sEndIndex !== -1) {
                // We replacing everything from Start Marker up to (but not including) End Marker.
                // This includes the opening <div class="grid services-grid"> and the closing </div> of the grid.
                // So we need to reconstruct the wrapper.
                // Wait, sEndIndex is at <div class="text-center". Ideally the character BEFORE it is the closing </div> (plus newline/spaces).
                // Let's just replace the substring with our new block.
                const oldServicesBlock = html.substring(sStartIndex, sEndIndex);
                html = html.replace(oldServicesBlock, `${servicesStartMarker}\n${contractorServices}\n            </div>\n            `);
            } else {
                console.log('Warning: Could not find Services block to replace');
            }

            // Pricing Replacement
            const contractorPricing = `
                <thead>
                    <tr><th>Service Item</th><th>Estimated Range</th></tr>
                </thead>
                <tbody>
                    <tr><td>Consultation / Service Call</td><td>$150 – $250</td></tr>
                    <tr><td>Small Remodels</td><td>$2,500+</td></tr>
                    <tr><td>Flooring Installation</td><td>$4 – $8 / sq ft</td></tr>
                    <tr><td>Deck Repair/Stain</td><td>$800 – $2,500</td></tr>
                    <tr><td>Door Installation</td><td>$350 – $800</td></tr>
                    <tr><td>Drywall Work</td><td>$500 – $1,500</td></tr>
                    <tr><td>Kitchen Updates</td><td>$3,000 – $15,000</td></tr>
                    <tr><td>Bathroom Updates</td><td>$2,500 – $10,000</td></tr>
                </tbody>
            `;

            const pricingStartMarker = '<table class="pricing-table">';
            const pricingEndMarker = '</table>';
            const pStartIndex = html.indexOf(pricingStartMarker);
            const pEndIndex = html.indexOf(pricingEndMarker, pStartIndex);

            if (pStartIndex !== -1 && pEndIndex !== -1) {
                const oldPricingBlock = html.substring(pStartIndex, pEndIndex + pricingEndMarker.length);
                html = html.replace(oldPricingBlock, `<table class="pricing-table">${contractorPricing}</table>`);
            } else {
                console.log('Warning: Could not find Pricing block to replace');
            }
        }

        // 6. Write HTML
        fs.writeFileSync(path.join(siteDir, 'index.html'), html);
    }

    console.log('Batch generation complete.');
}

main().catch(console.error);
